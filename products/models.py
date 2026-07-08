from django.db import models
from django.contrib.auth.models import User

# ===== CATEGORY MODEL =====
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='categories/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.name.lower().replace(' ', '-')
        super().save(*args, **kwargs)

# ===== PRODUCT MODEL =====
class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    image_url = models.URLField(blank=True, null=True, verbose_name="Image URL")  # NEW FIELD
    stock = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

# ===== COUPON MODELS =====
class Coupon(models.Model):
    DISCOUNT_TYPES = [
        ('percentage', 'Percentage (%)'),
        ('fixed', 'Fixed Amount (Naira)'),
    ]
    
    code = models.CharField(max_length=50, unique=True)
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPES, default='percentage')
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    minimum_order = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    usage_limit = models.IntegerField(default=1)
    used_count = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.code} - {self.discount_value}{'%' if self.discount_type == 'percentage' else ' Naira'}"

class UsedCoupon(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    used_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'coupon']

# ===== ORDER MODELS =====
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default='Nigeria')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Order #{self.id} - {self.first_name} {self.last_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    
    def get_subtotal(self):
        return self.quantity * self.price