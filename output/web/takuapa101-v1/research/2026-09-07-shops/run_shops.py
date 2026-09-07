"""Fan out shop discovery across agy, one batch per category slice."""
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
OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)
TMPL = open(os.path.join(HERE, "PROMPT.md"), encoding="utf-8").read()

BATCHES = [
    ("food-oldtown", "ร้านอาหารในย่านเมืองเก่าและตลาดใหญ่ ตะกั่วป่า · เน้นร้านเก่าแก่ ร้านประจำถิ่น อาหารใต้ อาหารจีนฮกเกี้ยน หมี่ฮกเกี้ยน ขนมจีน ติ่มซำ"),
    ("food-wider", "ร้านอาหารในอำเภอตะกั่วป่านอกย่านเมืองเก่า · รวมย่านยาว บางนายสี เขาหลัก คึกคัก · ร้านซีฟู้ด ร้านตามสั่ง ร้านที่นักท่องเที่ยวไป"),
    ("drinks", "ร้านเครื่องดื่มและคาเฟ่ในอำเภอตะกั่วป่า · ร้านกาแฟ โกปี๊ ร้านชา ร้านน้ำ ร้านนั่งชิลในตึกเก่า"),
    ("dessert", "ร้านขนมและเบเกอรีในอำเภอตะกั่วป่า · ขนมพื้นถิ่น ขนมจีนโบราณ เบเกอรี ไอศกรีม ขนมหวานใต้"),
    ("souvenir", "ร้านของฝากและสินค้าท้องถิ่นในอำเภอตะกั่วป่า · เต้าส้อ ขนมของฝาก ผ้า งานคราฟต์ ร้านในถนนสายวัฒนธรรม"),
]


def run(slug, brief):
    out = os.path.join(OUT, slug + ".json")
    if os.path.exists(out) and os.path.getsize(out) > 300:
        return slug, "skip(exists)"
    prompt = TMPL.replace("{CATEGORY}", brief).replace("{SLUG}", slug)
    p = subprocess.run(
        [AGY, "--dangerously-skip-permissions", "--model", "gemini-3.1-pro-high", "-p", prompt],
        cwd=PROJECT, capture_output=True, text=True, encoding="utf-8",
        errors="replace", timeout=3000)
    open(os.path.join(OUT, slug + ".log"), "w", encoding="utf-8").write(
        (p.stdout or "") + "\n--ERR--\n" + (p.stderr or ""))
    ok = os.path.exists(out) and os.path.getsize(out) > 300
    return slug, ("OK %dB" % os.path.getsize(out)) if ok else "FAIL rc=%d" % p.returncode


only = set(sys.argv[1:])
jobs = [b for b in BATCHES if not only or b[0] in only]
print("batches=%d" % len(jobs), flush=True)
with ThreadPoolExecutor(max_workers=3) as ex:
    for f in as_completed({ex.submit(run, s, b): s for s, b in jobs}):
        print("  %s: %s" % f.result(), flush=True)
print("done")
