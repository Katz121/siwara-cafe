# Fix report · English eat directory

วันที่ตรวจ: 8 กันยายน 2569 (2026)

แก้ `build_site.py` ให้ร้านจากแผ่นพับเทศบาลทั้ง 59 รายการมีลิงก์ค้นหา Google Maps รูปแบบ `https://www.google.com/maps/search/?api=1&query=<ชื่อร้าน>+ตะกั่วป่า` โดย encode ผ่าน `quote_plus` และไม่เติมที่อยู่หรือพิกัดที่ไม่มีแหล่งที่มา ป้ายภาษาไทย/อังกฤษถูกแปลงเป็น “หาในแผนที่ ↗” / “Find on map ↗” ตามภาษา

เติมชื่ออังกฤษจาก `name_en_as_printed` ของแผ่นพับลง `data/i18n/en/shops.json` และให้ `data-shop` ของ 59 ร้านมีชื่อไทยกับชื่ออังกฤษคั่นด้วย ` | ` เพื่อค้นได้ทั้งสองแบบ

## Build

- Thai: `python build_site.py` → สำเร็จ 44 หน้า, 59 directory entries
- English: `python build_en.py` → สำเร็จ 44 หน้า, ข้าม 0 หน้า

## Verification

ตรวจไฟล์ที่ build แล้ว `site/en/eat/index.html`:

- ลิงก์ Google Maps ของร้านแผ่นพับ: 59 รายการ
- `data-shop` ที่มีไทยและอังกฤษ: 59 รายการ
- ตัวอย่างคำค้นที่กรองพบจาก `data-shop`: `Hokkilao` → 1, `Chicken Rice` → 5, `Coffee` → 9
- ป้ายลิงก์ภาษาอังกฤษใน HTML: `Find on map ↗`

Playwright ไม่สามารถรันได้ใน workspace นี้ (`require('playwright')` ให้ `NO_PLAYWRIGHT`) และไม่มี browser surface ให้เปิดผ่าน Computer Use จึงแนบผลตรวจแบบ static/runtime-equivalent ข้างต้นแทน; ไม่อ้างว่าเป็นผลจากการคลิกเบราว์เซอร์จริง
