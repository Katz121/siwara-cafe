#!/usr/bin/env python3
"""
สร้างข้อมูลแผนที่ site/assets/map-points.json จาก data/places-enriched.json
แยกเป็น points (มี geo) และ unlocated (ไม่มี geo)
"""
import json
import sys
from pathlib import Path

# รองรับการพิมพ์ข้อความภาษาไทยใน Windows console
sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parent
SRC_PATH = ROOT / 'data' / 'places-enriched.json'
DEST_PATH = ROOT / 'site' / 'assets' / 'map-points.json'


def get_url(record: dict) -> str:
    """ส่งคืน URL ของสถานที่หรือประเพณี"""
    if record.get('category') == 'tradition' or record.get('type') == 'event':
        return '/takuapa/traditions/'
    return f"/takuapa/places/{record['id']}/"


def get_image(record: dict) -> str:
    """ส่งคืนรูปภาพ: ภาพ usable แรกถ้ามี ไม่มีใช้ /takuapa/assets/<id>.webp"""
    photos = record.get('photos') or {}
    usable = photos.get('usable') or []
    if usable and isinstance(usable, list):
        first = usable[0]
        if isinstance(first, dict):
            src = first.get('file') or first.get('url')
            if src:
                if src.startswith('/') and not src.startswith('/takuapa/'):
                    return f"/takuapa{src}"
                return src
    return f"/takuapa/assets/{record['id']}.webp"


def main():
    if not SRC_PATH.exists():
        print(f"Error: ไม่พบไฟล์ต้นทางที่ {SRC_PATH}", file=sys.stderr)
        sys.exit(1)

    with open(SRC_PATH, 'r', encoding='utf-8') as f:
        records = json.load(f)

    points = []
    unlocated = []

    for r in records:
        geo = r.get('geo')
        # ตรวจสอบ geo ว่าไม่ใช่ null และมีค่าพิกัด lat, lng
        if geo is not None and geo.get('lat') is not None and geo.get('lng') is not None:
            points.append({
                'id': r.get('id'),
                'name_th': r.get('name_th'),
                'name_en': r.get('name_en'),
                'category': r.get('category'),
                'lat': geo.get('lat'),
                'lng': geo.get('lng'),
                'confidence': geo.get('confidence'),
                'url': get_url(r),
                'image': get_image(r),
                'kicker': r.get('editorial_angle')
            })
        else:
            addr = r.get('address') or {}
            line_th = addr.get('line_th') if isinstance(addr, dict) else None
            # address.line_th ถ้ามี
            address_val = line_th if line_th else None

            unlocated.append({
                'id': r.get('id'),
                'name_th': r.get('name_th'),
                'category': r.get('category'),
                'address': address_val,
                'url': get_url(r)
            })

    output_data = {
        'points': points,
        'unlocated': unlocated
    }

    DEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(DEST_PATH, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
        f.write('\n')

    print(f"สร้างไฟล์สำเร็จ: {DEST_PATH}")
    print(f"points: {len(points)}")
    print(f"unlocated: {len(unlocated)}")


if __name__ == '__main__':
    main()
