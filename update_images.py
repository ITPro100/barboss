#!/usr/bin/env python3
"""Update content.json with mixed real and generated images"""

import json
import os

# Image mapping - mix of real AI-generated and stylized placeholders
image_updates = {
    "si-ghost-pants-001": {
        "img": "/assets/products/si-pants-real.jpg",
        "gallery": ["/assets/products/si-pants-real.jpg", "/assets/products/si-ghost-pants-001.jpg"]
    },
    "si-ice-jacket-001": {
        "img": "/assets/products/si-jacket-real.jpg", 
        "gallery": ["/assets/products/si-jacket-real.jpg", "/assets/products/si-ice-jacket-001.jpg"]
    },
    "cp-shirt-001": {
        "img": "/assets/products/cp-hoodie-real.jpg",
        "gallery": ["/assets/products/cp-hoodie-real.jpg", "/assets/products/cp-shirt-001.jpg"]
    }
}

# Lookbook updates
lookbook_images = [
    {"img": "/assets/lookbook/look-real-01.jpg", "title": "Kiev Streets"},
    {"img": "/assets/lookbook/look-01.jpg", "title": "Street Legend"},
    {"img": "/assets/lookbook/look-02.jpg", "title": "Urban Explorer"},
    {"img": "/assets/lookbook/look-03.jpg", "title": "Квадратура"},
    {"img": "/assets/lookbook/look-04.jpg", "title": "Premium Culture"},
    {"img": "/assets/lookbook/look-05.jpg", "title": "Stone Island Life"}
]

# Load current content
with open('content.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Update product images
for product in data['products']:
    if product['id'] in image_updates:
        updates = image_updates[product['id']]
        product['img'] = updates['img']
        product['gallery'] = updates['gallery']
        print(f"✅ Updated: {product['id']}")

# Update lookbook
data['lookbook'] = lookbook_images
print(f"✅ Updated lookbook with {len(lookbook_images)} images")

# Save updated content
with open('content.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("\n✨ Images updated successfully!")