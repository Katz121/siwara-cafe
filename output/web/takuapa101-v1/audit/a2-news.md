# รายงานตรวจระบบข่าวอัตโนมัติ

ตรวจไฟล์ `worker/src/index.js`, `worker/src/filter.js`, `worker/src/recheck.js`, `worker/src/sources.js`, `worker/wrangler.toml` และยิง endpoint production วันที่ 2026-09-08 · ไม่แก้ไฟล์ระบบตามกติกาใน `audit/SPEC.md`

## สรุป

- พบ `ผิด` 1 รายการ: ค่า `place_id` จาก AI ที่เป็นสตริง `"null"` หลุดเข้า feed จริง ทำให้ข้อมูลสถานที่ไม่เป็น null ตามสัญญาข้อมูล · หลักฐานคือผล `/api/news` รายการแรกมี `"place_id":"null"` และเส้นทางโค้ดใน `worker/src/recheck.js:121-128`
- พบ `ควรแก้` 1 รายการ: parser สำรองของคำตอบ AI ใช้ byte `0x08` แทน `\\b` จึงกู้คำตอบที่ไม่ใช่ JSON ตรงรูปแบบไม่ได้ · ระบบจะพักข่าวไว้ ไม่ปล่อยข่าวผิดขึ้นเว็บ แต่เสียข่าวที่อาจตรวจได้
- หัวข้อ feed ล่ม/503: ตรวจแล้วไม่พบปัญหาในเส้นทางแหล่งข้อมูล · แต่ไม่ได้ทดสอบรัน Worker จริงด้วยการบังคับ 503 เพราะไม่มีสิทธิ์เปลี่ยน upstream หรือ inject fetch ใน production
- สุ่มตรวจลิงก์บทความจริงได้ 4/5 เส้น · 4 เส้นตอบ HTTP 200/403 และไปถึงโดเมนบทความตาม URL ที่คืนมา · 1 เส้น timeout จึงตรวจไม่ได้ ไม่สรุปว่าเสีย
- ตรวจโค้ด deploy แล้วไม่พบค่าคีย์ลับฝังอยู่ในไฟล์ · พบเพียงชื่อ environment secret และค่า KV/vars ที่ไม่ใช่ secret

## 1) การกันข่าวซ้ำ

### ควรแก้ · fingerprint ไม่ normalize/unwrap ลิงก์ก่อนสร้าง seen key

หลักฐาน: `worker/src/filter.js:84-87` สร้าง fingerprint จาก `(item.link || '')` ดิบและหัวข้อ ขณะที่ `worker/src/filter.js:40-46` มี `urlKey()` ที่ unwrap Bing และตัด `www.`/slash ท้าย URL แล้ว · ดังนั้นบทความเดียวกันที่เข้ามาครั้งหนึ่งเป็น Bing wrapper และอีกครั้งเป็นลิงก์ตรงจะได้ fingerprint คนละค่า แม้ dedupe ภายในรันเดียวกันจะใช้ `urlKey` ที่ `worker/src/index.js:159-164` ก็ตาม

ผลกระทบที่ตรวจได้จากเส้นทางโค้ด: `seen:index` กันซ้ำข้ามรันด้วย fingerprint แต่ไม่ใช่ canonical URL · ข่าวที่ wrapper เปลี่ยนรูปจึงไม่ถูกกันด้วย seen key ข้ามรัน แม้ระบบยังมี title dedupe บางส่วน

การตรวจยืนยันซ้ำจาก production ทำได้เพียงอ่าน `/api/news` ไม่สามารถจำลอง KV หลายรอบโดยไม่แก้/รันระบบจริง · ข้อสรุปนี้อ้างจาก source trace โดยตรง

### ตรวจแล้วไม่พบปัญหา · dedupe ภายในชุด candidates และก่อน publish

หลักฐาน: `worker/src/index.js:147-165` ตรวจ fingerprint, URL และ title กับ live/current candidates; `worker/src/index.js:192-200` ตรวจ title ซ้ำอีกครั้งหลัง AI เปลี่ยนหัวข้อก่อนใส่ live

## 2) การแกะลิงก์ Bing

### ตรวจแล้วไม่พบปัญหาในกรณี URL query มาตรฐาน

หลักฐาน: `worker/src/filter.js:25-36` decode entities ก่อนหา `?url=`/`&url=`, decode ค่าและคืนเฉพาะ `http/https`; `worker/src/index.js:47-48` เรียก `unwrapLink()` ก่อนยอมรับรายการ; `worker/src/filter.js:40-46` เรียกซ้ำตอนสร้าง URL key

ข้อจำกัดที่ตรวจพบจากโค้ด: regex `url=([^&\\s]+)` จะตัดค่าที่มี ampersand แบบไม่ percent-encode · ไม่มีตัวอย่าง production ให้ทดสอบกรณีนี้ จึงไม่จัดเป็นปัญหาที่เกิดขึ้นจริง

## 3) feed ต้นทางล่มหรือคืน 503

### ตรวจแล้วไม่พบปัญหาในเส้นทางข้ามแหล่งข้อมูล

หลักฐาน: `worker/src/index.js:62-74` ครอบแต่ละ Bing query ด้วย `try/catch`; `worker/src/index.js:76-87` ครอบแต่ละ outlet feed แยกกัน; `worker/src/index.js:89-129` ครอบแต่ละ direct/first-party source แยกกัน · `fetchText()` ที่ `worker/src/index.js:36-39` throw เมื่อ `!r.ok` รวมถึง 503 แล้ว catch ของรายการนั้นจะ `continue`

