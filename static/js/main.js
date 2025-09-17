// static/js/main.js

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all functionality when DOM is loaded
    initScrollAnimations();
    initNavbar();
    initContactForm();
    initGallery();
    initLoadingStates();
});

// Scroll animations for elements
function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fade-up');
            }
        });
    }, observerOptions);

    // Observe all service items and gallery items
    const animateElements = document.querySelectorAll('.service-category, .gallery-item, .about-stats');
    animateElements.forEach(el => observer.observe(el));
}

// Navbar scroll effects
function initNavbar() {
    const navbar = document.querySelector('.custom-navbar');
    
    window.addEventListener('scroll', () => {
        if (window.scrollY > 100) {
            navbar.style.background = 'rgba(10, 10, 10, 0.98)';
            navbar.style.backdropFilter = 'blur(15px)';
        } else {
            navbar.style.background = 'rgba(10, 10, 10, 0.95)';
            navbar.style.backdropFilter = 'blur(10px)';
        }
    });

    // Smooth scroll for nav links
    const navLinks = document.querySelectorAll('.nav-link[href^="#"]');
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Contact form handling
function initContactForm() {
    const contactForm = document.getElementById('contactForm');
    
    if (contactForm) {
        contactForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;
            
            // Show loading state
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<span class="spinner"></span> Sending...';
            
            try {
                // Get form data
                const formData = {
                    name: this.querySelector('#name').value,
                    email: this.querySelector('#email').value,
                    car_info: this.querySelector('#carInfo').value,
                    message: this.querySelector('#message').value
                };
                
                // Get CSRF token
                const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
                
                // Send to Django backend
                const response = await fetch(window.location.href, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken
                    },
                    body: JSON.stringify(formData)
                });
                
                const data = await response.json();
                
                if (data.success) {
                    showMessage('success', data.message);
                    contactForm.reset();
                } else {
                    showMessage('error', data.message);
                }
                
            } catch (error) {
                console.error('Contact form error:', error);
                showMessage('error', 'Network error. Please try calling us directly at (555) TUNE-NOW');
            } finally {
                // Restore button
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalText;
            }
        });
    }
}

// Gallery lightbox functionality
function initGallery() {
    const galleryItems = document.querySelectorAll('.gallery-item');
    
    galleryItems.forEach(item => {
        item.addEventListener('click', () => {
            const img = item.querySelector('img');
            const title = item.querySelector('h5').textContent;
            const description = item.querySelector('p').textContent;
            
            openLightbox(img.src, title, description);
        });
    });
}

// Lightbox modal
function openLightbox(imageSrc, title, description) {
    // Create lightbox HTML
    const lightbox = document.createElement('div');
    lightbox.className = 'lightbox-overlay';
    lightbox.innerHTML = `
        <div class="lightbox-content">
            <button class="lightbox-close">&times;</button>
            <img src="${imageSrc}" alt="${title}" class="lightbox-image">
            <div class="lightbox-info">
                <h4>${title}</h4>
                <p>${description}</p>
            </div>
        </div>
    `;
    
    // Add lightbox styles
    lightbox.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.9);
        z-index: 9999;
        display: flex;
        align-items: center;
        justify-content: center;
        backdrop-filter: blur(5px);
    `;
    
    const content = lightbox.querySelector('.lightbox-content');
    content.style.cssText = `
        position: relative;
        max-width: 90%;
        max-height: 90%;
        text-align: center;
    `;
    
    const closeBtn = lightbox.querySelector('.lightbox-close');
    closeBtn.style.cssText = `
        position: absolute;
        top: -40px;
        right: -40px;
        background: var(--electric-blue);
        color: white;
        border: none;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        font-size: 24px;
        cursor: pointer;
        z-index: 10001;
    `;
    
    const image = lightbox.querySelector('.lightbox-image');
    image.style.cssText = `
        max-width: 100%;
        max-height: 70vh;
        border-radius: 10px;
        box-shadow: 0 20px 60px rgba(0, 212, 255, 0.3);
    `;
    
    const info = lightbox.querySelector('.lightbox-info');
    info.style.cssText = `
        margin-top: 20px;
        color: white;
    `;
    
    document.body.appendChild(lightbox);
    
    // Close lightbox events
    closeBtn.addEventListener('click', () => {
        document.body.removeChild(lightbox);
    });
    
    lightbox.addEventListener('click', (e) => {
        if (e.target === lightbox) {
            document.body.removeChild(lightbox);
        }
    });
    
    // ESC key to close
    const escapeHandler = (e) => {
        if (e.key === 'Escape') {
            document.body.removeChild(lightbox);
            document.removeEventListener('keydown', escapeHandler);
        }
    };
    document.addEventListener('keydown', escapeHandler);
}

// Loading states for buttons and forms
function initLoadingStates() {
    const buttons = document.querySelectorAll('.btn-primary, .btn-danger');
    
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            // Don't add loading state to submit buttons (handled separately)
            if (this.type === 'submit') return;
            
            const originalText = this.innerHTML;
            this.disabled = true;
            this.innerHTML = '<span class="spinner"></span> Loading...';
            
            // Simulate loading (remove this in real implementation)
            setTimeout(() => {
                this.disabled = false;
                this.innerHTML = originalText;
            }, 2000);
        });
    });
}

// Message display function
function showMessage(type, message) {
    // Remove existing messages
    const existingMessages = document.querySelectorAll('.alert-message');
    existingMessages.forEach(msg => msg.remove());
    
    // Create message element
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type === 'success' ? 'success' : 'danger'} alert-message`;
    alertDiv.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        z-index: 9998;
        max-width: 400px;
        border: 2px solid ${type === 'success' ? 'var(--neon-green)' : 'var(--deep-red)'};
        background: var(--charcoal);
        color: white;
        animation: slideInFromRight 0.5s ease-out;
    `;
    
    alertDiv.innerHTML = `
        <strong>${type === 'success' ? 'Success!' : 'Error!'}</strong> ${message}
        <button type="button" class="btn-close btn-close-white ms-2" onclick="this.parentElement.remove()"></button>
    `;
    
    document.body.appendChild(alertDiv);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
}

// CSRF token helper
function getCsrfToken() {
    const token = document.querySelector('[name=csrfmiddlewaretoken]');
    return token ? token.value : '';
}

// Smooth scroll to top function
function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

// Add scroll to top button
function addScrollToTopButton() {
    const scrollButton = document.createElement('button');
    scrollButton.innerHTML = '<i class="fas fa-chevron-up"></i>';
    scrollButton.className = 'scroll-to-top';
    scrollButton.style.cssText = `
        position: fixed;
        bottom: 30px;
        right: 30px;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background: var(--electric-blue);
        color: white;
        border: none;
        cursor: pointer;
        opacity: 0;
        transition: all 0.3s ease;
        z-index: 1000;
        font-size: 18px;
    `;
    
    document.body.appendChild(scrollButton);
    
    // Show/hide based on scroll position
    window.addEventListener('scroll', () => {
        if (window.scrollY > 500) {
            scrollButton.style.opacity = '1';
            scrollButton.style.transform = 'translateY(0)';
        } else {
            scrollButton.style.opacity = '0';
            scrollButton.style.transform = 'translateY(10px)';
        }
    });
    
    scrollButton.addEventListener('click', scrollToTop);
}

// Initialize scroll to top button
addScrollToTopButton();