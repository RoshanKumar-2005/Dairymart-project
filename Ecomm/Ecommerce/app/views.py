from django.shortcuts import render,redirect,get_object_or_404
from django.db.models import Q,Count
from django.views import View
from .models import product,Cart,Customer,product,ShippingAddress,Wishlist,OrderPlaced
from . forms import CustomerRegistrationForm,CustomerProfileForm,Customer
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django import template
register=template.Library()



# Create your views here.
def home(request):
    products = product.objects.all()
    wishlist_items = []
    if request.user.is_authenticated:
        wishlist_items = Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True)
    return render(request, 'app/home.html', {'products': products, 'wishlist_items': wishlist_items})

def about(request):
    return render(request,"app/about.html")

def contact(request):
    return render(request,"app/contact.html")


class categoryView(View):
    def get(self,request,val):
        self.product=product.objects.filter(category=val)
        title=product.objects.filter(category=val).values('title')
        return render(request,"app/category.html",{'product':self.product,'category':val})
    

class ProductDetailView(View):
    def get(self,request,pk):
        prod = get_object_or_404(product, pk=pk)
        return render(request, "app/productdetails.html", {'product': prod})
    
class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form':form})
    
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Congratulations! User Registration Successful')
        else:
            messages.warning(request,"Invalid Input Data")
        return render(request, 'app/customerregistration.html', {'form':form})

class ProfileView(View):
    def get(self, request):
        customer, created = Customer.objects.get_or_create(user=request.user)
        form = CustomerProfileForm(instance=customer)
        return render(request, 'app/profile.html', {'form': form})

    def post(self, request):
        customer, created = Customer.objects.get_or_create(user=request.user)
        form = CustomerProfileForm(request.POST, instance=customer)

        if form.is_valid():
            form.save()
            messages.success(request, "Congratulations! Profile Saved Successfully")
        else:
            messages.warning(request, "Invalid Input Data")

        return render(request, 'app/profile.html', {'form': form})
    
@login_required
def add_to_cart(request, id):
    prod= get_object_or_404(product, pk=id)
    user = request.user
    cart_item, created = Cart.objects.get_or_create(user=user, product=prod)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('show_cart')

@login_required
def increase_cart(request, id):
    cart_item = get_object_or_404(Cart, id=id, user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('show_cart')

@login_required
def decrease_cart(request, id):
    cart_item = get_object_or_404(Cart, id=id, user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('show_cart')

@login_required
def update_cart(request, id, action):
    cart_item = get_object_or_404(Cart, id=id, user=request.user)
    shipping = 40

    if action == 'increase':
        cart_item.quantity += 1
    elif action == 'decrease':
        cart_item.quantity -= 1
        if cart_item.quantity <= 0:
            cart_item.delete()
            total_price = sum(item.product.discounted_price * item.quantity for item in Cart.objects.filter(user=request.user))
            final_price = total_price + shipping if total_price > 0 else 0
            return JsonResponse({'quantity': 0, 'total_price': final_price})
    cart_item.save()
    total_price = sum(item.product.discounted_price * item.quantity for item in Cart.objects.filter(user=request.user))
    final_price = total_price + shipping if total_price > 0 else 0

    return JsonResponse({'quantity': cart_item.quantity, 'total_price': final_price})

@login_required
def buy_now(request, id):
    product_item = get_object_or_404(product, id=id) 
    context = {'product': product_item}
    return render(request, 'app/buy_now.html', context)

@login_required
def show_cart(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)
    
    subtotal = sum(item.quantity * item.product.discounted_price for item in cart_items)
    shipping = 40 if cart_items else 0
    total_amount = subtotal + shipping

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping': shipping,
        'total_amount': total_amount,
    }
    return render(request, 'app/add_to_cart.html', context)

@login_required
def remove_cart(request, id):
    item = get_object_or_404(Cart, id=id, user=request.user)
    item.delete()
    return redirect('show_cart')

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Cart, ShippingAddress

@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    shipping = 40

    subtotal= sum(item.quantity * item.product.discounted_price for item in cart_items)
    total_amount = subtotal + shipping

    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')

        ShippingAddress.objects.create(
            user=request.user,
            name=name,
            phone=phone,
            address=address,
            city=city,
            state=state,
            pincode=pincode
        )
        cart_items.delete()
        messages.success(request, "Your order has been placed successfully!")
        return redirect('home') 

    return render(request, 'app/checkout.html', {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping_charge': shipping,
        'total_amount': total_amount
    })

@register.filter
def mul(value, arg):
    return value * arg


@login_required
def place_order(request):
    if request.method == 'POST':

        print("POST DATA:", request.POST)

        full_name = request.POST.get('name')
        address = request.POST.get('address')
        city = request.POST.get('city')
        zip_code = request.POST.get('zip')
        phone = request.POST.get('phone')

        shipping = ShippingAddress.objects.create(
            user=request.user,
            full_name=full_name,
            address=address,
            city=city,
            zip_code=zip_code,
            phone=phone
        )

        cart_items = Cart.objects.filter(user=request.user)
        print("CART ITEMS:", cart_items)

        for item in cart_items:
            OrderPlaced.objects.create(
                user=request.user,
                product=item.product,
                quantity=item.quantity,
                address=shipping,
                status='Pending'
            )

        cart_items.delete()

        messages.success(request, "Order placed successfully!")
        return redirect('orders')

    return redirect('cart')

@login_required
def orders(request):
    orders = OrderPlaced.objects.filter(user=request.user).order_by('-ordered_date')
    return render(request, 'app/orders.html', {'orders': orders})


@login_required
def add_to_wishlist(request, id):
    prod = get_object_or_404(product, pk=id)
    user = request.user
    wishlist_item, created = Wishlist.objects.get_or_create(user=user, product=prod)

    if created:
        wishlist_item.save()

    return redirect('wishlist')


@login_required
def remove_from_wishlist(request, id):
    item = get_object_or_404(Wishlist, id=id, user=request.user)
    item.delete()
    return redirect('wishlist')


@login_required
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'app/wishlist.html', {'wishlist_items': wishlist_items})

