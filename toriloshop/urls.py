from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.contrib.auth.models import User

def create_sammysax(request):
    if not User.objects.filter(username='sammysax').exists():
        User.objects.create_superuser('sammysax', 'sammysax@example.com', 'admin123')
        return HttpResponse("✅ Admin created! Username: sammysax Password: admin123")
    else:
        return HttpResponse("✅ Admin already exists!")

urlpatterns = [
    path('create-sammysax/', create_sammysax, name='create_sammysax'),
    path('create-admin/', create_admin, name='create_admin'),
    path('admin/', admin.site.urls),
    path('', include('products.urls')),
    path('', include('users.urls')),
]

def create_admin(request):
    try:
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            return HttpResponse("✅ Admin created! Username: admin Password: admin123")
        else:
            return HttpResponse("✅ Admin already exists!")
    except Exception as e:
        return HttpResponse(f"❌ Error: {e}")