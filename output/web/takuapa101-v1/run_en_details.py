"""Translate the fields that carry most of a place page: history, timeline, news."""
import json
import os
import shutil
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.stdout.reconfigure(encoding='utf-8')

AGY = r"C:\Users\siwat\AppData\Local\agy\bin\agy.cmd"
if not os.path.exists(AGY):
    AGY = shutil.which("agy") or "agy"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "data", "i18n", "en", "details")
os.makedirs(OUT, exist_ok=True)

PLACES = json.load(open(os.path.join(HERE, "data", "places-enriched.json"), encoding="utf-8"))
IDS = [r["id"] for r in PLACES]
CHUNK = 3
GROUPS = [IDS[i:i + CHUNK] for i in range(0, len(IDS), CHUNK)]

PROMPT = """โฟลเดอร์งาน {HERE}
อ่าน `briefs/2026-09-07_english-spec.md` หัวข้อ "กฎการแปล" ให้ครบก่อนลงมือ

แปลข้อมูลรายละเอียดของสถานที่เป็นภาษาอังกฤษ **เฉพาะ {N} รายการนี้**: {IDS}
อ่านต้นฉบับจาก `data/places-enriched.json`

ฟิลด์ที่ต้องแปล (นี่คือเนื้อหาหลักของหน้า):
- `history[]` -> claim_th, quote
- `timeline[]` -> title_th, detail_th
- `news[]` -> title_th, summary_th
- `nearby[]` -> name_th
- `visit.best_time_th`, `visit.parking_th`, `visit.wheelchair_th`, `visit.dress_code_th`,
  `visit.opening_hours_th`, `visit.admission_fee_th`
- `address.line_th`

รูปแบบไฟล์ `data/i18n/en/details/{SLUG}.json`:
{{"<place_id>": {{
  "history": [{{"claim": "", "quote": ""}}],
  "timeline": [{{"title": "", "detail": ""}}],
  "news": [{{"title": "", "summary": ""}}],
  "nearby": [{{"name": ""}}],
  "visit": {{"best_time": "", "parking": "", "wheelchair": "", "dress_code": "", "opening_hours": "", "admission_fee": ""}},
  "address_line": ""
}}}}
**ลำดับใน array ต้องตรงกับต้นฉบับเป๊ะ** เพราะจะเอาไปจับคู่ทีละตัว
ฟิลด์ไหนต้นฉบับเป็น null ให้ใส่ null

ย้ำกฎ:
- ห้ามเพิ่มข้อเท็จจริงที่ต้นฉบับไม่มี
- คำกำกับความไม่แน่นอนต้องอยู่ครบ ("ยังไม่ยืนยัน" -> "not verified")
- ชื่อวัดและศาลเจ้าทับศัพท์ เช่น Wat Kongkha Phimuk
- ปีใช้ ค.ศ. พร้อมวงเล็บ พ.ศ. ครั้งแรกที่ปรากฏ
- ห้าม em-dash และ en-dash

เขียนลง path จริง ห้ามลง scratch · **UTF-8 เท่านั้น** · เสร็จแล้ว json.load ยืนยัน
"""


def run(i, ids):
    slug = "det-%02d" % (i + 1)
    out = os.path.join(OUT, slug + ".json")
    if os.path.exists(out) and os.path.getsize(out) > 300:
        return slug, "skip(exists)"
    prompt = (PROMPT.replace("{HERE}", HERE).replace("{N}", str(len(ids)))
              .replace("{IDS}", ", ".join(ids)).replace("{SLUG}", slug))
    for attempt in range(3):
        p = subprocess.run([AGY, "--dangerously-skip-permissions", "--model", "gemini-3.1-pro-high",
                            "-p", prompt],
                           cwd=HERE, capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=3000)
        log = (p.stdout or "") + "\n--ERR--\n" + (p.stderr or "")
        open(os.path.join(OUT, slug + ".log"), "w", encoding="utf-8").write(log)
        if os.path.exists(out) and os.path.getsize(out) > 300:
            return slug, "OK"
        if "quota reached" in log:
            time.sleep(900)
            continue
        break
    return slug, "FAIL"


only = set(sys.argv[1:])
groups = [(i, g) for i, g in enumerate(GROUPS) if not only or ("det-%02d" % (i + 1)) in only]
print("batches=%d" % len(groups), flush=True)
with ThreadPoolExecutor(max_workers=2) as ex:
    for f in as_completed({ex.submit(run, i, g): i for i, g in groups}):
        print("  %s: %s" % f.result(), flush=True)
print("done")
