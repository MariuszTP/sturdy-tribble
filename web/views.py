from django.shortcuts import render, redirect, get_object_or_404

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.hashers import make_password, check_password
from .models import *
from .middlewares.auth import auth_middleware
from django.views import View


from django.core.mail import send_mail, BadHeaderError

from web.models import Customer

from web.models import Product
from web.models import Order



from django.views import View






def main(request):
    if request.method =="POST":
        subject = request.POST.get("subject")
        message = request.POST.get("message")
        from_email = request.POST.get("from_email")
        data = {
            'subject' : subject,
            'message' : message,
            'from_email' : from_email,
        }
        message = '''
        New message:{}
        From: {}
        '''.format(data['message'], data['from_email'])
        send_mail(data['subject'], message, '', ['turekpython@gmail.com'])
    


    categories = Category.objects.all()
    context = {
        "categories" : categories
    }
    return render(request, 'mainv1.html', context)


def store(request):
    if request.method == 'POST':
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity - 1
                else:
                    cart[product] = quantity + 1
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        print(request.session['cart'])
        return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 


    else:
       
        categories = Category.objects.all()
        category_id = request.GET.get('category')
        if category_id:
            products = Product.objects.filter(category=category_id)
        else:
            products = Product.objects.all()
        context = {'products': products, 'categories': categories}
        return render(request, 'storev1.html', context)



def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        error_msg = None
        if customer:
            flag = check_password(password, customer.password)
            if flag:
                request.session['customer'] = customer.id
                request.session['email'] = customer.email
                return redirect("main")
            else:
                error_msg = "Email or Password is incorrect."
        else:
            error_msg = "Email or Password is incorrect."
        return render(request, 'login.html', {'error_msg': error_msg})


def validateCustomer(customer):
    err_msg = None
    if not customer.first_name:
        err_msg = "First Name Required."
    elif len(customer.first_name) < 3:
        err_msg = "First Name must be 3 characters long."
    elif not customer.last_name:
        err_msg = "Last Name Required."
    elif len(customer.last_name) < 3:
        err_msg = "Last Name must be 3 characters long."
    elif not customer.phone:
        err_msg = "Phone is Required."
    elif len(customer.phone) < 10:
        err_msg = "Phone Number must be 10 characters long."
    elif not customer.email:
        err_msg = "Email is Required."
    elif customer.does_exits():
        err_msg = "User with this email address already registered."
    return err_msg


def registerCustomer(request):
    first_name = request.POST.get('firstname')
    last_name = request.POST.get('lastname')
    phone = request.POST.get('phone')
    email = request.POST.get('email')
    password = request.POST.get('password')

    values = {
        'firstname': first_name,
        'lastname': last_name,
        'phone': phone,
        'email': email,
    }
    customer = Customer(first_name=first_name, last_name=last_name, phone=phone, email=email, password=password)

    err_msg = None
    err_msg = validateCustomer(customer)

    if not err_msg:
        customer.password = make_password(customer.password)
        customer.save()
        return redirect('cart')
    else:
        return render(request, 'signup.html', {'error_msg': err_msg, 'values': values})


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    else:
        return registerCustomer(request)


def logout(request):
    request.session.clear()
    return redirect('login')




class Cart(View):
    def get(self, request):
        cart = request.session.get('cart', None)
        if not cart:
            cart = {}
        request.session['cart'] = cart
        
        ids = list(request.session.get('cart').keys())
        products = Product.get_products_by_id(ids)
        print(products)
        return render(request , 'cart.html' , {'products' : products} )


""" def checkout(request):
    if request.method == "POST":
        address = request.POST.get("address")
        phone = request.POST.get("phone")
        customer = request.session.get("customer")
        cart = request.session.get("cart")
        products = Product.get_products_by_id(list(cart.keys()))

        for product in products:
            order = Order(customer=Customer(id=customer), product=product, price=product.price, address=address,
                          phone=phone, quantity=cart.get(str(product.id)))
            order.save()

        request.session['cart'] = {}

        return redirect("cart")
    else:
        return render(request, 'storev1.html')
 """




class CheckOut(View):
    def post(self, request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        products = Product.get_products_by_id(list(cart.keys()))
        print(address, phone, customer, cart, products)

        for product in products:
            print(cart.get(str(product.id)))
            order = Order(customer=Customer(id=customer),
                          product=product,
                          price=product.price,
                          address=address,
                          phone=phone,
                          quantity=cart.get(str(product.id)))
            order.save()
        request.session['cart'] = {}

#       return redirect('cart')
        return render(request, 'cart.html')




def product_detail(request, id):
    obj = get_object_or_404(Product, id=id)
    context = {
       "product" : obj
    }
    return render(request, 'product_detail.html', context)



    

@auth_middleware
def orderpage(request):
    customer = request.session.get('customer')
    order = Order.get_order_by_customer(customer)
    print(order)
    return render(request, 'order.html', {'order': order})






