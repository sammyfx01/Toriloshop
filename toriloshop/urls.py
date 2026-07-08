from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from django.contrib.auth.models import User
from products.models import Product
from django.shortcuts import render

# Homepage
def homepage(request):
    products = Product.objects.all()
    return render(request, 'products/home.html', {'products': products})

# Create Admin
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

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)