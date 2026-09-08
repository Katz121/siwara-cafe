"""ชุดตรวจถดถอย · รันหลังแก้ทุกครั้ง ต้องได้ ผ่าน ทุกข้อ

เขียนไว้เพราะรอบที่แล้วแก้หลายจุดพร้อมกัน แล้วการแก้จุดหนึ่งทำอีกจุดพัง
(ปุ่ม 44px ทำให้หน้าอังกฤษล้น · ย้ายฟอนต์ทำให้ make_og พัง)
"""
import asyncio
import collections
import functools
import glob
import http.server
import io
import json
import os
import re
import socketserver
import sys
import threading
from urllib.parse import unquote

sys.stdout.reconfigure(encoding='utf-8')
from playwright.async_api import async_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, 'site')
FAIL = []


def check(name, ok, detail=''):
    print(('  ผ่าน   ' if ok else '  ตก     ') + name + (('  · ' + detail) if detail else ''))
    if not ok:
        FAIL.append(name + (' · ' + detail if detail else ''))


def read(p):
    return io.open(p, encoding='utf-8').read()


pages = sorted(glob.glob(os.path.join(SITE, '**', 'index.html'), recursive=True))
en = [p for p in pages if os.path.relpath(p, SITE).replace(os.sep, '/').startswith('en/')]
th = [p for p in pages if p not in en]

print('\n== โครงสร้าง ==')
check('มี 88 หน้า', len(pages) == 88, str(len(pages)))
locs = re.findall(r'<loc>(.*?)</loc>', read(os.path.join(SITE, 'sitemap.xml')))
check('sitemap 88 URL ไม่ซ้ำ', len(locs) == 88 and len(set(locs)) == 88,
      '%d URL · ไม่ซ้ำ %d' % (len(locs), len(set(locs))))

print('\n== ข้อความ ==')
dashes = sum(len(re.findall(r'[—–]', read(p))) for p in pages)
check('ไม่มี em/en-dash', dashes == 0, '%d จุด' % dashes)

hype = collections.Counter()
for p in pages:
    body = read(p)
    for w in ('ดีที่สุด', 'ห้ามพลาด', 'สวยที่สุด', 'ที่เดียวในโลก'):
        hype[w] += body.count(w)
check('ไม่มีคำโฆษณาเกินจริง', sum(hype.values()) == 0,
      str({k: v for k, v in hype.items() if v}))

thai_attr = collections.Counter()
for p in en:
    for m in re.finditer(r'(alt|title|aria-label|placeholder)="([^"]*[฀-๿][^"]*)"', read(p)):
        thai_attr[m.group(2)] += 1
check('หน้าอังกฤษไม่มี attribute ภาษาไทย', not thai_attr, '%d ค่า' % len(thai_attr))

bad_quote = sum(len(re.findall(r'="[^"]*""[ >]', read(p))) for p in en)
check('ไม่มีเครื่องหมายคำพูดเกินใน attribute', bad_quote == 0, '%d จุด' % bad_quote)

moji = []
for f in (glob.glob(os.path.join(SITE, 'assets', '*.js'))
          + glob.glob(os.path.join(SITE, 'assets', '*.css'))
          + glob.glob(os.path.join(ROOT, '*.py'))
          + pages):
    body = read(f)
    if re.search(r'\?{3,}', body) or 'à¸' in body:
        moji.append(os.path.basename(f))
check('ไม่มี mojibake หรือ ??? ในไฟล์', not moji, ', '.join(moji[:4]))

print('\n== ลิงก์และแหล่งอ้างอิง ==')
dead = [d['url_prefix'] for d in json.load(
    io.open(os.path.join(ROOT, 'data', 'dead-sources.json'), encoding='utf-8'))]
dead_norm = [unquote(d).rstrip('/') for d in dead]
hits = 0
for p in pages:
    for m in re.finditer(r'href="([^"]+)"', read(p)):
        u = unquote(m.group(1)).rstrip('/')
        if any(u.startswith(d) for d in dead_norm):
            hits += 1
