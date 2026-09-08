# รายงานตรวจ SEO และเทคนิค · takuapa101.com

ตรวจจากไฟล์ build ใน `site/` จำนวน 88 หน้า และตรวจ production จริงด้วย HTTP เมื่อ 2026-09-08
(`https://takuapa101.com/`, `/en/`, `/sitemap.xml` ตอบ HTTP 200 ทั้งหมด) · รายงานนี้เป็นผลตรวจเท่านั้น ไม่มีการแก้ไฟล์ต้นฉบับ

## สรุปผล

- **ผิด:** canonical/hreflang ของหน้าอังกฤษหลัก `/en/` ขาด trailing slash และชี้คู่ภาษาเป็น URL ที่ไม่ตรงกับ route แบบมี slash
- **ผิด:** title เกิน 60 ตัวอักษร 11 หน้า · meta description เกิน 160 ตัวอักษร 3 หน้า
- **ผิด:** heading ข้ามระดับ 12 หน้า (ฝั่งไทยและอังกฤษเป็นชุดเดียวกัน)
- **ผิด:** sitemap มี 89 URL แต่มีหน้า build 88 หน้า และ `/rest/` ซ้ำ 2 ครั้ง
- **ข้อสังเกต:** JSON-LD parse ผ่านทั้งหมดที่ตรวจ · ทุกหน้ามี h1 เดียว · ไม่พบ img ที่ขาด `alt` หรือชี้ไฟล์ภาพไม่มีจริง · ไม่พบ title/description ซ้ำกัน
- **ข้อจำกัด:** ไม่มี browser session ให้เปิดดู DOM ที่ render หลัง JavaScript ได้ จึงใช้ HTTP response ของ production ประกอบกับ HTML build ที่ deploy; ข้อมูลเมตาใน response หลักสอดคล้องกับ build

## 1) Title

ไม่พบ title ว่างและไม่พบ title ซ้ำกันใน 88 หน้า (หลักฐาน: ตรวจ `<title>` ทุก `site/**/index.html`). พบเกิน 60 ตัวอักษร 11 หน้า:

| URL | ความยาว |
|---|---:|
| `/` | 62 |
| `/en/places/kue-chai/` | 69 |
| `/en/places/wat-boromthat/` | 75 |
| `/en/places/wat-khuha/` | 64 |
| `/en/places/wat-kongkha/` | 66 |
| `/en/places/wat-pathum/` | 65 |
| `/en/places/wat-sena/` | 64 |
| `/en/stories/` | 62 |
| `/en/traditions/chak-phra/` | 61 |
| `/en/traditions/narai-ceremony/` | 64 |
| `/en/traditions/vegetarian/` | 63 |

หลักฐานหน้า representative อยู่ใน `site/index.html:1`, `site/en/places/kue-chai/index.html:1` และไฟล์ตาม URL ข้างต้น (HTML build เป็นบรรทัดเดียว)

## 2) Meta description

ไม่พบ description ว่างและไม่พบค่าซ้ำกัน พบเกิน 160 ตัวอักษร 3 หน้า:

- `/en/routes/` · 164 · `site/en/routes/index.html:1`
- `/en/traditions/` · 165 · `site/en/traditions/index.html:1`
- `/en/places/` · 187 · `site/en/places/index.html:1`
- `/en/` ยังเป็นภาษาอังกฤษตามที่ควรเป็น; หน้าอังกฤษที่มีชื่อหน่วยงานไทยคงไว้ถูกนับเป็นข้อยกเว้นตาม SPEC

ตรวจภาษาเนื้อหาเมตาแล้วไม่พบ description หน้าอังกฤษที่เป็นภาษาไทยทั้งหมด แต่หน้าอังกฤษบางหน้ามีชื่อ/ข้อความหน่วยงานไทยในเนื้อหา ซึ่งเป็นข้อยกเว้นที่ระบุไว้ใน SPEC

## 3) Canonical

เกือบทุกหน้าชี้ self URL บน `https://takuapa101.com` ถูกต้องตาม route แบบมี slash ยกเว้น `/en/`:

- `site/en/index.html:1` มี `canonical` เป็น `https://takuapa101.com/en` แต่ไฟล์ route จริงคือ `/en/`
- production `https://takuapa101.com/en/` ตอบ 200 แต่ canonical ใน HTML ยังไม่มี slash

ควรเลือก convention เดียวให้ route, canonical และ hreflang ตรงกันทั้งหมด

## 4) Hreflang

ทุกหน้ามี `th`, `en`, `x-default` ครบ แต่มีปัญหาที่หน้า root ภาษาอังกฤษและ pattern ของ x-default:

