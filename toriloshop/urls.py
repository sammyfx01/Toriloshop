from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.contrib.auth.models import User

# Homepage view
def home_page(request):
    return HttpResponse("""
    <h1>🎉 Toriloshop is LIVE!</h1>
    <p>Your e-commerce website is running on Render!</p>
    <br>
    <h2>Quick Links:</h2>
    <ul>
        <li><a href="/admin/">🔐 Admin Panel</a></li>
        <li><a href="/create-admin/">👤 Create Admin User</a></li>
        <li><a href="/products/">🛍️ Products</a></li>
        <li><a href="/cart/">🛒 Cart</a></li>
        <li><a href="/register/">📝 Register</a></li>
        <li><a href="/login/">🔑 Login</a></li>
    </ul>
    <br>
    <p>📧 Email: admin@example.com</p>
    <p>🔑 Password: admin123</p>
    """)

# Create admin function
def create_admin(request):
    try:
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            return HttpResponse("""
            <h2>✅ Admin created successfully!</h2>
            <p><b>Username:</b> admin</p>
            <p><b>Password:</b> admin123</p>
            <br>
            <a href="/admin/">🔐 Go to Admin Panel</a>
            """)
        else:
            return HttpResponse("""
            <h2>✅ Admin already exists!</h2>
            <br>
            <a href="/admin/">🔐 Go to Admin Panel</a>
            """)
    except Exception as e:
        return HttpResponse(f"<h2>❌ Error</h2><p>{e}</p>")

urlpatterns = [
    path('', home_page, name='home'),
    path('create-admin/', create_admin, name='create_admin'),
    path('admin/', admin.site.urls),
    path('', include('products.urls')),
    path('', include('users.urls')),
]