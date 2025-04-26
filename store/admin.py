# store/admin.py
from django.contrib import admin
from .models import Product, ProductSize, CartItem, Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'is_paid', 'status')
    list_filter = ('is_paid', 'status', 'created_at')
    search_fields = ('user__username', 'id')
    ordering = ('-created_at',)
    inlines = [OrderItemInline]
    list_editable = ('status',)  # ✅ THIS makes it editable directly in the list view

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price')
    search_fields = ('name',)

@admin.register(ProductSize)
class ProductSizeAdmin(admin.ModelAdmin):
    list_display = ('product', 'size', 'stock')

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'product_size', 'quantity', 'added_at')