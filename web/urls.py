from django.urls import path
from . import views
from django.contrib import admin
from .views import Cart, CheckOut
from .middlewares.auth import  auth_middleware
from .views import OrderView


urlpatterns = [
   
    #path('store', views.homecart , name='hc'),
    path('store', views.store, name="store"),
    path('', views.main, name="main"),
    #path('con', views.contact, name='contact'),
    #path('home', views.homePage, name="home"),
    
    #path('', Index.as_view(), name='homepage'),
    #path('cart', auth_middleware(Cart.as_view()), name='cart'),
    path('cart', Cart.as_view(), name='cart'),
    path('checkout/', auth_middleware(CheckOut.as_view()), name='checkout'),
    path('login/', views.login, name="login"),
    path('signup/', views.signup, name="signup"),
    path('logout/', views.logout, name="logout"),
    #path('cart/', views.cart, name="cart"),
    #path('checkout/', views.checkout, name="checkout"),
    path('order', views.orderpage, name="order"),
    #path('rurl', views.reverse_url, name="rurl"),
    #path('jstry', views.reverse_url, name="jstry"),
    path('product/<int:id>', views.product_detail, name="detail"),
    #path('order', auth_middleware(OrderView.as_view()), name='order'),
]

