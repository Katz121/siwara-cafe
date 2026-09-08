# แก้กระทู้ อาภรณ์ · 2026-09-09

- เพิ่ม `data/stories/apaporn.json` โครงสร้างกระทู้ใหม่ครบทุก field และใช้ `id: apaporn`
- เนื้อหายึด `content.json` ส่วน `hero`, `six`, `events`, `houses` พร้อมระบุประเด็นที่ยังไม่ยืนยัน
- ใช้ภาพชุด `kuapapoh-charm-*`, `kuapapoh-expo-*` และ `kuapapoh-artist-card.webp` ตาม photo registry โดยไม่แก้ registry หรือ assets
- เพิ่มลิงก์เว็บไซต์โครงการในเนื้อหากลางบทและ call to action ท้ายบท
- ตรวจสถานที่แล้วใช้เฉพาะ `culture-street` และ `tao-ming`
- เพิ่มกระทู้ต่อจาก `kuapapoh` ใน `stories.py`
- เพิ่มคำแปลอังกฤษที่ `data/i18n/en/stories/apaporn.json`
- รัน `python build_site.py` ได้ 45 หน้า และ `python build_en.py` ได้ 45 หน้า
- ปรับชุดตรวจจาก 88 เป็น 90 หน้า

หมายเหตุ: ตอน build รอบแรกไฟล์ภาพชุดใหม่ยังไม่พบในโฟลเดอร์ assets จึงตรวจได้ตามการอนุญาตใน registry แต่หน้าอาจไม่แสดงภาพจนกว่า codex ที่เตรียมไฟล์จะวางไฟล์ครบ
