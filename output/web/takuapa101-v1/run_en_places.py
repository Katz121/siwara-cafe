"""Translate place data to English in small batches.

One agy call for all 27 records times out, so the work is split and each batch
writes its own file. merge_i18n.py stitches them back together.
"""
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
OUT = os.path.join(HERE, "data", "i18n", "en", "places-parts")
os.makedirs(OUT, exist_ok=True)

PLACES = json.load(open(os.path.join(HERE, "data", "places-enriched.json"), encoding="utf-8"))
IDS = [r["id"] for r in PLACES]
CHUNK = 4
GROUPS = [IDS[i:i + CHUNK] for i in range(0, len(IDS), CHUNK)]

PROMPT = """โฟลเดอร์งาน {HERE}
อ่าน `briefs/2026-09-07_english-spec.md` หัวข้อ "กฎการแปล" ให้ครบก่อนลงมือ

แปลข้อมูลสถานที่เป็นภาษาอังกฤษ **เฉพาะ {N} รายการนี้เท่านั้น**: {IDS}
อ่านต้นฉบับจาก `data/places-enriched.json`

ต่อรายการแปล: name, lead (จาก editorial_angle), eras.then/before/now (headline + body),
highlights (title + detail), getting_there (text), did_you_know (fact),
festival (months, venue, activities), unknowns

รูปแบบไฟล์ `data/i18n/en/places-parts/{SLUG}.json`:
{{"<place_id>": {{"name":"","lead":"","eras":{{"then":{{"headline":"","body":""}},"before":{{...}},"now":{{...}}}},
  "highlights":[{{"title":"","detail":""}}],"getting_there":[{{"from":"","text":""}}],
  "did_you_know":[""],"festival":{{"months":"","venue":"","activities":[""]}},"unknowns":[""]}}}}

ย้ำกฎ:
- ห้ามเพิ่มข้อเท็จจริงที่ต้นฉบับไทยไม่มี
- คำกำกับความไม่แน่นอนต้องอยู่ครบ ("ยังไม่ยืนยัน" -> "not verified" · "สันนิษฐาน" -> "suggested, not settled")
- ชื่อเฉพาะทับศัพท์แล้ววงเล็บอธิบาย เช่น Wat Boromthat Khiri Khet (the town's relic temple)
- ปีใช้ ค.ศ. พร้อมวงเล็บ พ.ศ. ครั้งแรกที่ปรากฏ
- เสียงแบบคู่มือเดินทางที่ดี ไม่ใช่โบรชัวร์ · ห้าม hidden gem, must-see, paradise, authentic ลอย ๆ
- ห้าม em-dash และ en-dash

เขียนลง path จริง ห้ามลง scratch · **UTF-8 เท่านั้น**
เสร็จแล้ว json.load ยืนยัน แล้วรายงานจำนวนรายการ
"""


def run(i, ids):
    slug = "part-%02d" % (i + 1)
    out = os.path.join(OUT, slug + ".json")
    if os.path.exists(out) and os.path.getsize(out) > 400:
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
        if os.path.exists(out) and os.path.getsize(out) > 400:
            return slug, "OK"
        if "quota reached" in log:
            time.sleep(900)
            continue
        break
    return slug, "FAIL"


only = set(sys.argv[1:])
groups = [(i, g) for i, g in enumerate(GROUPS) if not only or ("part-%02d" % (i + 1)) in only]
print("batches=%d (%d สถานที่)" % (len(groups), len(IDS)), flush=True)
with ThreadPoolExecutor(max_workers=2) as ex:
    for f in as_completed({ex.submit(run, i, g): i for i, g in groups}):
        print("  %s: %s" % f.result(), flush=True)
print("done")
