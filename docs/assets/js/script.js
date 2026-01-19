// ===================================
// Navigation Bar Scroll Effect
// ===================================

const navbar = document.getElementById('navbar');
let lastScroll = 0;

window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;

    if (currentScroll > 50) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }

    lastScroll = currentScroll;
});

// ===================================
// Smooth Scrolling for Navigation Links
// ===================================

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));

        if (target) {
            const offsetTop = target.offsetTop - 80;
            window.scrollTo({
                top: offsetTop,
                behavior: 'smooth'
            });
        }
    });
});

// ===================================
// Scroll to Top Button
// ===================================

const scrollTopBtn = document.getElementById('scrollTop');

window.addEventListener('scroll', () => {
    if (window.pageYOffset > 300) {
        scrollTopBtn.classList.add('show');
    } else {
        scrollTopBtn.classList.remove('show');
    }
});

scrollTopBtn.addEventListener('click', () => {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
});

// ===================================
// Copy Citation to Clipboard
// ===================================

function copyCitation() {
    const citationText = `@article{menvagent2026,
  title={MEnvAgent: Scalable Polyglot Environment Construction for Verifiable Software Engineering},
  author={TODO: Add authors from paper},
  journal={International Conference on Machine Learning (ICML)},
  year={2026}
}`;

    // Create a temporary textarea element
    const textarea = document.createElement('textarea');
    textarea.value = citationText;
    textarea.style.position = 'fixed';
    textarea.style.opacity = '0';
    document.body.appendChild(textarea);

    // Select and copy
    textarea.select();
    document.execCommand('copy');

    // Remove the textarea
    document.body.removeChild(textarea);

    // Update button text temporarily
    const copyBtn = document.querySelector('.copy-btn');
    const originalHTML = copyBtn.innerHTML;
    copyBtn.innerHTML = '<i class="fas fa-check"></i> Copied!';
    copyBtn.style.background = '#10b981';

    setTimeout(() => {
        copyBtn.innerHTML = originalHTML;
        copyBtn.style.background = '';
    }, 2000);
}

// ===================================
// Intersection Observer for Fade-in Animations
// ===================================

const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('fade-in');
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

// Observe all feature cards, stage cards, and other animatable elements
document.addEventListener('DOMContentLoaded', () => {
    const animatableElements = document.querySelectorAll(
        '.feature-card, .stage-card, .news-item, .language-card, .install-step, .stat-card, .improvement-card'
    );

    animatableElements.forEach(el => {
        observer.observe(el);
    });
});

// ===================================
// Active Navigation Link Highlighting
// ===================================

const sections = document.querySelectorAll('section[id]');
const navLinks = document.querySelectorAll('.nav-menu a[href^="#"]');

window.addEventListener('scroll', () => {
    let current = '';

    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;

        if (window.pageYOffset >= sectionTop - 100) {
            current = section.getAttribute('id');
        }
    });

    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === `#${current}`) {
            link.classList.add('active');
        }
    });
});

// ===================================
// Mobile Menu Toggle (for future implementation)
// ===================================

// This can be expanded when implementing a mobile hamburger menu
const createMobileMenu = () => {
    const navMenu = document.querySelector('.nav-menu');
    const hamburger = document.createElement('button');
    hamburger.className = 'hamburger';
    hamburger.innerHTML = '<i class="fas fa-bars"></i>';

    hamburger.addEventListener('click', () => {
        navMenu.classList.toggle('active');
        hamburger.classList.toggle('active');
    });

    // Add hamburger to navbar on mobile
    if (window.innerWidth <= 768) {
        const navBrand = document.querySelector('.nav-brand');
        navBrand.parentElement.appendChild(hamburger);
    }
};

// ===================================
// Dynamic Stats Counter Animation
// ===================================

