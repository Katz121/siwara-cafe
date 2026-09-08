# รายงานตรวจโค้ดและความถูกต้องของการ build

ตรวจตาม `audit/SPEC.md` โดยไม่แก้ไฟล์โค้ด · ตรวจเว็บจริงที่ `https://takuapa101.com` วันที่ 2026-09-08

## สรุป

- **ผิด** · เว็บล้นแนวนอนที่ viewport 390px ทุกหน้าที่กำหนด
- **ผิด** · ตะกร้าทริปเพิ่มจุดหมายไม่ได้จริง เพราะ `trip.js` ถูกโหลดซ้ำ
- **ผิด** · Python ในโฟลเดอร์หลักมีไฟล์ที่เป็น UTF-16 ซึ่ง Python อ่านเป็น source ปกติไม่ได้
- **ข้อสังเกต** · `build_en.py` จบสำเร็จ แต่รายงานคำแปลที่ยังไม่มี 71 แบบ
- หัวข้ออื่นที่ตรวจแล้วไม่พบปัญหา: build exit code, JavaScript syntax, console error/HTTP 4xx-5xx, theme persistence และ CSS display/media cascade ที่ตรวจใน runtime

## 1. Build

### ตรวจแล้วไม่พบปัญหา

- `python build_site.py` · exit 0 · output: `Built 45 pages, 20 places, 7 traditions, 59 directory entries.`
- `python build_en.py` · exit 0 · output: `สร้างหน้าอังกฤษ 44 หน้า · ข้าม 0 หน้า`

### ข้อสังเกต

`build_en.py` รายงาน `ข้อความที่ยังไม่มีคำแปล 71 แบบ` และเขียนไปที่ `data/i18n/en/missing.json` · เป็นสถานะข้อมูลคำแปลที่ build รายงาน ไม่ใช่ build error

## 2. Python ในโฟลเดอร์หลัก

### ตรวจแล้วไม่พบปัญหาเรื่อง top-level นิยามซ้ำ

ตรวจ AST ของไฟล์ `*.py` ในโฟลเดอร์หลักและตรวจชื่อ `FunctionDef`, `AsyncFunctionDef`, `ClassDef` ระดับไฟล์ · ไม่พบฟังก์ชัน/คลาสระดับ top-level ซ้ำแบบ `render_rest` ที่ตัวหลังทับตัวแรก

`build_en.py:208` และ `build_en.py:226` มี nested function ชื่อ `sub` เหมือนกัน แต่คนละ scopeใน `translate_attrs()` และ `repoint_links()` · ไม่ใช่นิยามซ้ำที่ทับกัน

### ผิด · source encoding ของ Python บางไฟล์ไม่ใช่ UTF-8 ที่ Python ใช้งานได้ตามปกติ

- `build_site_backup.py` และ `build_site_original.py` เริ่มด้วย UTF-16 BOM (`FF FE`) · AST parse ด้วย UTF-8 ล้มเหลวทันที
- `make_og.py`, `place_pages.py`, `preview_site.py`, `seo.py`, `seo_config.py`, `validate_phase3.py`, `validate_seo.py` มี UTF-8 BOM · ทำให้ `ast.parse()` ที่อ่านเป็น text ปกติรายงาน `invalid non-printable character U+FEFF`

หลักฐานคำสั่ง: สแกน bytes และ parse AST ของ `*.py` ในโฟลเดอร์หลัก · ไฟล์ข้างต้นคือไฟล์ที่ตรวจพบจริง

## 3. JavaScript syntax

### ตรวจแล้วไม่พบปัญหา

รัน `node --check` กับไฟล์ JavaScript ทุกไฟล์ใน `site/assets/` · ผ่านทั้งหมด (`ALL_JS_SYNTAX_OK`)

## 4. ข้อความไทยเสียรูป

### ตรวจแล้วไม่พบ `???` หรือ mojibake ใน Python source ที่สแกน

สแกนไฟล์ Python โฟลเดอร์หลักหา literal `???`, U+FFFD และ marker mojibake แบบ UTF-8 ที่พบบ่อย · ไม่พบข้อความเหล่านี้

พบปัญหา encoding ตามข้อ 2 คือ BOM/UTF-16 ของไฟล์ source ไม่ใช่ข้อความไทยกลายเป็น `???`

## 5. CSS

