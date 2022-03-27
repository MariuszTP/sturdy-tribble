from django.urls import path
from . import views
from django.contrib import admin
from .views import Cart, CheckOut
from .middlewares.auth import  auth_middleware




#from .views import OrderView


urlpatterns = [
   
    path('store', views.store, name="store"),
    path('', views.main, name="main"),
    path('cart', Cart.as_view(), name='cart'),
    path('checkout/', CheckOut.as_view(), name='checkout'),
    path('login/', views.login, name="login"),
    path('signup/', views.signup, name="signup"),
    path('logout/', views.logout, name="logout"),
    path('order', views.orderpage, name="order"),
    path('product/<int:id>', views.product_detail, name="detail"),
    #path('order', auth_middleware(OrderView.as_view()), name='order'),
]

