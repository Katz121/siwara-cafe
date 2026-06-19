/* ===== Google Places API key สำหรับดึงรูปสถานที่ลงแผนที่ "เที่ยวรอบศิวรา" =====
 *
 * วิธีตั้งค่า (ทำครั้งเดียว):
 * 1) ไป https://console.cloud.google.com → สร้าง/เลือกโปรเจกต์ → เปิดใช้ "Places API (New)"
 *    (ต้องผูกบัตร/billing · มี free credit รายเดือน พอสำหรับเว็บร้าน)
 * 2) APIs & Services → Credentials → Create credentials → API key
 * 3) ⚠️ สำคัญ (กันคนเอา key ไปใช้): กด Edit key แล้วตั้ง
 *    - Application restrictions → Websites → ใส่  https://siwara.cafe/*  และ  https://www.siwara.cafe/*
 *    - API restrictions → เลือกเฉพาะ "Places API (New)"
 * 4) เอา key มาวางแทน "" ด้านล่าง แล้ว push ขึ้นเว็บ
 *
 * ถ้าปล่อยว่าง = เว็บจะใช้รูปในโฟลเดอร์ images/places/ ตามเดิม (ไม่พัง)
 */
window.SS_GMAPS_KEY = "";