### ตรวจแล้วไม่พบปัญหา display/media query ที่ทำให้กฎแรกไม่มีผลโดยไม่ตั้งใจ

ตรวจ rules และ computed layout บนเว็บจริง · `theme.css:127-132` มี `theme-toggle { display:none }` ที่ max 1080px แล้ว `display:grid` ที่ max 900px ซึ่งเป็น override ตามลำดับ breakpoint ที่ตั้งใจและทำงานจริงบน 390px

อย่างไรก็ตามพบผลลัพธ์ layout ผิดจริงในข้อ 6 · สาเหตุที่ตรวจพบจาก computed DOM คือ `.header-tools` กว้างเกิน viewport ที่ 390px ไม่ใช่การสรุปจาก duplicate declaration เพียงอย่างเดียว

## 6. เว็บจริง · Playwright

ใช้ Playwright ผ่าน Python package เพราะ Node workspace ไม่มีโมดูล `playwright` (`Cannot find module 'playwright'`) · ตรวจครบ 8 URL ที่ 1440px และ 390px:

`/`, `/places/tao-ming/`, `/map/`, `/rest/`, `/eat/`, `/news/`, `/trip/`, `/en/`

### ตรวจแล้วไม่พบปัญหาที่ 1440px

- ทั้ง 8 URL ใน viewport นี้ไม่มี console error
- ไม่มี response 4xx/5xx
- `document.documentElement.scrollWidth === clientWidth === 1440` ทุกหน้า

### ผิด · ล้นแนวนอนที่ 390px

- ทุกหน้าไทยทั้ง 7 URL มี `scrollWidth = 411`, `clientWidth = 390`
- `/en/` มี `scrollWidth = 417`, `clientWidth = 390`
- element ที่ล้นชัดเจนคือ `.header-tools` · หน้าภาษาไทย `right = 410.96875` และหน้าอังกฤษ `right = 417.328125`
- หลักฐาน CSS ที่เกี่ยวข้อง: `site/assets/ui.css:18` กำหนด `.header-tools { display:flex; ... }`; `site/assets/theme.css:119-132` ปรับ gap/ซ่อนปุ่มบางตัว แต่ไม่ลดความกว้างรวมให้พอดี 390px

## 7. โหมดกลางคืน

### ตรวจแล้วไม่พบปัญหา

บน `/` ที่ 390px คลิกปุ่ม `[data-theme-toggle]` แล้ว `html[data-theme]` เปลี่ยนเป็น `dark` · ไป `/rest/` แล้วค่ายังเป็น `dark`

หลักฐานโค้ด: `site/assets/theme.js:4` ใช้ key `takuapa-theme`; `site/assets/theme.js:12-13` ตั้ง/ลบ `data-theme` และ event click อยู่ที่ `site/assets/theme.js:25-35`

## 8. ตะกร้าทริป

### ผิด · เพิ่มและลบจุดหมายไม่ได้จริงบนเว็บ

ทดสอบที่ `https://takuapa101.com/stories/water-trade/`:

- พบปุ่ม `[data-trip-add]` 4 ปุ่ม เช่น `data-trip-add="riverwalk"`
- ก่อนคลิก count เป็น `0`
- หลังคลิกปุ่มแรก count ยังเป็น `0` และ `localStorage['takuapa-trip']` เป็น `[]`
- ไป `/trip/` แล้วพบ `[data-remove]` 0 ปุ่ม ไม่มีรายการให้ลบ

หลักฐานสาเหตุ:

- `site/stories/water-trade/index.html` มี `<script src="/assets/trip.js" defer>` สองครั้ง
- `design.py:366` เติม `trip.js` ในชุด asset ใหม่ ขณะที่ template ที่สร้างหน้าดังกล่าวมี `trip.js` อยู่แล้ว
- `site/assets/trip.js:130-135` ผูก click handler กับ `[data-trip-add]`; การโหลด script ซ้ำทำให้ handler ทำงานสองรอบ · รอบแรก add และรอบที่สอง remove จึงเหลือ `[]`

## Verdict

**fix-then-ship** · ต้องแก้การโหลด `trip.js` ซ้ำและแก้ overflow ของ header ที่ 390px ก่อน เพราะผู้ใช้เพิ่มจุดหมายไม่ได้และหน้าเว็บล้นแนวนอนจริง
