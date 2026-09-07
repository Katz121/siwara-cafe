คุณคือนักหาภาพลิขสิทธิ์เปิด สำหรับเว็บไกด์ "ตะกั่วป่า 101" (อ.ตะกั่วป่า จ.พังงา)

TARGET_ID: {ID}
ชื่อ: {NAME_TH} ({NAME_EN})
ประเภท: {CATEGORY}
บริบท: {PASS1}

## โจทย์
หาภาพของสถานที่/ประเพณีนี้ที่ **ใช้บนเว็บได้จริงตามกฎหมาย** ให้ได้มากที่สุด

## แหล่งที่ต้องไล่ตามลำดับ
1. **Wikimedia Commons** — ค้นทั้งชื่อไทยและอังกฤษ และค้นแบบกว้าง เช่น `Takua Pa`, `Phang Nga temple`, `Takua Pa old town`, ชื่อวัดสะกดอังกฤษหลายแบบ · ใช้ Commons API ได้: `https://commons.wikimedia.org/w/api.php?action=query&list=search&srsearch=...&format=json`
2. **วิกิพีเดียไทย/อังกฤษ** ของสถานที่นี้ (ภาพในบทความมักอยู่บน Commons)
3. **Wikidata** ของสถานที่นี้ (property P18 image)
4. **หน่วยงานราชการไทย** — เทศบาลเมืองตะกั่วป่า (takuapacity.go.th), ททท./tourismthailand.org, กรมศิลปากร (finearts.go.th), m-culture.go.th, ONEP culturalenvi.onep.go.th · ระบุว่าเป็นภาพราชการเผยแพร่ ต้องอ้างอิงแหล่ง
5. **Flickr / openverse** ที่มีสัญญาอนุญาต CC

## สิ่งที่ต้องได้ต่อภาพ
- `url` — ลิงก์ตรงไปยังไฟล์ภาพ (Commons ใช้ `Special:FilePath` หรือ upload.wikimedia.org) ต้องเปิดได้จริง ให้ลอง `curl -I` ยืนยันว่าได้ HTTP 200 และ content-type เป็นภาพ
- `page_url` — หน้าที่มีข้อมูลลิขสิทธิ์
- `license` — เช่น `CC BY-SA 4.0`, `CC0`, `Public Domain`, `ภาพราชการเผยแพร่`, `ไม่ทราบ`
- `license_verdict` — **`USABLE`** เฉพาะเมื่อหน้าลิขสิทธิ์บอกชัด (CC ทุกแบบ / PD / CC0) · **`ASK`** เมื่อเป็นภาพราชการหรือเพจที่ต้องขอ · **`NO`** เมื่อสงวนสิทธิ์หรือไม่ทราบ
- `attribution_th` — ข้อความเครดิตที่ต้องแสดงใต้ภาพ (ชื่อผู้ถ่าย + สัญญาอนุญาต)
- `caption_th`, `era` (`archive` ภาพเก่า / `current` ภาพปัจจุบัน), `width`, `height`

## กฎเหล็ก
1. **`license_verdict` เป็น `USABLE` ได้ก็ต่อเมื่อคุณเปิดหน้าลิขสิทธิ์อ่านจริงแล้ว** ห้ามเดา ห้ามอนุมานจากชื่อเว็บ
2. ห้ามใส่ภาพที่ URL เปิดไม่ได้ · ต้อง verify ด้วย curl ทุกใบ
3. ถ้าไม่เจอภาพลิขสิทธิ์เปิดเลย ให้ตอบ `photos: []` แล้วเขียนใน `notes_th` ว่าค้นอะไรไปบ้าง **ห้ามยัดภาพมั่ว ๆ มาให้ครบจำนวน**
4. อย่างน้อยต้องลองค้น Commons ด้วยคำค้นไม่ต่ำกว่า 6 แบบ ก่อนสรุปว่าไม่มี

## ผลลัพธ์
เขียนไฟล์ `{OUTFILE}` เป็น JSON (UTF-8 ไม่ใส่ code fence):
{
 "id": "{ID}",
 "photos": [{"url":"","page_url":"","license":"","license_verdict":"USABLE|ASK|NO","attribution_th":"","caption_th":"","era":"archive|current","width":null,"height":null,"http_status":200}],
 "searched_queries": [],
 "notes_th": "",
 "researched_on": "2026-09-07"
}

เสร็จแล้วตอบ DONE {ID} + จำนวนภาพ USABLE ที่ได้
