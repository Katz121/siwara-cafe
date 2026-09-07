# ตะกั่วป่า 101

เว็บสร้างด้วย Python · รอบนี้ทำเฉพาะ Phase 2 SEO โดยคงดีไซน์ แผนที่ภาพ ฟิลเตอร์ และการใช้งานเมื่อปิด JavaScript

## สร้างเว็บ

```powershell
python merge_research.py
python build_site.py
python make_og.py
```

URL หลักคือ `https://siwaracafe.com/takuapa` กำหนดใน `seo_config.py` และ override ด้วยตัวแปรสภาพแวดล้อม `SITE_BASE_URL` ได้ `BASE_PATH` คำนวณจาก URL นี้เพียงจุดเดียว ลิงก์ภายในทั้งหมดเติม prefix หลังประกอบ HTML เสร็จ

## เปิดดูในเครื่อง

ปิดเซิร์ฟเวอร์เดิมที่ใช้พอร์ต 8091 ก่อน แล้วรัน:

```powershell
python preview_site.py
```

เปิด **http://127.0.0.1:8091/takuapa/** สคริปต์จะให้บริการ `site/` ภายใต้ `BASE_PATH` โดย canonical ยังคงเป็นโดเมนจริง ไม่ต้อง override URL เพื่อ preview ถ้าพอร์ตไม่ว่างใช้ `python preview_site.py 8093` แล้วเปิดพอร์ต 8093 แทน

```powershell
python validate_site.py
# เมื่อใช้พอร์ตอื่น:
python validate_redesign.py --base http://127.0.0.1:8093/takuapa
```

`python -m http.server 8092 --bind 127.0.0.1 --directory site` ใช้ตรวจ HTTP ของไฟล์ที่ `/places/` ฯลฯ ได้ แต่ไม่ได้จำลอง subfolder จึงใช้ `preview_site.py` สำหรับตรวจเว็บเต็มพร้อม assets

## ข้อมูล SEO

- HTML 40 หน้า · robots เป็น `index,follow,max-image-preview:large` · sitemap ครบทุกหน้าและวันที่ build
- `seo.py` อ่านข้อมูลจริงจาก `data/places-enriched.json` · พิกัด ที่อยู่ ช่องทางติดต่อ และ FAQ ไม่เติมค่าที่ขาดหาย
- เวลาเปิดแบบ schema ต้องยืนยันแล้วและแปลงได้โดยไม่มีความกำกวม ไม่ใช้เวลาเก่าที่ขัดกันเป็นเวลาเปิดปัจจุบัน
- ไม่ใส่วันจัดงานที่ไม่รู้จริง และไม่แปลงเดือนจันทรคติ เดือนโดยประมาณ หรือหลักฐานเฉพาะปีเป็นตารางประจำปีที่แน่นอน
- FAQ แสดงด้วย details และข้อความเดียวกับ FAQPage · ข้อมูลเวลาเปิดหรือค่าเข้าที่สถานะ UNVERIFIED มีข้อความกำกับ
- OG 28 ภาพ ขนาด 1200×630 · เนื่องจากต้นทางมีภาพสถานที่ 20 ภาพและไม่มีภาพประเพณี ใช้ภาพสถานที่ที่เกี่ยวข้องจาก `data/links.json` สำหรับประเพณี ส่วนรายการที่ไม่มีภาพเกี่ยวข้องใช้ภาพเต้าหมิงร่วมกับชื่อหน้า
- ไม่มีการเผยแพร่เว็บหรือทำ Phase 3–7

รูปแผนที่ต้นทางยังอยู่ที่ `site/assets/municipal-map.png` และชุดทดสอบตรวจความตรงกับไฟล์ต้นฉบับ รวมทั้งจอ 1440/390px ฟิลเตอร์ ค้นหา แผนที่ และ no-JS fallback ภาพหน้าจออยู่ใน `qa/2026-09-07-redesign/`
