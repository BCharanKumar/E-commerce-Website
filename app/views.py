
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from app.models import *
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import logout
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from app.forms import *
from twilio.rest import Client
from django.db.models import Avg, Count

# Create your views here.
def display_data(request):
    products = Product.objects.all()
    d = {'products': products}
    return render(request, 'index.html', d)

def home(request):
    category = Category.objects.all()
    CID = request.GET.get('category')
    if CID:
        products = Product.get_category_id(CID)
    else:
        products = Product.objects.all()
    for product in products:
        ratings = Rating.objects.filter(product=product)
        if ratings:
            product.avg_rating = ratings.aggregate(Avg('rating'))['rating__avg']
            product.rating_count = ratings.count()
        else:
            product.avg_rating = 0
            product.rating_count = 0
    d = {'products': products, 'category': category}
    return render(request, 'data.html', d)

def singup(request):
    if request.method == 'GET':
        return render(request, 'singup.html')
    else:
        fn = request.POST['fn']
        ln = request.POST['ln']
        email = request.POST['email']
        mobile = request.POST['mobile']
        password = request.POST['password']
        userValues = {
            'fn': fn,
            'ln': ln,
            'email': email,
            'mobile': mobile
        }
        error_msg = None
        if (not fn) or (not ln) or (not email) or (not mobile):
            error_msg = '* Should Not Be Empty '
        elif (not password):
            error_msg = '*Password First char Should Be Upper case / must be 8 characters'
        if not error_msg:
            CO = Customer(first_name=fn, last_name=ln, email=email, mobile=mobile, password=password)
            CO.password = make_password(CO.password)
            CO.save()
            d = {'success': 'Account Created Successfully'}
            return render(request, 'singup.html', d)
        else:
            d = {'error': error_msg, 'value': userValues}
            return render(request, 'singup.html', d)

def login_user(request):
    if request.method == 'GET':
        return render(request, 'login.html', {})
    else:
        email = request.POST['email']
        password = request.POST['password']
        try:
            User = Customer.objects.get(email=email)
        except Customer.DoesNotExist:
            error_msg = 'Invalid Email'
            d = {'error': error_msg}
            return render(request, 'login.html', d)
        if User:
            check = check_password(password, User.password)
            if check:
                otp = otp_gen()
                request.session['otp'] = otp
                request.session['email'] = email
                send_mail('Your OTP for Login', f'your OTP is {otp}', 'kumarbcharan77@gmail.com', [email], fail_silently=False)
                return redirect('home')
            else:
                error_msg = 'Invalid Password'
                d = {'error': error_msg}
                return render(request, 'login.html', d)
        else:
            error_msg = 'Invalid Email'
            d = {'error': error_msg}
            return render(request, 'login.html', d)

def logout_user(request):
    if 'email' in request.session:
        del request.session['email']
    return redirect('login_user')

def add_to_cart(request, id):
    email = request.session.get('email')
    if email:
        customer = Customer.objects.get(email=email)
        product = Product.objects.get(id=id)
        cart, created = Cart.objects.get_or_create(product=product, customer=customer)
        if not created:
            cart.quantity += 1
            cart.save()
        cart_count = Cart.objects.filter(customer=customer).count()
        request.session['cart_count'] = cart_count
        request.session['customer_id'] = customer.id
        return redirect('view_cart')
    else:
        return redirect('login_user')

def view_cart(request):
    if 'email' in request.session:
        email = request.session['email']
        try:
            customer = Customer.objects.get(email=email)
        except Customer.DoesNotExist:
            return redirect('login_user')
        if 'customer_id' in request.session:
            if request.session['customer_id'] != customer.id:
                request.session.flush()
                request.session['customer_id'] = customer.id
        items = Cart.objects.filter(customer_id=request.session['customer_id'])
        total_price = 0
