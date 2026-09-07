"""Produce the English site under /en/ from the built Thai pages.

Rewriting build_site.py to emit two languages would risk the Thai site on every
change. This runs after it instead: it reads what was built, swaps Thai strings
for their approved English counterparts, repoints internal links, and writes a
parallel tree. The Thai pages are only touched to add hreflang.
"""
import glob
import json
import os
import re
import sys
from datetime import date
from html import escape as esc

sys.stdout.reconfigure(encoding='utf-8')

from seo_config import SITE_BASE_URL, BASE_PATH

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(ROOT, 'site')
EN = os.path.join(SITE, 'en')
DATA = os.path.join(ROOT, 'data')
I18N = os.path.join(DATA, 'i18n', 'en')
BASE = SITE_BASE_URL.rstrip('/')
PREFIX = (BASE_PATH or '') + '/en'


def load(rel, default=None):
    fp = os.path.join(ROOT, rel)
    if not os.path.exists(fp):
        return default if default is not None else {}
    try:
        return json.load(open(fp, encoding='utf-8'))
    except Exception as e:
        print(f'  อ่าน {rel} ไม่ได้: {e}')
        return default if default is not None else {}


def build_memory():
    """Thai string -> English string, from every approved translation file."""
    mem = {}

    def add(th, en):
        if not isinstance(th, str) or not isinstance(en, str):
            return
        th, en = th.strip(), en.strip()
        if len(th) < 2 or not en or th == en:
            return
        if not re.search(r'[฀-๿]', th):
            return                       # nothing Thai to replace
        if th.startswith('http') or th.startswith('/'):
            return
        mem.setdefault(th, en)

    for k, v in load('data/i18n/en/ui.json').items():
        add(k, v)
    for k, v in load('data/i18n/en/publishers.json').items():
        add(k, f'{k} ({v})')

    places_th = {r['id']: r for r in load('data/places-enriched.json', [])}
    for pid, en in load('data/i18n/en/places.json').items():
        th = places_th.get(pid)
        if not th:
            continue
        add(th.get('name_th'), en.get('name'))
        add(th.get('editorial_angle'), en.get('lead'))
        for era in ('then', 'before', 'now'):
            t_era = (th.get('eras') or {}).get(era) or {}
            e_era = (en.get('eras') or {}).get(era) or {}
            add(t_era.get('headline_th'), e_era.get('headline'))
            add(t_era.get('body_th'), e_era.get('body'))
        for t_h, e_h in zip(th.get('highlights') or [], en.get('highlights') or []):
            add(t_h.get('title_th'), e_h.get('title'))
            add(t_h.get('detail_th'), e_h.get('detail'))
        for t_g, e_g in zip(th.get('getting_there') or [], en.get('getting_there') or []):
            add(t_g.get('text_th'), e_g.get('text'))
        for t_d, e_d in zip(th.get('did_you_know') or [], en.get('did_you_know') or []):
            add(t_d.get('fact_th') if isinstance(t_d, dict) else t_d,
                e_d.get('fact') if isinstance(e_d, dict) else e_d)
        for t_u, e_u in zip(th.get('unknowns') or [], en.get('unknowns') or []):
            add(t_u, e_u)

    for fp in sorted(os.listdir(os.path.join(DATA, 'stories'))) if os.path.isdir(os.path.join(DATA, 'stories')) else []:
        if not fp.endswith('.json'):
            continue
        sid = fp[:-5]
        th = load(f'data/stories/{fp}')
        en = load(f'data/i18n/en/stories/{fp}')
        if not en:
            continue
        add(th.get('title'), en.get('title'))
        add(th.get('dek'), en.get('dek'))
        for a, b in zip(th.get('lede') or [], en.get('lede') or []):
            add(a, b)
        for s_th, s_en in zip(th.get('sections') or [], en.get('sections') or []):
            add(s_th.get('heading_th'), s_en.get('heading') or s_en.get('heading_th'))
            for a, b in zip(s_th.get('paragraphs') or [], s_en.get('paragraphs') or []):
                add(a, b)
            for f_th, f_en in zip(s_th.get('flags') or [], s_en.get('flags') or []):
                add(f_th.get('text_th'), f_en.get('text') or f_en.get('text_th'))
        for a, b in zip(th.get('pull_quotes') or [], en.get('pull_quotes') or []):
            add(a, b)
        eb_th, eb_en = th.get('evidence_box') or {}, en.get('evidence_box') or {}
        add(eb_th.get('heading_th'), eb_en.get('heading') or eb_en.get('heading_th'))
        for i_th, i_en in zip(eb_th.get('items') or [], eb_en.get('items') or []):
            add(i_th.get('claim_th'), i_en.get('claim') or i_en.get('claim_th'))
            add(i_th.get('explain_th'), i_en.get('explain') or i_en.get('explain_th'))
        for a, b in zip(th.get('unknowns') or [], en.get('unknowns') or []):
            add(a, b)

    shops_th = {r['id']: r for r in load('data/shops-extra.json', [])}
    for sid, en in load('data/i18n/en/shops.json').items():
        th = shops_th.get(sid)
        if not th:
            continue
        add(th.get('name_th'), en.get('name'))
        add(th.get('one_liner_th'), en.get('one_liner'))

    # Detail fields translated in a later pass: history, timeline, news, visit.
    for fp in sorted(glob.glob(os.path.join(I18N, 'details', '*.json'))):
        try:
            part = json.load(open(fp, encoding='utf-8'))
        except Exception:
            continue
        for pid, en in part.items():
            th = places_th.get(pid)
            if not th:
                continue
            for t_h, e_h in zip(th.get('history') or [], en.get('history') or []):
                add(t_h.get('claim_th'), e_h.get('claim'))
                add(t_h.get('quote'), e_h.get('quote'))
            for t_t, e_t in zip(th.get('timeline') or [], en.get('timeline') or []):
                add(t_t.get('title_th'), e_t.get('title'))
                add(t_t.get('detail_th'), e_t.get('detail'))
            for t_n, e_n in zip(th.get('news') or [], en.get('news') or []):
                add(t_n.get('title_th'), e_n.get('title'))
                add(t_n.get('summary_th'), e_n.get('summary'))
            for t_nb, e_nb in zip(th.get('nearby') or [], en.get('nearby') or []):
                add(t_nb.get('name_th'), e_nb.get('name'))
            v_th, v_en = th.get('visit') or {}, en.get('visit') or {}
            for k_th, k_en in (('best_time_th', 'best_time'), ('parking_th', 'parking'),
                               ('wheelchair_th', 'wheelchair'), ('dress_code_th', 'dress_code'),
                               ('opening_hours_th', 'opening_hours'), ('admission_fee_th', 'admission_fee')):
                add(v_th.get(k_th), v_en.get(k_en))
            add((th.get('address') or {}).get('line_th'), en.get('address_line'))

    # Everything the previous run could not match, translated separately.
    for fp in sorted(glob.glob(os.path.join(I18N, 'missing-parts', '*.json'))):
        try:
            for k, v in json.load(open(fp, encoding='utf-8')).items():
                add(k, v)
        except Exception:
            continue

    for ph in (load('data/photo-registry.json').get('photos') or []):
        add(ph.get('caption_th'), ph.get('caption_en'))
        add(ph.get('credit'), ph.get('credit_en'))
        add(ph.get('license'), ph.get('license_en'))

    return mem


