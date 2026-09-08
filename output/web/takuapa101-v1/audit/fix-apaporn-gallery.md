# แก้แกลเลอรีกระทู้อาภรณ์

วันที่ 9 กันยายน 2569

## สิ่งที่แก้

- เพิ่ม `gallery` ในข้อมูลกระทู้ไทยและข้อมูลอังกฤษ แบ่งเป็นชุดผลงานเครื่องแต่งกายกับบรรยากาศนิทรรศการและศิลปิน รวมรูปที่ยังไม่ถูกใช้อีก 6 ใบ
- เพิ่ม renderer ใน `stories.py` ให้ตรวจรูปผ่าน `photo_for()` และใช้ `registry_caption()` เป็นแหล่งเดียวของ alt กับคำบรรยาย
- อ่าน width และ height จากไฟล์จริงด้วย Pillow และใส่ `loading="lazy"`
- เพิ่ม CSS gallery แบบ responsive ใน `site/assets/ui.css` โดยที่ viewport 390px ไม่ล้นแนวนอน
- เติมคำแปลหัวข้อ gallery ใน `data/i18n/en/ui.json`

## ตรวจสอบ

- `python build_site.py` · สร้าง 45 หน้า
- `python build_en.py` · สร้าง 45 หน้า
- `python audit/regress.py` · ผ่านทุกข้อ
- ตรวจผลลัพธ์ `/stories/apaporn/` และ `/en/stories/apaporn/` พบการ์ด gallery 6 ใบต่อภาษา
- จำนวนหน้าจริง 90 หน้า · ไทย 45 และอังกฤษ 45 · ค่าตรวจใน regression ตรงกับความจริงแล้ว

ไม่ได้แก้ `data/photo-registry.json` และไม่ได้เปลี่ยนย่อหน้าเดิมในกระทู้
