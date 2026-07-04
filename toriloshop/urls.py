from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.contrib.auth.models import User

def create_sammysax(request):
    if not User.objects.filter(username='sammysax').exists():
        User.objects.create_superuser('sammysax', 'sammysax@example.com', 'admin123')
        return HttpResponse("✅ Admin 'sammysax' created!<br>Username: <b>sammysax</b><br>Password: <b>admin123</b><br><br><a href='/admin/'>Go to Admin</a>")
    else:
        return HttpResponse("✅ Admin 'sammysax' already exists!<br><br><a href='/admin/'>Go to Admin</a>")

def create_admin(request):
    try:
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            return HttpResponse("<h2>✅ Admin created!</h2><p>Username: <b>admin</b></p><p>Password: <b>admin123</b></p><br><a href='/admin/'>Go to Admin</a>")
        else:
            return HttpResponse("<h2>✅ Admin already exists!</h2><br><a href='/admin/'>Go to Admin</a>")
    except Exception as e:
        return HttpResponse(f"<h2>❌ Error</h2><p>{e}</p>")

urlpatterns = [
    path('create-sammysax/', create_sammysax, name='create_sammysax'),
    path('create-admin/', create_admin, name='create_admin'),
    path('admin/', admin.site.urls),
    path('', include('products.urls')),
    path('', include('users.urls')),
]