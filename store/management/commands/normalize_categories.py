from django.core.management.base import BaseCommand
from store.models import Product

class Command(BaseCommand):
    help = 'Normalize product categories to match CATEGORY_CHOICES'

    def handle(self, *args, **kwargs):
        category_mapping = {
            'BIKINI': 'BIKINIS',
            'SWEATER': 'SWEATERS',
            'Sweater': 'SWEATERS',
            'HEADWEAR': 'HEADWEAR',
            'Headwear': 'HEADWEAR',
        }

        products = Product.objects.all()
        updated = 0

        for product in products:
            normalized_category = category_mapping.get(product.category, product.category)
            if product.category != normalized_category:
                product.category = normalized_category
                product.save()
                updated += 1

        self.stdout.write(self.style.SUCCESS(f'Normalized {updated} products.'))