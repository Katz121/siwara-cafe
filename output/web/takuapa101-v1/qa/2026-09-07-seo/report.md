# ผลตรวจ Phase 2 SEO

- python merge_research.py: merged 27 records
- python build_site.py: Built 40 pages
- python make_og.py: สร้างภาพ OG 28 ภาพ · 1200×630
- grep -r "127.0.0.1" site/ | wc -l: 0
- grep -rl "noindex" site/ | wc -l: 0
- คำสั่งอ่าน JSON-LD ทุก index.html ด้วย json.loads: JSON-LD ok
- python validate_seo.py: ผ่าน SEO 40 หน้า · OG 28 ภาพ · sitemap 40 URL
- python -m http.server 8092 --bind 127.0.0.1 --directory site: curl ได้ 200 ทั้ง /, /places/, /places/wat-boromthat/, /traditions/vegetarian/, /stories/ แล้วปิดเซิร์ฟเวอร์
- python validate_site.py --base http://127.0.0.1:8093/takuapa: ผ่าน 40 หน้า / 80 responsive route checks / 30 screenshots / errors []
- ตรวจ subfolder และ assets ผ่าน preview_site.py ที่พอร์ต 8093: 200 ทั้ง /takuapa/places/ และ /takuapa/assets/design.css
- พอร์ต 8091 มีเซิร์ฟเวอร์เดิม จึงทดสอบเต็มด้วยพอร์ต 8093 หลังการเรียก validate_site.py ค่าเริ่มต้นพบ 404
- FAQ 71 ข้อ / 20 หน้า · เฉลี่ย 3.55 ข้อ · ทุกหน้ามี 3–6 ข้อ
- geo 17 หน้า: culture-street, governor-wall, guan-yu, iron-bridge, khun-in, kue-chai, museum, phra-narai, pun-thao, riverwalk, tao-ming, thung-phra, wat-boromthat, wat-khuha, wat-kongkha, wat-nikorn, wat-sena
- ไม่มี geo: food-center, rong-jae, wat-pathum

ไม่มีไฟล์ภาพประเพณีเดิมทั้ง 7 รายการ จึงใช้ภาพสถานที่ที่เกี่ยวข้องจาก links.json และภาพกลางในกรณีที่ไม่มีความเชื่อมโยง ไม่สร้างภาพใหม่ด้วย AI

ไม่ใส่ eventSchedule เพราะข้อมูลเดือนทั้ง 7 รายการเป็นค่าประมาณ ตามจันทรคติ หรือหลักฐานเฉพาะปี ไม่รองรับเดือนสุริยคติที่แน่นอนทุกปี ไม่ใส่ startDate

openingHoursSpecification มีเฉพาะ culture-street ตารางวันอาทิตย์ที่ยืนยันและแปลงได้ชัดเจน ส่วน governor-wall ไม่ระบุเวลา และ food-center มีข้อมูลเวลาเก่าขัดกัน จึงไม่เดา

ไฟล์โค้ดที่แก้: build_site.py, site/assets/design.js, validate_redesign.py, README.md
ไฟล์ใหม่: seo_config.py, seo.py, make_og.py, preview_site.py, validate_seo.py
ผลสร้าง: site/**/index.html, site/sitemap.xml, site/robots.txt, site/assets/og/*.png และผล merge/QA ที่สคริปต์เดิมสร้าง
ภาพหน้าจอ: qa/2026-09-07-redesign/
