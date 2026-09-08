# รายงานตรวจลิงก์

ตรวจตาม `audit/SPEC.md` ด้วย Python HTTP HEAD และใช้ GET เป็นทางเลือกเมื่อ HEAD ใช้ไม่ได้ · ตรวจเมื่อ 2026-09-08 · ไม่แก้ข้อมูลต้นทาง

## 1) `source_url` ใน `data/places-enriched.json`

รวบรวมจากฟิลด์ `source_url` และ `source_urls` ทุกระดับ แล้วตัดรายการซ้ำ · พบทั้งหมด 134 URL ไม่ซ้ำ

### ลิงก์ที่พบว่าเสียหรือเปิดไม่ได้

หลักฐานด้านล่างคือผล HTTP โดยตรง · `404` = เซิร์ฟเวอร์ตอบว่าไม่พบ · `DNS` = หาโดเมนไม่พบ · `403/406` = เว็บปฏิเสธคำขอ จึงยังยืนยันว่าเนื้อหาปลายทางใช้ไม่ได้ไม่ได้

| ผลตรวจ | URL | หลักฐาน |
|---|---|---|
| 404 | https://www.dit.go.th/FILE/CONTENT_FILE/256202181736250948974.pdf | GET ตอบ HTTP 404 |
| 404 | https://www.dit.go.th/th/market/2383/%E0%B8%A0%E0%B8%B2%E0%B8%84%E0%B9%83%E0%B8%95/%E0%B8%9E-%E0%B8%87%E0%B8%87%E0%B8%87%E0%B8%B2/%E0%B8%96%E0%B8%99%E0%B8%99%E0%B8%A7-%E0%B8%92%E0%B8%99%E0%B8%98%E0%B8%A3%E0%B8%A3%E0%B8%A1%E0%B9%80%E0%B8%A1%E0%B8%AD%E0%B8%87%E0%B9%80%E0%B8%81-%E0%B8%B2%E0%B8%95%E0%B8%B0%E0%B8%81-%E0%B8%A7%E0%B8%9B-%E0%B8%B2/ | GET ตอบ HTTP 404 |
| 404 | https://radiothailand.prd.go.th/th/content/category/detail/id/9/iid/481052 | GET ตอบ HTTP 404 |
| เปิดไม่ได้ | https://www.takuacity.go.th/files/com_news_formdoc/2021-08_35dfd0d7b952500.pdf | GET: DNS lookup ล้มเหลว |
| เปิดไม่ได้ | https://www.takuacity.go.th/files/com_strategy/2022-12_231dcd9d5169573.pdf | GET: DNS lookup ล้มเหลว |
| เปิดไม่ได้ | https://www.takuacity.go.th/ | GET: DNS lookup ล้มเหลว |

ลิงก์ที่ตรวจไม่สำเร็จเนื่องจากปลายทางปฏิเสธคำขอ: `mapcarta.com` 5 รายการ, `books.classstart.org` 3 รายการ, `anyflip.com` 2 รายการ และ `www.innews.news/news.php?n=48726` · ตอบ 403 หรือ 406 · จึงรายงานว่าเปิดตรวจไม่ได้ ไม่จัดเป็น 404

มี URL บางรายการที่ Python ไม่สามารถส่งคำขอได้เพราะ URL มีอักขระไทยที่ไม่ได้ percent-encode ครบ เช่นบาง URL ของ `roijang.com`, `m-culture.in.th`, `www.khukkhak.go.th`, `www.wongnai.com` · รายงานนี้ไม่สรุปว่า URL เหล่านั้นเสีย เพราะยังไม่ได้ตรวจถึงเซิร์ฟเวอร์

### ลิงก์ที่พบปัญหาเชิงผลลัพธ์

- URL เทศบาล `takuapacity.go.th` ที่ใช้ได้ redirect ไป `files.takuapacity.go.th` และตอบ 200 · ไม่ถือว่าเสีย
- URL LoveThailand ของวัดนามือง redirect ไปหน้าชื่อ `Wat-Pathum-Thara-(Wat-Na-Mueang).html` และตอบ 200 · ไม่ถือว่าเสีย

URL อื่นที่ตรวจสำเร็จตอบ 200 หรือ redirect แล้วตอบ 200 · ไม่พบปัญหาจากการตรวจ HTTP รอบนี้

## 2) Google Maps ใน `data/guide-picks.json`

ตรวจครบ 13 รายการ · ทั้ง 13 URL ใช้รูปแบบ `https://maps.google.com/?q=...` ถูกต้อง และ query `q` มีข้อความระบุชื่อหรือส่วนสำคัญของรายการทุกตัว · ไม่พบ URL ที่รูปแบบผิด

| id | ข้อความใน `q` | ผลเทียบชื่อรายการ |
|---|---|---|
| `guide-lad-yai` | หลาดใหญ่ ตะกั่วป่า | ตรงกับชื่อ “หลาดใหญ่” |
| `guide-bang-deen` | ร้านบังดีน ตะกั่วป่า | ตรงกับ “บังดีน” |
| `guide-mee-talad-khwang` | บะหมี่ตลาดขวาง | ตรงกับชื่อ |
| `guide-moo-satay-kruaew` | หมูสะเต๊ะครูแอ๋ว | ตรงกับชื่อ |
| `guide-pa-da-hokkien` | ป้าดาหมี่ฮกเกี้ยน | ตรงกับชื่อ |
| `guide-pu-dam` | ร้านปูดำ บางนายสี | ตรงกับ “ปูดำ” และพื้นที่ |
| `guide-jae-ouan` | เจ๊อ้วน บ้านน้ำเค็ม | ตรงกับ “เจ๊อ้วน” และพื้นที่ |
| `guide-kae-padthai` | เก๋ผัดไทย ตะกั่วป่า | ตรงกับชื่อและพื้นที่ |
| `guide-baan-lapp` | Baan Lapp ตะกั่วป่า | ตรงกับชื่อและพื้นที่ |
| `guide-iron-bridge` | สะพานเหล็ก ตะกั่วป่า | ตรงกับ “สะพานเหล็ก” |
| `guide-old-town-street` | ถนนศรีตะกั่วป่า | ตรงกับสถานที่หลัก |
| `guide-tam-nang` | น้ำตกตำหนัง | ตรงกับชื่อ |
| `guide-tuangrat-taosor` | เต้าส้อตวงรัตน์ | ตรงกับชื่อ |

ลิงก์ Maps ทั้ง 13 รายการไม่มีพิกัด latitude/longitude ใน query · จึงตรวจได้เฉพาะรูปแบบ URL และความสอดคล้องของชื่อจากข้อความ `q` ไม่สามารถยืนยันความถูกต้องของพิกัดได้จาก URL เหล่านี้

## สรุป

พบ 3 URL ที่ตอบ 404 และ 3 URL ที่โดเมนเปิดไม่ได้ · พบกลุ่ม URL ที่ปลายทางปฏิเสธคำขอหรือ URL encode ไม่ครบ ซึ่งรายงานแยกไว้เป็น “เปิดตรวจไม่ได้” · Google Maps ครบ 13 รายการมีรูปแบบถูกต้องและชื่อใน query สอดคล้องกับรายการ แต่ไม่มีพิกัดให้ตรวจยืนยัน

