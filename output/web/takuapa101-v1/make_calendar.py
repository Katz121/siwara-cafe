"""Map the seven traditions onto a twelve-month calendar, honestly."""
import json, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
from seo_config import BASE_PATH

ROOT = os.path.dirname(os.path.abspath(__file__))
E = json.load(open(os.path.join(ROOT, 'data/places-enriched.json'), encoding='utf-8'))
MONTHS = ['มกราคม','กุมภาพันธ์','มีนาคม','เมษายน','พฤษภาคม','มิถุนายน',
          'กรกฎาคม','สิงหาคม','กันยายน','ตุลาคม','พฤศจิกายน','ธันวาคม']

out = []
for r in E:
    if r.get('category') != 'tradition':
        continue
    f = r.get('festival') or {}
    text = f.get('months_th') or ''
    months = sorted({MONTHS.index(m) + 1 for m in MONTHS if m in text})
    # "certain" only when the source names months without hedging language
    hedged = any(w in text for w in ('ไม่พบ', 'ไม่ระบุ', 'โดยทั่วไป', 'ขึ้นกับ', 'เปลี่ยนตาม', 'ตามลักษณะ'))
    out.append({
        'id': r['id'],
        'name_th': r['name_th'],
        'months': months,
        'months_note_th': text or None,
        'certainty': 'approximate' if (hedged or not months) else 'stated',
        'lunar_th': f.get('lunar_calendar_th'),
        'venue_th': f.get('venue_th'),
        'activities_th': f.get('activities_th') or [],
        'url': f'{BASE_PATH}/traditions/#{r["id"]}',
        'image': f'{BASE_PATH}/assets/{r["id"]}.webp' if os.path.exists(os.path.join(ROOT, 'site/assets', r['id'] + '.webp')) else None,
        'sources': (f.get('source_urls') or [])[:3],
    })

calendar = [{'month': i + 1, 'name_th': MONTHS[i],
             'events': [e['id'] for e in out if (i + 1) in e['months']]} for i in range(12)]
json.dump({'events': out, 'calendar': calendar},
          open(os.path.join(ROOT, 'data/calendar.json'), 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
placed = sum(1 for e in out if e['months'])
print(f'traditions {len(out)} · วางลงเดือนได้ {placed} · ไม่มีเดือนแน่นอน {len(out)-placed}')
for e in out:
    print(f"  {e['name_th'][:34]:36} {[MONTHS[m-1] for m in e['months']] or 'ไม่ระบุเดือน'} · {e['certainty']}")
