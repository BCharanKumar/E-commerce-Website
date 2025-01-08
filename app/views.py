from django.shortcuts import render,redirect,HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse
from app.models import *
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth import logout
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from app.forms import *
from django.shortcuts import render, redirect
from twilio.rest import Client
from django.contrib import messages



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

# #The view is Responsible for Verifying the generated otp
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
        
        try:
            User = Customer.objects.get(email=email)
        except Customer.DoesNotExist:
            error_msg = 'Invalid Email'
            d = {'error': error_msg}
            return render(request, 'login.html',d)

        print(email)
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

def change_password(request):
    if request.method == 'POST':
        pwd = request.POST['pwd']
        rpwd = request.POST['rpwd']
        email = request.session.get('email')
        if email:
            try:
                User = Customer.objects.get(email=email)
            except Customer.DoesNotExist:
                messages.error(request, 'Invalid Email')
                return render(request, 'change_password.html')
            if pwd == rpwd:
                User.password = pwd
                User.save()
                messages.success(request, 'Password changed successfully!')
                return redirect('home')
            else:
                messages.error(request, 'New password and confirm password do not match!')
                return render(request, 'change_password.html')
        else:
            messages.error(request, 'You must be logged in to change your password!')
            return redirect('login_user')
    return render(request, 'change_password.html')



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
        if item.quantity > 0:
            item.quantity -= 1
            item.save()
        else:
            if  item.quantity==0:
                item.delete()
        return redirect('view_cart')
    else:
        return redirect('view_cart')




# def view_cart(request):
#     if 'email' in request.session:
#         email = request.session['email']
#         customer = Customer.getemail(email)
#         items = Cart.objects.filter(customer=customer)
#         total_price = 0
#         for item in items:
#             total_price += item.product.price * item.quantity
#         return render(request, 'cart.html', {'items': items, 'total_price': total_price})
#     else:
#         return redirect('login_user')

# '''
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

# def view_cart(request):
#     if request.user.is_authenticated:
#         customer = request.user.customer
#     else:
#         customer_id = request.session['customer_id']
#         customer = Customer.objects.get(id=customer_id)

#     items = Cart.objects.filter(customer=customer)
#     total_price = 0

#     if request.method == 'POST':
#         selected_items = request.POST.getlist('selected_items')
#         for item_id in selected_items:
#             item = Cart.objects.get(id=item_id)
#             total_price += item.product.price * item.quantity

#     return render(request, 'cart.html', {'items': items, 'total_price': total_price})


def about_product(request,product_id):
    products=Product.objects.all()
    if request.method == 'POST':
        product = Product.objects.get(id=product_id)
        email = request.session.get('email')
        if email:
            customer = Customer.getemail(email)
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
            order_item.quantity += 1
            order_item.save()
            return redirect('order_address')
        else:
            return redirect('login_user')
    else:
        product = Product.objects.get(id=product_id)
        return render(request, 'About_product.html', {'product': product})
    #return render(request,'About_product.html')


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
            return redirect('order_address')
        else:
            return redirect('login_user')
    else:
        product = Product.objects.get(id=product_id)
        return render(request, 'buy_now.html', {'product': product})


def search_products(request):
    quanity=1
    if request.method == 'GET':
        query = request.GET.get('query')
        if query:
            products = Product.objects.filter(name__icontains=query)
            return render(request, 'search_results.html', {'products': products,'quanity':quanity})
        else:
            return render(request, 'search_results.html')
    return render(request, 'search_results.html')
from django.conf import settings
from .models import Cart



# def cart_count(request):

#     if request.user.is_authenticated:
#         customer = request.user.customer
#         cart_count = Cart.objects.filter(customer=customer).count()
#         return {'cart_count': cart_count}
#     else:
#         return {'cart_count': 0}
def checkout(request):
    if request.method == 'POST':
        selected_items = request.POST.getlist('selected_items')
        total_price = 0
        for item_id in selected_items:
            item = Cart.objects.get(id=item_id)
            total_price += item.product.price * item.quantity

        if request.user.is_authenticated:
            customer = request.user.customer
        else:
            customer_id = request.session['customer_id']
            customer = Customer.objects.get(id=customer_id)

        order = Order(customer=customer)
        order.save()
        for item_id in selected_items:
            item = Cart.objects.get(id=item_id)
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity
            )
            item.delete()
        return redirect('thank_you')
    else:
        return redirect('view_cart')






# def create_order(request):
    
#     if request.method == 'POST':
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('thank_you')
#     else:
#         form = OrderForm()
#     return render(request, 'create_order.html', {'form': form})

def order_address(request):
    userValues = {}
    error_msg = None
    otp = None


    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        mobile = request.POST['mobile']
        address_line_1 = request.POST['address_line_1']
        address_line_2 = request.POST['address_line_2']
        city = request.POST['city']
        state = request.POST['state']
        pincode = request.POST['pincode']

        # Save the data to database
        OrderAddress.objects.create(
            first_name=first_name,
            last_name=last_name,
            mobile=mobile,
            address_line_1=address_line_1,
            address_line_2=address_line_2,
            city=city,
            state=state,
            pincode=pincode
        )
        
         # Send email to customer
        subject = 'Order Successful'
        message = f'Dear {first_name} {last_name},\n\nYour order has been successfully placed. We will deliver your order to the following address:\n\n{address_line_1},\n{city}, {state} - {pincode}\n\nThank you for shopping with us!'
        from_email = settings.EMAIL_HOST_USER
        to_email = [request.POST['email']]  # Assuming email is also a field in the form
        send_mail(subject, message, from_email, to_email, fail_silently=False)
        
#         account_sid = "AC3220f2e3e5a3e7203a03976d9190019f"
#         auth_token  = "a89a9d17a06b67028e4f45c7934a065f"
#         client = Client(account_sid, auth_token)

#         message = client.messages.create(
#     to="+91 9346096771",
#     from_="+15705399880",
#     body=f"Dear {first_name} {last_name},\n\nYour order has been successfully placed. We will deliver your order to the following address:\n\n{address_line_1},\n{city}, {state} - {pincode}\n\nThank you for shopping with us!",
# )


 
        userValues={
            'first_name':first_name,
            'last_name':last_name,
            'mobile':mobile,
            'address_line_1':address_line_1,
            'address_line_2':address_line_2,
            'city':city,
            'state':state,
            'pincode':pincode
        }
        otp=otp_gen()
       
        if  (not first_name) or (not last_name) or (not mobile) or (not address_line_1) or (not city ) or (not state) or (not pincode ):
            error_msg='* Should Not Be Empty '
            return render(request,'order_address.html',{'error':error_msg,'value':userValues})
        

        #return redirect('thank_you')  # Redirect to a success page
        return render(request,'order_successful.html',{'value':userValues,'otp':otp})
    else:
        return render(request, 'order_address.html',{'value':userValues})

        


def thank_you(request):
    return render(request, 'order_successful.html')



def contact(request):
    return render(request,'contact.html')


