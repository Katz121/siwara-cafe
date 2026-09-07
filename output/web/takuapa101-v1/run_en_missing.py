"""Translate the strings build_en.py could not match, in ordered batches.

The most repeated strings are chrome and status labels; translating those first
unlocks whole pages, so batches run in frequency order.
"""
import hashlib
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
I18N = os.path.join(HERE, "data", "i18n", "en")
OUT = os.path.join(I18N, "missing-parts")
os.makedirs(OUT, exist_ok=True)

missing = json.load(open(os.path.join(I18N, "missing.json"), encoding="utf-8"))
already = {}
for name in ("ui.json",):
    fp = os.path.join(I18N, name)
    if os.path.exists(fp):
        already.update(json.load(open(fp, encoding="utf-8")))
todo = [k for k in missing if k not in already]
CHUNK = 45
GROUPS = [todo[i:i + CHUNK] for i in range(0, len(todo), CHUNK)]

PROMPT = """โฟลเดอร์งาน {HERE}
อ่าน `briefs/2026-09-07_english-spec.md` หัวข้อ "กฎการแปล" ให้ครบก่อนลงมือ

แปลข้อความไทยต่อไปนี้เป็นภาษาอังกฤษ · ทั้งหมด {N} รายการ
ข้อความเหล่านี้มาจากเว็บไกด์เมืองเก่าตะกั่วป่า มีทั้งป้ายสถานะ ปุ่ม หัวข้อ และเนื้อหา

{LIST}

เขียนไฟล์ `data/i18n/en/missing-parts/{SLUG}.json` เป็น JSON object
คีย์คือข้อความไทยเดิม **เป๊ะตัวต่อตัว** ค่าคือคำแปลอังกฤษ
```
{{"ยังไม่ยืนยัน": "Not verified", "ยืนยันแล้ว": "Verified"}}
```

กฎ:
- คีย์ต้องเหมือนต้นฉบับทุกตัวอักษร รวมช่องว่างและลูกศร ↗ ห้ามแก้ไข
- ค่าที่แปลให้คงลูกศร ↗ หรือ · ไว้ถ้าต้นฉบับมี
- ป้ายสถานะให้สั้น กระชับ เช่น "ยังไม่ยืนยัน" -> "Not verified"
- ห้ามเพิ่มข้อเท็จจริงที่ต้นฉบับไม่มี · คำกำกับความไม่แน่นอนต้องอยู่ครบ
- ชื่อวัด ศาลเจ้า ถนน ให้ทับศัพท์ เช่น Wat Kongkha Phimuk, Thanon Si Takua Pa
- ชื่อหน่วยงานราชการให้เขียนเป็น "ชื่อไทย (English name)"
- ปีใช้ ค.ศ. พร้อมวงเล็บ พ.ศ. ถ้าต้นฉบับระบุ พ.ศ.
- ห้าม em-dash และ en-dash · ห้ามคำโฆษณาลอย ๆ

เขียนลง path จริง ห้ามลง scratch · **UTF-8 เท่านั้น**
เสร็จแล้ว json.load ยืนยันว่าคีย์ครบ {N} รายการ แล้วรายงาน
"""


def run(i, keys):
    slug = "miss-" + hashlib.sha1(chr(10).join(keys).encode("utf-8")).hexdigest()[:10]
    out = os.path.join(OUT, slug + ".json")
    if os.path.exists(out) and os.path.getsize(out) > 200:
        return slug, "skip(exists)"
    listing = "\n".join("- " + k for k in keys)
    prompt = (PROMPT.replace("{HERE}", HERE).replace("{N}", str(len(keys)))
              .replace("{LIST}", listing).replace("{SLUG}", slug))
    for attempt in range(3):
        p = subprocess.run([AGY, "--dangerously-skip-permissions", "--model", "gemini-3.1-pro-high",
                            "-p", prompt],
                           cwd=HERE, capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=3000)
        log = (p.stdout or "") + "\n--ERR--\n" + (p.stderr or "")
        open(os.path.join(OUT, slug + ".log"), "w", encoding="utf-8").write(log)
        if os.path.exists(out) and os.path.getsize(out) > 200:
            return slug, "OK"
        if "quota reached" in log:
            time.sleep(900)
            continue
        break
    return slug, "FAIL"


only = set(sys.argv[1:])
groups = list(enumerate(GROUPS))
print("ต้องแปล %d ข้อความ · %d ชุด" % (len(todo), len(groups)), flush=True)
with ThreadPoolExecutor(max_workers=2) as ex:
    for f in as_completed({ex.submit(run, i, g): i for i, g in groups}):
        print("  %s: %s" % f.result(), flush=True)
print("done")
