"""Build the merged city-news feed and the site-wide search index."""
import json, sys, os, re
sys.stdout.reconfigure(encoding='utf-8')
from seo_config import BASE_PATH

ROOT = os.path.dirname(os.path.abspath(__file__))
E = json.load(open(os.path.join(ROOT, 'data/places-enriched.json'), encoding='utf-8'))
LIB = json.load(open(os.path.join(ROOT, 'data/library.json'), encoding='utf-8'))['records']

def url_for(r):
    return f"{BASE_PATH}/traditions/" if r.get('category') == 'tradition' else f"{BASE_PATH}/places/{r['id']}/"

# ---- news feed ----
news = []
for r in E:
    for n in (r.get('news') or []):
        if not n.get('title_th'):
            continue
        news.append({
            'date': n.get('date') or '',
            'title_th': n['title_th'],
            'summary_th': n.get('summary_th') or '',
            'outlet': n.get('outlet') or '',
            'url': n.get('url') or '',
            'place_id': r['id'],
            'place_name': r['name_th'],
            'place_url': url_for(r),
            'category': r.get('category'),
        })
seen, uniq = set(), []
for n in sorted(news, key=lambda x: x['date'], reverse=True):
    key = (n['title_th'], n['url'])
    if key in seen:
        continue
    seen.add(key); uniq.append(n)
json.dump(uniq, open(os.path.join(ROOT, 'data/news-feed.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

# ---- search index ----
idx = []
for r in E:
    kw = (r.get('seo') or {}).get('keywords_th') or []
    idx.append({'t': 'place' if r.get('category') != 'tradition' else 'tradition',
                'id': r['id'], 'name': r['name_th'], 'en': r.get('name_en') or '',
                'cat': r.get('category'), 'url': url_for(r),
                'kw': ' '.join(kw)[:400]})
for r in LIB:
    if r.get('category') in ('restaurant', 'drink_shop', 'souvenir_shop'):
        idx.append({'t': 'shop', 'id': r['id'], 'name': r['name_th'], 'en': r.get('name_en') or '',
                    'cat': r['category'], 'url': f"{BASE_PATH}/eat/#{r['id']}", 'kw': ''})
sd = os.path.join(ROOT, 'data/stories')
if os.path.isdir(sd):
    for f in sorted(os.listdir(sd)):
        if not f.endswith('.json'):
            continue
        try:
            s = json.load(open(os.path.join(sd, f), encoding='utf-8'))
        except Exception:
            continue
        if not s.get('id') or not s.get('sections'):
            continue
        idx.append({'t': 'story', 'id': s['id'], 'name': s.get('title', s['id']), 'en': '',
                    'cat': s.get('group', ''), 'url': f"{BASE_PATH}/stories/{s['id']}/",
                    'kw': s.get('dek', '')[:300]})
os.makedirs(os.path.join(ROOT, 'site/assets'), exist_ok=True)
json.dump(idx, open(os.path.join(ROOT, 'site/assets/search-index.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print(f"news {len(uniq)} · search index {len(idx)}")
