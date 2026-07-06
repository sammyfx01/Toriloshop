from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Product, Order, OrderItem, Coupon, UsedCoupon, Category
from .cart import Cart
from decimal import Decimal
from django.utils import timezone

# ===== HOME VIEW =====
def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    
    now = timezone.now()
    active_coupons = Coupon.objects.filter(
        active=True,
        valid_from__lte=now,
        valid_to__gte=now
    )[:5]
    
    return render(request, 'products/home.html', {
        'products': products,
        'active_coupons': active_coupons,
        'categories': categories,
    })

# ===== PRODUCT VIEWS =====
def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    category_id = request.GET.get('category')
    
    if category_id:
        products = products.filter(category_id=category_id)
    
    return render(request, 'products/product_list.html', {
        'products': products,
        'categories': categories,
        'selected_category': category_id,
    })

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'products/product_detail.html', {'product': product})

def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    categories = Category.objects.all()
    return render(request, 'products/category_products.html', {
        'category': category,
        'products': products,
        'categories': categories,
    })

# ===== CART VIEWS =====
def cart_detail(request):
    cart = Cart(request)
    cart_data = cart.get_items(Product)
    
    now = timezone.now()
    available_coupons = Coupon.objects.filter(
        active=True,
        valid_from__lte=now,
        valid_to__gte=now
    )[:10]
    
    discount = Decimal('0.00')
    coupon_code = None
    if 'coupon_discount' in request.session:
        discount = Decimal(str(request.session['coupon_discount']))
        coupon_code = request.session.get('coupon_code', '')
    
    final_total = cart_data['total'] - discount
    
    context = {
        'cart': cart_data,
        'discount': discount,
        'final_total': final_total,
        'coupon_code': coupon_code,
        'available_coupons': available_coupons,
    }
    return render(request, 'cart.html', context)

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    cart.add(product_id)
    messages.success(request, f'{product.name} added to cart!')
    return redirect('cart_detail')

def update_cart(request, product_id):
    cart = Cart(request)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart.update(product_id, quantity)
        messages.success(request, 'Cart updated!')
    return redirect('cart_detail')

def remove_from_cart(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)
    messages.success(request, 'Item removed from cart!')
    return redirect('cart_detail')

def clear_cart(request):
    cart = Cart(request)
    cart.clear()
    messages.info(request, 'Cart cleared!')
    return redirect('cart_detail')

# ===== COUPON VIEWS =====
@login_required
def apply_coupon(request):
    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code', '').strip().upper()
        cart = Cart(request)
        
        result = cart.apply_coupon(coupon_code)
        
        if result['valid']:
            request.session['coupon_code'] = coupon_code
            request.session['coupon_discount'] = float(result['discount'])
            messages.success(request, result['message'])
        else:
            messages.error(request, result['message'])
        
        return redirect('cart_detail')

@login_required
def remove_coupon(request):
    if 'coupon_code' in request.session:
        del request.session['coupon_code']
    if 'coupon_discount' in request.session:
        del request.session['coupon_discount']
    messages.success(request, 'Coupon removed')
    return redirect('cart_detail')

@login_required
def coupons_page(request):
    now = timezone.now()
    active_coupons = Coupon.objects.filter(
        active=True,
        valid_from__lte=now,
        valid_to__gte=now
    )
    return render(request, 'coupons.html', {'active_coupons': active_coupons})

# ===== CHECKOUT VIEWS =====
@login_required
def checkout(request):
    cart = Cart(request)
    cart_data = cart.get_items(Product)
    
    if not cart_data['items']:
        messages.warning(request, 'Your cart is empty!')
        return redirect('product_list')
    
    discount = Decimal('0.00')
    coupon_code = None
    if 'coupon_discount' in request.session:
        discount = Decimal(str(request.session['coupon_discount']))
        coupon_code = request.session.get('coupon_code', '')
    
    final_total = cart_data['total'] - discount
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country', 'Nigeria')
        
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            address=address,
            city=city,
            state=state,
            country=country,
            total_amount=final_total
        )
        
        for item in cart_data['items']:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price=item['product'].price
            )
        
        if 'coupon_code' in request.session:
            try:
                coupon = Coupon.objects.get(code=request.session['coupon_code'])
                UsedCoupon.objects.create(
                    user=request.user,
                    coupon=coupon,
                    order=order
                )
                coupon.used_count += 1
                coupon.save()
            except Coupon.DoesNotExist:
                pass
        
        cart.clear()
        if 'coupon_code' in request.session:
            del request.session['coupon_code']
        if 'coupon_discount' in request.session:
            del request.session['coupon_discount']
        
        messages.success(request, f'Order #{order.id} placed successfully!')
        return redirect('order_confirmation', order_id=order.id)
    
    context = {
        'cart': cart_data,
        'discount': discount,
        'final_total': final_total,
        'coupon_code': coupon_code
    }
    return render(request, 'checkout.html', context)

@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order_confirmation.html', {'order': order})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'order_history.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order_detail.html', {'order': order})

@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if order.status in ['pending', 'processing']:
        order.status = 'cancelled'
        order.save()
        messages.success(request, f'Order #{order.id} has been cancelled.')
    else:
        messages.error(request, 'This order cannot be cancelled.')
    
    return redirect('order_history')