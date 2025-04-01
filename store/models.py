from django.db import models

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