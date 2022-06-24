from datetime import date
from http import client
from urllib import response
from django.shortcuts import redirect, render
from requests import request
from cart.models import *
from order.form import OrderForm, PaymentForm
from order.models import *
from product.models import *
import razorpay
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@csrf_exempt       
def place_order(request,total=0,quantity=0):
    current_user=request.user

    cart_items =CartItem.objects.filter(user=current_user)
    cart_count =cart_items.count()
    if cart_count <= 0:
        return redirect('home')


    grand_total =0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity 
    tax = (18 * total)/100
    grand_total = total + tax 
    request.session['grand_total']=grand_total
    request.session['total']=total
    request.session['tax']=tax

    if request.method =="POST":
        form =OrderForm(request.POST)   
        if form.is_valid(): 

            data = Order()
            data.user = current_user
            data.full_name = form.cleaned_data['full_name'] 
            data.email = form.cleaned_data['email']
            data.address = form.cleaned_data['address']
            data.city = form.cleaned_data['city']
            data.state = form.cleaned_data['state']
            data.country = form.cleaned_data['country']  
            data.pin_code = form.cleaned_data['pin_code']
            data.mobile = form.cleaned_data['mobile']            
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax 
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()


            yr = int(date.today().strftime('%Y'))
            dt = int(date.today().strftime('%d'))
            mt = int(date.today().strftime('%m'))
            d = date(yr,mt,dt)
            current_date = d.strftime('%Y%m%d')
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user=current_user,is_ordered=False,order_number=order_number)
            print(order)
            order_id=order.order_number
            request.session['order_number']=order_number

            context= {
                'order':order,
                'cart_items':cart_items,
                'total':total,
                'tax':tax,
                'grand_total':grand_total,
            }
            return render(request,'payments.html',context)

    return render(request,'checkout.html')


def cash_on_delivery(request):
    if request.method == 'POST':
        try :            
            order_number = request.session['order_number']
            order= Order.objects.get(order_number=order_number) 
            order.is_ordered = True           
            order.save()
            
            # move the cart item to orderproduct table
            cart_items=CartItem.objects.filter(user=request.user)
            print(cart_items) 

            for item in cart_items:
                orderproduct = OrderProduct()
                orderproduct.order_id = order.id          
                orderproduct.user_id = request.user.id
                orderproduct.product_id = item.product_id
                print(orderproduct.product_id)
                print('oruderifididiqwertyertyu')
                orderproduct.quantity = item.quantity
                orderproduct.product_price = item.product.price
                orderproduct.ordered = True
                print('orderprosaved')
                orderproduct.save()

                cart_item = CartItem.objects.get(id=item.id)
                print(cart_item)
                product_variation = cart_item.variations.all()
                print(product_variation)
                print('productvariations')
                orderproduct = OrderProduct.objects.get(id=orderproduct.id)
                print(orderproduct)
                print('idididi')
                orderproduct.variations.set(product_variation)
                print('qwerrtyuu')
                orderproduct.save() 

                # Reduce the quantity of the sold products
                product = Product.objects.get(id=item.product_id)
                product.stock -= item.quantity
                product.save()

            # clear cart
            print('tptptptptpt')
            CartItem.objects.filter(user=request.user).delete()
                
            return redirect('home')


        except :
             return redirect('cart')




@csrf_exempt
def payments(request):
    user = request.user
    order_id=request.session['order_number']
    order=Order.objects.get(order_number=order_id)   
    cart_items =CartItem.objects.filter(user=user)
    total=request.session['total']
    tax=request.session['tax']
    grand_total=request.session['grand_total']

    if request.method =='POST':
        
        name = user.first_name
        amount =int(request.session['grand_total']) * 100


        # create razorpay client
        client =razorpay.Client(auth=('rzp_test_Wg9g7aSl8rGdmP','JhinxMUOsC3sN0oC8SiCsilE'))

        # create order
        response_payment = client.order.create(dict(amount=amount,
                                                    currency='INR')
                                                ) 
        
        order_id =response_payment['id']
        order_status= response_payment['status'] 

        if order_status == 'created':
            payment =Payment(
                name = name,
                amount = amount,
                order_id = order_id,
                
            )
            payment.save()       
            response_payment['name']=name

            form = PaymentForm(request.POST or None)
 
            context={
                'form':form,
                'payment':response_payment,
                'order':order,
                'cart_items':cart_items,
                'total':total,
                'tax':tax,
                'grand_total':grand_total,
            }
            return render(request,'payments.html',context)

    form = PaymentForm()
    return render(request,'payments.html',{'form':form ,'order':order})

@csrf_exempt
def payment_status(request,order_number):
    total=request.session['total']
    tax=request.session['tax']
    grand_total=request.session['grand_total']
    response = request.POST
    params_dict ={
        'razorpay_order_id':response['razorpay_order_id'],
        'razorpay_payment_id':response['razorpay_payment_id'],
        'razorpay_signature':response['razorpay_signature']
    }

    #client instance
    client = razorpay.Client(auth=('rzp_test_Wg9g7aSl8rGdmP','JhinxMUOsC3sN0oC8SiCsilE'))
    try:
        status = client.utility.verify_payment_signature(params_dict)
        payment =Payment.objects.get(order_id=response['razorpay_order_id']) 
        payment.razorpay_payment_id=response['razorpay_payment_id']
        payment.payment_method='Razorpay'
        payment.paid = True 

        
        payment.save()


        order_number=request.session['order_number'] 
        print(order_number)
        order= Order.objects.get(order_number=order_number) 
        order.payment= payment
        order.is_ordered = True
        order.save()

        # move the cart item to orderproduct table
        cart_items=CartItem.objects.filter(user=request.user)

        for item in cart_items:
            orderproduct = OrderProduct()
            orderproduct.order_id = order.id
            orderproduct.payment = payment
            orderproduct.user_id = request.user.id
            orderproduct.product_id = item.product_id
            orderproduct.quantity = item.quantity
            orderproduct.product_price = item.product.price
            orderproduct.ordered = True
            orderproduct.save()

            cart_item = CartItem.objects.get(id=item.id)
            product_variation = cart_item.variations.all()
            orderproduct = OrderProduct.objects.get(id=orderproduct.id)
            orderproduct.variations.set(product_variation)
            orderproduct.save()

            # Reduce the quantity of the sold products
            product = Product.objects.get(id=item.product_id)
            product.stock -= item.quantity
            product.save()

        # clear cart
        CartItem.objects.filter(user=request.user).delete()

        print(order)

        context={
                'order':order,
                'cart_items':cart_items,
                'total':total,
                'tax':tax,
                'grand_total':grand_total,
                'status':True,
        }
        return render(request,'payment_status.html',context) 

        
    except:
        context ={
            'order':order,
            'cart_items':cart_items,
            'total':total,
            'tax':tax,
            'grand_total':grand_total,
            'status':False,          
        }
        return render(request,'payment_status.html',context) 



