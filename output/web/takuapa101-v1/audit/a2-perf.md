# รายงานตรวจน้ำหนักและความเร็ว

ตรวจจากไฟล์ใน `site/` และเซิร์ฟเวอร์ `python -m http.server 8799 --directory site` ที่ `http://127.0.0.1:8799` · วัด runtime ด้วย Playwright Chromium headless · ตรวจวันที่ 8 กันยายน 2569

## สรุป

- พบไฟล์ใน `site/assets/` ที่เกิน 300KB จำนวนมาก โดยตัวหนักสุดคือ PDF 7.75MB, รูป JPG 4.71MB และแผนที่ PNG 1.83MB
- รูปทั้งหมด 316 จุดใน HTML · มี width และ height ครบ 182 จุด · ขาดอย่างน้อยหนึ่งค่า 134 จุด
- รูป 252 จุดมี `loading="lazy"` · 64 จุดไม่มี · การไม่มี lazy ไม่ใช่ปัญหาเสมอไปสำหรับรูป above-the-fold แต่ควรทบทวนกลุ่มรูปยาวในหน้า eat/rest และ leaflet
- หน้า HTML ที่ใหญ่สุดคือ `site/eat/index.html` 89.0KB
- มีฟอนต์ local แบบใช้งานจริง 3 ไฟล์ WOFF2 · มีไฟล์ต้นฉบับ TTF ซ้ำอีก 3 ไฟล์ใน assets แต่ runtime ไม่ได้โหลด TTF

## 1. ขนาดไฟล์ `site/assets/`

เกณฑ์ตรวจ: `Length > 307200` bytes · หลักฐานจากรายการไฟล์จริงเรียงจากใหญ่ไปเล็ก

ไฟล์ที่เกิน 300KB ที่เด่นและควรพิจารณาลด:

| ไฟล์ | ขนาดโดยประมาณ | แนวทางลด |
|---|---:|---|
| `site/assets/leaflet/takuapa-walk-leaflet.pdf` | 7,746.6KB | ลดความละเอียดภาพฝังและบีบอัด PDF สำหรับการดาวน์โหลด · ถ้าต้องคงต้นฉบับ ให้แยกไฟล์ดาวน์โหลดคุณภาพสูงออกจาก preview |
| `site/assets/guide/guide-tam-nang.jpg` | 4,705.3KB | แปลงเป็น WebP/AVIF และกำหนดความกว้างตามการแสดงผล |
| `site/assets/municipal-map.png` | 1,828.0KB | ใช้ WebP/AVIF หรือ PNG-8 หากสีเหมาะสม · ทำ responsive variant |
| `site/assets/CormorantGaramond.ttf` | 1,167.5KB | ไม่พบการโหลด TTF ใน runtime · ลบออกได้เมื่อยืนยันว่าไม่ใช่ไฟล์ต้นฉบับที่ workflow ต้องเก็บ หรือเก็บไว้นอก public assets |
| `site/assets/guide/guide-iron-bridge.jpg` | 813.3KB | แปลงเป็น WebP/AVIF และลดขนาดตามกล่องภาพ |
| `site/assets/guide/guide-bang-deen.jpg` | 691.2KB | แปลงเป็น WebP/AVIF และลดขนาดตามกล่องภาพ |
| `site/assets/guide/guide-lad-yai.jpg` | 539.3KB | แปลงเป็น WebP/AVIF และลดขนาดตามกล่องภาพ |
| `site/assets/guide/guide-pa-da-hokkien.jpg` | 479.2KB | แปลงเป็น WebP/AVIF และลดขนาดตามกล่องภาพ |
| `site/assets/guide/guide-tuangrat-taosor.jpg` | 472.2KB | แปลงเป็น WebP/AVIF และลดขนาดตามกล่องภาพ |
| `site/assets/guide/guide-baan-lapp.jpg` | 459.7KB | แปลงเป็น WebP/AVIF และลดขนาดตามกล่องภาพ |
| `site/assets/guide/guide-moo-satay-kruaew.jpg` | 456.9KB | แปลงเป็น WebP/AVIF และลดขนาดตามกล่องภาพ |

