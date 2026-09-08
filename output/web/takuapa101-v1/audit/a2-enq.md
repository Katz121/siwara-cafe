# รายงานตรวจคุณภาพภาษาอังกฤษ · 8 หน้า

ตรวจจาก HTML ของ 8 หน้าใน `site/en/` ตามที่ระบุในงาน · ไฟล์เหล่านี้เป็น HTML บรรทัดเดียว จึงอ้างบรรทัด 1 · ไม่ได้แก้ไฟล์เว็บไซต์

## 1) ประโยคที่อ่านแล้วรู้ว่าแปลมา

ระดับ `ควรแก้`

- `site/en/index.html:1` · “Through shrine doors, looking at old house windows / And know the city a bit more at every stop” เป็นประโยคไม่สมบูรณ์และใช้กาล/ประธานไม่สอดคล้องกัน โดยเฉพาะ “And know” · อ่านเหมือนแปลตรงตัวมากกว่างานเขียนภาษาอังกฤษ
- `site/en/index.html:1` · “Short walk from wooden house” ขาด article และฟังไม่เป็นธรรมชาติ · ควรมีอย่างน้อย “A short walk from the wooden house” หรือสำนวนที่สื่อความหมายเดียวกัน
- `site/en/index.html:1` และ `site/en/places/index.html:1` · “20 places to slowly get to know” เป็นการวางคำแบบแปลตรงตัว · ภาษาอังกฤษธรรมชาติกว่าคือ “20 places to discover at your own pace” หรือใกล้เคียง
- `site/en/index.html:1` · “Look at the story of the Chinese community” ฟังแข็งและไม่เป็นสำนวนแนะนำเส้นทาง · “Explore the story of the Chinese community” ชัดกว่า
- `site/en/places/tao-ming/index.html:1` · “the school formally declared its intention to be established in 1920” เป็นโครงสร้าง passive ที่ผิดธรรมชาติและสื่อไม่ชัดว่าใครยื่นขอจัดตั้งโรงเรียน
- `site/en/places/iron-bridge/index.html:1` · “the bridge became a mining town trace” เป็นการจับคำนามแบบแปลตรงตัว · “a trace of the town’s mining past” เป็นภาษาอังกฤษที่เป็นธรรมชาติกว่า
- `site/en/places/iron-bridge/index.html:1` · “The bridge thus stands between functioning infrastructure and a landmark for walking, views, and photography” อ่านแข็งและ “a landmark for walking” ไม่ใช่ collocation ปกติ
- `site/en/rest/index.html:1` · “with a Hidden Gem style” ใช้ชื่อหมวด/คำขยายแบบไม่เป็นธรรมชาติในภาษาอังกฤษ · ควรเขียนเป็น “with a hidden-gem feel” หรืออธิบายบรรยากาศตรง ๆ
- `site/en/rest/index.html:1` · “turning it into a beautiful orange” ใช้สีเป็นคำนามผิดความหมาย · ควรเป็น “turning it a beautiful orange” หรือ “giving it a beautiful orange glow”

## 2) ความหมายเพี้ยนจากไทย

ระดับ `ควรแก้`

- `site/en/index.html:1` · “And know the city a bit more at every stop” ไม่ได้ถ่ายทอดความหมายเชิญชวนแบบไทยให้ชัด และไวยากรณ์ทำให้ความหมายสะดุด · เป็นทั้งปัญหาภาษาและความหมายของข้อความโปรย
- `site/en/index.html:1` · “108 ร้านในย่าน” ยังเป็นไทย จึงไม่มีข้อความอังกฤษให้ผู้ใช้ต่างชาติเข้าใจว่าหมายถึงร้าน 108 แห่งในย่าน

ตรวจแล้วไม่พบหลักฐานเพียงพอที่จะฟันธงว่าข้อเท็จจริงในบทความ Tao Ming, Iron Bridge หรือ City แปลผิดจากไทย · เนื้อหาหลายจุดตั้งใจระบุสถานะว่า “not verified / no evidence” ตามบริบทของเว็บ จึงไม่นับเป็นความหมายเพี้ยน

## 3) ข้อความไทยตกค้างที่ไม่ใช่ชื่อหน่วยงานราชการ

ระดับ `ผิด`

