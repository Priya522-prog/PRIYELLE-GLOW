#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'priyelle_glow.settings')
django.setup()

from main.models import Product

products = Product.objects.all().order_by('id')

print("\n" + "="*120)
print("PRIYELLE GLOW - COMPLETE PRODUCT DATABASE")
print("="*120 + "\n")

print(f"{'ID':<3} {'Product Name':<50} {'Category':<12} {'Skin Type':<15} {'Price':<8} {'Country':<12}")
print("-"*120)

for p in products:
    print(f"{p.id:<3} {p.name:<50} {p.category:<12} {p.skin_type:<15} KES {p.price:<6} {p.country:<12}")

print("\n" + "="*120)
print(f"TOTAL PRODUCTS: {products.count()}")
print("="*120 + "\n")

# Summary by category
print("\nBY CATEGORY:")
print("-" * 50)
for category in ['skincare', 'makeup']:
    count = Product.objects.filter(category=category).count()
    print(f"  • {category.title()}: {count} products")

# Summary by skin type
print("\nBY SKIN TYPE:")
print("-" * 50)
for skin_type in ['oily', 'dry', 'combination', 'normal', 'sensitive']:
    count = Product.objects.filter(skin_type=skin_type).count()
    if count > 0:
        print(f"  • {skin_type.title()}: {count} products")

# Summary by country
print("\nBY COUNTRY:")
print("-" * 50)
countries = Product.objects.values('country').distinct()
for country_obj in countries:
    country = country_obj['country']
    count = Product.objects.filter(country=country).count()
    print(f"  • {country}: {count} products")
