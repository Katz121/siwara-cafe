"""Enforce the photo registry across the built data.

A photo may only appear where the registry says it depicts that subject, and its
caption always comes from the registry. Anything else is stripped, so an
illustration or nothing takes its place rather than a misleading picture.
"""
import glob
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.abspath(__file__))
REG = json.load(open(os.path.join(ROOT, 'data', 'photo-registry.json'), encoding='utf-8'))
BY_FILE = {p['file']: p for p in REG['photos']}
REJECTED = {f for group in REG['rejected'] for f in group['files']}


def allowed(file, subject):
    p = BY_FILE.get(file)
    return bool(p) and subject in p['allowed_on']


def fix_photo(node, subject, removed, kept):
    """Return a registry-backed photo dict, or None when it does not belong here."""
    if not node or not node.get('file'):
        return None
    f = node['file']
    if f in REJECTED or not allowed(f, subject):
        removed.append((subject, os.path.basename(f), node.get('caption_th', '')[:40]))
        return None
    p = BY_FILE[f]
    kept.append((subject, os.path.basename(f)))
    return {'file': f, 'caption_th': p['caption_th'], 'credit': p['credit'],
            'license': p['license'], 'era': p['era']}


def main():
    removed, kept = [], []

    for fp in sorted(glob.glob(os.path.join(ROOT, 'data', 'stories', '*.json'))):
        try:
            d = json.load(open(fp, encoding='utf-8'))
        except Exception:
            continue
        sid = d.get('id')
        if not sid:
            continue
        d['hero_photo'] = fix_photo(d.get('hero_photo'), sid, removed, kept)
        for s in d.get('sections', []):
            s['photo'] = fix_photo(s.get('photo'), sid, removed, kept)
        json.dump(d, open(fp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

    ep = os.path.join(ROOT, 'data', 'places-enriched.json')
    places = json.load(open(ep, encoding='utf-8'))
    for r in places:
        photos = r.get('photos') or {}
        usable = []
        for ph in photos.get('usable', []):
            f = ph.get('file') or ph.get('local_file') or ph.get('url')
            fixed = fix_photo({'file': f, 'caption_th': ph.get('caption_th', '')}, r['id'], removed, kept)
            if fixed:
                usable.append(fixed)
        photos['usable'] = usable
        r['photos'] = photos
    json.dump(places, open(ep, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

    counts = {}
    for subject, f in kept:
        counts[f] = counts.get(f, 0) + 1

    print(f'เอาออก {len(removed)} จุด · เก็บไว้ {len(kept)} จุด')
    if removed:
        print('  ที่เอาออก:')
        for subject, f, cap in removed:
            print(f'    {subject:16} {f:28} {cap}')
    reused = {f: n for f, n in counts.items() if n > 1}
    if reused:
        print('  ใช้ซ้ำ (ตรวจว่าตั้งใจ):', reused)
    print(f'  รูปที่ยังใช้อยู่ {len(counts)} ใบ')


if __name__ == '__main__':
    main()
