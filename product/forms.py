from django import forms
from django.db import models
from django.db.models import fields
from .models import *


class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("category_name", "image", "description")

    def __init__(self, *args, **kwargs):
        super(AddCategoryForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ("category", "name", "image", "description", "price", "stock")
        
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"