"""Queue of agy jobs: English translation, then the leftover coordinates."""
import os
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.stdout.reconfigure(encoding='utf-8')

AGY = r"C:\Users\siwat\AppData\Local\agy\bin\agy.cmd"
if not os.path.exists(AGY):
    AGY = shutil.which("agy") or "agy"
HERE = os.path.dirname(os.path.abspath(__file__))
LOGS = os.path.join(HERE, "_agy")
os.makedirs(LOGS, exist_ok=True)

SPEC = "briefs/2026-09-07_english-spec.md"

JOBS = {
    "rest-page": f"""โฟลเดอร์งาน {HERE}
อ่าน `briefs/2026-09-07_rest-page-spec.md` ให้ครบก่อนลงมือ แล้วทำตามทุกข้อ
อ่านแผ่นต้นทางด้วย: `output/pdf/2026-09-06_siwara-story-v5/2026-09-06_siwara-story-v5.html`

สรุปงาน: สร้างหน้า /rest/ · เพิ่มเส้นทางที่ 4 ใน /routes/ · เติมย่อหน้าที่มาใน /about/ ·
ใส่ลิงก์ตามบริบทเฉพาะ 4 หน้าสถานที่ในเส้นทางนี้

ย้ำกฎที่ห้ามฝ่าฝืน: หน้านี้ต้องอ่านเหมือนคู่มือเมือง ไม่ใช่โฆษณาร้าน ·
ห้ามใส่เมนู ราคา เวลาเปิดที่ไม่ยืนยัน · จุดพักอื่นในย่านต้องอยู่ในลิสต์ด้วย เรียงตามตัวอักษร
เขียนลง path จริง ห้ามลง scratch · UTF-8 เท่านั้น
เสร็จแล้วรัน build_site.py แล้วรายงานไฟล์ที่แก้และผลตรวจ""",
    "en-ui": f"""โฟลเดอร์งาน {HERE}
อ่าน {SPEC} ให้ครบก่อนลงมือ

รอบนี้ทำเฉพาะ **ส่วนที่ 1 · โครง i18n และ ui.json**
1. สร้าง `data/i18n/en/ui.json` · ไล่เก็บสตริงภาษาไทยที่ผู้ใช้เห็นจากไฟล์เหล่านี้แล้วแปลเป็นอังกฤษ:
   design.py · build_site.py · stories.py · site/assets/design.js (ส่วนแผนที่) ·
   site/assets/trip-page.js · site/assets/search.js · site/assets/live-news.js
   คีย์ให้ใช้ข้อความไทยเป็นคีย์ตรง ๆ เพื่อให้แทนที่ง่าย
2. สร้าง `data/i18n/romanisation.json` · ตารางทับศัพท์ชื่อสถานที่ 27 แห่ง (อ่านจาก data/places-enriched.json)
3. สร้างโมดูล `i18n.py` มีฟังก์ชัน `t(text, lang)` คืนคำแปลถ้ามี ไม่มีก็คืนต้นฉบับ
   และ `load(lang)` โหลดไฟล์ทั้งหมดใน data/i18n/<lang>/
**ยังไม่ต้องแก้ build_site.py หรือสร้างหน้า /en/ ในรอบนี้** ทำแค่ 3 ข้อนี้
เขียนไฟล์ลง path จริง ห้ามลง scratch · UTF-8 เท่านั้น
เสร็จแล้ว json.load ทุกไฟล์กลับมายืนยัน แล้วรายงานจำนวนคีย์""",

    "en-places": f"""โฟลเดอร์งาน {HERE}
อ่าน {SPEC} ให้ครบก่อนลงมือ (โดยเฉพาะหัวข้อ "กฎการแปล")

รอบนี้ทำเฉพาะ **คำแปลข้อมูลสถานที่**
สร้าง `data/i18n/en/places.json` · แปลจาก `data/places-enriched.json` ทั้ง 27 รายการ
ต่อรายการแปล: name_en (ถ้ายังไม่มี), lead, eras.then/before/now (headline_th + body_th),
highlights (title + detail), getting_there (text), did_you_know (fact), festival (months/venue/activities),
unknowns, และ visit ที่เป็นข้อความ

รูปแบบ: `{{"<place_id>": {{"name": "", "lead": "", "eras": {{"then": {{"headline":"","body":""}}, ...}}, "highlights": [...], ...}}}}`

ย้ำกฎ: ห้ามเพิ่มข้อเท็จจริงที่ต้นฉบับไม่มี · คำกำกับความไม่แน่นอนต้องอยู่ครบ
("ยังไม่ยืนยัน" -> "not verified" · "สันนิษฐาน" -> "suggested, not settled")
ห้าม em/en-dash · ห้ามคำโฆษณาลอย ๆ อย่าง hidden gem, must-see
เขียนลง path จริง ห้ามลง scratch · UTF-8 เท่านั้น
เสร็จแล้ว json.load ยืนยัน แล้วรายงานจำนวนรายการ""",

    "shop-coords": f"""โฟลเดอร์งาน {HERE}

อ่าน `data/shops-extra.json` · หาร้านที่ `geo` เป็น null (ประมาณ 39 ร้าน)
งานคือหาพิกัดให้ได้มากที่สุด

วิธีที่ให้ใช้ (ตามลำดับ):
1. ค้น Google Maps ด้วยชื่อร้าน + "ตะกั่วป่า" หรือ + "พังงา" แล้วอ่านพิกัดจาก URL ที่มีรูปแบบ `@LAT,LNG`
2. ค้น Wongnai / TripAdvisor / Retty หน้าร้านนั้น มักมีพิกัดในหน้า
3. เพจ Facebook ของร้าน ส่วน About มักมีที่อยู่และหมุด
4. ถ้าได้แค่ที่อยู่ ให้ค้นที่อยู่นั้นต่อเพื่อหาพิกัด

กฎเหล็ก:
- **ห้ามเดาพิกัดเด็ดขาด** หาไม่เจอให้ปล่อย null · พิกัดผิดแย่กว่าไม่มีพิกัด เพราะพานักท่องเที่ยวไปผิดที่
- พิกัดต้องอยู่ในกรอบ lat 8.55 ถึง 9.20 และ lng 98.10 ถึง 98.60 · นอกกรอบ = จับร้านผิด ให้ทิ้ง
- ทุกพิกัดต้องมี `source_url` ที่เปิดได้จริง
- เจอว่าร้านปิดแล้วให้ใส่ `"status": "closed"`

เขียนผลลง `research/2026-09-07-shops/coords/final.json` เป็น JSON array:
`[{{"id":"","name_th":"","lat":null,"lng":null,"source_url":null,"google_maps_url":null,"address_th":null,"subdistrict":null,"phone":null,"hours_th":null,"status":"open","note_th":""}}]`

เขียนลง path จริง ห้ามลง scratch · UTF-8 เท่านั้น
เสร็จแล้วรายงานว่าหาพิกัดเจอกี่ร้านจากทั้งหมด""",
}


def run(name):
    p = subprocess.run([AGY, "--dangerously-skip-permissions", "--model", "gemini-3.1-pro-high",
                        "-p", JOBS[name]],
                       cwd=HERE, capture_output=True, text=True, encoding="utf-8",
                       errors="replace", timeout=3000)
    open(os.path.join(LOGS, name + ".log"), "w", encoding="utf-8").write(
        (p.stdout or "") + "\n--ERR--\n" + (p.stderr or ""))
    return name, "rc=%d" % p.returncode


only = set(sys.argv[1:])
names = [n for n in JOBS if not only or n in only]
print("jobs=%d" % len(names), flush=True)
with ThreadPoolExecutor(max_workers=3) as ex:
    for f in as_completed({ex.submit(run, n): n for n in names}):
        print("  %s: %s" % f.result(), flush=True)
print("done")
