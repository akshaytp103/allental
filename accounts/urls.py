
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('login/',views.loginpage,name="login"),
    path('register/',views.register,name="register"),
    path('logout/',views.logoutuser,name='logout'),
    path('otp/', views.otp,name='otp'),
    path('home_view/<str:slug>/',views.home_view,name="home_view"),
    path('search/', views.search, name='search'),
    path('myaddress/',views.my_address,name='my_address'),
    path('delete_address/<str:id>/',views.delete_address,name='delete-address') 

]

