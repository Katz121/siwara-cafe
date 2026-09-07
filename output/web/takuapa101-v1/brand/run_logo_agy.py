"""Ask agy for logo marks as SVG, three design directions in parallel."""
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
PROJECT = os.path.dirname(HERE)
MARKS = os.path.join(HERE, "marks")
os.makedirs(MARKS, exist_ok=True)
TMPL = open(os.path.join(HERE, "_logo_prompt.txt"), encoding="utf-8").read()

DIRECTIONS = [
    ("arch", 3, "สถาปัตยกรรมของเมือง · ตึกแถวชิโน-โปรตุกีส หน้าจั่ว ซุ้มโค้ง ระเบียงไม้ฉลุ ประตูบานเฟี้ยม · ทำให้ดูร่วมสมัย ไม่ใช่ภาพวาดบ้านแบบเด็ก ๆ"),
    ("river", 3, "สายน้ำ การเดินทาง และการค้า · โค้งแม่น้ำตะกั่วป่า เส้นทางข้ามคาบสมุทร เรือ ท่าเรือ สะพานเหล็ก · เน้นเรียบ ทันสมัย เป็นรูปทรงเรขาคณิต"),
    ("craft", 3, "งานฝีมือและศรัทธา · ลายกระเบื้องเปอรานากัน ลายฉลุ ตราจีน เจดีย์ ตะเกียงเทศกาลกินผัก · เน้นลวดลายที่เอาไปทำสินค้าและสติกเกอร์ต่อได้"),
]


def run(prefix, count, direction):
    prompt = (TMPL.replace("{COUNT_PAD}", "%02d" % count)
                  .replace("{COUNT}", str(count))
                  .replace("{PREFIX}", prefix)
                  .replace("{DIRECTION}", direction))
    p = subprocess.run(
        [AGY, "--dangerously-skip-permissions", "--model", "gemini-3.1-pro-high", "-p", prompt],
        cwd=PROJECT, capture_output=True, text=True, encoding="utf-8",
        errors="replace", timeout=3000)
    open(os.path.join(MARKS, prefix + ".log"), "w", encoding="utf-8").write(
        (p.stdout or "") + "\n--ERR--\n" + (p.stderr or ""))
    made = [f for f in os.listdir(MARKS) if f.startswith(prefix + "-") and f.endswith(".svg")]
    return prefix, "%d svg" % len(made)


only = set(sys.argv[1:])
jobs = [d for d in DIRECTIONS if not only or d[0] in only]
print("directions=%d" % len(jobs), flush=True)
with ThreadPoolExecutor(max_workers=3) as ex:
    for f in as_completed({ex.submit(run, *d): d[0] for d in jobs}):
        print("  %s: %s" % f.result(), flush=True)
print("done")
