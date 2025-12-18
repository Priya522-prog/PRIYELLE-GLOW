from django.core.management.base import BaseCommand
from django.core.files.images import ImageFile
from main.models import Product
import os

class Command(BaseCommand):
    help = 'Upload product images from media/products folder'

    def handle(self, *args, **options):
        image_folder = 'media/products'
        
        if not os.path.exists(image_folder):
            self.stdout.write(self.style.ERROR(f'Folder not found: {image_folder}'))
            return

        products = Product.objects.all().order_by('id')
        image_files = sorted([f for f in os.listdir(image_folder) 
                            if f.lower().endswith(('.jpg', '.jpeg', '.png'))])

        self.stdout.write(f'Found {len(image_files)} images for {len(products)} products\n')

        for idx, product in enumerate(products):
            if idx < len(image_files):
                image_filename = image_files[idx]
                image_path = os.path.join(image_folder, image_filename)
                
                try:
                    with open(image_path, 'rb') as img_file:
                        # Save to product
                        product.image.save(image_filename, ImageFile(img_file), save=True)
                        self.stdout.write(
                            self.style.SUCCESS(f'✓ {product.name[:40]:40} ← {image_filename}')
                        )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'✗ {product.name}: {e}')
                    )
            else:
                self.stdout.write(f'⚠ No image for: {product.name}')

        self.stdout.write(self.style.SUCCESS('\n✓ Image upload complete!'))
