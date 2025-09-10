# Barboss Room - Premium Streetwear Store

A minimalistic, raw-styled MVP online store for premium streetwear brands like Stone Island, C.P. Company, and more.

## 🚀 Features

- **Responsive Design**: Mobile-first approach with full desktop optimization
- **Dynamic Content**: All product and content data loaded from `content.json`
- **No Framework Dependencies**: Pure HTML, CSS, and JavaScript
- **Modern UI/UX**: Minimalistic design with smooth animations and transitions
- **Complete E-commerce Flow**: Browse → Filter → Product Details → Contact for Purchase

## 📁 Project Structure

```
/
├── index.html          # Homepage with hero, categories, new arrivals, bestsellers
├── shop.html           # Product catalog with filters and sorting
├── product.html        # Product detail page with gallery and info
├── about.html          # About the brand and team
├── contacts.html       # Contact information and form
├── privacy.html        # Privacy policy
├── terms.html          # Terms and conditions
├── styles.css          # Complete styling for all pages
├── main.js             # JavaScript for dynamic functionality
├── content.json        # All content data (products, categories, etc.)
├── /public             # Public assets directory
│   └── /assets
│       ├── /img        # General images
│       ├── /products   # Product images
│       └── /lookbook   # Lookbook/lifestyle images
└── README.md           # This file
```

## 🎨 Design System

### Colors
- **Black**: #111111 (Primary background)
- **Graphite**: #1a1a1a (Secondary background)
- **White**: #FFFFFF (Text and elements)
- **Accent**: #FF4500 (Orange-red for CTAs and highlights)
- **Success**: #39FF14 (Neon green for badges)

### Typography
- **Font**: Inter (Google Fonts)
- **Weights**: 300, 400, 500, 600, 700, 900
- **Responsive sizing**: Using clamp() for fluid typography

## 🛠️ Technologies

- **HTML5**: Semantic markup
- **CSS3**: Modern features including Grid, Flexbox, Custom Properties
- **JavaScript**: ES6+ with async/await for data loading
- **JSON**: Data storage for products and content

## 📱 Key Features

### Homepage
- Fullscreen hero banner with CTA
- Category cards grid
- New arrivals horizontal scroll
- Bestsellers slider
- Lookbook gallery
- Instagram feed placeholder

### Shop Page
- Advanced filtering (category, brand, price, size)
- Sorting options (price, name, featured)
- Responsive product grid
- Mobile-optimized filter sidebar

### Product Page
- Image gallery with zoom functionality
- Size selection
- Direct Telegram purchase link
- Product specifications tabs
- Related products section

### Additional Pages
- About: Brand story, mission, values, team
- Contacts: Multiple contact methods, form, FAQ
- Legal: Privacy policy and terms

## 🚀 Deployment

### Netlify

1. **Via Git**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin YOUR_REPO_URL
   git push -u origin main
   ```
   Then connect to Netlify via GitHub/GitLab/Bitbucket

2. **Via Drag & Drop**:
   - Visit [Netlify Drop](https://app.netlify.com/drop)
   - Drag the entire project folder to deploy

3. **Via CLI**:
   ```bash
   npm install -g netlify-cli
   netlify deploy
   netlify deploy --prod
   ```

### Vercel

1. **Via Git**:
   - Push to GitHub/GitLab/Bitbucket
   - Import project in Vercel dashboard

2. **Via CLI**:
   ```bash
   npm install -g vercel
   vercel
   ```

### Configuration

No build step required! The site is ready to deploy as-is.

**Netlify Settings**:
- Build command: (leave empty)
- Publish directory: `/`

**Vercel Settings**:
- Framework Preset: Other
- Build command: (leave empty)
- Output directory: ./

## 🖼️ Image Assets

To complete the store, add images to the following directories:

### `/public/assets/img/`
- `hero-bg.jpg` - Hero banner background
- `category-jackets.jpg` - Jackets category image
- `category-hoodies.jpg` - Hoodies category image
- `category-pants.jpg` - Pants category image
- `category-accessories.jpg` - Accessories category image
- `about-*.jpg` - About page images

### `/public/assets/products/`
Product images referenced in `content.json`:
- `si-jacket-001.jpg` - Stone Island jacket
- `cp-hoodie-001.jpg` - C.P. Company hoodie
- etc.

### `/public/assets/lookbook/`
Lifestyle/lookbook images:
- `look-01.jpg` through `look-06.jpg`

## 🔧 Customization

### Update Content
Edit `content.json` to:
- Add/remove products
- Update categories
- Change brand information
- Modify social links

### Style Changes
Modify CSS variables in `styles.css`:
```css
:root {
    --color-accent: #FF4500; /* Change accent color */
    --max-width: 1200px;     /* Change container width */
}
```

### Add Products
Add new product objects to the `products` array in `content.json`:
```json
{
    "id": "unique-id",
    "name": "Product Name",
    "brand": "Brand Name",
    "category": "category-id",
    "price": 999,
    "sizes": ["S", "M", "L"],
    "img": "/assets/products/image.jpg",
    "description": "Product description",
    "new": true,
    "bestseller": false
}
```

## 📞 Contact Purchase Flow

The store uses a "Contact to Purchase" model:
1. Customer browses products
2. Selects desired item and size
3. Clicks "Buy via Telegram"
4. Completes purchase through direct messaging

## 🔐 Security & Performance

- No database required (static site)
- Fast loading with optimized CSS/JS
- Lazy loading for images
- Mobile-optimized performance
- Secure contact forms (client-side validation)

## 📄 License

This is an MVP project for Barboss Room. All brand names and trademarks belong to their respective owners.

## 🤝 Support

For questions or support:
- Telegram: @barboss_room
- Instagram: @barboss_room
- Email: info@barbossroom.com

---

Built with ❤️ for streetwear culture