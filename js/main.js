// ZENIA — Main initialization

// Nav scroll effect + active link highlight
var nav = document.getElementById('nav');
var navAnchors = document.querySelectorAll('.nav-links a[href^="#"]');
var sections = [];
navAnchors.forEach(function(a) {
  var s = document.querySelector(a.getAttribute('href'));
  if (s) sections.push({ el: s, link: a });
});
var mobileCta = document.getElementById('mobileCta');
var heroSection = document.getElementById('hero');
window.addEventListener('scroll', function() {
  nav.classList.toggle('scrolled', window.scrollY > 40);
  var scrollPos = window.scrollY + 120;
  var current = null;
  sections.forEach(function(s) {
    if (s.el.offsetTop <= scrollPos) current = s.link;
  });
  navAnchors.forEach(function(a) { a.classList.remove('active'); });
  if (current) current.classList.add('active');
  // Mobile sticky CTA: show after scrolling past hero
  if (mobileCta && heroSection) {
    var heroBottom = heroSection.offsetTop + heroSection.offsetHeight;
    mobileCta.classList.toggle('visible', window.scrollY > heroBottom - 200);
  }
}, { passive: true });

// Reveal on scroll (IntersectionObserver)
var observer = new IntersectionObserver(function(entries) {
  entries.forEach(function(entry) {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });
document.querySelectorAll('.reveal').forEach(function(el) { observer.observe(el); });

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(function(link) {
  link.addEventListener('click', function(e) {
    var t = document.querySelector(link.getAttribute('href'));
    if (t) { e.preventDefault(); t.scrollIntoView({ behavior: 'smooth', block: 'start' }); }
  });
});

// Mobile hamburger menu toggle
var navToggle = document.getElementById('navToggle');
var navLinks = document.querySelector('.nav-links');
var navRight = document.querySelector('.nav-right');
function closeMobileMenu() {
  navLinks.classList.remove('nav-open');
  navRight.classList.remove('nav-open');
  document.body.classList.remove('nav-menu-open');
  navToggle.setAttribute('aria-expanded', 'false');
}
if (navToggle) {
  navToggle.addEventListener('click', function() {
    var isOpen = navLinks.classList.toggle('nav-open');
    navRight.classList.toggle('nav-open');
    document.body.classList.toggle('nav-menu-open', isOpen);
    navToggle.setAttribute('aria-expanded', String(isOpen));
  });
  // Close menu when a nav link is clicked
  navLinks.querySelectorAll('a').forEach(function(link) {
    link.addEventListener('click', closeMobileMenu);
  });
}

// Initialize language
var detectedLang = detectLanguage();
if (detectedLang) {
  applyTranslations(detectedLang);
} else {
  // No preference saved — default to English while modal shows
  applyTranslations('en');
  showLangModal();
}
