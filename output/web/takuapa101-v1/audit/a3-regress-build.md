# A3 · regression/build audit

ตรวจจาก state ปัจจุบันหลังการแก้หลายมือ · ไม่แก้ source หรือไฟล์ site

## ผลตรวจ

- `python build_site.py` · ผ่าน, exit 0. Output: `Built 44 pages, 20 places, 7 traditions, 59 directory entries.`
- `python build_en.py` · ผ่าน, exit 0. สร้างอังกฤษ 44 หน้า, ข้าม 0 หน้า แต่รายงาน `ข้อความที่ยังไม่มีคำแปล 98 แบบ` และเขียน `data/i18n/en/missing.json` · เป็น warning ที่ build รายงานเอง ไม่ตีความเป็น regression โดยไม่มีหลักฐานเพิ่ม
- Python duplicate definitions · ตรวจ AST ทุก `.py` แบบรองรับ UTF-8 BOM แล้ว ไม่พบ function/class ชื่อซ้ำใน scope เดียวกัน
- Import ใช้/ไม่ใช้ · ตรวจด้วย `pyflakes` ไม่ได้ เพราะ environment นี้ไม่มีคำสั่ง `pyflakes` (`The term 'pyflakes' is not recognized...`) จึงไม่สรุปผลข้อนี้เกินหลักฐาน
- `node --check` · ผ่านทุกไฟล์ JS ที่พบ รวม `worker/src/*.js`, `router/src/index.js` และ `site/assets/*.js`
- `python -m unittest test_translate_attrs` · ผ่าน: Ran 3 tests, OK, exit 0
- เสิร์ฟตามคำสั่ง `python -m http.server 8798 --directory site` · ทดสอบ GET `/` ได้ HTTP 200
- sitemap · พบ `<loc>` 88 รายการ และตรวจ mapping ทุก URL ไปยัง `site/.../index.html` แล้ว missing 0; จำนวน HTML ทั้งหมด 88 ไฟล์

## Findings

### ผิด · `site/assets/map.js:6-12,59,64,79,82` · ข้อความภาษาไทยถูกแทนด้วย `?`

**หลักฐาน:** พบ literal `???` รวม 96 จุดใน `site/assets/map.js` (เช่น category labels ที่บรรทัด 6-12 และข้อความ UI ที่บรรทัด 59, 64, 79, 82) และ `node --check` ยังผ่านเพราะเป็น string ที่ syntactically valid

**ผลกระทบ:** หน้าแผนที่จะแสดงเครื่องหมายคำถามแทน label/ข้อความภาษาไทยจริง เป็น regression ที่ผู้ใช้เห็นได้โดยตรง และสอดคล้องกับประวัติไฟล์ที่อาจถูกบันทึกด้วย encoding ผิด

**แก้ขั้นต่ำ:** กู้ข้อความจาก source/data เดิมแล้วเขียน `site/assets/map.js` เป็น UTF-8; ตรวจทุก literal `???` ซ้ำหลัง build

## สรุป

fix-then-ship · build และ artifact count ผ่าน แต่ `site/assets/map.js` มีข้อความเสียหายที่ render จริง