SCRIPT_RE = re.compile(r'(<script[^>]*>.*?</script>)', re.S | re.I)
TAG_RE = re.compile(r'(<[^>]+>)')
TRANSLATABLE_ATTRS = ('alt', 'title', 'aria-label', 'placeholder', 'content')


def translate_html(html, mem, missing=None):
    """Translate whole text nodes only.

    Substring replacement produced wreckage like "อ่านแหล่งReferences" because a
    short key matched inside a longer Thai phrase. A text node is either
    translated in full or left as it is and recorded as missing.
    """
    out = []
    for block in SCRIPT_RE.split(html):
        if block.lower().startswith('<script'):
            out.append(block)
            continue
        pieces = TAG_RE.split(block)
        for i, piece in enumerate(pieces):
            if piece.startswith('<'):
                pieces[i] = translate_attrs(piece, mem, missing)
                continue
            stripped = piece.strip()
            if not stripped or not re.search(r'[฀-๿]', stripped):
                continue
            hit = mem.get(stripped)
            if hit:
                pieces[i] = piece.replace(stripped, hit)
            elif missing is not None:
                missing[stripped] = missing.get(stripped, 0) + 1
        out.append(''.join(pieces))
    return ''.join(out)


def translate_attrs(tag, mem, missing=None):
    """Same whole-value rule for the handful of attributes a reader sees."""
    def sub(m):
        name, quote, val = m.group(1), m.group(2), m.group(3)
        if name.lower() not in TRANSLATABLE_ATTRS or not re.search(r'[฀-๿]', val):
            return m.group(0)
        hit = mem.get(val.strip())
        if hit:
            return f'{name}={quote}{esc(hit, quote=True)}{quote}'
        if missing is not None:
            missing[val.strip()] = missing.get(val.strip(), 0) + 1
        return m.group(0)

    return re.sub(r'([\w:-]+)=(["\'])([^"\']*)', sub, tag)


