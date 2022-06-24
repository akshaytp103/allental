from email.mime import image
from sre_constants import CATEGORY_LOC_NOT_WORD
from tkinter import CASCADE
from typing import final
from django.db import models
from django.forms import DateTimeField
from accounts.models import *
from django.urls import reverse
# Create your models here.




class Category(models.Model):
    category_name = models.CharField(max_length=50,null=True)
    slug = models.SlugField(max_length=100, unique=True,null=True)
    description = models.TextField(max_length=250,blank=True)
    image= models.ImageField(upload_to='photos/categories',blank=True)
    
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_url(self):
        return reverse('products-by-category', args=[self.slug])



    def __str__(self):
        return self.category_name


class Product(models.Model):
    name         = models.CharField(max_length=100,null=True)
    category     = models.ForeignKey(Category,on_delete=models.CASCADE)
    slug         = models.SlugField(max_length=200,db_index=True)
    price        = models.FloatField()
    image        = models.ImageField (upload_to="image/product")
    description  = models.TextField(max_length=1000)
    available    = models.BooleanField(default=True,verbose_name="available")
    stock        = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['name']
        index_together = [
            ['id', 'slug']
        ]
        verbose_name = 'item'
        verbose_name_plural = 'item'
 
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product-details', args=[self.category.slug, self.slug])



class VariationManager(models.Manager):
    def color(self):
        return super(VariationManager,self).filter(variation_category ='color',is_active=True)

    def size(self):
        return super(VariationManager,self).filter(variation_category ='size',is_active=True)

variation_category_choices =(
    ('color','color'),
    ('size','size'),
)

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category =models.CharField(max_length=100,choices=variation_category_choices)
    variation_value =models.CharField(max_length=100)
    is_active       =models.BooleanField(default=True)
    created_date    =models.DateTimeField(auto_now=True)

    objects = VariationManager()

    def __str__(self):
        return self.variation_value
        


class OrderItem(models.Model):
    user          =   models.ForeignKey(Account,on_delete = models.CASCADE,blank=True,null=True)
    product       =   models.ForeignKey(Product,on_delete = models.CASCADE)
    ordered       =   models.BooleanField(default=False,null=True,blank=False)
    quantity      =   models.IntegerField(null=False,blank=False)

    def __str__(self):
        return f"{self.quantity} - {self.product.name}"
    def get_total_price(self):
        return self.quantity * self.product.price

    def get_final_price(self):
        return self.get_total_price()

    


