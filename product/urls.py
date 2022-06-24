
from . import views
from django.urls import path




urlpatterns = [
    path('product-details/<slug:slug>/',views.product_details,name="product-details"),
    path('store/<slug:category_slug>/',views.store,name="products-by-category"),
]   