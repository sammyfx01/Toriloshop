from django.contrib import admin
from .models import Product, Order, OrderItem, Coupon, UsedCoupon

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'total_amount', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['id', 'first_name', 'last_name', 'email']
    inlines = [OrderItemInline]

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock']
    search_fields = ['name']

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount_type', 'discount_value', 'minimum_order', 'valid_from', 'valid_to', 'active', 'used_count']
    list_filter = ['active', 'discount_type']
    search_fields = ['code']

@admin.register(UsedCoupon)
class UsedCouponAdmin(admin.ModelAdmin):
    list_display = ['user', 'coupon', 'order', 'used_at']

    @admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock', 'category']
    list_filter = ['category']
    search_fields = ['name']
    fields = ['name', 'description', 'price', 'image', 'image_url', 'stock', 'category']  # ← ADD image_url