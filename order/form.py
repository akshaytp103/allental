
from django import forms
from .models import *
from django import forms
from .models import *


class OrderForm(forms.ModelForm):
    class Meta:
        model =Order
        fields =['full_name','email','address','city','state','country','pin_code','mobile','order_note']




class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = '__all__'
