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
    list_display = ('id', 'user', 'is_paid', 'colored_status', 'created_at')
    list_filter = ('status', 'is_paid', 'created_at')
    search_fields = ('user__username', 'id')
    readonly_fields = ('created_at',)
    actions = ['mark_as_processing', 'mark_as_shipped', 'mark_as_delivered']

    fieldsets = (
        ('Order Information', {
            'fields': ('user', 'created_at', 'is_paid')
        }),
        ('Shipping Status', {
            'fields': ('status',)
        }),
    )

    def colored_status(self, obj):
        color = {
            'processing': 'orange',
            'shipped': 'blue',
            'delivered': 'green',
        }.get(obj.status, 'gray')

        return format_html(
            '<span style="color: white; background-color: {}; padding: 4px 8px; border-radius: 12px;">{}</span>',
            color,
            obj.get_status_display()
        )
    colored_status.short_description = 'Status'


    @admin.action(description='Mark selected orders as Processing')
    def mark_as_processing(self, request, queryset):
        updated = queryset.update(status='processing')
        self.message_user(request, f"{updated} orders marked as Processing.")

    @admin.action(description='Mark selected orders as Shipped')
    def mark_as_shipped(self, request, queryset):
        updated = queryset.update(status='shipped')
        self.message_user(request, f"{updated} orders marked as Shipped.")

    @admin.action(description='Mark selected orders as Delivered')
    def mark_as_delivered(self, request, queryset):
        updated = queryset.update(status='delivered')
        self.message_user(request, f"{updated} orders marked as Delivered.")
