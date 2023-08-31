from django.shortcuts import render, redirect
from .models import Product, Category, Cart, ProductCart, Order, ProductOrder
from .forms import SignupForm, CheckoutForm
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()

            messages.success(request, f'Your account has been successfully created.')
            return redirect('login')
    else:
        form = SignupForm()

    context = {'form': form}
    return render(request, 'register.html', context)


def index(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'index.html', context)


@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.productcart_set.all()  # Get the products in the cart

    context = {
        'cart': cart,
        'cart_items': cart_items,
    }

    return render(request, 'cart.html', context)


def product_details(request, slug):
    product = get_object_or_404(Product, slug=slug)
    context = {'product': product}
    return render(request, 'product.html', context)


def products_by_category(request, slug):
    category = Category.objects.get(slug=slug)
    products = Product.objects.filter(category=category)

    context = {
        'category': category,
        'products': products,
    }
    return render(request, 'category.html', context)


@login_required
def checkout(request):
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            cart = Cart.objects.filter(active=True, user=request.user).first()
            cart.active = False
            cart.save()
            order = Order(cart=cart, full_name=request.POST.get('full_name'), address=request.POST.get('address'),
                          delivery_status='new')
            order.save()
            print(order)
            return redirect('/orders')
    else:
        form = CheckoutForm()

    context = {
        'form': form
    }
    return render(request, 'checkout.html', context)


def success(request):
    return render(request, 'success.html')


@login_required
def add_to_cart(request, slug):
    product = Product.objects.get(slug=slug)
    cart, created = Cart.objects.get_or_create(user=request.user)
    product_cart, created = ProductCart.objects.get_or_create(product=product, cart=cart)
    product_cart.quantity += 1
    if created:
        product_cart.quantity = 1
    product_cart.save()

    return redirect('/')


@login_required
def remove_from_cart(request, slug):
    cart = Cart.objects.get_or_create(user=request.user)[0]
    product = Product.objects.get(slug=slug)

    product_in_cart = ProductCart.objects.get(cart=cart, product=product)

    if product_in_cart is not None:
        product_in_cart.delete()

    return redirect('/')


@login_required
def profile(request):
    context = {'user': request.user}
    return render(request, 'profile.html', context)


@login_required
def orders(request):
    context = {'orders': Order.objects.filter(user=request.user)}
    return render(request, 'orders.html', context)
