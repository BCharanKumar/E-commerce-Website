from django.shortcuts import render,redirect,HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse
from app.models import *
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth import logout
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from app.forms import *

# Create your views here.


def display_data(request):
    products=Product.objects.all()
    d={'products':products}
    #return HttpResponse('<center><h1> Welcome To My E-commerce Website</h1></center>')
    return render(request,'index.html',d)


def home(request):
    
    category=Category.objects.all()
    CID=request.GET.get('category')
    if CID:
        products=Product.get_category_id(CID)
    else:
        products=Product.objects.all()
    
    d={'products':products,'category':category}
    return render(request,'data.html',d)


#View for singup process
def singup(request):
    if request.method=='GET':
       
        return render(request,'singup.html')
    else:
        fn=request.POST['fn']
        ln=request.POST['ln']
        email=request.POST['email']
        mobile=request.POST['mobile']
        password=request.POST['password']
        #password=make_password(password)
        UD=[fn,ln,email,mobile,password]
        print(UD)
        #Customer object creating
        

        userValues={
            'fn':fn,
            'ln':ln,
            'email':email,
            'mobile':mobile
        }

        CO=Customer(first_name=fn,last_name=ln,email=email,mobile=mobile,password=password)
        #Validation of The Data
        error_msg=None
        success_msg=None
        if  (not fn) or (not ln) or (not email) or (not mobile):
            error_msg='* Should Not Be Empty '
        elif ((not password)):
            error_msg='*Password First char  Should  Be Upper case  / must be 8 characters'
        elif (CO.isexit()):
            error_msg='Your Email Alter Exists'

        #Account Creation Succesfully
        if (not error_msg):
            CO.password=make_password(CO.password)

            
            success_msg='Account Created Successfully'
            CO.save()
            d={'success':success_msg} 
            send_mail('Registration',
                      'Your Registration is Succesfully Done....!',
                      from_email='kumarbcharan77@gmail.com',
                      recipient_list=['luckymahi7418@gmail.com'],
                      fail_silently=False)
            return render(request,'singup.html',d)
        else: 

            d={'error':error_msg,'value':userValues}
            return render(request,'singup.html',d)


import random
#The view is responsible for OTP Generation
def otp_gen():
    get_otp=random.randint(100000,999999)
    return get_otp

#The view is Responsible for Verifying the generated otp
def verify_otp(request):
    error_msg=None
    if request.method=='POST':
        enter_otp=request.POST['otp']
        gen_otp=request.session['otp']

        if enter_otp and str(gen_otp)==enter_otp:

            del request.session['otp']

            return HttpResponseRedirect(reverse('home'))

        else:
            error_msg='Invalid Otp'
    return render(request,'verify_otp.html',{'error_msg':error_msg})



#The following view is responsible for Login functionality
def login_user(request):
    if request.method=='GET':
        return render(request,'login.html',{})
    else:
        email=request.POST['email']
        password=request.POST['password']
        
        #Here Checking  of the email is found or not 
        #User=Customer.getemail(email)
        User=Customer.objects.get(email=email)
        #print(email)
        #print(Users.email)
        error_msg=None
        if User:
            check=check_password(password,User.password),password
            
            if check:
                otp=otp_gen()
                request.session['otp']=otp

                request.session['email']=email

                send_mail('Your  OTP for Login',
                          f'your OTP is {otp}',
                          'kumarbcharan77@gmail.com',
                          [email],
                          fail_silently=False)
                
                #return redirect('verify_otp')
                return redirect('home')
            else:
                error_msg='Invalid Password'
                d={'error':error_msg}
                return render(request,'login.html',d)
        else:
            error_msg='Invalid Email'
            d={'error':error_msg}
            return render(request,'login.html',d)


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
        request.session['customer_id'] =customer.id
        return redirect('view_cart')
    else:
        return redirect('login_user')




def remove_from_cart(request, id):
    email = request.session.get('email')
    if email:
        customer = Customer.getemail(email)
        item = Cart.objects.get(id=id, customer=customer)
        item.delete()
        return redirect('view_cart')
    else:
        return redirect('login_user')


def increase_cart_quantity(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        item = Cart.objects.get(id=item_id)
        item.quantity += 1
        item.save()
        return redirect('view_cart')
    else:
        return redirect('view_cart')
    
def decrease_cart_quantity(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        item = Cart.objects.get(id=item_id)
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
        return redirect('view_cart')
    else:
        return redirect('view_cart')



'''
def view_cart(request):
    if 'email' in request.session:
        email = request.session['email']
        customer = Customer.getemail(email)
        items = Cart.objects.filter(customer=customer)
        total_price = 0
        for item in items:
            total_price += item.product.price * item.quantity
        return render(request, 'cart.html', {'items': items, 'total_price': total_price})
    else:
        return redirect('login_user')
'''

def view_cart(request):
    if 'email' in request.session:
        email = request.session['email']
        try:
            customer = Customer.objects.get(email=email)
        except Customer.DoesNotExist:
            # Handle the case where the customer does not exist
            return redirect('login_user')

        if 'customer_id' in request.session:
            if request.session['customer_id'] != customer.id:
                request.session.flush()
        request.session['customer_id'] = customer.id

        items = Cart.objects.filter(customer_id=request.session['customer_id'])
        total_price = 0
        for item in items:
            total_price += item.product.price * item.quantity

        return render(request, 'cart.html', {'items': items, 'total_price': total_price})
    else:
        return redirect('login_user')



def buy_now(request, product_id):
    if request.method == 'POST':
        product = Product.objects.get(id=product_id)
        email = request.session.get('email')
        if email:
            customer = Customer.getemail(email)
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
            order_item.quantity += 1
            order_item.save()
            return redirect('payment_gateway')
        else:
            return redirect('login_user')
    else:
        product = Product.objects.get(id=product_id)
        return render(request, 'buy_now.html', {'product': product})


def search_products(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        if query:
            products = Product.objects.filter(name__icontains=query)
            return render(request, 'search_results.html', {'products': products})
        else:
            return render(request, 'search_results.html')
    return render(request, 'search_results.html')
from django.conf import settings
from .models import Cart



def cart_count(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        cart_count = Cart.objects.filter(customer=customer).count()
        return {'cart_count': cart_count}
    else:
        return {'cart_count': 0}