def repoint_links(html):
    """Internal links inside the English tree point at English pages."""
    base = BASE_PATH or ''

    def sub(m):
        attr, quote, url = m.group(1), m.group(2), m.group(3)
        if url.startswith(('http', '//', '#', 'mailto:', 'tel:')):
            return m.group(0)
        if base and not url.startswith(base + '/') and url != base:
            return m.group(0)
        rest = url[len(base):] if base else url
        if rest.startswith('/assets/') or rest.startswith('/en/'):
            return m.group(0)
        return f'{attr}={quote}{base}/en{rest}{quote}'

    return re.sub(r'\b(href|action)=(["\'])([^"\']+)\2', sub, html)


def main():
    mem = build_memory()
    print(f'คำแปลในหน่วยความจำ {len(mem)} รายการ')
    missing = {}

    pages = []
    for dirpath, dirnames, filenames in os.walk(SITE):
        dirnames[:] = [d for d in dirnames if d not in ('assets', 'en')]
        if 'index.html' not in filenames:
            continue
        rel = os.path.relpath(dirpath, SITE).replace('\\', '/')
        route = '/' if rel == '.' else '/' + rel + '/'
        pages.append((route, os.path.join(dirpath, 'index.html')))

    made = skipped = 0
    for route, src in sorted(pages):
        html = open(src, encoding='utf-8').read()
        out = translate_html(html, mem, missing)
        left = len(re.findall(r'[฀-๿]', re.sub(SCRIPT_RE, '', re.sub(r'<[^>]+>', ' ', out))))
        before = len(re.findall(r'[฀-๿]', re.sub(SCRIPT_RE, '', re.sub(r'<[^>]+>', ' ', html))))
        # A page that barely changed has no real translation behind it.
        if before and left / before > 0.55:
            skipped += 1
            print(f'  ข้าม {route} · แปลได้ {100 - int(left / before * 100)}%')
            continue

        out = repoint_links(out)
        out = out.replace('<html lang="th"', '<html lang="en"', 1)
        out = out.replace('"og:locale":"th_TH"', '"og:locale":"en_US"')
        out = out.replace('og:locale" content="th_TH"', 'og:locale" content="en_US"')
        en_url = BASE + PREFIX + ('' if route == '/' else route)
        th_url = BASE + (BASE_PATH or '') + ('' if route == '/' else route)
        out = re.sub(r'<link rel="canonical" href="[^"]*"', f'<link rel="canonical" href="{esc(en_url)}"', out, count=1)
        alts = (f'<link rel="alternate" hreflang="th" href="{esc(th_url)}">'
                f'<link rel="alternate" hreflang="en" href="{esc(en_url)}">'
                f'<link rel="alternate" hreflang="x-default" href="{esc(th_url)}">')
        out = out.replace('</head>', alts + '</head>', 1)
        out = out.replace('"@context": "https://schema.org"', '"@context": "https://schema.org", "inLanguage": "en"')
        switch = f'<a class="lang-switch" href="{esc((BASE_PATH or "") + ("/" if route == "/" else route))}" hreflang="th" lang="th">ไทย</a>'
        out = out.replace('<div class="header-tools">', '<div class="header-tools">' + switch, 1)

        dest = os.path.join(EN, '' if route == '/' else route.strip('/'), 'index.html')
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        open(dest, 'w', encoding='utf-8').write(out)
        made += 1

        # The Thai page gains the same alternates plus a link to its English twin.
        th_html = html
        if 'hreflang="en"' not in th_html:
            th_html = th_html.replace('</head>', alts + '</head>', 1)
            en_switch = f'<a class="lang-switch" href="{esc(PREFIX + ("" if route == "/" else route))}" hreflang="en" lang="en">EN</a>'
            th_html = th_html.replace('<div class="header-tools">', '<div class="header-tools">' + en_switch, 1)
            open(src, 'w', encoding='utf-8').write(th_html)

    sm = os.path.join(SITE, 'sitemap.xml')
    if os.path.exists(sm) and made:
        xml = open(sm, encoding='utf-8').read()
        extra = ''.join(
            f'<url><loc>{esc(BASE + PREFIX + ("" if r == "/" else r))}</loc>'
            f'<lastmod>{date.today().isoformat()}</lastmod></url>'
            for r, _ in sorted(pages)
            if os.path.exists(os.path.join(EN, '' if r == '/' else r.strip('/'), 'index.html')))
        if '/en/' not in xml:
            open(sm, 'w', encoding='utf-8').write(xml.replace('</urlset>', extra + '</urlset>'))

    if missing:
        with open(os.path.join(I18N, 'missing.json'), 'w', encoding='utf-8') as f:
            json.dump(dict(sorted(missing.items(), key=lambda kv: -kv[1])), f, ensure_ascii=False, indent=1)
    print(f'สร้างหน้าอังกฤษ {made} หน้า · ข้าม {skipped} หน้า (คำแปลไม่พอ)')
    print(f'ข้อความที่ยังไม่มีคำแปล {len(missing)} แบบ · เขียนไว้ที่ data/i18n/en/missing.json')


if __name__ == '__main__':
    main()
