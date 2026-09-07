"""Fill in coordinates from OpenStreetMap.

Nominatim and Overpass return real, checkable records rather than a model's
recollection, so nothing here is invented: a shop either matches an OSM object
inside Takua Pa district or it keeps a null coordinate.
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
# Generous box around Takua Pa district; anything outside is a wrong match.
BOX = {'lat': (8.55, 9.20), 'lng': (98.10, 98.60)}
CACHE_FP = os.path.join(ROOT, 'data', 'geocode-cache.json')
CACHE = json.load(open(CACHE_FP, encoding='utf-8')) if os.path.exists(CACHE_FP) else {}


def inside(lat, lng):
    return BOX['lat'][0] <= lat <= BOX['lat'][1] and BOX['lng'][0] <= lng <= BOX['lng'][1]


def get(url, tries=3):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept-Language': 'th,en'})
            with urllib.request.urlopen(req, timeout=40) as r:
                return json.loads(r.read().decode('utf-8'))
        except Exception as e:
            if i == tries - 1:
                print(f'    ! {e}')
                return None
            time.sleep(3 * (i + 1))
    return None


def norm(s):
    s = unicodedata.normalize('NFKC', str(s or '')).lower()
    s = re.sub(r'\b(ร้าน|คาเฟ่|cafe|restaurant|the|บาย|by|coffee)\b', ' ', s)
    return re.sub(r'[^0-9a-zก-๙]', '', s)


def nominatim(query):
    """Free-text search, restricted to the district's bounding box."""
    key = 'nom:' + query
    if key in CACHE:
        return CACHE[key]
    url = ('https://nominatim.openstreetmap.org/search?format=jsonv2&limit=5&addressdetails=1'
           '&viewbox=98.10,9.20,98.60,8.55&bounded=1&q=' + urllib.parse.quote(query))
    data = get(url) or []
    time.sleep(1.1)  # Nominatim asks for at most one request per second
    CACHE[key] = data
    return data


def overpass_pois():
    """Every named eating, drinking and shop node in the district, once."""
    if 'overpass' in CACHE:
        return CACHE['overpass']
    q = """
    [out:json][timeout:120];
    area["boundary"="administrative"]["name"~"ตะกั่วป่า"]->.a;
    (
      node["name"]["amenity"~"restaurant|cafe|fast_food|bar|ice_cream|food_court"](area.a);
      way["name"]["amenity"~"restaurant|cafe|fast_food|bar|ice_cream|food_court"](area.a);
      node["name"]["shop"](area.a);
      way["name"]["shop"](area.a);
      node["name"]["tourism"~"attraction|museum|artwork"](area.a);
      node["name"]["amenity"~"place_of_worship|marketplace"](area.a);
      way["name"]["amenity"~"place_of_worship|marketplace"](area.a);
    );
    out center tags;
    """
    url = 'https://overpass-api.de/api/interpreter?data=' + urllib.parse.quote(q)
    data = get(url, tries=2)
    elems = (data or {}).get('elements', [])
    out = []
    for e in elems:
        lat = e.get('lat') or (e.get('center') or {}).get('lat')
        lng = e.get('lon') or (e.get('center') or {}).get('lon')
        if lat is None or lng is None or not inside(lat, lng):
            continue
        tags = e.get('tags', {})
        out.append({
            'osm': f"{e['type']}/{e['id']}",
            'name': tags.get('name'),
            'name_en': tags.get('name:en'),
            'lat': lat, 'lng': lng,
            'kind': tags.get('amenity') or tags.get('shop') or tags.get('tourism'),
            'phone': tags.get('phone') or tags.get('contact:phone'),
            'hours': tags.get('opening_hours'),
        })
    CACHE['overpass'] = out
    return out


def match_local(name, pois):
    """Exact-ish name match against the OSM extract."""
    key = norm(name)
    if len(key) < 4:
        return None
    for p in pois:
        for cand in (p.get('name'), p.get('name_en')):
            if not cand:
                continue
            k = norm(cand)
            if k and (k == key or (len(key) >= 6 and (key in k or k in key))):
                return p
    return None


def resolve(name, pois, extra_query=None):
    hit = match_local(name, pois)
    if hit:
        return {'lat': hit['lat'], 'lng': hit['lng'], 'source': 'overpass',
                'osm': hit['osm'], 'phone': hit.get('phone'), 'hours': hit.get('hours'),
                'source_url': f"https://www.openstreetmap.org/{hit['osm']}"}
    for q in filter(None, [extra_query, f'{name} ตะกั่วป่า', f'{name} พังงา']):
        for r in nominatim(q):
            lat, lng = float(r['lat']), float(r['lon'])
            if not inside(lat, lng):
                continue
            if norm(r.get('name') or '') and norm(r.get('name', '')) not in norm(name) and norm(name) not in norm(r.get('name', '')):
                # A loose text hit that is not the same place is worse than nothing.
                continue
            return {'lat': lat, 'lng': lng, 'source': 'nominatim',
                    'osm': f"{r.get('osm_type')}/{r.get('osm_id')}",
                    'source_url': f"https://www.openstreetmap.org/{r.get('osm_type')}/{r.get('osm_id')}"}
    return None


def main():
    print('ดึงรายการสถานที่จาก OpenStreetMap ในเขตอำเภอตะกั่วป่า ...')
    pois = overpass_pois()
    print(f'  ได้ {len(pois)} รายการ')

    filled_places = filled_shops = 0

    ep = os.path.join(ROOT, 'data', 'places-enriched.json')
    places = json.load(open(ep, encoding='utf-8'))
    for r in places:
        if r.get('geo') or r.get('category') == 'tradition':
            continue
        hit = resolve(r['name_th'], pois, extra_query=f"{r['name_th']} ตะกั่วป่า พังงา")
        if hit:
            r['geo'] = {'lat': hit['lat'], 'lng': hit['lng'], 'confidence': 'medium',
                        'source_name': 'OpenStreetMap', 'source_url': hit['source_url']}
            filled_places += 1
            print(f"  + {r['name_th'][:34]} -> {hit['lat']:.5f},{hit['lng']:.5f} ({hit['source']})")
        else:
            print(f"  - {r['name_th'][:34]} ยังหาไม่เจอ")
    json.dump(places, open(ep, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

    sp = os.path.join(ROOT, 'data', 'shops-extra.json')
    shops = json.load(open(sp, encoding='utf-8'))
    for r in shops:
        if r.get('geo'):
            continue
        hit = resolve(r['name_th'], pois)
        if hit:
            r['geo'] = {'lat': hit['lat'], 'lng': hit['lng'], 'source_url': hit['source_url'],
                        'source_name': 'OpenStreetMap'}
            if hit.get('phone') and not r.get('phone'):
                r['phone'] = hit['phone']
            if hit.get('hours') and not r.get('hours_th'):
                r['hours_th'] = hit['hours']
            filled_shops += 1
            print(f"  + {r['name_th'][:30]} -> {hit['lat']:.5f},{hit['lng']:.5f}")
    json.dump(shops, open(sp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

    json.dump(CACHE, open(CACHE_FP, 'w', encoding='utf-8'), ensure_ascii=False)

    place_total = sum(1 for r in places if r.get('category') != 'tradition')
    have = sum(1 for r in places if r.get('geo') and r.get('category') != 'tradition')
    print()
    print(f'สถานที่ {have}/{place_total} มีพิกัด (เพิ่มรอบนี้ {filled_places})')
    print(f'ร้าน {sum(1 for r in shops if r.get("geo"))}/{len(shops)} มีพิกัด (เพิ่มรอบนี้ {filled_shops})')


if __name__ == '__main__':
    main()
