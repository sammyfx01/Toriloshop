from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Product, Order, OrderItem, Coupon, UsedCoupon, Category
from .cart import Cart
from decimal import Decimal
from django.utils import timezone

# ===== HOME VIEW =====
def home(request):
    products = Product.objects.all()[:8]
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
    categories = Category.objects.all()
    return render(request, 'products/product_detail.html', {
        'product': product,
        'categories': categories,
    })

def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    categories = Category.objects.all()
    return render(request, 'products/category_products.html', {
        'category': category,
        'products': products,
        'categories': categories,
    })