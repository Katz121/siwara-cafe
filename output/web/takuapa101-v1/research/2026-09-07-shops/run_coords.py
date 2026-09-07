"""Second pass: find coordinates and contact details for the researched shops."""
import json
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
PROJECT = os.path.dirname(os.path.dirname(HERE))
COORDS = os.path.join(HERE, "coords")
os.makedirs(COORDS, exist_ok=True)

SHOPS = json.load(open(os.path.join(PROJECT, "data", "shops-extra.json"), encoding="utf-8"))
TODO = [s for s in SHOPS if not s.get("geo")]
CHUNK = 8
GROUPS = [TODO[i:i + CHUNK] for i in range(0, len(TODO), CHUNK)]

PROMPT = """โฟลเดอร์งาน D:\\Siwaracafeweb\\output\\web\\takuapa101-v1

คุณคือนักหาข้อมูลตำแหน่งร้านค้า · หาพิกัดและช่องทางติดต่อของร้านในอำเภอตะกั่วป่า จังหวัดพังงา

รายชื่อร้านที่ต้องหา ({N} ร้าน):
{LIST}

## สิ่งที่ต้องหาต่อร้าน
- `lat` และ `lng` จาก Google Maps, OpenStreetMap, Wongnai หรือ Mapcarta
- `google_maps_url` ลิงก์ตรงไปหน้าร้านบน Google Maps
- `address_th` ที่อยู่เต็ม · `subdistrict` ตำบล
- `phone` · `facebook` · `hours_th` ถ้ายังไม่มี

## กฎเหล็ก
1. **ห้ามเดาพิกัดเด็ดขาด** ถ้าหาไม่เจอให้ `lat` และ `lng` เป็น null แล้วเขียนเหตุผลใน `note_th`
   พิกัดที่ผิดแย่กว่าไม่มีพิกัด เพราะจะพานักท่องเที่ยวไปผิดที่
2. พิกัดต้องอยู่ในกรอบ lat 8.5 ถึง 9.2 และ lng 98.1 ถึง 98.6 (อำเภอตะกั่วป่าและใกล้เคียง)
   ถ้าได้ค่านอกกรอบนี้ แปลว่าจับร้านผิด ให้ทิ้งแล้วใส่ null
3. ทุกพิกัดต้องมี `source_url` ที่เปิดได้จริง
4. ถ้าเจอว่าร้านปิดกิจการแล้ว ให้ `status: "closed"`

## ผลลัพธ์
เขียนไฟล์ `research/2026-09-07-shops/coords/{SLUG}.json` เป็น JSON array (UTF-8 ไม่ใส่ code fence)
```
[{{"id":"<id เดิมจากรายชื่อ>","name_th":"","lat":null,"lng":null,"source_url":null,
  "google_maps_url":null,"address_th":null,"subdistrict":null,"phone":null,
  "facebook":null,"hours_th":null,"status":"open","note_th":""}}]
```

เขียนลง path จริง ห้ามลง scratch · **UTF-8 เท่านั้น** (PowerShell ใส่ -Encoding utf8 · Python ใส่ encoding='utf-8')
เสร็จแล้ว json.load กลับมายืนยัน แล้วรายงานว่าหาพิกัดเจอกี่ร้านจาก {N}
"""


def run(i, group):
    slug = "batch-%02d" % (i + 1)
    out = os.path.join(COORDS, slug + ".json")
    if os.path.exists(out) and os.path.getsize(out) > 200:
        return slug, "skip(exists)"
    listing = "\n".join(
        "- id=%s | %s | %s" % (s["id"], s["name_th"], s.get("address_th") or "ไม่ทราบที่อยู่")
        for s in group)
    prompt = PROMPT.replace("{N}", str(len(group))).replace("{LIST}", listing).replace("{SLUG}", slug)
    p = subprocess.run(
        [AGY, "--dangerously-skip-permissions", "--model", "gemini-3.1-pro-high", "-p", prompt],
        cwd=PROJECT, capture_output=True, text=True, encoding="utf-8",
        errors="replace", timeout=3000)
    open(os.path.join(COORDS, slug + ".log"), "w", encoding="utf-8").write(
        (p.stdout or "") + "\n--ERR--\n" + (p.stderr or ""))
    ok = os.path.exists(out) and os.path.getsize(out) > 200
    return slug, ("OK" if ok else "FAIL rc=%d" % p.returncode)


print("ร้านที่ยังไม่มีพิกัด %d · แบ่ง %d ชุด" % (len(TODO), len(GROUPS)), flush=True)
with ThreadPoolExecutor(max_workers=3) as ex:
    for f in as_completed({ex.submit(run, i, g): i for i, g in enumerate(GROUPS)}):
        print("  %s: %s" % f.result(), flush=True)
print("done")
