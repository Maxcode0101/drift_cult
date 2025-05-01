from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('SHOP ALL', 'Shop All'),
        ('T-SHIRTS', 'T-Shirts'),
        ('SHIRTS', 'Shirts'),
        ('SWEATERS', 'Sweaters'),
        ('FLEECE', 'Fleece'),
        ('TRUNKS', 'Trunks'),
        ('WALK SHORTS', 'Walk Shorts'),
        ('PANTS', 'Pants'),
        ('HEADWEAR', 'Headwear'),
        ('BIKINIS', 'Bikinis'),
    ]

    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    color = models.CharField(max_length=50, blank=True, null=True)
    size = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='T-SHIRTS')
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    def __str__(self):
        return self.name


class ProductSize(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='sizes')
    size = models.CharField(max_length=10)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.product.name} - {self.size}'


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_size = models.ForeignKey('ProductSize', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.quantity} x {self.product_size}'


class Order(models.Model):
    STATUS_CHOICES = [
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='processing')

    def __str__(self):
        return f'Order #{self.id} by {self.user.username}'

    def get_total(self):
        """Return the total cost of all items in this order."""
        return sum(item.product_size.product.price * item.quantity for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product_size = models.ForeignKey('ProductSize', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} x {self.product_size.product.name} ({self.product_size.size})'
    
    
class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
