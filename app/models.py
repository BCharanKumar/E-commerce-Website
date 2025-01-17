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


from django.db import models
from .models import Product  # Assuming you already have a Product model

class Rating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Link to the Product model
    user = models.CharField(max_length=255, blank=True, null=True)  # Just a name, not linked to User model
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], default=0)  # Rating scale from 1 to 5
    comment = models.TextField(blank=True, null=True)  # Optional comment field

    def __str__(self):
        return f"Rating for {self.product.name} by {self.user if self.user else 'Anonymous'} - {self.rating}"

    class Meta:
        unique_together = ('product', 'user')  # Ensure each user can rate a product only once





class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    complete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.first_name} - {self.created_at}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"


class OrderAddress(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    mobile = models.CharField(max_length=15)
    address_line_1 = models.CharField(max_length=150)
    address_line_2 = models.CharField(max_length=150, blank=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)
   


