

from django.utils import timezone
from multiprocessing import context
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from accounts.otp import send_otp, verify_otp
from .forms import *
from .models import *
from django.contrib import messages , auth
from django.contrib.auth import authenticate, logout
from product.models import *
from django.core.paginator import Paginator


# Create your views here.
def home(request):
    products = Product.objects.all()
    catogory = Category.objects.all()
    context = {'products':products , 'catogory':catogory}
    return render(request,'index.html',context)


def home_view(request,slug):
    if (Category.objects.filter(slug=slug )):
        category_item=Product.objects.filter(slug=slug)
        catogory = Category.objects.all()
        context = {
         'catogory_item':category_item,
         'catogory':catogory
        }
        return render(request,'index.html',context)

def search(request) :
    
    if 'keyword' in request.GET :
        keyword = request.GET['keyword']
        if keyword :
            products = Product.objects.filter(name__icontains = keyword)
            
            paginator = Paginator(products, 6)
            page = request.GET.get('page')
            paged_products = paginator.get_page(page)
            product_count = products.count()
        else :
            products = Product.objects.all().filter(available=True).order_by('id')
            paginator = Paginator(products, 6)
            page = request.GET.get('page')
            paged_products = paginator.get_page(page)
            product_count = products.count()
    
    context = {
        'products' : paged_products,
        'product_count' : product_count
    }
    return render(request, 'shop.html', context)





def loginpage(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = Account.objects.get(email=email)
        except :
            messages.error(request,"user Does not exist..")

        user = authenticate(request,email=email,password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('home')
        else:
            messages.error(request,'user does not exist..')

    return render(request,'login.html')


def logoutuser(request):
    logout(request)
    return redirect('home')


def register(request):
    form = RegistrationForm()

    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name  = form.cleaned_data['last_name']
            email      = form.cleaned_data['email']
            gender     = form.cleaned_data['gender']
            mobile     = form.cleaned_data['mobile']
            password   = form.cleaned_data['password']

            request.session['first_name'] = first_name
            request.session['last_name']  = last_name
            request.session['email']      = email
            request.session['gender']     = gender
            request.session['mobile']     = mobile
            request.session['password']   = password

            send_otp(mobile)
            return redirect('otp')

    context = {'form' : form}
    return render(request,'register.html',context)



def otp(request):
    if  request.method == 'POST':
        otp_check = request.POST.get('otp')
        mobile=request.session['mobile']

        verify=verify_otp(mobile,otp_check)

        if  verify:
            messages.success(request,'account has created successfuly please login now') 

            first_name = request.session['first_name']
            last_name  = request.session['last_name']
            email      = request.session['email']
            gender     = request.session['gender']
            mobile     = request.session['mobile']
            password   = request.session['password']

            user = Account.objects.create_user(
                first_name =  first_name,
                last_name  =  last_name,
                email      =  email,
                gender     =  gender,
                mobile     =  mobile,
                password   =  password
            )
            user.is_verified = True
            user.save()
            return redirect('login')
        
        else:
            messages.error(request,'invalid otp recheck')
            return redirect ('otp')
        
    return render(request,'otp.html')



@login_required(login_url='login')
def my_address(request) :
    if request.method =='POST':
        form = AddressForm(request.POST)
        if form.is_valid() :
            new_address = form.save(commit=False)
            new_address.user = request.user
            new_address.save() 
            
            messages.success(request, 'Address Added Successfully!')
            return redirect('my_address')
        else :
            messages.error(request, 'Oops, There is an error adding the Address')
            return redirect('my_address')       
    address = Address.objects.filter(user=request.user).order_by('-created_at')
    form = AddressForm()
    context = {
        'form' : form,
        'address' : address,
    }
    return render(request, 'useraccount.html', context)



@login_required(login_url='login')
def delete_address(request, id) :
    if request.method == 'POST' :
        delete_address = Address.objects.get(pk=id)
        delete_address.delete()
        return redirect('my_address')

