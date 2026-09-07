"""Fold newly researched shops into the directory the site renders.

The municipal brochure list stays exactly as it is. Researched shops are kept in
a separate file with their sources attached, so a reader can always tell which
list an entry came from.
"""
import glob
import json
import os
import re
import sys
import unicodedata

sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.abspath(__file__))
RESEARCH = os.path.join(ROOT, 'research', '2026-09-07-shops', 'out')
OUT = os.path.join(ROOT, 'data', 'shops-extra.json')

# The site renders three columns; researched entries carry finer categories.
CATEGORY_MAP = {
    'restaurant': 'restaurant',
    'food': 'restaurant',
    'drink_shop': 'drink_shop',
    'cafe': 'drink_shop',
    'coffee': 'drink_shop',
    'dessert': 'drink_shop',
    'bakery': 'drink_shop',
    'souvenir_shop': 'souvenir_shop',
    'souvenir': 'souvenir_shop',
    'shop': 'souvenir_shop',
}

MANUAL = [
    {'id': 'siwara-cafe', 'name_th': 'ศิวรา คาเฟ่', 'name_en': 'Siwara Cafe',
     'category': 'drink_shop', 'website': 'https://siwaracafe.com/',
     'one_liner_th': 'คาเฟ่ในตะกั่วป่า ผู้จัดทำคู่มือเมืองเล่มนี้', 'provenance': 'first-party'},
    {'id': 'baan-bai', 'name_th': 'บ้านใบ', 'name_en': None,
     'category': 'drink_shop', 'one_liner_th': None, 'provenance': 'owner-added'},
]


def norm(name):
    """Loose key for duplicate detection across spelling and spacing."""
    s = unicodedata.normalize('NFKC', str(name or '')).lower()
    s = re.sub(r'\b(ร้าน|คาเฟ่|cafe|restaurant|the|บาย|by)\b', ' ', s)
    return re.sub(r'[^0-9a-zก-๙]', '', s)


def slug(name, taken):
    base = re.sub(r'[^0-9a-z]+', '-', unicodedata.normalize('NFKD', str(name)).encode('ascii', 'ignore').decode().lower()).strip('-')
    if not base:
        base = 'shop'
    candidate, n = base, 2
    while candidate in taken:
        candidate, n = f'{base}-{n}', n + 1
    taken.add(candidate)
    return candidate


def load_existing():
    lib = json.load(open(os.path.join(ROOT, 'data', 'library.json'), encoding='utf-8'))['records']
    return [r for r in lib if r.get('category') in CATEGORY_MAP.values()]


def main():
    existing = load_existing()
    seen = {norm(r['name_th']) for r in existing}
    for m in MANUAL:
        seen.discard(norm(m['name_th']))  # manual entries are intentionally kept

    taken = {r['id'] for r in existing}
    out, dupes, rejected = [], [], []

    for m in MANUAL:
        taken.add(m['id'])
        out.append({**m, 'sources': [], 'status': 'open'})
        seen.add(norm(m['name_th']))

    for fp in sorted(glob.glob(os.path.join(RESEARCH, '*.json'))):
        batch = os.path.splitext(os.path.basename(fp))[0]
        try:
            rows = json.load(open(fp, encoding='utf-8'))
        except Exception as e:
            print(f'ข้าม {batch}: {e}')
            continue
        for r in rows if isinstance(rows, list) else []:
            name = (r.get('name_th') or '').strip()
            if not name:
                continue
            key = norm(name)
            if key in seen:
                dupes.append(name)
                continue
            if not (r.get('sources') or []):
                rejected.append((name, 'ไม่มีแหล่งอ้างอิง'))
                continue
            if r.get('status') == 'closed':
                rejected.append((name, 'ปิดกิจการ'))
                continue
            cat = CATEGORY_MAP.get(r.get('category'), None)
            if cat is None:
                rejected.append((name, f"หมวดไม่รู้จัก: {r.get('category')}"))
                continue
            seen.add(key)
            geo = r.get('geo') or {}
            out.append({
                'id': slug(r.get('name_en') or name, taken),
                'name_th': name,
                'name_en': r.get('name_en'),
                'category': cat,
                'sub_category': r.get('category'),
                'one_liner_th': r.get('one_liner_th'),
                'signature_th': r.get('signature_th') or [],
                'address_th': r.get('address_th'),
                'subdistrict': r.get('subdistrict'),
                'geo': {'lat': geo.get('lat'), 'lng': geo.get('lng')} if geo.get('lat') else None,
                'hours_th': r.get('hours_th'),
                'price_range_th': r.get('price_range_th'),
                'phone': r.get('phone'),
                'facebook': r.get('facebook'),
                'google_maps_url': r.get('google_maps_url'),
                'near_old_town': bool(r.get('near_old_town')),
                'status': r.get('status') or 'uncertain',
                'unknowns': r.get('unknowns') or [],
                'sources': r.get('sources') or [],
                'provenance': 'researched',
                'batch': batch,
            })

    json.dump(out, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

    by_cat = {}
    for r in out:
        by_cat[r['category']] = by_cat.get(r['category'], 0) + 1
    print(f'เขียน {OUT}')
    print(f'  ร้านที่เพิ่ม {len(out)} · {by_cat}')
    print(f'  มีพิกัด {sum(1 for r in out if r.get("geo"))} · มีเวลาเปิด {sum(1 for r in out if r.get("hours_th"))}')
    print(f'  ซ้ำกับของเดิม ตัดออก {len(dupes)}')
    if rejected:
        print('  ไม่รับ:')
        for n, why in rejected:
            print(f'    {n} · {why}')


if __name__ == '__main__':
    main()
