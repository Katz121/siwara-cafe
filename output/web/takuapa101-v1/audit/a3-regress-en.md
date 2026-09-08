# A3 · ตรวจ regression หน้าอังกฤษ

ตรวจวันที่ 2026-09-08 · เสิร์ฟด้วย `python -m http.server 8798 --directory site` · ตรวจบน `http://127.0.0.1:8798`

## สรุป

ตรวจแล้วไม่พบปัญหา regression ที่ยืนยันได้จากรอบแก้ล่าสุดในขอบเขตที่กำหนด

## 1. เปิดหน้าอังกฤษ 10 หน้า

ตรวจด้วย Playwright ที่ `/en/`, `/en/eat/`, `/en/map/`, `/en/trip/`, `/en/news/`, `/en/traditions/`, `/en/stories/`, `/en/places/`, `/en/places/wat-sena/`, `/en/places/food-center/`

- Console error: ไม่พบทั้ง 10 หน้า
- Network response สถานะ 4xx/5xx: ไม่พบทั้ง 10 หน้า
- ล้นแนวนอน: ไม่พบ · ทุกหน้าที่ตรวจมี `document.documentElement.scrollWidth = 1280` และ `clientWidth = 1280`

หลักฐาน: ผล Playwright จากทั้ง 10 URL ข้างต้น · ไฟล์หน้าเว็บอยู่ใน `site/en/**/index.html`

## 2. attribute และโครงสร้าง HTML

ตรวจไฟล์อังกฤษครบ 44 หน้า (`site/en/**/index.html`)

- พบ `=""` ในทุกหน้าที่ตรวจ แต่เป็น attribute ว่างที่ระดับ `<html>` เท่านั้น คือ `data-base="" data-news-api=""` · ไม่ใช่เครื่องหมายคำพูดซ้อน และไม่ทำให้ HTML เสีย
- ตรวจ parse ด้วย lxml ครบ 44 ไฟล์ · ไม่พบ parse error
- ไม่พบรูปแบบ tag เปิดซ้อนผิดหรือ closing tag ที่ทำให้ parser อ่านโครงสร้างเสีย

หลักฐาน: `site/en/index.html:1` และรูปแบบเดียวกันใน `site/en/**/index.html:1` · ผล parse ครบ 44 ไฟล์ไม่มี error

## 3. UI translation และ aria-label

ตรวจจาก DOM ที่ render จริงของ 10 หน้า

- ป้าย UI ภาษาอังกฤษถูกวางใน element ที่สอดคล้องกับหน้าที่ เช่น `Main menu`, `Open menu`, `Search website (Press Ctrl+K)`, `Filter the news`, `Zoom in`, `Zoom out`, `Toggle attribution`, `On this page`
- ไม่พบ `aria-label` ที่แปลผิดบริบทจากรายการที่ตรวจ
- ป้ายบนหมุดแผนที่ใช้ `Map marker` ซ้ำตามชนิด element เดียวกัน · ไม่ใช่ข้อความผิดบริบท

หลักฐาน: ค่า `[aria-label]` จาก Playwright ของ `/en/`, `/en/eat/`, `/en/map/`, `/en/trip/`, `/en/news/`, `/en/traditions/`, `/en/stories/`, `/en/places/`, `/en/places/wat-sena/`, `/en/places/food-center/`

## 4. Google Maps

ตรวจลิงก์ Google Maps ที่แสดงในหน้าอังกฤษ โดยหน้า `site/en/eat/index.html:1` มีลิงก์ Maps 105 รายการ (105 URL ไม่ซ้ำ) ซึ่งรวมชุดร้านที่เพิ่มเข้ามา

- URL ที่ตรวจมีรูปแบบ `https://www.google.com/maps/search/?api=1&query=...`
- ค่า `query` ถูก percent-encode สำหรับชื่อภาษาไทย/อักขระพิเศษ · ไม่พบ query ว่างหรือ URL ที่มีอักขระไทยดิบ
- สุ่มเปิด 5 เส้นแรกด้วย Playwright แล้วได้ HTTP 200 ทุกเส้น

หลักฐาน: `site/en/eat/index.html:1` · URL ตัวอย่างที่ตรวจเริ่มจาก query ของ `ขนมจีนป้าม่อม`, `ขนมจีนพี่เหน่ง`, `ขนมจีนในนา`, `คาคีนอส เขาหลัก`, `ทับทิม ติ่มซำ` · ผลตอบกลับตามลำดับ `200, 200, 200, 200, 200`

## 5. SEO metadata

ตรวจไฟล์อังกฤษครบ 44 หน้า

- ทุกหน้ามี `<title>` ไม่ว่าง
- ทุกหน้ามี `meta[name="description"]` ไม่ว่าง
- ทุกหน้ามี canonical
- ทุกหน้ามี hreflang อย่างน้อย `th`, `en`, `x-default`
- ทุกหน้ามี `<html lang="en">`

หลักฐาน: ผลตรวจ DOM/HTML ครบ 44 ไฟล์ใน `site/en/**/index.html` · ตัวอย่าง `/en/`: title `Takua Pa Old Town Guide · Phang Nga, Thailand · Takua Pa 101`, canonical `https://takuapa101.com/en/`, hreflang ครบ 3 ค่า

