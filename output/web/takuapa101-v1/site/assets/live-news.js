/* Tops up the baked-in news list with items the Worker has harvested and
   re-checked. The server-rendered list is the floor: if the Worker is down,
   unreachable, or returns nothing, the page keeps exactly what it shipped with. */
(function () {
  'use strict';
  var BASE = document.documentElement.dataset.base || '';
  var API = document.documentElement.dataset.newsApi || '';
  if (!API) return;

  var MONTHS = ['ม.ค.', 'ก.พ.', 'มี.ค.', 'เม.ย.', 'พ.ค.', 'มิ.ย.', 'ก.ค.', 'ส.ค.', 'ก.ย.', 'ต.ค.', 'พ.ย.', 'ธ.ค.'];

  function thaiDate(iso) {
    if (!iso) return '';
    var p = String(iso).split('-');
    if (p.length < 3) return iso;
    return Number(p[2]) + ' ' + MONTHS[Number(p[1]) - 1] + ' ' + (Number(p[0]) + 543);
  }

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  // Feed items are harvested from third parties, so a link is only rendered when
  // it is an ordinary web URL. Escaping alone would still allow javascript: hrefs.
  function safeUrl(u) {
    try {
      var parsed = new URL(String(u), window.location.href);
      return (parsed.protocol === 'http:' || parsed.protocol === 'https:') ? parsed.href : '';
    } catch (e) {
      return '';
    }
  }

  // Place ids come from a fixed vocabulary; anything else is not a real place.
  function safeId(id) {
    return /^[a-z0-9-]{1,40}$/.test(String(id || '')) ? String(id) : '';
  }

  function row(n, placeName) {
    var pid = safeId(n.place_id);
    var place = pid && placeName
      ? '<a href="' + BASE + '/places/' + esc(pid) + '/">' + esc(placeName) + '</a>'
      : '';
    var outlet = n.outlet ? (place ? ' · ' : '') + esc(n.outlet) : '';
    var href = safeUrl(n.url);
    var link = href
      ? '<a class="news-out" href="' + esc(href) + '" target="_blank" rel="noopener noreferrer">อ่านข่าวต้นทาง ↗</a>'
      : '';
    return '<li class="news-row is-auto">' +
      '<span class="news-date">' + esc(thaiDate(n.date)) + '</span>' +
      '<span class="news-main"><b>' + esc(n.title_th) + '</b>' +
      (n.summary_th ? '<span class="news-sum">' + esc(n.summary_th) + '</span>' : '') +
      '<span class="news-meta">' + place + outlet + '</span>' + link +
      '<span class="news-auto-tag" title="ดึงอัตโนมัติและผ่านการตรวจซ้ำด้วย AI แล้ว ยังไม่ผ่านการอ่านโดยคน">ดึงอัตโนมัติ</span>' +
      '</span></li>';
  }

  function existingTitles(list) {
    var out = {};
    Array.prototype.forEach.call(list.querySelectorAll('.news-row b'), function (b) {
      out[b.textContent.trim()] = true;
    });
    return out;
  }

  function apply(data, names) {
    var lists = document.querySelectorAll('[data-news-list]');
    if (!lists.length || !data.items || !data.items.length) return;
    Array.prototype.forEach.call(lists, function (list) {
      var max = Number(list.getAttribute('data-news-max') || 8);
      var have = existingTitles(list);
      var html = '';
      var added = 0;
      data.items.forEach(function (n) {
        if (added >= max || have[String(n.title_th).trim()]) return;
        html += row(n, names[n.place_id]);
        added += 1;
      });
      if (!html) return;
      list.insertAdjacentHTML('afterbegin', html);
      // Keep the list from growing without bound on the homepage.
      var rows = list.querySelectorAll('.news-row');
      var keep = Number(list.getAttribute('data-news-keep') || 0);
      if (keep) {
        for (var i = keep; i < rows.length; i += 1) rows[i].remove();
      }
    });
    var stamp = document.querySelector('[data-news-updated]');
    if (stamp && data.updated) {
      stamp.textContent = 'อัปเดตอัตโนมัติล่าสุด ' + thaiDate(String(data.updated).slice(0, 10));
      stamp.hidden = false;
    }
  }

  function start() {
    var names = {};
    fetch(BASE + '/assets/search-index.json')
      .then(function (r) { return r.json(); })
      .then(function (idx) {
        idx.forEach(function (i) { names[i.id] = i.name; });
      })
      .catch(function () { /* names are optional */ })
      .then(function () {
        return fetch(API.replace(/\/$/, '') + '/api/news?limit=20', { mode: 'cors' });
      })
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (d) { if (d) apply(d, names); })
      .catch(function () { /* the page already shows the shipped list */ });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start);
  else start();
})();
