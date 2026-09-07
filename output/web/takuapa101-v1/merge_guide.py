"""Fold the curated Siwara guide into the site's data.

These 13 entries were checked on the ground by the guide's author, so unlike the
auto researched directory they carry real opening hours, a working map link and
an English version. They are marked as curated so a reader can tell the
difference between "someone went there" and "found in a brochure".
"""
import json
import os
import re
import shutil
import sys
import unicodedata

sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, 'data', 'siwara-guide.json')
SITE_IMG = os.path.join(ROOT, 'site', 'assets', 'guide')
GUIDE_HOME = r'D:\Siwaracafeweb'

CAT = {'dining': 'restaurant', 'attraction': 'attraction', 'souvenir': 'souvenir_shop'}
EMOJI = re.compile(r'[\U0001F300-\U0001FAFF\u2600-\u27BF\uFE0F]')


def clean(s):
    """Labels arrive with emoji; the site does not use them."""
    return EMOJI.sub('', str(s or '')).strip(' ·-')


def norm(name):
    s = unicodedata.normalize('NFKC', str(name or '')).lower()
    s = re.sub(r'\((?:[^)]*)\)', ' ', s)
    s = re.sub(r'\b(ร้าน|คาเฟ่|cafe|restaurant|the)\b', ' ', s)
    return re.sub(r'[^0-9a-zก-๙]', '', s)


def main():
    items = json.load(open(SRC, encoding='utf-8'))
    os.makedirs(SITE_IMG, exist_ok=True)

    out, en, copied, missing_img = [], {}, 0, []
    for it in items:
        sid = 'guide-' + it['id'].replace('_', '-')
        img = None
        if it.get('image'):
            src = os.path.join(GUIDE_HOME, it['image'].replace('/', os.sep))
            if os.path.exists(src):
                name = sid + os.path.splitext(src)[1]
                shutil.copy2(src, os.path.join(SITE_IMG, name))
                img = f'/assets/guide/{name}'
                copied += 1
            else:
                missing_img.append(it['image'])
        rec = {
            'id': sid,
            'name_th': clean(it.get('name')),
            'name_en': clean(it.get('nameEn')),
            'category': CAT.get(it.get('cat'), 'restaurant'),
            'guide_group': it.get('cat'),
            'label_th': clean(it.get('catLabel')),
            'one_liner_th': it.get('desc'),
            'menu_th': it.get('menu'),
            'tip_th': it.get('tip'),
            'hours_th': it.get('hours'),
            'distance_th': it.get('dist'),
            'image': img,
            'google_maps_url': it.get('url'),
            # Checked in person by the guide's author, unlike the brochure list.
            'status': 'open',
            'provenance': 'siwara-guide',
            'sources': [{'name': 'คู่มือกินเที่ยวตะกั่วป่า โดยศิวรา คาเฟ่',
                         'url': 'https://siwaracafe.com/guide', 'accessed': '2026-09-07'}],
        }
        out.append(rec)
        en[sid] = {
            'name': clean(it.get('nameEn')) or clean(it.get('name')),
            'label': clean(it.get('catLabelEn')),
            'one_liner': it.get('descEn'),
            'menu': it.get('menuEn'),
            'tip': it.get('tipEn'),
            'hours': it.get('hoursEn'),
            'distance': it.get('distEn'),
        }

    json.dump(out, open(os.path.join(ROOT, 'data', 'guide-picks.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
    endir = os.path.join(ROOT, 'data', 'i18n', 'en')
    os.makedirs(endir, exist_ok=True)
    json.dump(en, open(os.path.join(endir, 'guide-picks.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)

    # Anything the researched directory duplicates is downgraded: the curated
    # entry has verified hours and a working link, so it wins.
    sp = os.path.join(ROOT, 'data', 'shops-extra.json')
    shops = json.load(open(sp, encoding='utf-8'))
    keys = {norm(r['name_th']) for r in out}
    dropped = []
    keep = []
    for r in shops:
        if norm(r['name_th']) in keys:
            dropped.append(r['name_th'])
            continue
        keep.append(r)
    json.dump(keep, open(sp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

    by = {}
    for r in out:
        by[r['category']] = by.get(r['category'], 0) + 1
    print(f'คู่มือคัดสรร {len(out)} รายการ · {by}')
    print(f'  คัดลอกรูป {copied} ใบ' + (f' · หารูปไม่เจอ {len(missing_img)}' if missing_img else ''))
    print(f'  คำแปลอังกฤษ {len(en)} รายการ')
    print(f'  ตัดร้านซ้ำออกจากลิสต์ค้นหา {len(dropped)}: {dropped or "ไม่มี"}')
    print(f'  ร้านจากการค้นหาที่เหลือ {len(keep)}')


if __name__ == '__main__':
    main()
