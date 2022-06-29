from multiprocessing import context
from django.shortcuts import redirect, render
from django.contrib import messages, auth
from product.forms import ProductForm
from product.models import *
from order.models import *
from django.contrib.auth.decorators import login_required


# Create your views here.

def master_signin(request):
    if request.user.is_authenticated:
        return redirect("admin_home")

    if request.method == "POST":

        email = request.POST["email"]
        password = request.POST["password"]
        user = auth.authenticate(email=email, password=password, is_superadmin=True)

        if user is not None:
            auth.login(request, user)
            messages.success(request, "Login Successful")
            return redirect("admin_home")
        else:
            messages.error(request, "Invalid credentials")
            return redirect("admin_signin")

    else:
        return render(request, "admin/adminlogin.html")


def admin_home(request):
    total_user = Account.objects.count()
    total_product=Product.objects.count()
    total_order=Order.objects.count()
    context={
        'total_user':total_user,
        'total_product':total_product,
        'total_order':total_order
    }
    return render (request,'admin/admindash.html',context)


def customer(request):
    users = Account.objects.all()
    context = {"users": users}
    return render(request, "admin/customer.html", context)


def customer_pickoff(request, customer_id):
    customer = Account.objects.get(id=customer_id)
    if customer.is_active:
        customer.is_active = False 
        print('user is blocked') 
    else:
        customer.is_active = True
    customer.save()

    return redirect("customer")


def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():
            print('valid')
            form.save()
            print('data saved successfully')
            return redirect('add_product')
        else:
            print('product not added')
            messages.info(request,'product not added')
    else:
        form = ProductForm()
    return render(request,'admin/addproduct.html',{'form':form})


def master_logout(request):
    auth.logout(request)
    return redirect("admin_signin")


def view_product(request):
    products = Product.objects.all()
    context = {"products": products}
    return render(request, "admin/product.html", context)


def product_delete(request, id) :
    products = Product.objects.get(id=id)
    context = {'product' : products}
    
    if request.method == 'POST' :
        products.delete()
        return redirect('viewproduct')
    
    return render(request, 'admin/productdelete.html', context)


def product_edit(request, id) :
    products = Product.objects.get(id=id)
    if request.method == 'POST' :
        form = ProductForm(request.POST, request.FILES, instance=products)   
        if form.is_valid() :
            form.save()
            return redirect('viewproduct')
        
    form = ProductForm(instance=products)
    context = {'form' : form}
    return render(request, 'admin/productedit.html', context)



@login_required(login_url='admin_signin')
def product_orders(request) :
    orders = Order.objects.all().order_by('-created_at')
    context = {
        'orders' : orders
    }
    return render(request, 'admin/orders.html', context)

@login_required(login_url='admin_signin')
def view_shipping_product(request,track_no):
    order = Order.objects.get(order_number=track_no)
    order_item = OrderProduct.objects.filter(order__order_number=track_no)
    
        
    context ={
        'order_item' : order_item,
        'order' : order,
    }
    
    return render(request, "admin/order-details.html", context)


@login_required(login_url='admin_signin')
def edit_shipping_product(request, pk):
    url = request.META.get('HTTP_REFERER')
    order_item = OrderProduct.objects.get(id=pk)
    
    if  order_item.status == 'ordered':
        order_item.status = 'shipped'
    elif order_item.status == 'shipped':
        order_item.status = 'out_for_delivery'
    elif order_item.status == 'out_for_delivery':
        order_item.status = 'delivered'
        if order_item.status == 'delivered':
           if order_item.is_paid == False:
               order_item.is_paid = True
    else:
        pass
   
    order_item.save()
    return redirect(url)
        
        
        


