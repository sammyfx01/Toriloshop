from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.contrib.auth.models import User
from products.models import Product
from django.shortcuts import render

def homepage(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})

def create_admin(request):
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        return HttpResponse("✅ Admin created! Username: admin Password: admin123")
    return HttpResponse("✅ Admin already exists!")

urlpatterns = [
    path('', homepage, name='home'),
    path('create-admin/', create_admin, name='create_admin'),
    path('admin/', admin.site.urls),
    path('', include('products.urls')),
    path('', include('users.urls')),
]