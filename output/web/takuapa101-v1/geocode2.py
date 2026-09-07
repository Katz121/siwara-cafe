"""Second geocoding pass: per-name Nominatim lookups with a token-overlap check.

Overpass only covers what someone has mapped in OSM, which in Takua Pa skews to
Khao Lak's English-named tourist restaurants. This pass asks Nominatim directly
for each remaining name and accepts a hit only when the returned name genuinely
overlaps ours and sits inside the district.
"""
import json
import os
import re
import sys
import time
import unicodedata
import urllib.parse
import urllib.request

sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.abspath(__file__))
UA = 'takuapa101-site/1.0 (https://takuapa101.com; contact siwaracafe.com)'
BOX_LAT = (8.55, 9.20)
BOX_LNG = (98.10, 98.60)
CACHE_FP = os.path.join(ROOT, 'data', 'geocode-cache.json')
CACHE = json.load(open(CACHE_FP, encoding='utf-8')) if os.path.exists(CACHE_FP) else {}

STOP = ('ร้าน', 'คาเฟ่', 'cafe', 'restaurant', 'the', 'บาย', 'by', 'coffee', 'shop',
        'ตะกั่วป่า', 'พังงา', 'สาขา', 'and', 'แอนด์')


def tokens(s):
    s = unicodedata.normalize('NFKC', str(s or '')).lower()
    s = re.sub(r'[^0-9a-zก-๙\s]', ' ', s)
    out = []
    for t in s.split():
        if t in STOP or len(t) < 2:
            continue
        out.append(t)
    return out


def overlap(a, b):
    ta, tb = set(tokens(a)), set(tokens(b))
    if not ta or not tb:
        return 0.0
    inter = 0
    for x in ta:
        if any(x == y or (len(x) >= 4 and (x in y or y in x)) for y in tb):
            inter += 1
    return inter / min(len(ta), len(tb))


def search(q):
    key = 'n2:' + q
    if key in CACHE:
        return CACHE[key]
    url = ('https://nominatim.openstreetmap.org/search?format=jsonv2&limit=8&addressdetails=1'
           '&viewbox=98.10,9.20,98.60,8.55&bounded=1&q=' + urllib.parse.quote(q))
    try:
        req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept-Language': 'th,en'})
        with urllib.request.urlopen(req, timeout=40) as r:
            data = json.loads(r.read().decode('utf-8'))
    except Exception as e:
        print(f'    ! {e}')
        data = []
    time.sleep(1.1)
    CACHE[key] = data
    return data


def best(name, queries, threshold=0.6):
    for q in queries:
        for r in search(q):
            lat, lng = float(r['lat']), float(r['lon'])
            if not (BOX_LAT[0] <= lat <= BOX_LAT[1] and BOX_LNG[0] <= lng <= BOX_LNG[1]):
                continue
            cand = r.get('name') or r.get('display_name', '').split(',')[0]
            score = overlap(name, cand)
            if score >= threshold:
                return {'lat': lat, 'lng': lng, 'matched': cand, 'score': round(score, 2),
                        'source_url': f"https://www.openstreetmap.org/{r.get('osm_type')}/{r.get('osm_id')}"}
    return None


def main():
    added_p = added_s = 0

    ep = os.path.join(ROOT, 'data', 'places-enriched.json')
    places = json.load(open(ep, encoding='utf-8'))
    for r in places:
        if r.get('geo') or r.get('category') == 'tradition':
            continue
        n = r['name_th']
        alt = re.sub(r'\s*\(.*?\)', '', n).strip()
        hit = best(n, [n, alt, f'{alt} ตะกั่วป่า', f'{alt} พังงา'], threshold=0.5)
        if hit:
            r['geo'] = {'lat': hit['lat'], 'lng': hit['lng'], 'confidence': 'medium',
                        'source_name': 'OpenStreetMap', 'source_url': hit['source_url']}
            added_p += 1
            print(f"  + {n[:32]} -> {hit['matched'][:28]} ({hit['score']})")
        else:
            print(f"  - {n[:32]} ยังหาไม่เจอ")
    json.dump(places, open(ep, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

    sp = os.path.join(ROOT, 'data', 'shops-extra.json')
    shops = json.load(open(sp, encoding='utf-8'))
    todo = [r for r in shops if not r.get('geo')]
    print(f'\nร้านที่ยังไม่มีพิกัด {len(todo)} ร้าน')
    for r in todo:
        n = r['name_th']
        qs = [n, f'{n} ตะกั่วป่า']
        if r.get('name_en'):
            qs.append(r['name_en'])
        hit = best(n if not r.get('name_en') else f"{n} {r['name_en']}", qs)
        if hit:
            r['geo'] = {'lat': hit['lat'], 'lng': hit['lng'],
                        'source_name': 'OpenStreetMap', 'source_url': hit['source_url']}
            added_s += 1
            print(f"  + {n[:28]} -> {hit['matched'][:26]} ({hit['score']})")
    json.dump(shops, open(sp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

    json.dump(CACHE, open(CACHE_FP, 'w', encoding='utf-8'), ensure_ascii=False)
    tot_p = sum(1 for r in places if r.get('category') != 'tradition')
    have_p = sum(1 for r in places if r.get('geo') and r.get('category') != 'tradition')
    print(f'\nสถานที่ {have_p}/{tot_p} (เพิ่ม {added_p}) · ร้าน {sum(1 for r in shops if r.get("geo"))}/{len(shops)} (เพิ่ม {added_s})')


if __name__ == '__main__':
    main()
