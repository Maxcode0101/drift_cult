from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from .models import Product

class ProductSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Product.objects.all()

    def location(self, obj):
        return reverse("product_detail", args=[obj.pk])

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = "monthly"

    def items(self):
        return ["home", "shop", "about", "community"]

    def location(self, item):
        return reverse(item)
