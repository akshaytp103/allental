from django.contrib import admin
from .models import *
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('category_name',)}
       

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields ={'slug' : ('name',)}

class VariationAdmin(admin.ModelAdmin):
    list_display  =('product','variation_category','variation_value','is_active')
    list_editable =('is_active',)
    list_filter   =('product','variation_category','variation_value')
   
    
admin.site.register(Product,ProductAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Variation,VariationAdmin)

   