check('ไม่มีลิงก์ไปแหล่งที่ตายแล้ว', hits == 0, '%d เส้น' % hits)
check('ไม่มีโดเมนที่สะกดผิด takuacity',
      sum(read(p).count('takuacity.go.th') for p in pages) == 0)

print('\n== ไฟล์ที่อ้างถึง ==')
missing = set()
for p in pages:
    for m in re.finditer(r'(?:src|href)="(/assets/[^"?#]+)"', read(p)):
        if not os.path.exists(os.path.join(SITE, m.group(1).lstrip('/').replace('/', os.sep))):
            missing.add(m.group(1))
check('ทุก asset ที่อ้างถึงมีไฟล์จริง', not missing, str(sorted(missing)[:4]))
check('ไม่มี .ttf หลงใน site/',
      not glob.glob(os.path.join(SITE, '**', '*.ttf'), recursive=True))
# ไฟล์ที่หน้าเว็บโหลดเองต้องเบา · ไฟล์ที่มีแค่ลิงก์ให้ดาวน์โหลด (แผนที่ต้นฉบับ
# กับแผ่นพับ PDF) ใหญ่ได้ เพราะผู้ชมเลือกกดเอง
loaded = set()
for p in pages:
    for m in re.finditer(r'src="(/assets/[^"?#]+)"', read(p)):
        loaded.add(m.group(1))
big = [f for f in glob.glob(os.path.join(SITE, 'assets', '**', '*'), recursive=True)
       if os.path.isfile(f) and os.path.getsize(f) > 700_000
       and '/' + os.path.relpath(f, SITE).replace(os.sep, '/') in loaded]
check('ไม่มีไฟล์หนักเกิน 700KB ที่หน้าเว็บโหลดเอง', not big,
      ', '.join(os.path.basename(f) for f in big))

print('\n== หัวข้อ ==')
bad_h = []
for p in pages:
    body = read(p).split('<main', 1)[-1].split('</main>', 1)[0]
    lv = [int(x) for x in re.findall(r'<h([1-6])[\s>]', body)]
    if lv.count(1) != 1 or any(b > a + 1 for a, b in zip(lv, lv[1:])):
        bad_h.append(os.path.relpath(p, SITE))
check('ลำดับหัวข้อถูกทุกหน้า', not bad_h, ', '.join(bad_h[:3]))

print('\n== SEO ==')
for label, group in (('ไทย', th), ('อังกฤษ', en)):
    no_canon = [p for p in group if 'rel="canonical"' not in read(p)]
    # นับเฉพาะ <link rel=alternate> · ปุ่มสลับภาษาก็มี hreflang เหมือนกัน
    no_hl = [p for p in group
             if len(re.findall(r'<link[^>]*hreflang=', read(p))) != 3]
    check('%s · canonical ครบ' % label, not no_canon, '%d หน้า' % len(no_canon))
    check('%s · hreflang 3 อันทุกหน้า' % label, not no_hl, '%d หน้า' % len(no_hl))

titles = collections.Counter()
for p in pages:
    m = re.search(r'<title>(.*?)</title>', read(p), re.S)
    titles[m.group(1) if m else ''] += 1
dups = [k for k, v in titles.items() if v > 1]
check('title ไม่ซ้ำกัน', not dups, str(dups[:2]))
long_t = [t for t in titles if len(t) > 60]
check('title ไม่เกิน 60 ตัวอักษร', not long_t,
      '%d หน้า · ยาวสุด %d' % (len(long_t), max((len(t) for t in titles), default=0)))

print('\n== ตัวเลขต้องตรงกันทั้งเว็บ ==')
home = read(os.path.join(SITE, 'index.html'))
shop_nums = set(re.findall(r'(\d+) ร้าน(?!จาก)', home))
check('ตัวเลขร้านบนหน้าแรกตรงกัน', shop_nums <= {'108'}, str(sorted(shop_nums)))
cats = [int(x) for x in re.findall(r'<b>(\d+)</b>[฀-๿]', home)]
check('ผลรวมรายหมวดเท่ายอดรวม', sum(cats) == 108, '%s = %d' % (cats, sum(cats)))

