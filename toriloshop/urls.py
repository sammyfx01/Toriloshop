from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.contrib.auth.models import User

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
    path('create-admin/', create_admin, name='create_admin'),
    path('admin/', admin.site.urls),
    path('', include('products.urls')),
    path('', include('users.urls')),
]