- `/en/` ใน `site/en/index.html:1` ชี้ `th=https://takuapa101.com`, `en=https://takuapa101.com/en`, `x-default=https://takuapa101.com` ขณะที่คู่หน้าที่ deploy คือ `/` และ `/en/`
- หน้าคู่อื่น ๆ มี th/en เป็นคู่กันถูกหน้า ไม่ได้ชี้กลับไปหน้าแรก เช่น `/places/...` ↔ `/en/places/...`
- `x-default` ของหน้าคู่ส่วนใหญ่ชี้ URL ภาษาไทยของหน้านั้นซ้ำกับ `th` (ตัวอย่าง `site/places/culture-street/index.html:1` และ `site/en/places/culture-street/index.html:1`) จึงไม่ใช่ default ที่เป็นกลาง/คู่ภาษาอังกฤษ หากนโยบายของเว็บกำหนด x-default เป็นภาษาอังกฤษหรือ landing กลาง ควรแก้ให้เป็นค่าเดียวตามนโยบาย

## 5) JSON-LD

ตรวจ script `application/ld+json` ทุก 88 หน้า: JSON parse ผ่านทั้งหมด, ทุก object มี `@type`, และไม่พบค่า top-level ที่เป็น `null`, string ว่าง หรือ array ว่าง

ตัวอย่างที่ตรวจได้จาก `site/index.html:1`: `BreadcrumbList`, `WebSite`, `ItemList` มี type และ URL ครบถ้วน ไม่พบ rich-result field ว่างจากการตรวจนี้

## 6) Sitemap

`site/sitemap.xml:1` มี 89 `<loc>` แต่ build มี 88 หน้า และตรวจ path แล้วทุก URL มีไฟล์ปลายทางใน `site/` พบรายการซ้ำ:

- `https://takuapa101.com/rest/` ปรากฏ 2 ครั้ง

ไม่พบ URL ใน sitemap ที่ไม่มีหน้า build รองรับ และ production endpoint `https://takuapa101.com/sitemap.xml` ตอบ 200

## 7) ลิงก์ภายใน

ตรวจ href ที่เป็น path ภายในและเทียบกับหน้าใน `site/` โดยไม่นับ asset/file download เป็นหน้าเว็บ พบ 1 ลิงก์ผิด:

- `site/en/index.html:1` มีลิงก์ `/en/en` ซึ่งไม่มี `site/en/en/index.html`

ลิงก์ asset เช่น `/assets/...` ถูกแยกออกจากการตรวจลิงก์หน้าเว็บ และไฟล์ปลายทางมีอยู่จริงตามข้อ 8

## 8) รูป

ตรวจ `<img>` ทุกหน้า:

- ไม่พบ `<img>` ที่ไม่มี attribute `alt`
- ไม่พบ `src` ของรูปที่ไม่มีไฟล์จริงใน `site/`
- พบ `alt=""` บางรูปที่ใช้เป็นภาพประกอบตกแต่ง/thumbnail; การตรวจนี้ไม่จัดเป็น “ไม่มี alt” เพราะ attribute มีอยู่แล้ว

## 9) Keyword stuffing

ไม่พบลิสต์คำค้นที่แสดงเป็นบล็อก keyword บนหน้า และไม่พบ title/description ซ้ำกันหรือข้อความที่ผิดธรรมชาติจากการยัดคำแบบรายการคำค้น

คำว่า `Takua`/`Takua Pa` ปรากฏถี่ใน title/description เพราะเป็นชื่อสถานที่และแบรนด์ของเว็บ ไม่ถือเป็น stuffing จากหลักฐานที่ตรวจได้; ไม่พบ pattern คำเดิมซ้ำติดกันหรือ title/description ที่เป็นเพียงลิสต์คำค้น

## 10) Heading

ทุกหน้ามี h1 เดียว แต่พบการข้ามระดับ heading ดังนี้:

- `/places/` และ `/en/places/`: ลำดับ `h1 → h3 ... → h2` (มีการเริ่ม h3 ก่อน h2)
- story detail ทั้ง 5 เรื่อง ทั้งไทยและอังกฤษ: มี `h2 → h4` ในส่วนเนื้อหา/การ์ด โดยไม่มี h3 คั่น
- รายชื่อไฟล์หลัก: `site/places/index.html:1`, `site/en/places/index.html:1`, `site/stories/architecture/index.html:1`, `site/en/stories/architecture/index.html:1` และ story detail อื่นตาม pattern เดียวกัน

## ลำดับแก้ที่แนะนำ

1. แก้ `/en/` ให้ canonical และ hreflang ใช้ `/en/` และ `/` แบบมี slash ให้สอดคล้องกัน พร้อมทบทวน policy ของ `x-default`
2. ตัด title/description ที่เกินขอบเขต โดยคง intent และชื่อสถานที่ไว้
3. แก้ `/en/en` เป็น `/en/`
4. ลบ `<url>` ซ้ำของ `/rest/` ใน sitemap
5. ปรับ heading ของ places/story ให้ไม่ข้ามระดับ