นอกจากนี้ไฟล์ OG PNG หลายไฟล์อยู่ราว 300 ถึง 444KB · เหมาะกับการลด palette/metadata หรือแปลงเป็น WebP หาก pipeline และแพลตฟอร์มแชร์รองรับ · ไม่ควรสรุปว่าเป็นปัญหา runtime ทุกหน้า เพราะ OG image มักถูกโหลดโดย crawler เมื่อแชร์ ไม่ใช่ browser page load ปกติ

## 2. width/height และ lazy loading ของรูป

หลักฐานจากการสแกน `<img>` ทุกไฟล์ HTML 88 หน้า:

- ทั้งหมด 316 จุด
- มีทั้ง `width` และ `height`: 182 จุด
- ขาดอย่างน้อยหนึ่งค่า: 134 จุด
- มี `loading="lazy"`: 252 จุด
- ไม่มี `loading="lazy"`: 64 จุด

กลุ่มที่ขาด dimensions ปรากฏใน `site/index.html`, `site/en/index.html`, `site/stories/index.html`, `site/en/stories/index.html`, กลุ่ม `stories/*`, `places/culture-street`, `places/riverwalk`, `places/tao-ming`, `rest` และ `leaflet` ทั้งไทย/อังกฤษ · ตัวอย่างหลักฐานจากหน้าแรก: `site/index.html` มีรูป `riverwalk.webp`, `culture-street.webp`, `iron-bridge.webp`, `food-center.webp`, `tao-ming.webp` ที่ไม่มี width/height ใน tag

64 จุดที่ไม่มี lazy กระจายอยู่ในกลุ่มหน้าแรก/หน้าเนื้อหาและหน้ารายการ · รูปสำคัญที่อยู่เหนือ fold อาจตั้งใจไม่ lazy ได้ แต่รูปที่อยู่ท้ายรายการควรทบทวนเป็นรายหน้า · จาก static scan เพียงอย่างเดียวระบุตำแหน่ง above-the-fold ทุก viewport ไม่ได้ จึงไม่ฟันธงว่าทั้ง 64 จุดผิด

คำแนะนำเชิงปฏิบัติ: เติม intrinsic dimensions หรือ `aspect-ratio` ให้รูปทุกใบก่อน · คงรูป hero ที่จำเป็นต่อการแสดงผลแรกเป็น eager ได้ · ใช้ lazy กับรูปที่อยู่นอก viewport เริ่มต้น

## 3. HTML ใหญ่ผิดปกติ · 5 อันดับ

เรียงจากขนาดไฟล์บนดิสก์:

1. `site/eat/index.html` · 89.0KB
2. `site/en/eat/index.html` · 77.2KB
3. `site/index.html` · 50.8KB
4. `site/news/index.html` · 50.1KB
5. `site/places/culture-street/index.html` · 49.2KB

สาเหตุที่ยืนยันได้จากโครงสร้างคือเนื้อหาและรายการถูก render ลง HTML แบบ static · ยังไม่พบหลักฐานเพียงพอที่จะเรียกว่าเป็นปัญหาความเร็วโดยตัวมันเอง เพราะ payload document ของหน้าแรกที่วัดจริงมี 52,026 bytes และ `/map/` มี 30,988 bytes

## 4. Playwright runtime

วัดด้วย Chromium headless, localhost, `wait_until="domcontentloaded"` · `content-length` รวมเฉพาะ response ที่ browser ได้รับและ header ระบุค่า · เวลาเป็นการวัดใน run นี้ ไม่ใช่ benchmark เครื่องผู้ใช้ทุกเครื่อง

| URL | requests | ขนาดรวม | DOMContentLoaded |
|---|---:|---:|---:|
| `/` | 21 | 3,749,736 bytes · 3.58MiB | 24.3ms |
| `/map/` | 45 | 6,378,410 bytes · 6.08MiB | 186.3ms |

