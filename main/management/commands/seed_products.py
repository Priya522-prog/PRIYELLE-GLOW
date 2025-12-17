from django.core.management.base import BaseCommand
from main.models import Product

class Command(BaseCommand):
    help = 'Seed the database with sample skincare and makeup products'

    def handle(self, *args, **options):
        # Sample products data
        products_data = [
            # Oily Skin - Skincare (Kenya)
            {'name': 'Cetaphil Oily Skin Cleanser', 'description': 'Gentle oil-free cleanser', 'price': 2500, 'category': 'skincare', 'skin_type': 'oily', 'country': 'Kenya'},
            {'name': 'The Ordinary Niacinamide 10%', 'description': 'Oil control serum with niacinamide', 'price': 3500, 'category': 'skincare', 'skin_type': 'oily', 'country': 'Kenya'},
            {'name': 'Maybelline Fit Me Matte', 'description': 'Matte finish foundation for oily skin', 'price': 2800, 'category': 'makeup', 'skin_type': 'oily', 'country': 'Kenya'},
            {'name': 'Maybelline Pore Minimizer', 'description': 'Pore minimizing primer', 'price': 1800, 'category': 'makeup', 'skin_type': 'oily', 'country': 'Kenya'},
            
            # Dry Skin - Skincare (Kenya)
            {'name': 'CeraVe Hydrating Cream Cleanser', 'description': 'Rich hydrating cleanser for dry skin', 'price': 2200, 'category': 'skincare', 'skin_type': 'dry', 'country': 'Kenya'},
            {'name': 'The Ordinary Hyaluronic Acid 2%', 'description': 'Hydrating serum for dry skin', 'price': 1500, 'category': 'skincare', 'skin_type': 'dry', 'country': 'Kenya'},
            {'name': 'MAC Fix+', 'description': 'Setting spray for dewy finish', 'price': 3200, 'category': 'makeup', 'skin_type': 'dry', 'country': 'Kenya'},
            {'name': 'Fenty Beauty Pro Filt\'r', 'description': 'Hydrating foundation with luminous finish', 'price': 4500, 'category': 'makeup', 'skin_type': 'dry', 'country': 'Kenya'},
            
            # Combination Skin (Kenya)
            {'name': 'Neutrogena Hydro Boost Hydrating Toner', 'description': 'Balancing toner for combination skin', 'price': 1900, 'category': 'skincare', 'skin_type': 'combination', 'country': 'Kenya'},
            {'name': 'Clinique Dramatically Different Moisturizer', 'description': 'Balanced moisturizer', 'price': 3800, 'category': 'skincare', 'skin_type': 'combination', 'country': 'Kenya'},
            {'name': 'L\'Oreal True Match Foundation', 'description': 'Balanced finish foundation', 'price': 2600, 'category': 'makeup', 'skin_type': 'combination', 'country': 'Kenya'},
            {'name': 'Rimmel Stay Matte Primer', 'description': 'Multi-purpose primer for balanced skin', 'price': 1400, 'category': 'makeup', 'skin_type': 'combination', 'country': 'Kenya'},
            
            # Normal Skin (Kenya)
            {'name': 'Cetaphil Gentle Skin Cleanser', 'description': 'Mild gentle cleanser', 'price': 1800, 'category': 'skincare', 'skin_type': 'normal', 'country': 'Kenya'},
            {'name': 'Olay Complete Daily Moisturizer', 'description': 'Daily hydrating moisturizer', 'price': 2200, 'category': 'skincare', 'skin_type': 'normal', 'country': 'Kenya'},
            {'name': 'Revlon ColorStay Foundation', 'description': 'Long-wearing natural foundation', 'price': 2400, 'category': 'makeup', 'skin_type': 'normal', 'country': 'Kenya'},
            {'name': 'Milani Conceal + Perfect', 'description': 'Universal concealer', 'price': 1600, 'category': 'makeup', 'skin_type': 'normal', 'country': 'Kenya'},
            
            # Sensitive Skin (Kenya)
            {'name': 'Vanicream Gentle Facial Cleanser', 'description': 'Hypoallergenic gentle cleanser', 'price': 2000, 'category': 'skincare', 'skin_type': 'sensitive', 'country': 'Kenya'},
            {'name': 'Aveeno Ultra-Calming Cleanser', 'description': 'Soothing cleanser for sensitive skin', 'price': 2100, 'category': 'skincare', 'skin_type': 'sensitive', 'country': 'Kenya'},
            {'name': 'Bare Minerals Original Foundation', 'description': 'Hypoallergenic powder foundation', 'price': 3000, 'category': 'makeup', 'skin_type': 'sensitive', 'country': 'Kenya'},
            {'name': 'Physicians Formula Concealer', 'description': 'Gentle hypoallergenic concealer', 'price': 1700, 'category': 'makeup', 'skin_type': 'sensitive', 'country': 'Kenya'},
            
            # Tanzania Products
            {'name': 'Shea Moisture Raw Shea Butter', 'description': 'Natural moisturizer for all skin types', 'price': 2800, 'category': 'skincare', 'skin_type': 'dry', 'country': 'Tanzania'},
            {'name': 'Black Up Cosmetics Foundation', 'description': 'Foundation for rich skin tones', 'price': 4200, 'category': 'makeup', 'skin_type': 'normal', 'country': 'Tanzania'},
            
            # Uganda Products
            {'name': 'Lush Fresh Cleanser', 'description': 'Organic face cleanser', 'price': 3500, 'category': 'skincare', 'skin_type': 'combination', 'country': 'Uganda'},
            {'name': 'MAC Lipstick', 'description': 'Long-wearing lipstick', 'price': 3200, 'category': 'makeup', 'skin_type': 'normal', 'country': 'Uganda'},
        ]
        
        # Create products
        created_count = 0
        for product_data in products_data:
            product, created = Product.objects.get_or_create(
                name=product_data['name'],
                defaults={
                    'description': product_data['description'],
                    'price': product_data['price'],
                    'category': product_data['category'],
                    'skin_type': product_data['skin_type'],
                    'country': product_data['country']
                }
            )
            if created:
                created_count += 1
                self.stdout.write(f"Created: {product.name}")
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} products')
        )
