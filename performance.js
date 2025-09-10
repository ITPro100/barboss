// Performance monitoring and optimization
(function() {
    'use strict';
    
    // Monitor page load performance
    window.addEventListener('load', function() {
        if ('performance' in window) {
            const perfData = window.performance.timing;
            const pageLoadTime = perfData.loadEventEnd - perfData.navigationStart;
            const connectTime = perfData.responseEnd - perfData.requestStart;
            const renderTime = perfData.domComplete - perfData.domLoading;
            
            console.log('🚀 Performance Metrics:');
            console.log(`  Page Load: ${pageLoadTime}ms`);
            console.log(`  Connect: ${connectTime}ms`);
            console.log(`  Render: ${renderTime}ms`);
            
            // Send to analytics if needed
            if (pageLoadTime > 3000) {
                console.warn('⚠️ Slow page load detected');
            }
        }
    });
    
    // Optimize images based on connection speed
    if ('connection' in navigator) {
        const connection = navigator.connection;
        const slowConnection = connection.effectiveType === '2g' || connection.effectiveType === 'slow-2g';
        
        if (slowConnection) {
            document.documentElement.classList.add('slow-connection');
            console.log('📶 Slow connection detected - optimizing images');
            
            // Load lower quality images
            document.querySelectorAll('img').forEach(img => {
                const src = img.src || img.dataset.src;
                if (src && !src.includes('?q=')) {
                    const lowQualitySrc = src + '?q=60';
                    if (img.dataset.src) {
                        img.dataset.src = lowQualitySrc;
                    } else {
                        img.src = lowQualitySrc;
                    }
                }
            });
        }
    }
    
    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Preload critical images
    const criticalImages = [
        '/assets/img/hero-bg.jpg',
        '/assets/products/si-jacket-real.jpg',
        '/assets/products/cp-hoodie-real.jpg'
    ];
    
    criticalImages.forEach(src => {
        const link = document.createElement('link');
        link.rel = 'preload';
        link.as = 'image';
        link.href = src;
        document.head.appendChild(link);
    });
    
    // Add touch feedback for mobile
    if ('ontouchstart' in window) {
        document.body.classList.add('touch-device');
        
        document.querySelectorAll('.btn, .product-card, .category-card').forEach(element => {
            element.addEventListener('touchstart', function() {
                this.classList.add('touch-active');
            });
            
            element.addEventListener('touchend', function() {
                setTimeout(() => {
                    this.classList.remove('touch-active');
                }, 100);
            });
        });
    }
    
    // Monitor image loading
    let loadedImages = 0;
    const totalImages = document.querySelectorAll('img').length;
    
    document.querySelectorAll('img').forEach(img => {
        if (img.complete) {
            loadedImages++;
        } else {
            img.addEventListener('load', () => {
                loadedImages++;
                const progress = (loadedImages / totalImages) * 100;
                
                // Update loading indicator if exists
                const loader = document.querySelector('.loading-progress');
                if (loader) {
                    loader.style.width = progress + '%';
                }
                
                if (loadedImages === totalImages) {
                    console.log('✅ All images loaded');
                    document.body.classList.add('images-loaded');
                }
            });
        }
    });
})();