print('\n== เบราว์เซอร์ ==')
H = functools.partial(http.server.SimpleHTTPRequestHandler, directory=SITE)


class Quiet(socketserver.TCPServer):
    allow_reuse_address = True


srv = Quiet(("127.0.0.1", 8797), H)
threading.Thread(target=srv.serve_forever, daemon=True).start()
BASE = "http://127.0.0.1:8797"
ROUTES = ["/", "/places/", "/places/tao-ming/", "/stories/city/", "/map/", "/eat/",
          "/rest/", "/news/", "/trip/", "/en/", "/en/eat/", "/en/places/tao-ming/"]


async def browse():
    errs, bad_req, over = [], [], []
    async with async_playwright() as pw:
        br = await pw.chromium.launch()
        for w in (390, 1440):
            pg = await br.new_page(viewport={"width": w, "height": 900})
            pg.on("console", lambda m: errs.append(m.text[:70]) if m.type == "error" else None)
            pg.on("response", lambda r: bad_req.append(
                str(r.status) + " " + r.url.split("8797")[-1]) if r.status >= 400 else None)
            for r in ROUTES:
                await pg.goto(BASE + r + "index.html", wait_until="networkidle")
                o = await pg.evaluate(
                    "()=>document.documentElement.scrollWidth-document.documentElement.clientWidth")
                if o > 0:
                    over.append("%s@%d %dpx" % (r, w, o))
            await pg.close()

        pg = await br.new_page(viewport={"width": 390, "height": 900})
        await pg.goto(BASE + "/places/tao-ming/index.html", wait_until="networkidle")
        n0 = await pg.evaluate("()=>window.TakuaTrip.count()")
        await pg.click("[data-trip-add]")
        n1 = await pg.evaluate("()=>window.TakuaTrip.count()")
        await pg.goto(BASE + "/trip/index.html", wait_until="networkidle")
        n2 = await pg.evaluate("()=>window.TakuaTrip.count()")

        await pg.goto(BASE + "/index.html", wait_until="networkidle")
        await pg.click("[data-theme-toggle]")
        t1 = await pg.evaluate("()=>document.documentElement.dataset.theme")
        await pg.goto(BASE + "/places/index.html", wait_until="networkidle")
        t2 = await pg.evaluate("()=>document.documentElement.dataset.theme")

        await pg.goto(BASE + "/en/eat/index.html", wait_until="networkidle")
        await pg.fill("#shop-search", "Coffee")
        await pg.wait_for_timeout(300)
        found = await pg.eval_on_selector_all(
            "[data-shop]", "e=>e.filter(x=>x.offsetParent!==null).length")

        small = await pg.evaluate(
            "()=>[...document.querySelectorAll('button,select,input')]"
            ".filter(e=>{const r=e.getBoundingClientRect();"
            "return r.width>0&&r.height>0&&(r.width<44||r.height<44)}).length")
        await br.close()
    return errs, bad_req, over, (n0, n1, n2), (t1, t2), found, small


errs, bad_req, over, trip, theme, found, small = asyncio.run(browse())
srv.shutdown()
check('ไม่มี console error', not errs, ' | '.join(sorted(set(errs))[:2]))
check('ไม่มี request 4xx/5xx', not bad_req, ' | '.join(sorted(set(bad_req))[:3]))
check('ไม่ล้นแนวนอนทั้ง 390 และ 1440', not over, ' | '.join(over[:3]))
check('ตะกร้าทริปเพิ่มได้และจำค่าข้ามหน้า', trip == (0, 1, 1), str(trip))
check('โหมดกลางคืนจำค่าข้ามหน้า', theme == ('dark', 'dark'), str(theme))
check('ค้นร้านด้วยคำอังกฤษเจอ', found > 0, 'Coffee -> %s' % found)
check('ปุ่มบนมือถือไม่เล็กกว่า 44px', small == 0, '%s ปุ่ม' % small)

print('')
print('เจอปัญหา %d ข้อ' % len(FAIL) if FAIL else 'ผ่านทุกข้อ')
for f in FAIL:
    print('  -', f)
sys.exit(1 if FAIL else 0)
