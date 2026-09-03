document.addEventListener('DOMContentLoaded', function () {
  var navToggle = document.getElementById('navToggle');
  var siteNav = document.getElementById('siteNav');

  navToggle.addEventListener('click', function () {
    var isOpen = siteNav.classList.toggle('is-open');
    navToggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
  });

  siteNav.querySelectorAll('a').forEach(function (link) {
    link.addEventListener('click', function () {
      siteNav.classList.remove('is-open');
      navToggle.setAttribute('aria-expanded', 'false');
    });
  });

  var yearEl = document.getElementById('year');
  if (yearEl) {
    yearEl.textContent = new Date().getFullYear();
  }

  var contactForm = document.getElementById('contactForm');
  var hiddenIframe = document.getElementById('hidden_iframe');
  var formThanks = document.getElementById('formThanks');
  if (contactForm && hiddenIframe && formThanks) {
    var submitted = false;
    contactForm.addEventListener('submit', function () {
      submitted = true;
    });
    hiddenIframe.addEventListener('load', function () {
      if (submitted) {
        contactForm.hidden = true;
        formThanks.hidden = false;
        submitted = false;
      }
    });
  }
});
