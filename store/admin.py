from django.contrib import admin
from django.utils.html import format_html
from .models import Product, ProductSize, CartItem, Order, OrderItem

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price')
    list_filter = ('category',)

@admin.register(ProductSize)
class ProductSizeAdmin(admin.ModelAdmin):
    list_display = ('product', 'size', 'stock')

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'product_size', 'quantity')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'is_paid', 'status', 'colored_status', 'created_at')
    list_filter = ('status', 'is_paid', 'created_at')
    search_fields = ('user__username', 'id')
    readonly_fields = ('created_at',)
    fields = ('user', 'is_paid', 'status', 'created_at')

    def colored_status(self, obj):
        color = {
            'processing': 'orange',
            'shipped': 'blue',
            'delivered': 'green',
        }.get(obj.status, 'gray')

        return format_html(
            '<span style="color: white; background-color: {}; padding: 2px 8px; border-radius: 8px;">{}</span>',
            color,
            obj.get_status_display()
        )
    colored_status.short_description = 'Status'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product_size', 'quantity')
