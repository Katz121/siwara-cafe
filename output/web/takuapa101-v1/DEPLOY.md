# ขึ้นเว็บบน Cloudflare

ตรวจแล้วเมื่อ 7 ก.ย. 2569: `siwaracafe.com` ใช้ nameserver ของ Cloudflare อยู่แล้ว
(`achiel.ns.cloudflare.com`, `venus.ns.cloudflare.com`) และวิ่งผ่าน IP ของ Cloudflare
จึงทำแบบที่ดีที่สุดได้เลยโดยไม่ต้องย้าย DNS

## ทำไมต้องเป็น `siwaracafe.com/takuapa/`

เว็บนี้ถูก build ให้เป็นโฟลเดอร์ย่อยของโดเมนศิวราตั้งแต่ต้น (`BASE_PATH = /takuapa`)
เหตุผลคือ **น้ำหนักที่ Google ให้กับโดเมนจะสะสมอยู่ที่ siwaracafe.com ทั้งก้อน**
ถ้าแยกไปโดเมนใหม่ ต้องเริ่มสร้างความน่าเชื่อถือใหม่หมด และต้องพึ่ง backlink

## แผน A · Pages + Worker route (แนะนำ)

เว็บอยู่บน Cloudflare Pages แต่คนเข้าถึงผ่าน `siwaracafe.com/takuapa/` เหมือนเดิม

```powershell
cd D:\Siwaracafeweb\output\web\takuapa101-v1
npx wrangler login                      # ต้องรันในเทอร์มินัลจริง
npx wrangler pages project create takuapa101 --production-branch main
python build_site.py
npx wrangler pages deploy site --project-name takuapa101
```

จากนั้นสร้าง Worker ตัวบางที่ทำหน้าที่ส่งต่อ (ไฟล์ `router/src/index.js` ในโปรเจกต์นี้)
แล้วผูก route `siwaracafe.com/takuapa/*` ใน Cloudflare dashboard หรือ

```powershell
cd router
npx wrangler deploy
```

ผลลัพธ์
- URL ที่คนเห็นและที่ Google เก็บ: `https://siwaracafe.com/takuapa/...`
- น้ำหนัก SEO ตกที่โดเมนศิวราโดยตรง ไม่ต้องพึ่ง backlink สักลิงก์
- เว็บกับ Worker ข่าวอยู่แพลตฟอร์มเดียวกัน เรียก `/takuapa/api/news` แบบ same-origin ได้ ไม่ต้องตั้ง CORS

## แผน B · Pages โดเมนของตัวเอง

```powershell
npx wrangler pages deploy site --project-name takuapa101
```

ได้ `takuapa101.pages.dev` ทันที ตั้งโดเมนเองก็ได้ในหน้า Pages
ง่ายกว่า แต่เสียข้อได้เปรียบเรื่องโดเมนที่มีอายุแล้ว และต้องเปลี่ยน `SITE_BASE_URL` กับ build ใหม่

```powershell
$env:TAKUAPA_SITE_URL = "https://takuapa101.pages.dev"
python build_site.py
```

## หลัง deploy ต้องทำทันที

1. เปิด Google Search Console เพิ่ม property `siwaracafe.com` (ถ้ายังไม่มี)
2. ส่ง `https://siwaracafe.com/takuapa/sitemap.xml`
3. ขอ index หน้าแรกและหน้าเสาหลัก 5-6 หน้าด้วยมือ (URL Inspection > Request Indexing)
4. ตรวจ structured data ที่ `search.google.com/test/rich-results` อย่างน้อย 1 หน้าสถานที่ 1 ประเพณี
5. ตั้ง Bing Webmaster Tools ด้วย (ฟรี และ AI หลายตัวดึงผลจาก Bing)
6. เพิ่มลิงก์จากหน้าแรก siwaracafe.com มาที่ `/takuapa/` เพื่อให้ Google ไต่เจอเร็ว

Google มักใช้เวลา 4-12 สัปดาห์กว่าจะจัดอันดับเว็บใหม่ให้เข้าที่
ยิ่ง deploy เร็วเท่าไหร่ นาฬิกาก็เริ่มเดินเร็วเท่านั้น เนื้อหาที่เหลือเติมทีหลังได้

## ตรวจก่อน deploy ทุกครั้ง

```powershell
python merge_research.py
python make_feeds.py
python make_calendar.py
python build_site.py
python make_og.py
python validate_site.py
python validate_seo.py
```