หลักฐานสำคัญของ `/` คือโหลด `municipal-map.png` 1,871,863 bytes แม้เป็นรูปแผนที่ในหน้าแรก · รวมฟอนต์ WOFF2 190,488 bytes และรูปภาพเนื้อหาหลายใบ

หลักฐานสำคัญของ `/map/` คือโหลด MapLibre JS 203,149 bytes, รูปภาพสถานที่หลายใบ, `municipal-map.png` 1,871,863 bytes, sprite 49,454 bytes และ tile/vector/font requests จาก `tiles.openfreemap.org` · มี response บางรายการเป็น 0 bytes ตาม `content-length` จึงอาจต่ำกว่าขนาดถ่ายโอนจริงในกรณีที่ใช้ chunked/ไม่มี header

## 5. ฟอนต์

### ไฟล์ที่มีใน assets

- `NotoSerifThai.woff2` · 121.0KB
- `IBMPlexSansThaiLooped-Regular.woff2` · 28.1KB
- `CormorantGaramond.woff2` · 36.9KB
- มี TTF ซ้ำ: `NotoSerifThai.ttf` 285.3KB, `IBMPlexSansThaiLooped-Regular.ttf` 122.1KB, `CormorantGaramond.ttf` 1,167.5KB

### การใช้งาน

`site/assets/design.css:1-3` ประกาศ `@font-face` สำหรับ WOFF2 ทั้ง 3 family · `site/assets/site.css:1` ก็ประกาศชุดเดียวกันอีกครั้ง แต่หน้า runtime ที่ตรวจโหลด stylesheet หลักเป็น `design.css`, `ui.css`, `theme.css` · ใน run จริง `/` โหลด WOFF2 3 ไฟล์ และ `/map/` โหลด WOFF2 3 ไฟล์ รวม 190,488 bytes ต่อหน้า · ไม่พบการโหลด TTF จาก network

### preload

HTML มี preload สำหรับ `NotoSerifThai.woff2` และ `IBMPlexSansThaiLooped-Regular.woff2` · ทั้งสองไฟล์ถูกโหลดจริงใน `/` และ `/map/` จึงไม่พบ preload ที่ไม่ได้ใช้จากการตรวจนี้ · `CormorantGaramond.woff2` ถูกโหลดจริงแต่ไม่ได้ preload · ไม่พบหลักฐานว่าเป็นปัญหา จึงรายงานเป็นข้อสังเกต ไม่ใช่ข้อผิดพลาด

## ข้อจำกัดการตรวจ

- ไม่ได้แก้ไขไฟล์ใดนอกจากสร้างรายงานนี้ตามขอบเขตงาน
- ไม่ได้ทดสอบบนอุปกรณ์จริงหรือเครือข่ายช้า · ตัวเลขเวลาเป็น localhost headless run เดียว
- ไม่ได้วัด transfer size จาก compressed production server เพราะ `http.server` ไม่ได้ทำ Brotli/Gzip และบาง external response ไม่มี `content-length`
- ไม่ได้ตัดสินว่า lazy loading ของแต่ละรูป “ควรมี” จาก viewport ทุกแบบ · ตรวจได้เพียง presence ใน HTML และระบุจุดที่ควรทบทวนตามตำแหน่งเนื้อหา

## บทสรุป

พบโอกาสลดน้ำหนักที่ยืนยันได้จริง โดยเฉพาะ `takuapa-walk-leaflet.pdf`, `guide-tam-nang.jpg`, `municipal-map.png` และ TTF ที่ไม่ได้ถูกโหลด · ปัญหาความเสี่ยง layout shift ที่ยืนยันได้คือรูป 134 จุดขาด dimensions · runtime `/map/` หนักกว่า `/` ชัดเจนจาก MapLibre, tiles และรูปแผนที่ · ไม่ได้พบ preload ที่ไม่ได้ใช้จากการวัดนี้
