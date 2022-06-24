
from django.contrib import admin
from .models import *

# Register your models here.

class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('payment','user','product','quantity','product_price','ordered')
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number','full_name','email','city','order_total','tax','is_ordered','created_at']
    list_filter = ['is_ordered']
    search_fields =['order_number','full_name','mobile','email']
    list_per_page=20
    inlines = [OrderProductInline]



admin.site.register(Order,OrderAdmin)
admin.site.register(OrderProduct)
admin.site.register(Payment)
