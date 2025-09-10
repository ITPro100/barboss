#!/usr/bin/env python3
"""Optimize images for web performance"""

from PIL import Image
import os
import glob

def optimize_image(filepath, max_width=1200, quality=85):
    """Optimize a single image"""
    try:
        img = Image.open(filepath)
        
        # Convert RGBA to RGB if needed
        if img.mode == 'RGBA':
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3] if len(img.split()) > 3 else None)
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize if too large
        if img.width > max_width:
            ratio = max_width / img.width
            new_height = int(img.height * ratio)
            img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
        
        # Save optimized version
        img.save(filepath, 'JPEG', quality=quality, optimize=True)
        
        # Get file size
        size = os.path.getsize(filepath) / 1024  # KB
        return size
    except Exception as e:
        print(f"Error optimizing {filepath}: {e}")
        return None

def main():
    print("🔧 Optimizing images for web performance...")
    
    # Optimize product images
    product_images = glob.glob('public/assets/products/*.jpg')
    print(f"\n📦 Optimizing {len(product_images)} product images...")
    
    for filepath in product_images:
        original_size = os.path.getsize(filepath) / 1024
        
        # Different settings for different images
        if 'real' in filepath:
            # Higher quality for real photos
            new_size = optimize_image(filepath, max_width=1000, quality=90)
        else:
            # Standard quality for generated images
            new_size = optimize_image(filepath, max_width=800, quality=85)
        
        if new_size:
            print(f"  ✅ {os.path.basename(filepath)}: {original_size:.0f}KB → {new_size:.0f}KB")
    
    # Optimize lookbook images
    lookbook_images = glob.glob('public/assets/lookbook/*.jpg')
    print(f"\n📸 Optimizing {len(lookbook_images)} lookbook images...")
    
    for filepath in lookbook_images:
        original_size = os.path.getsize(filepath) / 1024
        
        if 'real' in filepath:
            new_size = optimize_image(filepath, max_width=1400, quality=88)
        else:
            new_size = optimize_image(filepath, max_width=1000, quality=85)
        
        if new_size:
            print(f"  ✅ {os.path.basename(filepath)}: {original_size:.0f}KB → {new_size:.0f}KB")
    
    # Optimize category images
    category_images = glob.glob('public/assets/img/category-*.jpg')
    print(f"\n📁 Optimizing {len(category_images)} category images...")
    
    for filepath in category_images:
        original_size = os.path.getsize(filepath) / 1024
        new_size = optimize_image(filepath, max_width=800, quality=85)
        
        if new_size:
            print(f"  ✅ {os.path.basename(filepath)}: {original_size:.0f}KB → {new_size:.0f}KB")
    
    # Optimize hero background
    hero_path = 'public/assets/img/hero-bg.jpg'
    if os.path.exists(hero_path):
        print(f"\n🏠 Optimizing hero background...")
        original_size = os.path.getsize(hero_path) / 1024
        new_size = optimize_image(hero_path, max_width=1920, quality=82)
        if new_size:
            print(f"  ✅ hero-bg.jpg: {original_size:.0f}KB → {new_size:.0f}KB")
    
    print("\n✨ Optimization complete!")

if __name__ == "__main__":
    main()