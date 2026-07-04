from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.db import connection

# Function to create admin user
def create_admin(request):
    try:
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            return HttpResponse("✅ Admin created!<br>Username: <b>admin</b><br>Password: <b>admin123</b><br><br><a href='/admin/'>Go to Admin</a>")
        else:
            return HttpResponse("✅ Admin already exists!<br><br><a href='/admin/'>Go to Admin</a>")
    except Exception as e:
        return HttpResponse(f"❌ Error: {e}")

urlpatterns = [
    path('create-admin/', create_admin, name='create_admin'),
    path('admin/', admin.site.urls),
    path('', include('products.urls')),
    path('', include('users.urls')),
]