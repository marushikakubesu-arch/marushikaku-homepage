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

  var slideshow = document.getElementById('gallerySlideshow');
  if (slideshow) {
    var slides = slideshow.querySelectorAll('.slideshow-slide');
    var dots = slideshow.parentElement.querySelectorAll('.slideshow-dot');
    var prevBtn = slideshow.querySelector('.slideshow-prev');
    var nextBtn = slideshow.querySelector('.slideshow-next');
    var current = 0;
    var timer;

    var showSlide = function (index) {
      slides[current].classList.remove('is-active');
      dots[current].classList.remove('is-active');
      var oldVideo = slides[current].querySelector('video');
      if (oldVideo) {
        oldVideo.pause();
        oldVideo.currentTime = 0;
      }
      current = (index + slides.length) % slides.length;
      slides[current].classList.add('is-active');
      dots[current].classList.add('is-active');
      var newVideo = slides[current].querySelector('video');
      if (newVideo) {
        newVideo.currentTime = 0;
        newVideo.play().catch(function () {});
      }
    };

    var startTimer = function () {
      clearInterval(timer);
      timer = setInterval(function () {
        showSlide(current + 1);
      }, 4500);
    };

    prevBtn.addEventListener('click', function () {
      showSlide(current - 1);
      startTimer();
    });
    nextBtn.addEventListener('click', function () {
      showSlide(current + 1);
      startTimer();
    });
    dots.forEach(function (dot, i) {
      dot.addEventListener('click', function () {
        showSlide(i);
        startTimer();
      });
    });

    startTimer();
  }

  var blogList = document.querySelector('.blog-list');
  var blogMoreBtn = document.getElementById('blogMoreBtn');
  if (blogList && blogMoreBtn) {
    var blogItems = blogList.querySelectorAll('li');
    var blogVisibleCount = 3;
    if (blogItems.length > blogVisibleCount) {
      for (var bi = blogVisibleCount; bi < blogItems.length; bi++) {
        blogItems[bi].hidden = true;
      }
      blogMoreBtn.addEventListener('click', function () {
        var expanded = blogMoreBtn.getAttribute('aria-expanded') === 'true';
        for (var bj = blogVisibleCount; bj < blogItems.length; bj++) {
          blogItems[bj].hidden = expanded;
        }
        blogMoreBtn.textContent = expanded ? 'もっと見る' : '閉じる';
        blogMoreBtn.setAttribute('aria-expanded', String(!expanded));
      });
    } else {
      blogMoreBtn.hidden = true;
    }
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