ดังนั้น 503 ของหนึ่ง feed ไม่ทำให้ harvest ทั้งระบบหยุด · หาก KV เขียนล้มเหลวภายหลังที่ `worker/src/index.js:210-213` จะทำให้ run ล้มได้ แต่เป็นคนละกรณีกับ upstream feed และยังไม่ได้ทดสอบจริง

## 4) AI ตอบผิดรูปแบบและโอกาสข่าวผิดหลุด

### ควรแก้ · salvage parser ใช้ตัวคั่นผิด แต่ผลที่ตรวจได้คือ fail-safe

หลักฐาน: `worker/src/recheck.js:25-40` มี regex ที่ไฟล์จริงเป็น byte `08` รอบคำว่า `publish|hold|drop` ไม่ใช่ regex word boundary `\\b` · จึงไม่ match verdict ในข้อความ prose/code fence ที่ไม่มี JSON object สมบูรณ์

ผลตามเส้นทางจริง: `parseVerdict()` ที่ `worker/src/recheck.js:43-63` จะคืน null เมื่อ salvage ไม่สำเร็จ · `recheck()` ที่ `worker/src/recheck.js:116-119` แปลงเป็น `verdict:'hold', confidence:0` · `bucketOf()` ที่ `worker/src/recheck.js:133-136` ส่งเข้า held ไม่ใช่ live ดังนั้นจากโค้ดนี้ยังไม่พบช่องให้คำตอบผิดรูปแบบหลุดขึ้นเว็บ

### ผิด · ค่า `place_id` สตริง `"null"` หลุดเข้า public feed

หลักฐานจาก production: `GET https://takuapa101-news.siwatid-99.workers.dev/api/news` ตอบรายการแรก `title_th:"ตะกั่วป่าจัดทิ้งกระจาด ครั้งที่ 14` พร้อม `place_id:"null"` (เป็นสตริง ไม่ใช่ JSON null)

หลักฐานจากโค้ด: `worker/src/recheck.js:125` ใช้ `v.place_id || item.place_id || null` · ค่า string `"null"` เป็น truthy จึงถูกเก็บต่อที่ `worker/src/index.js:184` และ serialize ออกที่ `worker/src/index.js:231`

## 5) ตรวจลิงก์ production แบบสุ่ม 5 เส้น

URL ที่สุ่มจาก `/api/news` และผลตรวจด้วย `curl -L --ssl-no-revoke --max-time 12`:

| URL | ผล HTTP | ผลตรวจ |
|---|---:|---|
| `https://www.naewna.com/n/national-news/48965/` | timeout | ตรวจไม่ได้เพราะปลายทางไม่ส่งข้อมูลภายใน 12 วินาที |
| `https://siamrath.co.th/regional/news/142138` | 200 | ไปถึงปลายทาง |
| `https://mgronline.com/south/photo-gallery/9690000008004` | 403 | ไปถึงเว็บไซต์ แต่ปลายทางปฏิเสธการเข้าถึงจากสภาพแวดล้อมตรวจ |
| `https://www.topnews.co.th/news/1368822` | 200 | ไปถึงปลายทาง |
| `https://www.naewna.com/local/825858` | 200 | ไปถึงปลายทาง |

ลิงก์ 403 ยังยืนยันได้ว่าโดเมน/เส้นทางตอบกลับจริง แต่ตรวจเนื้อหาบทความไม่ได้ · ลิงก์ timeout ก็ตรวจเนื้อหาไม่ได้ · ไม่รายงานว่าเป็นลิงก์เสีย

## 6) ข้อมูลลับหรือคีย์ที่หลุดในโค้ด deploy

### ตรวจแล้วไม่พบปัญหา

หลักฐาน: `worker/src/recheck.js:65-78` อ่าน `env.ANTHROPIC_API_KEY` จาก secret และไม่ฝังค่า; `worker/src/index.js:297-303` อ่าน `env.RUN_KEY`; `worker/wrangler.toml:14-22` มีเพียง allowed origins, limits และ AI binding ไม่มีค่า API key/token; `worker/src/sources.js:33-34` เป็นข้อความบอกชื่อ secret เท่านั้น

การตรวจนี้ครอบคลุม source และ `wrangler.toml` ใน workspace · ตรวจค่า secret ที่เก็บอยู่บน Cloudflare จริงไม่ได้เพราะไม่มีสิทธิ์เข้าถึง secret store และ endpoint ที่อ่านได้ไม่เปิดเผยค่าเหล่านั้น

## ข้อสรุป

ระบบมี fail-safe เมื่อ AI ตอบผิดรูปแบบและข้าม feed ที่คืน 503 ได้ · รายการที่ต้องแก้ก่อนคือการแปลง `"null"` เป็น null/ตรวจค่า `place_id` ให้ถูกชนิด และควรแก้ salvage regex เพื่อไม่ทิ้งข่าวที่ AI ตอบเป็น prose หรือ JSON ไม่สมบูรณ์ · การตรวจลิงก์ครบ 5 เส้นทำไม่ได้ 1 เส้นเพราะ timeout จึงระบุไว้ตามกติกา ไม่สรุปเกินหลักฐาน
