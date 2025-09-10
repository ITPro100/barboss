// ============================================
// BARBOSS ROOM - Main JavaScript
// ============================================

// Global data store
let contentData = {};
let currentProducts = [];
let filteredProducts = [];

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', async () => {
    await loadContent();
    initializeNavigation();
    initializePageContent();
});

// Load content from JSON
async function loadContent() {
    try {
        const response = await fetch('content.json');
        contentData = await response.json();
        currentProducts = contentData.products || [];
        filteredProducts = [...currentProducts];
    } catch (error) {
        console.error('Error loading content:', error);
        // Fallback to placeholder data
        contentData = {
            brand: { name: "Barboss Room", slogan: "Premium streetwear." },
            products: [],
            categories: [],
            lookbook: []
        };
    }
}

// Initialize navigation
function initializeNavigation() {
    const navbar = document.getElementById('navbar');
    const mobileMenuToggle = document.getElementById('mobileMenuToggle');
    const navMenu = document.getElementById('navMenu');

    // Handle scroll effect
    if (navbar && !navbar.classList.contains('navbar-dark')) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
    }

    // Mobile menu toggle
    if (mobileMenuToggle && navMenu) {
        mobileMenuToggle.addEventListener('click', () => {
            mobileMenuToggle.classList.toggle('active');
            navMenu.classList.toggle('active');
        });

        // Close mobile menu when clicking outside
        document.addEventListener('click', (e) => {
            if (!mobileMenuToggle.contains(e.target) && !navMenu.contains(e.target)) {
                mobileMenuToggle.classList.remove('active');
                navMenu.classList.remove('active');
            }
        });
    }
}

// Initialize page-specific content
function initializePageContent() {
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';

    switch (currentPage) {
        case 'index.html':
        case '':
            initializeHomePage();
            break;
        case 'shop.html':
            initializeShopPage();
            break;
        case 'product.html':
            initializeProductPage();
            break;
        case 'about.html':
            initializeAboutPage();
            break;
        case 'contacts.html':
            initializeContactsPage();
            break;
    }
}

// ============================================
// HOME PAGE
// ============================================

function initializeHomePage() {
    loadCategories();
    loadNewArrivals();
    loadBestSellers();
    loadLookbook();
    initializeSlider();
}

function loadCategories() {
    const grid = document.getElementById('categoriesGrid');
    if (!grid || !contentData.categories) return;

    grid.innerHTML = contentData.categories.map(category => `
        <a href="${category.url}" class="category-card">
            <div class="category-overlay">
                <h3 class="category-title">${category.name}</h3>
            </div>
        </a>
    `).join('');
}

function loadNewArrivals() {
    const container = document.getElementById('newArrivals');
    if (!container || !contentData.products) return;

    const newProducts = contentData.products.filter(p => p.new).slice(0, 4);
    container.innerHTML = newProducts.map(product => createProductCard(product)).join('');
}

function loadBestSellers() {
    const container = document.getElementById('bestSellers');
    if (!container || !contentData.products) return;

    const bestProducts = contentData.products.filter(p => p.bestseller);
    container.innerHTML = bestProducts.map(product => createProductCard(product)).join('');
}

function loadLookbook() {
    const gallery = document.getElementById('lookbookGallery');
    if (!gallery || !contentData.lookbook) return;

    gallery.innerHTML = contentData.lookbook.map((item, index) => `
        <div class="lookbook-item">
            <img src="${item.img}" alt="${item.title || 'Lookbook ' + (index + 1)}" loading="lazy">
        </div>
    `).join('');
}

function createProductCard(product) {
    const soldClass = product.sold ? 'sold' : '';
    const priceDisplay = product.priceOnRequest 
        ? '<span class="price-on-request">✏️ Цена по запросу</span>'
        : product.sold 
        ? '<span class="product-price">❌ ПРОДАНО</span>'
        : `<div class="product-price">${product.price} ${product.currency || 'грн'}</div>`;
    
    return `
        <div class="product-card ${soldClass}" onclick="${!product.sold ? `goToProduct('${product.id}')` : 'return false;'}">
            <div class="product-image">
                ${product.new && !product.sold ? '<span class="product-badge">NEW</span>' : ''}
                ${product.sold ? '<span class="product-badge" style="background: red;">SOLD</span>' : ''}
                <img src="${product.img}" alt="${product.name}" loading="lazy">
            </div>
            <div class="product-info">
                <div class="product-brand">${product.brand}</div>
                <h3 class="product-name">${product.name}</h3>
                ${priceDisplay}
            </div>
        </div>
    `;
}

function goToProduct(productId) {
    window.location.href = `product.html?id=${productId}`;
}