- `site/en/index.html:1` · ข้อความที่ผู้ใช้เห็น “20 สถานที่ · 7 ประเพณี · 108 ร้าน” และ “ตั้งต้นจากแผ่นพับเทศบาลเมืองตะกั่วป่า แล้วค้นเพิ่มพร้อมแหล่งที่มา” ยังเป็นภาษาไทย
- `site/en/index.html:1` · การ์ด “What to eat” มีคำว่า “108 ร้านในย่าน” เป็นไทย
- `site/en/index.html:1` · ป้าย/คำอธิบายที่ตั้งใจเป็น English แต่ยังเป็นไทยใน accessibility labels ได้แก่ `aria-label="เมนูหลัก"`, `สลับเป็นโหมดกลางคืน`, `เปิดเมนู`, `ค้นหาในเว็บไซต์ (กด Ctrl+K)`, `ทริปของคุณ`, `เริ่มต้นใช้งาน`, `เปิดแผนที่เทศบาล`, `หมวดสถานที่`, `เมนูด่วน`, และ `กลับขึ้นด้านบน`
- `site/en/places/index.html:1` · ช่องค้นหามี placeholder ไทย `ชื่อวัด ศาลเจ้า หรือจุดที่อยากไป` และ `aria-label="หมวดสถานที่"`
- `site/en/eat/index.html:1` · ช่องค้นหามี placeholder ไทย `พิมพ์ชื่อร้านที่ต้องการ`
- `site/en/places/tao-ming/index.html:1` และ `site/en/places/iron-bridge/index.html:1` · มีข้อความไทยในชื่อแหล่งอ้างอิง/หน่วยงานบางรายการ · รายการที่เป็นชื่อหน่วยงานราชการไทยและมีคำแปลอังกฤษกำกับ ไม่นับเป็นปัญหาตามข้อยกเว้นของสเปก

## 4) ปุ่มและป้ายกำกับ

ระดับ `ควรแก้`

- ป้ายกำกับที่ผู้ใช้เห็นส่วนใหญ่เข้าใจได้ทันที เช่น “Places”, “Map”, “Your trip”, “Open map”, “Find on Google Maps”, “Clear filters”, “Plan my trip” · ตรวจจาก `site/en/index.html:1`, `site/en/places/index.html:1`, `site/en/eat/index.html:1`, `site/en/trip/index.html:1`
- `site/en/index.html:1` · “Choose your destination” เข้าใจได้ แต่ในบริบทที่มีหลายสถานที่ “Choose a place to visit” จะตรงและเป็นธรรมชาติกว่า
- `site/en/places/index.html:1` · placeholder ไทยทำให้ผู้ใช้ต่างชาติไม่เข้าใจว่าค้นหาอะไร แม้ label หลัก “Search places” จะชัด
- `site/en/eat/index.html:1` · placeholder ไทย `พิมพ์ชื่อร้านที่ต้องการ` ทำให้ช่องค้นหาไม่สื่อสารกับผู้ใช้ภาษาอังกฤษ
- ทุกหน้าที่ตรวจมี `aria-label` สำคัญเป็นภาษาไทย เช่น เมนู, ค้นหา, สลับธีม, trip และกลับขึ้นบน · ผู้ใช้โปรแกรมอ่านหน้าจอที่เป็นชาวต่างชาติจะไม่ได้รับป้ายกำกับภาษาอังกฤษ จึงควรแปลเป็น English แม้ข้อความบนปุ่มไอคอนจะเข้าใจได้จากภาพ

## สรุปการตรวจที่ทำไม่ได้

- ไม่ได้ตัดสินความถูกต้องของข้อเท็จจริงทางประวัติศาสตร์หรือเวลาเปิดทำการ เพราะงานนี้จำกัดเฉพาะคุณภาพภาษาอังกฤษ และหน้าเว็บเองระบุหลายรายการว่าไม่ยืนยัน
- ไม่ได้ตรวจการแสดงผลจริงด้วยเบราว์เซอร์ในรอบนี้ · จึงไม่สรุปเรื่องการตัดคำ, ล้นกรอบ, หรือพฤติกรรมปุ่มจาก visual UI · รายงานข้างต้นอ้างเฉพาะข้อความและ attributes ที่พบใน HTML จริง
