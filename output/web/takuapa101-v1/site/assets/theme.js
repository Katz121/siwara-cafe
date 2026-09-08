/* Remembers the reader's choice; follows the device until they make one. */
(function () {
  'use strict';
  var KEY = 'takuapa-theme';
  var root = document.documentElement;

  function stored() {
    try { return localStorage.getItem(KEY); } catch (e) { return null; }
  }

  function apply(mode) {
    if (mode === 'dark' || mode === 'light') root.setAttribute('data-theme', mode);
    else root.removeAttribute('data-theme');
    var btn = document.querySelector('[data-theme-toggle]');
    if (btn) {
      var dark = root.getAttribute('data-theme') === 'dark' ||
        (!root.getAttribute('data-theme') && window.matchMedia('(prefers-color-scheme: dark)').matches);
      btn.setAttribute('aria-pressed', dark ? 'true' : 'false');
      btn.setAttribute('aria-label', dark ? 'สลับเป็นโหมดกลางวัน' : 'สลับเป็นโหมดกลางคืน');
    }
  }

  apply(stored());

  document.addEventListener('click', function (e) {
    var btn = e.target.closest('[data-theme-toggle]');
    if (!btn) return;
    var isDark = root.getAttribute('data-theme') === 'dark' ||
      (!root.getAttribute('data-theme') && window.matchMedia('(prefers-color-scheme: dark)').matches);
    var next = isDark ? 'light' : 'dark';
    try { localStorage.setItem(KEY, next); } catch (err) { /* private mode */ }
    apply(next);
  });

  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function () {
    if (!stored()) apply(null);
  });
})();
