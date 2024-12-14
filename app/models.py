from django.db import models
from django.core.validators import *
# Create your models here.
class Category(models.Model):
    product_category=models.CharField(max_length=75)
    def __str__(self):
        return self.product_category
    

class Product(models.Model):
    name=models.CharField(max_length=125)
    product_category=models.ForeignKey(Category,on_delete=models.CASCADE,default=1)
    image=models.ImageField(upload_to='img')
    desc=models.TextField()
    price=models.IntegerField()

    #Static method
    @staticmethod
    def get_category_id(get_id):
        if get_id:
            return Product.objects.filter(product_category=get_id)
        else:
            return Product.objects.all()

    def __str__(self):
        return self.name
    

class Customer(models.Model):
    first_name=models.CharField(max_length=25)
    last_name=models.CharField(max_length=25)
    email=models.EmailField(unique=True)
    mobile=models.CharField(max_length=10,validators=[RegexValidator('[6-9]\d{9}')])
    password=models.CharField(max_length=200)

    def __str__(self):
        return self.first_name
    
    #Customer email is existing or not 
    def isexit(self):
        if Customer.objects.filter(email=self.email):
            return True
        return False
    
    #Now checking the email is exists or not
    @staticmethod
    def getemail(email):
        try:
            return Customer.objects.get(email=email)
        except:
            return False
        

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    customer= models.ForeignKey(Customer, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f'{self.quantity} x {self.product.name}'

    


