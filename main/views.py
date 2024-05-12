from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from . models import Product, Order, OrderItem, MyUser
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})


def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not username or not password:
            messages.error(request, 'Please enter both username and password.')
            return redirect('signin')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home') 
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
    return render(request, 'signin.html')


from .models import MyUser  

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        contact_number = request.POST.get('contact_number')
        confirm_password = request.POST.get('confirm_password')

        if not username or not password or not confirm_password:
            messages.error(request, 'Please fill out all fields.')
            return redirect('signup')

        # Check if the passwords match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match. Please try again.')
            return redirect('signup')

        # Check if the username is already taken
        if MyUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please choose a different one.')
            return redirect('signup')

        # Create new user with contact number
        user = MyUser.objects.create_user(username=username, password=password, contact_number=contact_number)
        login(request, user)
        return redirect('home') 

    return render(request, 'signup.html')


def signout(request):
    logout(request)
    return redirect('home')


from django.shortcuts import render, redirect
from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'image', 'description']

@staff_member_required
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')  
    else:
        form = ProductForm()
    return render(request, 'create_product.html', {'form': form})
    

def orders(request):

    user_orders = Order.objects.filter(user=request.user)
    orders_by_status = {}
    for order in user_orders:
        status = order.get_status_display()  
        if status not in orders_by_status:
            orders_by_status[status] = []
        orders_by_status[status].append(order)

    return render(request, 'orders.html', {'orders_by_status': orders_by_status})


@login_required
def transaction(request):
    selected_products = request.session.get('selected_products', {})
    subtotal = 0
    for product_id, product_data in selected_products.items():
        subtotal += product_data['subtotal']

    shipping_fee = 48
    total = subtotal + shipping_fee

    if request.method == 'POST':
        selected_products = {}
        subtotal = 0
        for product in Product.objects.all():
            quantity = int(request.POST.get(f'quantity_{product.id}', 0))
            if quantity > 0:
                selected_products[product.id] = {
                    'name': product.name,
                    'quantity': quantity,
                    'price': product.price,
                    'subtotal': product.price * quantity
                }
                subtotal += selected_products[product.id]['subtotal']

        shipping_fee = 48
        total = subtotal + shipping_fee
        request.session['selected_products'] = selected_products

    return render(request, 'transaction.html', {'selected_products': selected_products, 'subtotal': subtotal, 'shipping_fee': shipping_fee, 'total': total})



@login_required
def finalize_order(request):
    if request.method == 'POST':
        shipping_address = request.POST.get('shipping_address')
        print(shipping_address)
        if not shipping_address:
            messages.error(request, "Shipping address is required.")
            return redirect('transaction')

        request.session['shipping_address'] = shipping_address
        messages.success(request, "Shipping address saved successfully.")

        selected_products = request.session.get('selected_products', {})
        if not selected_products:
            messages.error(request, "No products selected for order.")
            return redirect('transaction')

        user = request.user

        order = Order.objects.create(user=user, status='Pending', shipping_fee=48, total_price=0, shipping_address=shipping_address)

        total_price = 0
        for product_id, product_data in selected_products.items():
            product = Product.objects.get(pk=product_id)
            order_item = OrderItem.objects.create(order=order, product=product, quantity=product_data['quantity'])
            total_price += product_data['subtotal']

        order.total_price = total_price
        order.save()

        del request.session['selected_products']
        del request.session['shipping_address']

        messages.success(request, "Order finalized successfully.")
        return redirect('home')

    return render(request, 'finalize_order.html')



