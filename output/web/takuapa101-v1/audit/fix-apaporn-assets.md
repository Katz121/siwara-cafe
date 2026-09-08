# ตรวจปิดงาน: รูปกระทู้ “อาภรณ์”

วันที่ตรวจ: 2026-09-09

- เพิ่มรูปจาก `D:\Takuapa\images\event\` จำนวน 9 ใบ ลง `site/assets/photos/`
- แปลงด้วย Pillow เป็น WebP quality 80 และจำกัดด้านยาวไม่เกิน 1,400 px
- ไฟล์ปลายทางครบ 9 ไฟล์ ทุกไฟล์ขนาดต่ำกว่า 400 KB (ประมาณ 108–230 KB)
- เพิ่มระเบียนใหม่ใน `data/photo-registry.json` โดยใช้คำบรรยายตามทะเบียนที่กำหนด, `era: now`, สิทธิ์ใช้งาน และ `allowed_on` ตามโจทย์
- สร้าง `site/assets/og/apaporn.png` ขนาด 1200×630 โดยใช้ `kuapapoh-charm-09.webp` และตัดคำไทยด้วย pythainlp engine `newmm` ตาม `make_og.py`

## ผลตรวจ

- `python -c "import json;json.load(open('data/photo-registry.json',encoding='utf-8'))"` — ผ่าน
- ตรวจมิติและขนาดรูปปลายทาง — ผ่าน
- ตรวจระเบียนใหม่ 9 รายการและเส้นทาง `/stories/apaporn/` — ผ่าน
- ไม่แก้ `stories.py`, `build_site.py`, `design.py` หรือไฟล์ใน `data/stories/`

หมายเหตุ: พบการเปลี่ยนแปลง/ไฟล์ที่ไม่เกี่ยวข้องใน working tree อยู่ก่อนแล้ว จึงไม่ได้แตะต้อง
