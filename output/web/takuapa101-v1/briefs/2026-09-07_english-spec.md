# ตะกั่วป่า 101 · เวอร์ชันภาษาอังกฤษ

โฟลเดอร์งาน `D:\Siwaracafeweb\output\web\takuapa101-v1`
static site generator ภาษา Python vanilla · `build_site.py` + `design.py` + `stories.py` + `seo.py`
โดเมนจริง `https://takuapa101.com` · ตอนนี้ preview อยู่ที่ `https://takuapa101.pages.dev`

## ทำไมต้องมี
เขาหลักอยู่ห่างตะกั่วป่า 30 กม. มีนักท่องเที่ยวยุโรปทั้งปี · คำค้น `Takua Pa old town`,
`things to do Takua Pa`, `Takua Pa Sunday market` แทบไม่มีเว็บที่ตอบได้จริง
นี่คือตลาดที่ว่างที่สุดของเว็บนี้

## โครงที่ต้องได้
- ไทยอยู่ที่ราก `/` เหมือนเดิม · อังกฤษอยู่ใต้ `/en/` (เช่น `/en/places/tao-ming/`)
- ทุกหน้ามี `<link rel="alternate" hreflang="th">`, `hreflang="en"`, `hreflang="x-default"` ชี้หน้าไทย
- หน้าอังกฤษ `<html lang="en">` · canonical ชี้ตัวเอง · sitemap รวมทั้งสองภาษา
- ปุ่มสลับภาษาบนหัวเว็บ (TH / EN) ไปหน้าคู่กันเสมอ ไม่ใช่กลับหน้าแรก
- ถ้าหน้าไหนยังไม่มีคำแปล **ห้ามสร้างหน้าอังกฤษเปล่า** ให้ข้ามไปเลย ไม่งั้น Google เจอหน้าโหล ๆ

## คำแปล
เก็บใน `data/i18n/en/` แยกไฟล์:
- `ui.json` — เมนู ปุ่ม หัวข้อ section ป้ายสถานะ ข้อความในตัวกรอง ฯลฯ (ดึงสตริงจาก design.py, build_site.py, stories.py, trip-page.js, map ใน design.js, search.js)
- `places.json` — 27 สถานที่/ประเพณี: `name_en`, `lead`, `eras.then/before/now` (headline + body), `highlights`, `getting_there`, `did_you_know`, `visit` labels
- `stories.json` — 5 บทความ: title, dek, lede, sections (heading + paragraphs), pull_quotes, evidence_box
- `shops.json` — คำอธิบายร้าน 49 ร้าน (one_liner) และชื่อหมวด

## กฎการแปล
1. **แปลเพื่อคนอ่านจริง ไม่ใช่แปลตรงตัว** · ชื่อเฉพาะให้ทับศัพท์แล้ววงเล็บคำอธิบาย เช่น
   `Wat Boromthat Khiri Khet (the town's relic temple)` · `Tao Ming School (the town's first Chinese school)`
2. ชื่อสถานที่ใช้ระบบทับศัพท์เดียวกันทั้งเว็บ · ทำ `data/i18n/romanisation.json` เป็นตารางกลาง
3. **ห้ามเพิ่มข้อเท็จจริงที่ไม่มีในต้นฉบับไทย** และห้ามตัดคำกำกับความไม่แน่นอนทิ้ง
   `ยังไม่ยืนยัน` ต้องกลายเป็น `not verified` ไม่ใช่หายไป
   `สันนิษฐาน` เป็น `suggested, not settled`
4. อธิบายบริบทที่คนต่างชาติไม่รู้เพิ่มได้ **เฉพาะที่เป็นความรู้ทั่วไป** เช่น บอกว่า Loy Krathong คือ
   เทศกาลลอยกระทงเดือนพฤศจิกายน · แต่ห้ามเพิ่มข้อมูลเฉพาะของตะกั่วป่าที่ต้นฉบับไม่ได้พูด
5. หน่วยและวันที่: ใช้ปี ค.ศ. ในภาษาอังกฤษ พร้อมวงเล็บ พ.ศ. ครั้งแรกที่ปรากฏในแต่ละหน้า
6. เสียงเล่า: กระชับ ตรงไปตรงมา แบบคู่มือเดินทางที่ดี ไม่ใช่โบรชัวร์ ไม่ใช้คำโฆษณาเกินจริง
   ห้าม `hidden gem`, `must-see`, `paradise`, `authentic` แบบลอย ๆ
7. ห้าม em-dash และ en-dash · ใช้ `·` หรือเขียนเป็นประโยคใหม่
8. **เขียนไฟล์เป็น UTF-8 เท่านั้น**

## SEO ฝั่งอังกฤษ
- title/description ต่อหน้าเขียนใหม่ให้ตรงคำค้นอังกฤษ ไม่ใช่แปล title ไทยตรงตัว
- JSON-LD ของหน้าอังกฤษใช้ `inLanguage: "en"` และชื่ออังกฤษ
- คำค้นเป้าหมาย: `Takua Pa old town`, `Takua Pa Phang Nga`, `things to do Takua Pa`,
  `Takua Pa Sunday market`, `Khao Lak day trip old town`, `Sino Portuguese Takua Pa`,
  `Takua Pa temples`, `Takua Pa vegetarian festival`

## ตรวจก่อนจบ
```
python build_site.py
python -c "import glob;print(len(glob.glob('site/en/**/index.html',recursive=True)),'หน้าอังกฤษ')"
grep -c hreflang site/index.html
python validate_site.py
```
แล้วเปิด `/en/`, `/en/places/`, `/en/places/tao-ming/`, `/en/stories/city/` ด้วย Playwright
ตรวจว่า: ไม่มี console error · ไม่มีข้อความไทยหลงในหน้าอังกฤษ · ปุ่มสลับภาษาไปหน้าคู่กันถูกต้อง