// Slider functionality
function initializeSlider() {
    const slider = document.getElementById('bestSellers');
    const prevBtn = document.getElementById('sliderPrev');
    const nextBtn = document.getElementById('sliderNext');

    if (!slider || !prevBtn || !nextBtn) return;

    let scrollAmount = 0;
    const scrollStep = 304; // Card width + gap

    prevBtn.addEventListener('click', () => {
        scrollAmount = Math.max(0, scrollAmount - scrollStep);
        slider.style.transform = `translateX(-${scrollAmount}px)`;
    });

    nextBtn.addEventListener('click', () => {
        const maxScroll = slider.scrollWidth - slider.clientWidth;
        scrollAmount = Math.min(maxScroll, scrollAmount + scrollStep);
        slider.style.transform = `translateX(-${scrollAmount}px)`;
    });
}

// ============================================
// SHOP PAGE
// ============================================

function initializeShopPage() {
    loadShopProducts();
    initializeFilters();
    initializeSorting();
    initializeMobileFilters();
    
    // Check URL parameters for initial filters
    const urlParams = new URLSearchParams(window.location.search);
    const category = urlParams.get('cat');
    const filter = urlParams.get('filter');
    
    if (category) {
        const checkbox = document.querySelector(`#categoryFilter input[value="${category}"]`);
        if (checkbox) {
            checkbox.checked = true;
            applyFilters();
        }
    }
    
    if (filter === 'new') {
        filteredProducts = currentProducts.filter(p => p.new);
        displayProducts();
    } else if (filter === 'bestseller') {
        filteredProducts = currentProducts.filter(p => p.bestseller);
        displayProducts();
    }
}

function loadShopProducts() {
    displayProducts();
    loadBrandFilters();
}

function displayProducts() {
    const grid = document.getElementById('productsGrid');
    const noResults = document.getElementById('noResults');
    const resultsCount = document.getElementById('resultsCount');
    
    if (!grid) return;

    if (filteredProducts.length === 0) {
        grid.style.display = 'none';
        if (noResults) noResults.style.display = 'block';
        if (resultsCount) resultsCount.textContent = '0';
    } else {
        grid.style.display = 'grid';
        if (noResults) noResults.style.display = 'none';
        if (resultsCount) resultsCount.textContent = filteredProducts.length;
        grid.innerHTML = filteredProducts.map(product => createProductCard(product)).join('');
    }
}

function loadBrandFilters() {
    const brandFilter = document.getElementById('brandFilter');
    if (!brandFilter || !contentData.brands) return;

    brandFilter.innerHTML = contentData.brands.map(brand => `
        <label class="filter-option">
            <input type="checkbox" value="${brand}">
            <span>${brand}</span>
        </label>
    `).join('');
}

function initializeFilters() {
    // Category filters
    const categoryFilters = document.querySelectorAll('#categoryFilter input');
    categoryFilters.forEach(input => {
        input.addEventListener('change', applyFilters);
    });

    // Brand filters
    const brandFilter = document.getElementById('brandFilter');
    if (brandFilter) {
        brandFilter.addEventListener('change', applyFilters);
    }

    // Price filters
    const priceFilters = document.querySelectorAll('input[name="price"]');
    priceFilters.forEach(input => {
        input.addEventListener('change', applyFilters);
    });

    // Size filters
    const sizeButtons = document.querySelectorAll('.size-option');
    sizeButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            btn.classList.toggle('active');
            applyFilters();
        });
    });

    // Clear filters
    const clearBtn = document.getElementById('clearFilters');
    if (clearBtn) {
        clearBtn.addEventListener('click', clearAllFilters);
    }
}

function applyFilters() {
    filteredProducts = [...currentProducts];

    // Category filter
    const selectedCategories = Array.from(document.querySelectorAll('#categoryFilter input:checked'))
        .map(input => input.value);
    
    if (selectedCategories.length > 0) {
        filteredProducts = filteredProducts.filter(p => 
            selectedCategories.includes(p.category)
        );
    }

    // Brand filter
    const selectedBrands = Array.from(document.querySelectorAll('#brandFilter input:checked'))
        .map(input => input.value);
    
    if (selectedBrands.length > 0) {
        filteredProducts = filteredProducts.filter(p => 
            selectedBrands.includes(p.brand)
        );
    }

    // Price filter
    const selectedPrice = document.querySelector('input[name="price"]:checked');
    if (selectedPrice) {
        const priceRange = selectedPrice.value;
        if (priceRange === '0-500') {
            filteredProducts = filteredProducts.filter(p => p.price < 500);
        } else if (priceRange === '500-1000') {
            filteredProducts = filteredProducts.filter(p => p.price >= 500 && p.price <= 1000);
        } else if (priceRange === '1000+') {
            filteredProducts = filteredProducts.filter(p => p.price > 1000);
        }
    }

    // Size filter
    const selectedSizes = Array.from(document.querySelectorAll('.size-option.active'))
        .map(btn => btn.dataset.size);
    
    if (selectedSizes.length > 0) {
        filteredProducts = filteredProducts.filter(p => 
            p.sizes && p.sizes.some(size => selectedSizes.includes(size))
        );
    }

    displayProducts();
}

