#!/usr/bin/env python
"""Generate colorful sample product images for all 24 products."""
from PIL import Image, ImageDraw
import os

media_dir = os.path.join(os.path.dirname(__file__), 'media', 'products')
os.makedirs(media_dir, exist_ok=True)

# Nice color palette for skincare/makeup products
colors = [
    (255, 200, 124, "Peachy Skincare"),
    (230, 150, 180, "Pink Makeup"),
    (200, 230, 150, "Green Wellness"),
    (150, 200, 230, "Blue Calm"),
    (230, 200, 150, "Beige"),
    (200, 180, 220, "Purple"),
    (255, 230, 100, "Golden"),
    (200, 220, 200, "Mint"),
]

for i in range(24):
    try:
        color = colors[i % len(colors)]
        img = Image.new('RGB', (400, 300), color=color[:3])
        draw = ImageDraw.Draw(img)
        
        # Add gradient effect by drawing rectangles
        for j in range(0, 400, 20):
            alpha = int(255 * (j / 400))
            overlay = Image.new('RGBA', (20, 300), (255, 255, 255, int(30 * (1 - j/400))))
            img.paste(Image.new('RGB', (20, 300), color=tuple(min(255, c + 20) for c in color[:3])), (j, 0))
        
        # Save
        img.save(os.path.join(media_dir, f'product_{i}.jpg'))
        print(f"✓ Created: product_{i}.jpg ({color[3]})")
    except Exception as e:
        print(f"✗ Error creating product_{i}.jpg: {e}")

print(f"\n✓ Generated {len(os.listdir(media_dir))} images in {media_dir}")
