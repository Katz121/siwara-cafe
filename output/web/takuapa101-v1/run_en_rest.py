"""Remaining English work: story articles, shop blurbs, then wire /en/ into the build."""
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
LOGS = os.path.join(HERE, "_agy")
os.makedirs(LOGS, exist_ok=True)
RULES = "อ่าน `briefs/2026-09-07_english-spec.md` หัวข้อ \"กฎการแปล\" ให้ครบก่อนลงมือ"

STORY_IDS = ["city", "architecture", "water-trade", "food-people", "kuapapoh"]

JOBS = {}

for sid in STORY_IDS:
    JOBS["story-" + sid] = f"""โฟลเดอร์งาน {HERE}
{RULES}

แปลบทความ `data/stories/{sid}.json` เป็นภาษาอังกฤษทั้งบท
เขียนลง `data/i18n/en/stories/{sid}.json` โครงเดียวกับต้นฉบับ แปลฟิลด์เหล่านี้:
title, dek, lede[], sections[].heading_th -> heading, sections[].paragraphs[],
sections[].flags[].text_th, pull_quotes[], evidence_box.heading_th + items[].claim_th + items[].explain_th,
unknowns[] · ส่วน id, places, sources, photo, file, url, reading_minutes ให้คงเดิมไม่ต้องแปล

ย้ำ: ห้ามเพิ่มข้อเท็จจริงที่ต้นฉบับไม่มี · คำกำกับความไม่แน่นอนต้องอยู่ครบ
("ยังไม่มีข้อยุติ" -> "not settled" · "สันนิษฐาน" -> "suggested, not settled")
ชื่อเฉพาะทับศัพท์แล้ววงเล็บอธิบาย · ปีใช้ ค.ศ. พร้อมวงเล็บ พ.ศ. ครั้งแรก
เสียงแบบคู่มือเดินทางที่ดี ห้าม hidden gem, must-see, paradise · ห้าม em/en-dash
เขียนลง path จริง ห้ามลง scratch · **UTF-8 เท่านั้น** · เสร็จแล้ว json.load ยืนยัน"""

JOBS["shops"] = f"""โฟลเดอร์งาน {HERE}
{RULES}

แปลคำอธิบายร้านเป็นภาษาอังกฤษ · อ่าน `data/shops-extra.json` (49 ร้าน)
เขียนลง `data/i18n/en/shops.json` รูปแบบ:
{{"<shop_id>": {{"name": "ชื่อทับศัพท์อังกฤษ", "one_liner": "คำอธิบายภาษาอังกฤษ 1 ประโยค"}}}}
ถ้าร้านมี name_en อยู่แล้วให้ใช้ค่านั้น

ห้ามเพิ่มข้อมูลที่ต้นฉบับไม่มี (ห้ามแต่งเมนู ราคา หรือคำชม)
ห้ามคำโฆษณาลอย ๆ อย่าง best, must-try, hidden gem · ห้าม em/en-dash
เขียนลง path จริง ห้ามลง scratch · **UTF-8 เท่านั้น** · เสร็จแล้ว json.load ยืนยัน แล้วรายงานจำนวนร้าน"""

JOBS["wire-en"] = f"""โฟลเดอร์งาน {HERE}
อ่าน `briefs/2026-09-07_english-spec.md` ให้ครบ

คำแปลพร้อมแล้วทั้งหมด:
- `data/i18n/en/ui.json` (272 คีย์) · `data/i18n/en/places.json` (27 สถานที่)
- `data/i18n/en/stories/*.json` (5 บทความ) · `data/i18n/en/shops.json`
- `i18n.py` มีฟังก์ชัน t() และ load() แล้ว
- `data/photo-registry.json` มี caption_en, credit_en, license_en แล้ว ใช้ค่าเหล่านี้ในหน้าอังกฤษ
- `data/i18n/en/publishers.json` เป็นคำอธิบายอังกฤษของหน่วยงานไทย · ในหน้าอังกฤษให้แสดงเป็น
  "ชื่อไทย (English gloss)" เพื่อให้คนตามไปหาต้นทางภาษาไทยได้


งานรอบนี้คือ **ต่อสายเข้า build ให้สร้างหน้าอังกฤษใต้ /en/**
1. `build_site.py` รับ lang แล้ววนสร้างสองภาษา · ไทยที่ราก `/` · อังกฤษที่ `/en/...`
   ใช้ i18n.t() แทนสตริงไทยที่ผู้ใช้เห็น · หน้าอังกฤษ `<html lang="en">`
2. ทุกหน้ามี `<link rel="alternate" hreflang="th">`, `hreflang="en"`, `hreflang="x-default"` ชี้ไทย
   canonical ของหน้าอังกฤษชี้ตัวเอง · sitemap รวมทั้งสองภาษา
3. ปุ่มสลับภาษา TH / EN บนหัวเว็บ ไปหน้าคู่กันเสมอ ไม่ใช่กลับหน้าแรก
4. **หน้าไหนไม่มีคำแปล ห้ามสร้างหน้าอังกฤษเปล่า** ให้ข้ามไป
5. JSON-LD หน้าอังกฤษใช้ `inLanguage: "en"` และชื่ออังกฤษ
6. title/description อังกฤษเขียนให้ตรงคำค้นอังกฤษ ไม่ใช่แปลตรงตัว

ตรวจก่อนจบ:
```
python build_site.py
python -c "import glob;print(len(glob.glob('site/en/**/index.html',recursive=True)),'หน้าอังกฤษ')"
grep -c hreflang site/index.html
python validate_site.py
```
แล้วเปิด /en/ และ /en/places/tao-ming/ ด้วย Playwright ตรวจว่าไม่มี console error
และไม่มีข้อความไทยหลงในหน้าอังกฤษ
เขียนลง path จริง ห้ามลง scratch · **UTF-8 เท่านั้น** · ห้ามทำหน้าไทยพัง"""


def run(name):
    for attempt in range(3):
        p = subprocess.run([AGY, "--dangerously-skip-permissions", "--model", "gemini-3.1-pro-high",
                            "-p", JOBS[name]],
                           cwd=HERE, capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=3000)
        log = (p.stdout or "") + "\n--ERR--\n" + (p.stderr or "")
        open(os.path.join(LOGS, name + ".log"), "w", encoding="utf-8").write(log)
        if "quota reached" in log:
            time.sleep(900)
            continue
        return name, "rc=%d" % p.returncode
    return name, "quota"


order = sys.argv[1:] or (["story-" + s for s in STORY_IDS] + ["shops"])
print("jobs=%d" % len(order), flush=True)
with ThreadPoolExecutor(max_workers=2) as ex:
    for f in as_completed({ex.submit(run, n): n for n in order if n in JOBS}):
        print("  %s: %s" % f.result(), flush=True)
print("done")
