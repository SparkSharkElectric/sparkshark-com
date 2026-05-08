// site.js — sparkshark.com
// Minimal interactive: mobile menu toggle. No frameworks, no dependencies.
(function () {
  'use strict';
  var toggle = document.querySelector('.menu-toggle');
  var menu = document.querySelector('.mobile-menu');
  if (toggle && menu) {
    toggle.addEventListener('click', function () {
      var open = menu.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }
})();
