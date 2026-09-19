/**
 * Victor Lopes — Portfólio
 * Interações e animações
 */

document.addEventListener('DOMContentLoaded', () => {
    // === Menu Mobile ===
    const menuToggle = document.querySelector('.menu-toggle');
    const navLinks = document.querySelector('.nav-links');

    if (menuToggle && navLinks) {
        menuToggle.addEventListener('click', () => {
            navLinks.classList.toggle('active');
        });

        // Fechar menu ao clicar em um link
        navLinks.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                navLinks.classList.remove('active');
            });
        });
    }

    // === Animações de entrada com Intersection Observer ===
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observar seções principais
    document.querySelectorAll('.section, .project-card, .timeline-item, .stat-card').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });

    // === Smooth scroll para links internos ===
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            e.preventDefault();
            const target = document.querySelector(targetId);
            if (target) {
                const headerHeight = 70;
                const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - headerHeight;
                window.scrollTo({
                    behavior: 'smooth',
                    top: targetPosition
                });
            }
        });
    });

    // === Formulário de contato (simulação) ===
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', (e) => {
            e.preventDefault();
            
            const name = document.getElementById('name')?.value || '';
            const email = document.getElementById('email')?.value || '';
            const message = document.getElementById('message')?.value || '';
            
            if (name && email && message) {
                const btn = contactForm.querySelector('button[type="submit"]');
                const originalText = btn.textContent;
                btn.textContent = 'Enviando...';
                btn.disabled = true;
                
                setTimeout(() => {
                    alert('Obrigado pelo contato, ' + name + '! Sua mensagem foi recebida. Responderei em breve.');
                    contactForm.reset();
                    btn.textContent = originalText;
                    btn.disabled = false;
                }, 1500);
            }
        });
    }

    // === Efeito de parallax suave no hero ===
    const hero = document.querySelector('.hero');
    if (hero) {
        window.addEventListener('scroll', () => {
            const scrollY = window.pageYOffset;
            const heroContent = hero.querySelector('.hero-content');
            if (heroContent && scrollY < window.innerHeight) {
                heroContent.style.transform = `translateY(${scrollY * 0.15}px)`;
                heroContent.style.opacity = 1 - (scrollY / window.innerHeight) * 0.3;
            }
        });
    }

    // === Navbar scrolled effect ===
    const header = document.querySelector('.header');
    if (header) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                header.style.boxShadow = '0 4px 20px rgba(0, 0, 0, 0.3)';
            } else {
                header.style.boxShadow = 'none';
            }
        });
    }

    // === Preview de links externos com tooltip ===
    document.querySelectorAll('a[href^="http"]').forEach(link => {
        link.setAttribute('rel', 'noopener noreferrer');
        if (!link.target) {
            link.target = '_blank';
        }
    });
});
