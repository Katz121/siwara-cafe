# Image/PDF weight audit

รัน `python optimize_assets.py` ซ้ำได้ ผลลัพธ์ไม่สร้างไฟล์ซ้ำและไม่ลบไฟล์ต้นฉบับจนกว่าจะเขียน WebP สำเร็จ

## ผลรายไฟล์

| ไฟล์ | ก่อน | หลัง |
|---|---:|---:|
| guide-tam-nang.jpg → .webp | 4.59 MiB | 283 KiB |
| guide-iron-bridge.jpg → .webp | 813 KiB | 536 KiB |
| guide-bang-deen.jpg → .webp | 691 KiB | 447 KiB |
| guide-lad-yai.jpg → .webp | 539 KiB | 343 KiB |
| guide-pa-da-hokkien.jpg → .webp | 479 KiB | 278 KiB |
| guide-tuangrat-taosor.jpg → .webp | 472 KiB | 264 KiB |
| guide-baan-lapp.jpg → .webp | 460 KiB | 382 KiB |
| guide-moo-satay-kruaew.jpg → .webp | 457 KiB | 243 KiB |
| guide-jae-ouan.jpg → .webp | 267 KiB | 270 KiB |
| guide-kae-padthai.jpg → .webp | 284 KiB | 133 KiB |
| guide-mee-talad-khwang.jpg → .webp | 86 KiB | 83 KiB |
| guide-pu-dam.jpg → .webp | 300 KiB | 83 KiB |
| guide-old-town-street.jpg → .webp | 200 KiB | 219 KiB |
| og/*.png (28 files) | 9.10 MiB | 3.55 MiB |
| municipal-map.png | 1.78 MiB | 1.78 MiB (lossless fallback) |
| municipal-map.webp (คู่ picture) | — | 521 KiB |
| takuapa-walk-leaflet.pdf | 7.57 MiB | 7.57 MiB (คงเดิม) |

guide images ถูกจำกัดด้านยาวไม่เกิน 1600px และ WebP quality 82; OG ยังคงเป็น PNG ขนาด 1200×630 และลด palette แบบ lossless ต่อสีที่ใช้จริง แผนที่ยังมี PNG fallback และ WebP quality 90 สำหรับเบราว์เซอร์ที่รองรับ

## ตรวจสอบ

- `python build_site.py` ผ่าน: 44 หน้า
- `python build_en.py` ผ่าน: 44 หน้า
- ทุกภาพใน HTML ที่สร้างมี `width` และ `height` จากไฟล์จริง รวมถึงภาพ guide, leaflet และ story cards
- ตรวจ `src` ของ HTML กับ `site/assets` หลัง build แล้ว: ไม่พบไฟล์ภาพที่หาย
- ขนาดรวม `site/assets/` หลังงาน: 22,452,814 bytes; PDF ไม่ถูกลบและลิงก์แสดงขนาด 7.6 MB ก่อนดาวน์โหลด
