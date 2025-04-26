from django.contrib import admin
from .models import Product, ProductSize, CartItem, Order, OrderItem, Category, Review, Wishlist, DiscountCode

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
    list_display = ('id', 'user', 'created_at', 'is_paid', 'colored_status')
    list_filter = ('is_paid', 'status')
    readonly_fields = ('created_at',)

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

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product')

@admin.register(DiscountCode)
class DiscountCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount', 'active')