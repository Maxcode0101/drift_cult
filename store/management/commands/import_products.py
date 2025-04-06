import csv
import os
from django.core.management.base import BaseCommand
from store.models import Product

class Command(BaseCommand):
    help = 'Import products from CSV'

    def add_arguments(self, parser):
        parser.add_argument('csv_path', type=str)

    def handle(self, *args, **options):
        csv_path = options['csv_path']
        if not os.path.isfile(csv_path):
            self.stderr.write(self.style.ERROR(f"File not found: {csv_path}"))
            return

        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            count = 0

            for row in reader:
                name = row['name']
                price = float(row['price'])
                color = row['color']
                size = row['size']
                category = row['category']
                description = row['description']
                image = f"products/{row['image']}" if row.get('image') else None

                product, created = Product.objects.update_or_create(
                    name=name,
                    defaults={
                        'price': price,
                        'color': color,
                        'size': size,
                        'category': category,
                        'description': description,
                        'image': image,
                    }
                )

                count += 1
                self.stdout.write(self.style.SUCCESS(f"{'Created' if created else 'Updated'}: {name}"))

        self.stdout.write(self.style.SUCCESS(f"✅ Successfully imported {count} products."))