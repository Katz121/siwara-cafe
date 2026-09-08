/* Site-wide search: places, traditions, shops and stories. No dependencies. */
(function () {
  'use strict';
  var BASE = (document.documentElement.dataset.base || '');
  var LABEL = {
    place: 'สถานที่', tradition: 'ประเพณี', story: 'เรื่องเล่า',
    restaurant: 'ร้านอาหาร', drink_shop: 'เครื่องดื่ม', souvenir_shop: 'ของฝาก'
  };
  var index = null, loading = null, dlg, input, list, status, lastFocus, active = -1, rows = [];

  function load() {
    if (index) return Promise.resolve(index);
    if (loading) return loading;
    loading = fetch(BASE + '/assets/search-index.json')
      .then(function (r) { return r.json(); })
      .then(function (d) { index = d; return d; })
      .catch(function () { index = []; return index; });
    return loading;
  }

  function build() {
    dlg = document.createElement('div');
    dlg.className = 'searchbox';
    dlg.hidden = true;
    dlg.setAttribute('role', 'dialog');
    dlg.setAttribute('aria-modal', 'true');
    dlg.setAttribute('aria-label', 'ค้นหาในเว็บไซต์');
    dlg.innerHTML =
      '<div class="searchbox-backdrop" data-close></div>' +
      '<div class="searchbox-panel">' +
      '<label class="visually-hidden" for="site-search-input">ค้นหาสถานที่ ประเพณี ร้าน หรือเรื่องเล่า</label>' +
      '<input id="site-search-input" type="search" autocomplete="off" placeholder="ค้นหาสถานที่ ร้าน หรือเรื่องเล่า">' +
      '<p class="searchbox-status" role="status" aria-live="polite"></p>' +
      '<ul class="searchbox-results" role="listbox"></ul>' +
      '<p class="searchbox-hint">กด Esc เพื่อปิด · ลูกศรขึ้นลงเพื่อเลือก · Enter เพื่อเปิด</p>' +
      '</div>';
    document.body.appendChild(dlg);
    input = dlg.querySelector('input');
    list = dlg.querySelector('.searchbox-results');
    status = dlg.querySelector('.searchbox-status');
    dlg.addEventListener('click', function (e) { if (e.target.hasAttribute('data-close')) close(); });
    input.addEventListener('input', function () { render(input.value); });
    input.addEventListener('keydown', key);
  }

  function score(item, q) {
    var name = (item.name || '').toLowerCase();
    var en = (item.en || '').toLowerCase();
    var kw = (item.kw || '').toLowerCase();
    if (name.indexOf(q) === 0) return 0;
    if (name.indexOf(q) > -1) return 1;
    if (en.indexOf(q) > -1) return 2;
    if (kw.indexOf(q) > -1) return 3;
    return -1;
  }

  function render(raw) {
    var q = (raw || '').trim().toLowerCase();
    list.innerHTML = ''; rows = []; active = -1;
    if (!q) { status.textContent = 'พิมพ์เพื่อค้นหาจาก 89 รายการในเว็บนี้'; return; }
    var hits = [];
    (index || []).forEach(function (it) {
      var s = score(it, q);
      if (s > -1) hits.push([s, it]);
    });
    hits.sort(function (a, b) { return a[0] - b[0]; });
    hits = hits.slice(0, 12);
    if (!hits.length) { status.textContent = 'ไม่พบ "' + raw + '" ลองคำอื่นดู'; return; }
    status.textContent = 'พบ ' + hits.length + ' รายการ';
    hits.forEach(function (h, i) {
      var it = h[1];
      var li = document.createElement('li');
      li.setAttribute('role', 'option');
      li.innerHTML = '<a href="' + it.url + '"><span class="sr-name">' + it.name + '</span>' +
        '<span class="sr-kind">' + (LABEL[it.cat] || LABEL[it.t] || it.t) + '</span></a>';
      li.addEventListener('mouseenter', function () { setActive(i); });
      list.appendChild(li);
      rows.push(li);
    });
    setActive(0);
  }

  function setActive(i) {
    rows.forEach(function (r) { r.classList.remove('is-active'); r.setAttribute('aria-selected', 'false'); });
    active = i;
    if (rows[i]) { rows[i].classList.add('is-active'); rows[i].setAttribute('aria-selected', 'true'); }
  }

  function key(e) {
    if (e.key === 'Escape') { e.preventDefault(); close(); return; }
    if (e.key === 'ArrowDown') { e.preventDefault(); setActive(Math.min(active + 1, rows.length - 1)); }
    else if (e.key === 'ArrowUp') { e.preventDefault(); setActive(Math.max(active - 1, 0)); }
    else if (e.key === 'Enter' && rows[active]) { e.preventDefault(); rows[active].querySelector('a').click(); }
  }

  function open() {
    if (!dlg) build();
    lastFocus = document.activeElement;
    dlg.hidden = false;
    document.body.classList.add('searchbox-open');
    load().then(function () { render(input.value); });
    input.value = '';
    input.focus();
    render('');
  }

  function close() {
    if (!dlg) return;
    dlg.hidden = true;
    document.body.classList.remove('searchbox-open');
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }

  document.addEventListener('keydown', function (e) {
    var tag = (e.target.tagName || '').toLowerCase();
    var typing = tag === 'input' || tag === 'textarea' || e.target.isContentEditable;
    if ((e.key === 'k' || e.key === 'K') && (e.metaKey || e.ctrlKey)) { e.preventDefault(); open(); }
    else if (e.key === '/' && !typing && (!dlg || dlg.hidden)) { e.preventDefault(); open(); }
  });

  document.addEventListener('click', function (e) {
    var t = e.target.closest('[data-open-search]');
    if (t) { e.preventDefault(); open(); }
  });

  window.TakuaSearch = { open: open, close: close };
})();

/* Collapsed header menu on narrow screens. */
(function () {
  'use strict';
  var mq = window.matchMedia('(max-width: 900px)');
  var nav = document.getElementById('main-nav');
  var btn = document.querySelector('[data-nav-toggle]');
  if (!nav || !btn) return;
  function sync() {
    var open = btn.getAttribute('aria-expanded') === 'true';
    if (mq.matches) {
      // Phone: the whole menu is the drawer.
      nav.hidden = !open;
      nav.classList.remove('is-open');
    } else {
      // Desktop: six links stay in the bar and the drawer adds the rest.
      nav.hidden = false;
      nav.classList.toggle('is-open', open);
    }
  }

  document.addEventListener('click', function (e) {
    if (btn.getAttribute('aria-expanded') !== 'true') return;
    if (e.target.closest('#main-nav') || e.target.closest('[data-nav-toggle]')) return;
    btn.setAttribute('aria-expanded', 'false');
    sync();
  });
  btn.addEventListener('click', function () {
    btn.setAttribute('aria-expanded', btn.getAttribute('aria-expanded') === 'true' ? 'false' : 'true');
    sync();
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && mq.matches && btn.getAttribute('aria-expanded') === 'true') {
      btn.setAttribute('aria-expanded', 'false'); sync(); btn.focus();
    }
  });
  mq.addEventListener('change', sync);
  sync();
})();
