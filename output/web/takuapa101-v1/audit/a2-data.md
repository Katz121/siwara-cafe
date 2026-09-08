# รายงานตรวจความสอดคล้องข้อมูล · A2

ตรวจแบบอ่านไฟล์เท่านั้น ณ 2026-09-08 · ไม่ได้แก้ไฟล์ข้อมูลหรือไฟล์เว็บ

## 1) JSON parse / ไฟล์ว่าง / BOM

ตรวจ `data/**/*.json` จำนวน 103 ไฟล์ด้วย UTF-8 (รองรับการตรวจ BOM แยกต่างหาก)

- parse ไม่ผ่าน: ไม่พบ
- ไฟล์ว่าง: ไม่พบ
- BOM: ไม่พบ

ผล: ตรวจแล้วไม่พบปัญหา

## 2) ID สถานที่ที่อ้างถึง

ฐานอ้างอิงคือ `data/places-enriched.json` มี 27 IDs

- `data/stories/*.json`: ID ที่อ้างถึงทั้งหมดมีอยู่จริง · ไม่พบ ID หาย
- `data/map-points.json`: 20 รายการที่อ้างถึงมีอยู่จริง · ไม่พบ ID หาย
- `data/guide-picks.json`: อ้างถึง ID ต่อไปนี้ที่ไม่มีใน `places-enriched.json`: `guide-baan-lapp`, `guide-bang-deen`, `guide-iron-bridge`, `guide-jae-ouan`, `guide-kae-padthai`, `guide-lad-yai`, `guide-mee-talad-khwang`, `guide-moo-satay-kruaew`, `guide-old-town-street`, `guide-pa-da-hokkien`, `guide-pu-dam`, `guide-tam-nang`, `guide-tuangrat-taosor`
- routes (`data/siwara-guide.json`): อ้างถึงค่าต่อไปนี้ที่ไม่มีใน `places-enriched.json`: `baan_lapp`, `bang_deen`, `iron_bridge`, `jae_ouan`, `kae_padthai`, `lad_yai`, `mee_talad_khwang`, `moo_satay_kruaew`, `old_town_street`, `pa_da_hokkien`, `pu_dam`, `tam_nang`, `tuangrat_taosor`

หลักฐานไฟล์: `data/places-enriched.json`, `data/stories/*.json`, `data/guide-picks.json`, `data/map-points.json`, `data/siwara-guide.json`

## 3) ทะเบียนรูปและการใช้รูปบนเว็บ

`data/photo-registry.json` ทะเบียน 12 รูป · ตรวจไฟล์ตามฟิลด์ `file` กับ `site/assets/` แล้วพบไฟล์หาย: ไม่พบ

ตรวจการอ้างอิงรูปใน HTML/JS/CSS/JSON/XML ใต้ `site/` แล้วพบรูปที่ใช้งานแต่ไม่อยู่ในทะเบียน (สรุปตามกลุ่ม):

- รูปสถานที่: `culture-street.webp`, `food-center.webp`, `governor-wall.webp`, `guan-yu.webp`, `iron-bridge.webp`, `khun-in.webp`, `kue-chai.webp`, `museum.webp`, `phra-narai.webp`, `pun-thao.webp`, `relic-procession.webp`, `riverwalk.webp`, `rong-jae.webp`, `ruler-ceremony.webp`, `tao-ming.webp`, `thung-phra.webp`, `wat-boromthat.webp`, `wat-khuha.webp`, `wat-kongkha.webp`, `wat-nikorn.webp`, `wat-pathum.webp`, `wat-sena.webp`, `narai-ceremony.webp`
- รูปคู่มือ: `assets/guide/` ทั้ง 13 ไฟล์
- รูป OG: `assets/og/` ทั้ง 27 ไฟล์
- อื่น ๆ: `assets/favicon.svg`, `assets/leaflet/leaflet-page-1.webp`, `assets/leaflet/leaflet-page-2.webp`, `assets/municipal-map.png`

รูปใน `assets/photos/` ทั้ง 12 ไฟล์มีทะเบียนและถูกตรวจว่ามีไฟล์จริงแล้ว

## 4) สถานที่ไม่มี geo / รูป / source

ตรวจสถานที่ 27 รายการใน `data/places-enriched.json`:

- ไม่มี geo: `rong-jae`, `new-year-alms`, `vegetarian`, `loy-krathong`, `chak-phra`
- ไม่มีรูป: ไม่พบ
- ไม่มี source: ไม่พบ

หมายเหตุ: การตรวจนี้ยึดฟิลด์ข้อมูลที่มีอยู่จริงใน JSON ไม่ได้อนุมานจากรูปที่หน้าเว็บแสดง

## 5) จำนวนที่เขียนบนหน้าเว็บเทียบข้อมูลจริง

- 20 สถานที่: ตรงกับสถานที่ที่ไม่ใช่ประเพณีใน `places-enriched.json` (27 ทั้งหมด − 7 ประเพณี) และตรงกับ `data/map-points.json` 20 รายการ
- 7 ประเพณี: ตรงกับ `calendar.events` 7 รายการใน `data/calendar.json` และรายการประเพณี 7 รายการใน `places-enriched.json`
- 59 รายการ: ไม่ตรงกับข้อมูลร้านที่ตรวจพบ · `site/en/index.html` ระบุ “59 shops” และแจกแจง 32 + 20 + 08 = 60 แต่ `data/shops-extra.json` มี 49 รายการ และ `data/i18n/en/shops.json` มี 49 keys

การเปิดเว็บ/เสิร์ฟ HTTP: ไม่ได้ทำ เพราะงานนี้กำหนดเป็นงานอ่านไฟล์ล้วน และการตรวจข้อ 3/5 ทำได้จากไฟล์เว็บที่สร้างแล้ว

