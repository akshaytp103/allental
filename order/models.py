
from unicodedata import name
from product.models import *
from telnetlib import STATUS
from django.db import models
from accounts.models import *
from product.models import Product

# Create your models here.
class Payment(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE,null=True) 
    name =models.CharField(max_length=100,null=True )
    amount = models.CharField(max_length=100)
    order_id =models.CharField(max_length=100,blank=True)
    razorpay_payment_id= models.CharField(max_length=100, blank=True,null=True)  
    payment_method=models.CharField(max_length=100)
    paid =models.BooleanField(default=False)
    created_at=models.DateField(auto_now_add=True)

    
class Order(models.Model):
    user =models.ForeignKey(Account,on_delete=models.SET_NULL,null=True)
    Payment=models.ForeignKey(Payment,on_delete=models.SET_NULL,null=True)
    order_number = models.CharField(max_length=100)
    full_name =models.CharField(max_length=50)
    email=models.EmailField(max_length=50)
    address=models.CharField(max_length=50)
    city=models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    country=models.CharField(max_length=50)
    pin_code = models.CharField(max_length=6)
    mobile=models.CharField(max_length=15)
    order_note=models.CharField(max_length=100,blank=True)
    order_total=models.FloatField()
    tax=models.FloatField()
    ip = models.CharField(blank=True,max_length=20)
    is_ordered =models.BooleanField(default=False)
    created_at=models.DateField(auto_now_add=True)
    updated_at=models.DateField(auto_now_add=True)


    def __str__(self):
        return self.full_name

  
        

                             

class OrderProduct(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,blank=True,null=True)
    payment=models.ForeignKey(Payment,on_delete=models.SET_NULL,blank=True,null=True)
    user =models.ForeignKey(Account,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation,blank=True)
    quantity=models.IntegerField()
    product_price=models.FloatField()
    ordered=models.BooleanField(default=False)
    created_at=models.DateField(auto_now_add=True)
    updated_at=models.DateField(auto_now_add=True)
    ORDER_STATUS = (
        ('ordered', 'ordered'),
        ('shipped','shipped'),
        ('out_for_delivery', 'out_for_delivery'),
        ('delivered','delivered'),
        ('cancelled','cancelled'),
    )
    status = models.CharField(max_length=150,choices=ORDER_STATUS, default='ordered')
    is_paid = models.BooleanField(default=False)


    def __str__(self):
        return self.product.name
    

