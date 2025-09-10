#!/usr/bin/env python3
"""
Generate stylized placeholder images for Barboss Room products
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
import json

# Configuration
IMAGE_WIDTH = 800
IMAGE_HEIGHT = 1000
CATEGORY_HEIGHT = 600

# Color palette - Dark premium style
COLORS = {
    'bg_dark': '#0a0a0a',
    'bg_medium': '#1a1a1a',
    'bg_light': '#2a2a2a',
    'accent': '#FFD700',  # Ukrainian gold
    'text_primary': '#FFFFFF',
    'text_secondary': '#999999',
    'ukraine_blue': '#0057B7',
    'ukraine_yellow': '#FFD700',
    'stone_island': '#2C2C2C',
    'cp_company': '#1E3A5F'
}

def create_gradient_background(width, height, color1, color2):
    """Create a gradient background"""
    img = Image.new('RGB', (width, height), color1)
    draw = ImageDraw.Draw(img)
    
    for i in range(height):
        ratio = i / height
        r1, g1, b1 = tuple(int(color1[j:j+2], 16) for j in (1, 3, 5))
        r2, g2, b2 = tuple(int(color2[j:j+2], 16) for j in (1, 3, 5))
        
        r = int(r1 * (1 - ratio) + r2 * ratio)
        g = int(g1 * (1 - ratio) + g2 * ratio)
        b = int(b1 * (1 - ratio) + b2 * ratio)
        
        draw.rectangle([(0, i), (width, i + 1)], fill=(r, g, b))
    
    return img

def add_brand_badge(img, brand):
    """Add brand badge to image"""
    draw = ImageDraw.Draw(img)
    
    # Brand colors
    brand_colors = {
        'Stone Island': ('#2C2C2C', '#FFD700'),
        'C.P. Company': ('#1E3A5F', '#FFFFFF')
    }
    
    bg_color, text_color = brand_colors.get(brand, ('#1a1a1a', '#FFFFFF'))
    
    # Draw badge
    badge_width = 200
    badge_height = 40
    badge_x = IMAGE_WIDTH - badge_width - 20
    badge_y = 20
    
    # Badge background
    draw.rectangle(
        [(badge_x, badge_y), (badge_x + badge_width, badge_y + badge_height)],
        fill=bg_color
    )
    
    # Badge text
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
    except:
        font = ImageFont.load_default()
    
    text_bbox = draw.textbbox((0, 0), brand.upper(), font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    text_x = badge_x + (badge_width - text_width) // 2
    text_y = badge_y + (badge_height - text_height) // 2
    
    draw.text((text_x, text_y), brand.upper(), fill=text_color, font=font)
    
    return img

def add_product_text(img, name, price, is_sold=False):
    """Add product name and price to image"""
    draw = ImageDraw.Draw(img)
    
    # Load fonts
    try:
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 32)
        font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Product name (multi-line)
    y_offset = IMAGE_HEIGHT - 250
    lines = name.split(' ')
    line_text = ''
    line_count = 0
    
    for word in lines:
        test_line = line_text + word + ' '
        bbox = draw.textbbox((0, 0), test_line, font=font_medium)
        if bbox[2] - bbox[0] > IMAGE_WIDTH - 80:
            if line_text:
                draw.text((40, y_offset + line_count * 35), line_text.strip(), 
                         fill=COLORS['text_primary'], font=font_medium)
                line_count += 1
                line_text = word + ' '
            else:
                draw.text((40, y_offset + line_count * 35), word, 
                         fill=COLORS['text_primary'], font=font_medium)
                line_count += 1
                line_text = ''
        else:
            line_text = test_line
    
    if line_text:
        draw.text((40, y_offset + line_count * 35), line_text.strip(), 
                 fill=COLORS['text_primary'], font=font_medium)
    
    # Price or SOLD status
    price_y = IMAGE_HEIGHT - 100
    if is_sold:
        draw.text((40, price_y), "❌ ПРОДАНО / SOLD ❌", 
                 fill='#FF0000', font=font_large)
    elif price > 0:
        draw.text((40, price_y), f"{price} грн 🇺🇦", 
                 fill=COLORS['accent'], font=font_large)
    else:
        draw.text((40, price_y), "✏️ Ціна по запросу", 
                 fill=COLORS['accent'], font=font_medium)
    
    # Add "NEW" badge if applicable
    if not is_sold:
        new_badge_x = 40
        new_badge_y = 40
        draw.rectangle(
            [(new_badge_x, new_badge_y), (new_badge_x + 80, new_badge_y + 35)],
            fill='#FF4500'
        )
        draw.text((new_badge_x + 20, new_badge_y + 8), "NEW", 
                 fill=COLORS['text_primary'], font=font_small)
    
    return img

def create_product_image(product):
    """Create a product image"""
    # Create gradient background
    if 'Stone Island' in product.get('brand', ''):
        img = create_gradient_background(IMAGE_WIDTH, IMAGE_HEIGHT, 
                                        COLORS['bg_dark'], COLORS['stone_island'])
    elif 'C.P. Company' in product.get('brand', ''):
        img = create_gradient_background(IMAGE_WIDTH, IMAGE_HEIGHT, 
                                        COLORS['bg_dark'], COLORS['cp_company'])
    else:
        img = create_gradient_background(IMAGE_WIDTH, IMAGE_HEIGHT, 
                                        COLORS['bg_dark'], COLORS['bg_medium'])
    
    # Add pattern overlay for texture
    draw = ImageDraw.Draw(img)
    for i in range(0, IMAGE_WIDTH, 40):
        for j in range(0, IMAGE_HEIGHT, 40):
            if (i + j) % 80 == 0:
                draw.ellipse([(i, j), (i + 3, j + 3)], fill=COLORS['bg_light'])
    
    # Add product silhouette based on category
    category = product.get('category', '')
    draw_product_silhouette(draw, category)
    
    # Add brand badge
    img = add_brand_badge(img, product.get('brand', 'BARBOSS'))
    
    # Add product text
    img = add_product_text(img, product.get('name', ''), 
                          product.get('price', 0), 
                          product.get('sold', False))
    
    # Add Ukrainian flag stripe
    draw.rectangle([(0, IMAGE_HEIGHT - 10), (IMAGE_WIDTH, IMAGE_HEIGHT - 5)], 
                  fill=COLORS['ukraine_blue'])
    draw.rectangle([(0, IMAGE_HEIGHT - 5), (IMAGE_WIDTH, IMAGE_HEIGHT)], 
                  fill=COLORS['ukraine_yellow'])
    
    return img

def draw_product_silhouette(draw, category):
    """Draw product silhouette based on category"""
    center_x = IMAGE_WIDTH // 2
    center_y = IMAGE_HEIGHT // 2 - 100
    
    if category == 'jackets':
        # Jacket silhouette
        points = [
            (center_x - 150, center_y - 100),  # Left shoulder
            (center_x - 100, center_y - 120),  # Left collar
            (center_x, center_y - 130),        # Top collar
            (center_x + 100, center_y - 120),  # Right collar
            (center_x + 150, center_y - 100),  # Right shoulder
            (center_x + 160, center_y),        # Right side
            (center_x + 140, center_y + 200),  # Right bottom
            (center_x + 60, center_y + 180),   # Right inner
            (center_x, center_y + 170),        # Center bottom
            (center_x - 60, center_y + 180),   # Left inner
            (center_x - 140, center_y + 200),  # Left bottom
            (center_x - 160, center_y),        # Left side
        ]
        draw.polygon(points, fill=COLORS['bg_light'], outline=COLORS['accent'], width=2)
        
    elif category == 'pants' or category == 'shorts':
        # Pants/Shorts silhouette
        length = 250 if category == 'pants' else 150
        points = [
            (center_x - 80, center_y - 100),   # Left waist
            (center_x + 80, center_y - 100),   # Right waist
            (center_x + 85, center_y),         # Right hip
            (center_x + 70, center_y + length), # Right bottom
            (center_x + 40, center_y + length), # Right inner bottom
            (center_x + 10, center_y + 50),    # Crotch right
            (center_x, center_y + 40),         # Center
            (center_x - 10, center_y + 50),    # Crotch left
            (center_x - 40, center_y + length), # Left inner bottom
            (center_x - 70, center_y + length), # Left bottom
            (center_x - 85, center_y),         # Left hip
        ]
        draw.polygon(points, fill=COLORS['bg_light'], outline=COLORS['accent'], width=2)
        
    elif category == 'tracksuits':
        # Tracksuit silhouette (top and bottom)
        # Top part
        points_top = [
            (center_x - 120, center_y - 150),
            (center_x - 80, center_y - 170),
            (center_x + 80, center_y - 170),
            (center_x + 120, center_y - 150),
            (center_x + 130, center_y - 50),
            (center_x + 110, center_y + 50),
            (center_x - 110, center_y + 50),
            (center_x - 130, center_y - 50),
        ]
        draw.polygon(points_top, fill=COLORS['bg_light'], outline=COLORS['accent'], width=2)
        
        # Bottom part
        points_bottom = [
            (center_x - 60, center_y + 70),
            (center_x + 60, center_y + 70),
            (center_x + 65, center_y + 120),
            (center_x + 50, center_y + 250),
            (center_x + 20, center_y + 250),
            (center_x, center_y + 100),
            (center_x - 20, center_y + 250),
            (center_x - 50, center_y + 250),
            (center_x - 65, center_y + 120),
        ]
        draw.polygon(points_bottom, fill=COLORS['bg_light'], outline=COLORS['accent'], width=2)
        
    else:
        # Generic clothing silhouette
        draw.rectangle(
            [(center_x - 100, center_y - 100), (center_x + 100, center_y + 100)],
            fill=COLORS['bg_light'], outline=COLORS['accent'], width=2
        )

def create_category_image(category_name, category_id):
    """Create a category banner image"""
    img = create_gradient_background(IMAGE_WIDTH, CATEGORY_HEIGHT, 
                                    COLORS['bg_dark'], COLORS['bg_medium'])
    
    draw = ImageDraw.Draw(img)
    
    # Add geometric pattern
    for i in range(0, IMAGE_WIDTH, 60):
        draw.line([(i, 0), (i + 30, CATEGORY_HEIGHT)], 
                 fill=COLORS['bg_light'], width=1)
        draw.line([(i + 30, 0), (i, CATEGORY_HEIGHT)], 
                 fill=COLORS['bg_light'], width=1)
    
    # Add category name
    try:
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 64)
        font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 32)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
    
    # Main text
    text_bbox = draw.textbbox((0, 0), category_name.upper(), font=font_large)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    text_x = (IMAGE_WIDTH - text_width) // 2
    text_y = (CATEGORY_HEIGHT - text_height) // 2
    
    # Text shadow
    draw.text((text_x + 3, text_y + 3), category_name.upper(), 
             fill=COLORS['bg_dark'], font=font_large)
    # Main text
    draw.text((text_x, text_y), category_name.upper(), 
             fill=COLORS['accent'], font=font_large)
    
    # Add "PREMIUM COLLECTION" subtitle
    subtitle = "PREMIUM COLLECTION"
    sub_bbox = draw.textbbox((0, 0), subtitle, font=font_medium)
    sub_width = sub_bbox[2] - sub_bbox[0]
    
    sub_x = (IMAGE_WIDTH - sub_width) // 2
    sub_y = text_y + text_height + 20
    
    draw.text((sub_x, sub_y), subtitle, fill=COLORS['text_secondary'], font=font_medium)
    
    # Add Ukrainian flag accent
    flag_y = CATEGORY_HEIGHT - 20
    draw.rectangle([(0, flag_y), (IMAGE_WIDTH, flag_y + 10)], fill=COLORS['ukraine_blue'])
    draw.rectangle([(0, flag_y + 10), (IMAGE_WIDTH, flag_y + 20)], fill=COLORS['ukraine_yellow'])
    
    return img

def create_lookbook_image(index, title):
    """Create a lookbook lifestyle image"""
    img = create_gradient_background(IMAGE_WIDTH, IMAGE_HEIGHT, 
                                    '#0a0a0a', '#2a2a2a')
    
    draw = ImageDraw.Draw(img)
    
    # Add urban texture pattern
    for i in range(0, IMAGE_WIDTH, 20):
        for j in range(0, IMAGE_HEIGHT, 20):
            if (i + j) % 40 == 0:
                draw.rectangle([(i, j), (i + 2, j + 2)], fill='#333333')
    
    # Add diagonal lines for dynamic effect
    for i in range(-IMAGE_HEIGHT, IMAGE_WIDTH, 100):
        draw.line([(i, 0), (i + IMAGE_HEIGHT, IMAGE_HEIGHT)], 
                 fill='#1a1a1a', width=2)
    
    # Add title
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
    except:
        font = ImageFont.load_default()
    
    text_bbox = draw.textbbox((0, 0), title.upper(), font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    text_x = (IMAGE_WIDTH - text_width) // 2
    text_y = IMAGE_HEIGHT - 150
    
    # Background for text
    draw.rectangle(
        [(text_x - 20, text_y - 10), (text_x + text_width + 20, text_y + text_height + 10)],
        fill='#0a0a0a'
    )
    
    draw.text((text_x, text_y), title.upper(), fill=COLORS['accent'], font=font)
    
    # Add BARBOSS ROOM branding
    brand_text = "BARBOSS ROOM"
    brand_bbox = draw.textbbox((0, 0), brand_text, font=font)
    brand_width = brand_bbox[2] - brand_bbox[0]
    
    draw.text(((IMAGE_WIDTH - brand_width) // 2, 50), brand_text, 
             fill=COLORS['text_secondary'], font=font)
    
    return img

def create_hero_background():
    """Create hero banner background"""
    img = create_gradient_background(1920, 1080, '#000000', '#1a1a1a')
    draw = ImageDraw.Draw(img)
    
    # Add grid pattern
    for i in range(0, 1920, 40):
        draw.line([(i, 0), (i, 1080)], fill='#0a0a0a', width=1)
    for j in range(0, 1080, 40):
        draw.line([(0, j), (1920, j)], fill='#0a0a0a', width=1)
    
    # Add BARBOSS text watermark
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 120)
    except:
        font = ImageFont.load_default()
    
    draw.text((100, 400), "BARBOSS", fill='#111111', font=font)
    draw.text((900, 600), "ROOM", fill='#111111', font=font)
    
    # Add Ukrainian colors accent
    draw.rectangle([(0, 1070), (1920, 1075)], fill=COLORS['ukraine_blue'])
    draw.rectangle([(0, 1075), (1920, 1080)], fill=COLORS['ukraine_yellow'])
    
    return img

def main():
    """Generate all images"""
    print("🎨 Generating Barboss Room product images...")
    
    # Load products from JSON
    with open('content.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Create product images
    print("\n📦 Creating product images...")
    for product in data['products']:
        filename = product['id'] + '.jpg'
        filepath = os.path.join('public/assets/products', filename)
        
        img = create_product_image(product)
        img.save(filepath, 'JPEG', quality=85, optimize=True)
        print(f"  ✅ {filename} - {product['name'][:40]}...")
        
        # Update product image paths in JSON
        product['img'] = f"/assets/products/{filename}"
        if 'gallery' not in product or not product['gallery']:
            product['gallery'] = [f"/assets/products/{filename}"]
    
    # Create category images
    print("\n📁 Creating category images...")
    categories = [
        ("КУРТКИ", "jackets"),
        ("КОСТЮМЫ", "tracksuits"),
        ("ШТАНЫ", "pants"),
        ("ШОРТЫ", "shorts")
    ]
    
    for name, cat_id in categories:
        filename = f"category-{cat_id}.jpg"
        filepath = os.path.join('public/assets/img', filename)
        
        img = create_category_image(name, cat_id)
        img.save(filepath, 'JPEG', quality=85, optimize=True)
        print(f"  ✅ {filename}")
    
    # Create lookbook images
    print("\n📸 Creating lookbook images...")
    lookbook_titles = [
        "STREET LEGEND",
        "URBAN EXPLORER", 
        "КВАДРАТУРА",
        "KIEV STREETS",
        "PREMIUM ONLY",
        "STONE ISLAND CULTURE"
    ]
    
    for i, title in enumerate(lookbook_titles, 1):
        filename = f"look-{i:02d}.jpg"
        filepath = os.path.join('public/assets/lookbook', filename)
        
        img = create_lookbook_image(i, title)
        img.save(filepath, 'JPEG', quality=85, optimize=True)
        print(f"  ✅ {filename} - {title}")
    
    # Create hero background
    print("\n🏠 Creating hero background...")
    hero_img = create_hero_background()
    hero_img.save('public/assets/img/hero-bg.jpg', 'JPEG', quality=90, optimize=True)
    print("  ✅ hero-bg.jpg")
    
    # Update and save JSON with new image paths
    with open('content.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("\n✨ All images generated successfully!")
    print(f"📊 Total: {len(data['products'])} products, {len(categories)} categories, {len(lookbook_titles)} lookbook images")

if __name__ == "__main__":
    main()