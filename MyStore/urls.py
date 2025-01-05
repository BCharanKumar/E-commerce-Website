"""
URL configuration for MyStore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from app.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/',home,name='home'),
    path('display_data/',display_data,name='display_data'),
    path('singup/',singup,name='singup'),
   
    path('otp_gen/',otp_gen,name='otp_gen'),
    path('verify_otp/',verify_otp,name='verify_otp'),
    path('',login_user,name='login_user'),
    path('logout_user/',logout_user,name='logout_user'),   

    path('add_to_cart/<int:id>/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:id>/',remove_from_cart, name='remove_from_cart'),

    path('increase_cart_quantity/',increase_cart_quantity, name='increase_cart_quantity'),
    path('decrease_cart_quantity/',decrease_cart_quantity, name='decrease_cart_quantity'),
    path('cart/',view_cart, name='view_cart'),
    path('buy-now/<int:product_id>/',buy_now, name='buy_now'),
    path('search/',search_products, name='search_products'),



    
   


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
