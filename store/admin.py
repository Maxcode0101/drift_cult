from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Product,
    ProductSize,
    CartItem,
    Order,
    OrderItem,
    NewsletterSubscriber
)

admin.site.register(NewsletterSubscriber)


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


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    fields = ('product_size', 'quantity')  # Editable quantity
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'is_paid', 'colored_status', 'created_at')
    list_filter = ('status', 'is_paid', 'created_at')
    search_fields = ('user__username', 'id')
    readonly_fields = (
        'created_at', 'get_total_display', 'get_payment_method_display')
    inlines = [OrderItemInline]

    actions = ['mark_as_processing', 'mark_as_shipped', 'mark_as_delivered']

    fieldsets = (
        (None, {
            'fields': (
                'user',
                'is_paid',
                'status',
                'get_payment_method_display',
                'get_total_display',
                'created_at',
            )
        }),
    )

    def mark_as_processing(self, request, queryset):
        queryset.update(status='processing')

    def mark_as_shipped(self, request, queryset):
        queryset.update(status='shipped')

    def mark_as_delivered(self, request, queryset):
        queryset.update(status='delivered')

    mark_as_processing.short_description = "Mark selected orders as Processing"
    mark_as_shipped.short_description = "Mark selected orders as Shipped"
    mark_as_delivered.short_description = "Mark selected orders as Delivered"

    def colored_status(self, obj):
        color = {
            'processing': 'orange',
            'shipped': 'blue',
            'delivered': 'green',
        }.get(obj.status, 'gray')

        return format_html(
            '<span style="color: white; background-color: {};'
            'padding: 2px 8px; border-radius: 8px;">{}</span>',
            color,
            obj.get_status_display()
        )
    colored_status.short_description = 'Status'

    def get_total_display(self, obj):
        return f"${obj.get_total():.2f}"
    get_total_display.short_description = 'Order Total'

    def get_payment_method_display(self, obj):
        return "Stripe"
    get_payment_method_display.short_description = 'Payment Method'