const animateCounter = (element, target, duration = 2000) => {
    let start = 0;
    const increment = target / (duration / 16); // 60fps

    const timer = setInterval(() => {
        start += increment;
        if (start >= target) {
            element.textContent = target.toLocaleString();
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(start).toLocaleString();
        }
    }, 16);
};

// Trigger counter animation when stats section is visible
const statsObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const statNumbers = entry.target.querySelectorAll('.stat-number');
            statNumbers.forEach(stat => {
                const target = parseInt(stat.textContent.replace(/,/g, ''));
                animateCounter(stat, target);
            });
            statsObserver.unobserve(entry.target);
        }
    });
}, { threshold: 0.5 });

document.addEventListener('DOMContentLoaded', () => {
    const benchmarkStats = document.querySelector('.benchmark-stats');
    if (benchmarkStats) {
        statsObserver.observe(benchmarkStats);
    }
});

// ===================================
// Code Snippet Copy Functionality
// ===================================

const addCopyButtonsToCodeSnippets = () => {
    const codeSnippets = document.querySelectorAll('.code-snippet');

    codeSnippets.forEach(snippet => {
        if (snippet.querySelector('.copy-code-btn')) return; // Already has button

        const copyBtn = document.createElement('button');
        copyBtn.className = 'copy-code-btn';
        copyBtn.innerHTML = '<i class="fas fa-copy"></i>';
        copyBtn.title = 'Copy code';

        copyBtn.addEventListener('click', () => {
            const code = snippet.querySelector('code').textContent;
            const textarea = document.createElement('textarea');
            textarea.value = code;
            textarea.style.position = 'fixed';
            textarea.style.opacity = '0';
            document.body.appendChild(textarea);
            textarea.select();
            document.execCommand('copy');
            document.body.removeChild(textarea);

            copyBtn.innerHTML = '<i class="fas fa-check"></i>';
            copyBtn.style.color = '#10b981';

            setTimeout(() => {
                copyBtn.innerHTML = '<i class="fas fa-copy"></i>';
                copyBtn.style.color = '';
            }, 2000);
        });

        snippet.style.position = 'relative';
        snippet.appendChild(copyBtn);
    });
};

document.addEventListener('DOMContentLoaded', addCopyButtonsToCodeSnippets);

// ===================================
// Image Placeholder Click Handler
// ===================================

document.addEventListener('DOMContentLoaded', () => {
    const placeholders = document.querySelectorAll('.image-placeholder');

    placeholders.forEach(placeholder => {
        placeholder.addEventListener('click', () => {
            placeholder.style.borderColor = 'var(--primary-color)';
            placeholder.style.background = 'var(--bg-secondary)';

            setTimeout(() => {
                placeholder.style.borderColor = '';
                placeholder.style.background = '';
            }, 500);
        });
    });
});

// ===================================
// Lazy Loading for Images (when added)
// ===================================

const lazyLoadImages = () => {
    const images = document.querySelectorAll('img[data-src]');

    const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                imageObserver.unobserve(img);
            }
        });
    });

    images.forEach(img => imageObserver.observe(img));
};

document.addEventListener('DOMContentLoaded', lazyLoadImages);

// ===================================
// External Link Handler
// ===================================

document.addEventListener('DOMContentLoaded', () => {
    const externalLinks = document.querySelectorAll('a[href^="http"]');

    externalLinks.forEach(link => {
        if (!link.hasAttribute('target')) {
            link.setAttribute('target', '_blank');
            link.setAttribute('rel', 'noopener noreferrer');
        }
    });
});

// ===================================
// Console Log (Easter Egg)
// ===================================

console.log('%cMEnvAgent', 'font-size: 24px; font-weight: bold; color: #6366f1;');
console.log('%cScalable Polyglot Environment Construction for Verifiable Software Engineering', 'font-size: 14px; color: #6b7280;');
console.log('%cInterested in contributing? Check out our GitHub: https://github.com/your-org/MEnvAgent', 'font-size: 12px; color: #10b981;');
