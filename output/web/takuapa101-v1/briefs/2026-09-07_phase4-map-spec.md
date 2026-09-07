คุณทำงานในโฟลเดอร์ D:\Siwaracafeweb\output\web\takuapa101-v1 (static site generator ภาษา Python vanilla ไม่มี framework)

**สำคัญมาก: ต้องเขียนไฟล์ลง path จริงในโฟลเดอร์นี้เท่านั้น ห้ามเขียนลง scratch directory ของตัวเอง**

อ่านก่อนลงมือ: briefs/2026-09-07_claude-build-spec-v2.md · README.md · build_site.py · design.py · place_pages.py · seo_config.py · site/assets/design.css · site/assets/design.js

Phase 1-3 เสร็จแล้ว (ข้อมูลจริง 27 สถานที่ · SEO · หน้าสถานที่แบบเต็ม)
รอบนี้ทำ **PHASE 4 · แผนที่จริงปักหมุด** เท่านั้น ห้ามทำ phase 5-7

## ข้อมูล
`data/places-enriched.json` มี 27 record · 20 record มี `geo{lat,lng,confidence,source_url,source_name}` · อีก 7 เป็น null
สถานที่ที่ยังไม่มีพิกัด: food-center, rong-jae, wat-pathum และประเพณี 4 อย่าง (new-year-alms, vegetarian, chak-phra, loy-krathong)

## งาน
สร้างหน้าแผนที่ใหม่ที่ `/map/` (แทนของเดิมที่เป็นภาพนิ่ง แต่ **ห้ามทิ้งภาพแผนที่เทศบาลเดิม** ต้องยังเข้าถึงได้)

1. **MapLibre GL JS** โหลดจาก CDN `https://cdnjs.cloudflare.com/ajax/libs/maplibre-gl/5.6.1/maplibre-gl.js` และ css คู่กัน
   สไตล์แผนที่ใช้ OpenFreeMap: `https://tiles.openfreemap.org/styles/liberty` (ฟรี ไม่ต้องใช้ API key ห้ามใส่ token)
   ศูนย์กลางเริ่มต้นให้คำนวณจากค่าเฉลี่ยพิกัดทั้งหมด · zoom พอเห็นเมืองเก่าทั้งย่าน
2. **ปักหมุด 20 จุดที่มีพิกัด** · สีหมุดแยกตามหมวด (temple / shrine / heritage / museum / park / market / street / food_center) มีคำอธิบายสีข้างแผนที่
3. **คลิกหมุด** → popup การ์ด: ภาพ (usable ถ้ามี ไม่มีใช้ illustration) · ชื่อ · หมวด · บรรทัดสรุป · ปุ่ม "เปิดหน้าเต็ม" (ลิงก์ภายใน) · ปุ่ม "นำทาง" (`https://www.google.com/maps/search/?api=1&query=LAT,LNG` เปิดแท็บใหม่ rel="noopener")
4. **แถบฟิลเตอร์หมวด** เหนือแผนที่ · กดแล้วซ่อน/แสดงหมุด · ปุ่ม "ทั้งหมด" · แสดงจำนวนที่เห็นอยู่
5. **รายการข้างแผนที่** — ลิสต์ 27 จุด hover/คลิกแล้วแผนที่บินไปหาหมุด · **7 จุดที่ไม่มีพิกัดให้อยู่ในกลุ่มแยกท้ายลิสต์ หัวข้อ "ยังไม่มีพิกัด รอปักหมุด" พร้อมที่อยู่เท่าที่รู้** และห้ามใส่หมุดให้เด็ดขาด **ห้ามเดาพิกัด**
6. **สลับเลเยอร์** — ปุ่มเปิด/ปิด overlay ภาพแผนที่เทศบาลเดิม (`/assets/municipal-map.png`) ทับบนแผนที่จริง ปรับความทึบด้วย slider · ใช้ maplibre image source กำหนดมุมภาพแบบประมาณจากพิกัดที่ครอบเมืองเก่า และเขียนกำกับบนหน้าว่า "ภาพแผนที่เทศบาลวางทับแบบประมาณ ไม่ใช่การอ้างอิงตำแหน่งแม่นยำ"
7. **ปุ่มลิงก์ไปดูภาพแผนที่เทศบาลต้นฉบับเต็ม ๆ** ต้องยังอยู่
8. **fallback ไม่มี JS** — ต้องเห็นภาพแผนที่เทศบาลเดิม + รายชื่อ 27 จุดพร้อมลิงก์ (ของเดิมทำไว้แล้ว อย่าทำถอยหลัง) · ใส่ใน `<noscript>` หรือ render static แล้วให้ JS มาแทนที่

## กฎ
- อย่าเปลี่ยนบุคลิกเว็บ · ธีมครีม/เขียวเข้ม · ฟอนต์ Noto Serif Thai + IBM Plex Sans Thai Looped
- ลิงก์ภายในทุกอันต้องผ่าน BASE_PATH `/takuapa` (ดู seo_config.py) ห้าม hardcode `/`
- ใช้ได้ที่ 390px · แผนที่สูงพอใช้งานบนมือถือ · รองรับ prefers-reduced-motion
- ภาษาไทยทั้งหมด · ใช้ `·` แทน em-dash/en-dash · ห้ามใช้ emoji
- เปิดไฟล์ด้วย encoding='utf-8' เสมอ · ใส่ `sys.stdout.reconfigure(encoding='utf-8')` ต้นสคริปต์ที่พิมพ์ไทย
- อย่าทำหน้าอื่นพัง

## ตรวจก่อนจบ (ต้องรันจริง)
```
python merge_research.py && python build_site.py && python make_og.py
python validate_site.py
```
แล้วรัน `python preview_site.py 8096` พื้นหลัง เปิด `http://127.0.0.1:8096/takuapa/map/` ด้วย Playwright (ติดตั้งแล้ว)
ตรวจ: ไม่มี console error · นับจำนวน `.maplibregl-marker` ต้องได้ 20 · กดฟิลเตอร์แล้วจำนวนเปลี่ยน · ถ่าย screenshot 1440px และ 390px เก็บที่ `qa/2026-09-07-phase4/`
ตรวจ noscript fallback ด้วย context ที่ปิด JavaScript

รายงานท้ายงาน: ไฟล์ที่แก้/สร้าง (path เต็ม) · ผลตรวจทุกคำสั่ง · path screenshot · ปัญหาที่เจอ
