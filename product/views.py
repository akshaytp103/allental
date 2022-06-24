
from django.shortcuts import get_object_or_404, render,redirect
from product.models import *
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator

# Create your views here.

def product_details(request,slug):
    item =Product.objects.filter(slug=slug)
    context= {'items':item}
    return render(request,'product_details.html',context)

def store(request,category_slug=None):
    categories = None
    products = None
    if category_slug != None:
        categories = get_object_or_404(Category,slug=category_slug)
        products = Product.objects.filter(category=categories,available=True) 
        paginator = Paginator(products,6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page) 
        product_count = products.count()
    else:
        products = Product.objects.all().filter(available=True).order_by('id') 
        paginator = Paginator(products,6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count() 

    context = {        
        'product_count':product_count,
        'products':paged_products,
    }
    return render(request,'store.html',context) 

