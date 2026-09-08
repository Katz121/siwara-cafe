"""Print every built page, grouped, with its title."""
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(ROOT, 'site')

GROUPS = {
    'places': 'สถานที่',
    'traditions': 'ประเพณี',
    'stories': 'เรื่องเล่า',
    'map': 'แผนที่ เส้นทาง ทริป',
    'routes': 'แผนที่ เส้นทาง ทริป',
    'trip': 'แผนที่ เส้นทาง ทริป',
    'eat': 'กิน ดื่ม ของฝาก',
    'rest': 'กิน ดื่ม ของฝาก',
    'news': 'ข่าวสารของเมือง',
    'leaflet': 'แผ่นพับ',
    'about': 'เกี่ยวกับ',
}
ORDER = ['หน้าแรก', 'สถานที่', 'ประเพณี', 'เรื่องเล่า', 'แผนที่ เส้นทาง ทริป',
         'กิน ดื่ม ของฝาก', 'ข่าวสารของเมือง', 'แผ่นพับ', 'เกี่ยวกับ']


def title_of(fp):
    html = open(fp, encoding='utf-8').read()
    m = re.search(r'<title>(.*?)</title>', html, re.S)
    if not m:
        return '?'
    return re.sub(r'\s*·\s*(ตะกั่วป่า 101|Takua Pa 101)\s*$', '', m.group(1)).strip()


def main():
    thai, english = [], []
    for dirpath, dirnames, files in os.walk(SITE):
        dirnames[:] = [d for d in dirnames if d != 'assets']
        if 'index.html' not in files:
            continue
        rel = os.path.relpath(dirpath, SITE).replace(os.sep, '/')
        route = '/' if rel == '.' else '/' + rel + '/'
        row = (route, title_of(os.path.join(dirpath, 'index.html')))
        (english if route.startswith('/en') else thai).append(row)

    buckets = {}
    for route, name in sorted(thai):
        key = 'หน้าแรก' if route == '/' else GROUPS.get(route.strip('/').split('/')[0], 'อื่น ๆ')
        buckets.setdefault(key, []).append((route, name))

    print(f'ภาษาไทย {len(thai)} หน้า · ภาษาอังกฤษ {len(english)} หน้า · รวม {len(thai) + len(english)}\n')
    for key in ORDER + [k for k in buckets if k not in ORDER]:
        rows = buckets.get(key)
        if not rows:
            continue
        print(f'{key} · {len(rows)} หน้า')
        for route, name in rows:
            print(f'   {route:32} {name[:56]}')
        print()


if __name__ == '__main__':
    main()
