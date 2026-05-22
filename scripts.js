// Naddi's Ceramiche — Minimal JS

document.addEventListener('DOMContentLoaded', function () {
  // Mobile nav
  var burger = document.querySelector('.burger');
  var mobileNav = document.querySelector('.mobile-nav');
  var closeBtn = document.querySelector('.mobile-nav-close');

  if (burger && mobileNav) {
    burger.addEventListener('click', function () {
      mobileNav.classList.add('open');
      document.body.style.overflow = 'hidden';
    });
    if (closeBtn) {
      closeBtn.addEventListener('click', function () {
        mobileNav.classList.remove('open');
        document.body.style.overflow = '';
      });
    }
    mobileNav.addEventListener('click', function (e) {
      if (e.target === mobileNav) {
        mobileNav.classList.remove('open');
        document.body.style.overflow = '';
      }
    });
  }

  // Active nav link
  var currentPage = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-links a, .mobile-nav a').forEach(function (a) {
    if (a.getAttribute('href') === currentPage) {
      a.classList.add('active');
    }
  });
});