function clearAllFilters() {
    // Clear all checkboxes
    document.querySelectorAll('.filters-sidebar input[type="checkbox"]').forEach(input => {
        input.checked = false;
    });
    
    // Clear radio buttons
    document.querySelectorAll('.filters-sidebar input[type="radio"]').forEach(input => {
        input.checked = false;
    });
    
    // Clear size buttons
    document.querySelectorAll('.size-option').forEach(btn => {
        btn.classList.remove('active');
    });
    
    filteredProducts = [...currentProducts];
    displayProducts();
}

function initializeSorting() {
    const sortSelect = document.getElementById('sortSelect');
    if (!sortSelect) return;

    sortSelect.addEventListener('change', (e) => {
        const sortBy = e.target.value;
        
        switch (sortBy) {
            case 'price-low':
                filteredProducts.sort((a, b) => a.price - b.price);
                break;
            case 'price-high':
                filteredProducts.sort((a, b) => b.price - a.price);
                break;
            case 'name':
                filteredProducts.sort((a, b) => a.name.localeCompare(b.name));
                break;
            default:
                // Featured - restore original order
                applyFilters();
                return;
        }
        
        displayProducts();
    });
}

function initializeMobileFilters() {
    const mobileToggle = document.getElementById('mobileFilterToggle');
    const filtersSidebar = document.getElementById('filtersSidebar');
    
    if (!mobileToggle || !filtersSidebar) return;

    mobileToggle.addEventListener('click', () => {
        filtersSidebar.classList.toggle('active');
    });

    // Close filters when clicking outside
    document.addEventListener('click', (e) => {
        if (!mobileToggle.contains(e.target) && !filtersSidebar.contains(e.target)) {
            filtersSidebar.classList.remove('active');
        }
    });
}

// ============================================
// PRODUCT PAGE
// ============================================

function initializeProductPage() {
    const urlParams = new URLSearchParams(window.location.search);
    const productId = urlParams.get('id');
    
    if (!productId) {
        // Default to first product if no ID provided
        const firstProduct = contentData.products?.[0];
        if (firstProduct) {
            loadProductDetails(firstProduct);
        }
        return;
    }
    
    const product = contentData.products?.find(p => p.id === productId);
    if (product) {
        loadProductDetails(product);
    }
}

function loadProductDetails(product) {
    // Update breadcrumb
    const breadcrumb = document.getElementById('breadcrumbProduct');
    if (breadcrumb) breadcrumb.textContent = product.name;
    
    // Update product info
    document.getElementById('productBrand').textContent = product.brand;
    document.getElementById('productTitle').textContent = product.name;
    
    // Handle price display
    const priceElement = document.getElementById('productPrice');
    if (product.sold) {
        priceElement.innerHTML = '<span style="color: red;">❌ ПРОДАНО/SOLD ❌</span>';
    } else if (product.priceOnRequest) {
        priceElement.innerHTML = '<span style="color: var(--color-ukraine-yellow);">✏️ Цена по запросу</span>';
    } else {
        priceElement.textContent = `${product.price} ${product.currency || 'грн'} 🇺🇦`;
    }
    
    document.getElementById('productDescription').textContent = product.description;
    
    // Show/hide new badge
    const newBadge = document.getElementById('productNew');
    if (newBadge) {
        newBadge.style.display = product.new ? 'inline-block' : 'none';
    }
    
    // Load main image
    const mainImage = document.getElementById('mainImage');
    if (mainImage) {
        mainImage.src = product.img;
        mainImage.alt = product.name;
    }
    
    // Load gallery thumbnails
    const galleryThumbs = document.getElementById('galleryThumbs');
    if (galleryThumbs && product.gallery) {
        galleryThumbs.innerHTML = product.gallery.map((img, index) => `
            <div class="gallery-thumb ${index === 0 ? 'active' : ''}" onclick="changeMainImage('${img}', this)">
                <img src="${img}" alt="${product.name} ${index + 1}">
            </div>
        `).join('');
    }
    
    // Load sizes
    const sizeOptions = document.getElementById('sizeOptions');
    if (sizeOptions && product.sizes) {
        sizeOptions.innerHTML = product.sizes.map(size => `
            <button class="size-option" onclick="selectSize(this)">${size}</button>
        `).join('');
    }
    
    // Load brand info
    updateBrandInfo(product.brand);
    
    // Load related products
    loadRelatedProducts(product);
    
    // Initialize tabs
    initializeProductTabs();
    
    // Initialize zoom
    initializeImageZoom();
}

