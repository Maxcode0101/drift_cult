import os
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from store.models import Product


class Command(BaseCommand):
    help = "Auto-assign product images based on slugified product names."

    def handle(self, *args, **kwargs):
        updated = 0
        for product in Product.objects.all():
            filename = slugify(product.name) + '.jpg'
            product.image = f'products/{filename}'
            product.save()
            updated += 1
            self.stdout.write(self.style.SUCCESS(f"Updated {product.name} → products/{filename}"))

        self.stdout.write(self.style.SUCCESS(f"✅ Assigned images for {updated} products."))