@login_required
def add_to_wishlist(request, id):
    prod = get_object_or_404(product, pk=id)
    user = request.user
    wishlist_item, created = Wishlist.objects.get_or_create(user=user, product=prod)

    if created:
        wishlist_item.save()

    return redirect('wishlist')


@login_required
def remove_from_wishlist(request, id):
    item = get_object_or_404(Wishlist, id=id, user=request.user)
    item.delete()
    return redirect('wishlist')


@login_required
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'app/wishlist.html', {'wishlist_items': wishlist_items})


@login_required
def toggle_wishlist(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        prod = get_object_or_404(product, id=product_id)
        user = request.user

        wishlist_item, created = Wishlist.objects.get_or_create(user=user, product=prod)

        if not created:
            wishlist_item.delete()
            return JsonResponse({"status": "removed"})
        else:
            return JsonResponse({"status": "added"})

    return JsonResponse({"status": "failed"}, status=400)


def search(request):
    query = request.GET.get('query')
    products = []
    wishlist_items = []

    if query:
        products = product.objects.filter(
            Q(title__icontains=query) | 
            Q(category__icontains=query) |
            Q(description__icontains=query)
        ).distinct()

    if request.user.is_authenticated:
        wishlist_items = Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True)

    return render(request, 'app/search.html', {
        'products': products,
        'query': query,
        'wishlist_items': wishlist_items,
    })

@login_required
def payment_page(request):
    return render(request, 'app/payment_page.html')


@login_required
def confirm_payment(request):
    if request.method == 'POST':
        transaction_id = request.POST.get('transaction_id')

        shipping = ShippingAddress.objects.filter(user=request.user).last()

        cart_items = Cart.objects.filter(user=request.user)

        for item in cart_items:
            OrderPlaced.objects.create(
                user=request.user,
                product=item.product,
                quantity=item.quantity,
                address=shipping,
                payment_id=transaction_id,
                status='Pending'
            )

        cart_items.delete()

        messages.success(request, "Payment Successful! Order Placed 🎉")
        return redirect('orders')

    return redirect('cart')


from django.contrib.auth import logout
from django.shortcuts import redirect

def user_logout(request):
    logout(request)
    return redirect('login')