function changeMainImage(src, thumb) {
    const mainImage = document.getElementById('mainImage');
    if (mainImage) {
        mainImage.src = src;
    }
    
    // Update active thumb
    document.querySelectorAll('.gallery-thumb').forEach(t => t.classList.remove('active'));
    if (thumb) thumb.classList.add('active');
}

function selectSize(button) {
    document.querySelectorAll('#sizeOptions .size-option').forEach(btn => {
        btn.classList.remove('active');
    });
    button.classList.add('active');
}

function updateBrandInfo(brand) {
    const brandInfo = document.getElementById('brandInfo');
    if (!brandInfo) return;
    
    const brandDescriptions = {
        'Stone Island': 'Since 1982, Stone Island has been the pinnacle of research in fibers and textiles. Their innovative approach to garment design and unique dyeing techniques have made them legends in streetwear culture.',
        'C.P. Company': 'Founded by Massimo Osti in 1971, C.P. Company pioneered garment dyeing and continues to push boundaries with their Metropolis and Chrome collections.',
        'Ma.Strum': 'Born from a sailing heritage, Ma.Strum combines technical innovation with contemporary design.',
        'Peaceful Hooligan': 'British streetwear brand inspired by terrace culture and the casual movement.',
        'Weekend Offender': 'Premium casual wear brand with roots in football terrace culture.'
    };
    
    brandInfo.textContent = brandDescriptions[brand] || `Premium ${brand} merchandise, 100% authentic.`;
}

function loadRelatedProducts(currentProduct) {
    const container = document.getElementById('relatedProducts');
    if (!container || !contentData.products) return;
    
    // Get products from same category
    const related = contentData.products
        .filter(p => p.category === currentProduct.category && p.id !== currentProduct.id)
        .slice(0, 4);
    
    if (related.length === 0) {
        // If no related products in same category, show random products
        related.push(...contentData.products
            .filter(p => p.id !== currentProduct.id)
            .slice(0, 4));
    }
    
    container.innerHTML = related.map(product => createProductCard(product)).join('');
}

function initializeProductTabs() {
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabPanes = document.querySelectorAll('.tab-pane');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const targetTab = button.dataset.tab;
            
            // Update active button
            tabButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            
            // Update active pane
            tabPanes.forEach(pane => {
                pane.classList.remove('active');
                if (pane.id === targetTab) {
                    pane.classList.add('active');
                }
            });
        });
    });
}

function initializeImageZoom() {
    const mainImage = document.getElementById('mainImage');
    const zoomModal = document.getElementById('zoomModal');
    const zoomImage = document.getElementById('zoomImage');
    const zoomClose = document.querySelector('.zoom-close');
    
    if (!mainImage || !zoomModal || !zoomImage) return;
    
    mainImage.addEventListener('click', () => {
        zoomModal.style.display = 'block';
        zoomImage.src = mainImage.src;
    });
    
    if (zoomClose) {
        zoomClose.addEventListener('click', () => {
            zoomModal.style.display = 'none';
        });
    }
    
    zoomModal.addEventListener('click', (e) => {
        if (e.target === zoomModal) {
            zoomModal.style.display = 'none';
        }
    });
}

// ============================================
// ABOUT PAGE
// ============================================

function initializeAboutPage() {
    // Load dynamic content if needed
    if (contentData.about) {
        const storyElement = document.getElementById('aboutStory');
        const missionElement = document.getElementById('aboutMission');
        const teamElement = document.getElementById('aboutTeam');
        
        if (storyElement && contentData.about.story) {
            storyElement.textContent = contentData.about.story;
        }
        
        if (missionElement && contentData.about.mission) {
            missionElement.textContent = contentData.about.mission;
        }
        
        if (teamElement && contentData.about.team) {
            teamElement.textContent = contentData.about.team;
        }
    }
}

// ============================================
// CONTACTS PAGE
// ============================================

function initializeContactsPage() {
    const contactForm = document.getElementById('contactForm');
    
    if (contactForm) {
        contactForm.addEventListener('submit', (e) => {
            e.preventDefault();
            
            // Get form data
            const formData = new FormData(contactForm);
            const data = Object.fromEntries(formData);
            
            // Here you would normally send the data to a server
            console.log('Contact form submission:', data);
            
            // Show success message
            alert('Thank you for your message! We will get back to you within 24 hours.');
            
            // Reset form
            contactForm.reset();
        });
    }
}

// ============================================
// UTILITY FUNCTIONS
// ============================================

// Smooth scroll to element
function smoothScrollTo(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

// Format price
function formatPrice(price) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    }).format(price);
}

// Debounce function for search/filter
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Lazy load images
if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.add('loaded');
                observer.unobserve(img);
            }
        });
    });
    
    document.addEventListener('DOMContentLoaded', () => {
        const lazyImages = document.querySelectorAll('img[data-src]');
        lazyImages.forEach(img => imageObserver.observe(img));
    });
}