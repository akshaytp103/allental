from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('',views.master_signin,name="admin_signin"),
    path('admin_home/',views.admin_home,name="admin_home"),
    path('customer/',views.customer,name="customer"),
    path('customer_pickoff/<customer_id>/',views.customer_pickoff,name="customer_pickoff"),
    path('add_product/',views.add_product,name="add_product"),
    path('masterlogout/',views.master_logout,name="masterlogout"),
    path('viewproduct/',views.view_product,name="viewproduct"),
    path('product_delete/<str:id>/', views.product_delete,name='productdelete'),
    path('product_edit/<str:id>/', views.product_edit,name='productedit'),
    path('orders/', views.product_orders, name='orders'),
    path('orders/order-details/<str:track_no>/', views.view_shipping_product, name='ordered-products'),
    path('orders/edit-shipping-product/<str:pk>/', views.edit_shipping_product, name='edit-shipping-product'),  
]