"""Fan out the review across codex and agy, one area each, reports only."""
import os
import shutil
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.stdout.reconfigure(encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.dirname(HERE)
CODEX = shutil.which("codex") or shutil.which("codex.cmd") or "codex"
AGY = r"C:\Users\siwat\AppData\Local\agy\bin\agy.cmd"
if not os.path.exists(AGY):
    AGY = shutil.which("agy") or "agy"

SPEC = "อ่าน `audit/SPEC.md` ให้ครบก่อนลงมือ แล้วทำตามกฎทุกข้อ โดยเฉพาะข้อที่ห้ามแก้ไฟล์และห้ามแต่งปัญหา\n\n"

JOBS = {
    # ---------- codex ----------
    "seo-tech": ("codex", SPEC + """งานของคุณ: **ตรวจ SEO และเทคนิคหน้าเว็บ**

ตรวจจากไฟล์ที่ build แล้วใน `site/` และเปิดเว็บจริง https://takuapa101.com ประกอบ

1. title ทุกหน้า · ซ้ำกันไหม ยาวเกิน 60 ตัวอักษรไหม ว่างไหม
2. meta description ทุกหน้า · ซ้ำกันไหม ยาวเกิน 160 ไหม ว่างไหม
   หน้าอังกฤษต้องเป็นภาษาอังกฤษ (ยกเว้นชื่อหน่วยงานไทยที่ตั้งใจคงไว้)
3. canonical ทุกหน้าชี้ตัวเองและเป็น https://takuapa101.com ถูกต้องไหม
4. hreflang · ทุกหน้ามี th, en, x-default ครบไหม และชี้หน้าคู่กันถูกต้องไหม
   หน้าไทยชี้หน้าอังกฤษของตัวเอง ไม่ใช่ชี้หน้าแรก
5. JSON-LD ทุกหน้า · parse ผ่านไหม type ถูกไหม มี field ที่ค่าว่างหรือ null ไหม
   (field ว่างทำให้ rich result โดนปฏิเสธ)
6. sitemap.xml · URL ครบไหม ตรงกับหน้าที่มีจริงไหม มี URL ที่ 404 ไหม
7. ลิงก์ภายในทั้งเว็บ · มีลิงก์ที่ชี้หน้าที่ไม่มีอยู่ไหม (ตรวจจากไฟล์ ไม่ต้องยิง HTTP ทุกเส้น)
8. รูป · มี img ที่ไม่มี alt ไหม · มี src ที่ไฟล์ไม่มีอยู่จริงไหม
9. **ตรวจว่ามี keyword stuffing ไหม** คำเดียวซ้ำถี่ผิดปกติใน title หรือ description
   หรือมีลิสต์คำค้นโชว์บนหน้า ซึ่งไม่ควรมี
10. heading · ทุกหน้ามี h1 เดียวไหม ลำดับ h1 h2 h3 ข้ามขั้นไหม

เขียนรายงานที่ `audit/report-seo-tech.md`""".strip()),

    "code-quality": ("codex", SPEC + """งานของคุณ: **ตรวจโค้ดและความถูกต้องของการ build**

1. รัน `python build_site.py` แล้ว `python build_en.py` · มี warning หรือ error ไหม
2. ตรวจไฟล์ Python ทุกไฟล์ในโฟลเดอร์หลัก · มีฟังก์ชันหรือตัวแปรที่นิยามซ้ำสองที่ไหม
   (เคยเจอ render_rest ซ้ำสองตัวมาแล้ว ตัวหลังทับตัวแรก)
3. ตรวจ JS ทุกไฟล์ใน `site/assets/` ด้วย `node --check` · มีไฟล์ไหน syntax พังไหม
4. ตรวจว่ามีข้อความไทยที่กลายเป็น ??? หรือ mojibake ในไฟล์ไหนไหม
   (เคยเกิดจากการเซฟเป็น cp1252)
5. ตรวจ CSS · มีกฎที่เขียนทับกันเองจนกฎแรกไม่มีผลไหม โดยเฉพาะ display กับ media query
6. เปิดเว็บจริง 8 หน้าด้วย Playwright (ติดตั้งแล้ว) ที่ 1440px และ 390px
   ตรวจ console error, request ที่ตอบ 4xx/5xx, และการล้นแนวนอน
   หน้าที่ต้องตรวจ: / /places/tao-ming/ /map/ /rest/ /eat/ /news/ /trip/ /en/
7. ตรวจว่าปุ่มสลับโหมดกลางคืนทำงานและจำค่าข้ามหน้าไหม
8. ตรวจว่าตะกร้าทริปเพิ่มและลบจุดหมายได้จริงไหม

เขียนรายงานที่ `audit/report-code.md`""".strip()),

    # ---------- agy ----------
    "content-facts": ("agy", SPEC + """งานของคุณ: **ตรวจความถูกต้องของเนื้อหาเทียบแหล่งอ้างอิง**

1. สุ่มตรวจ claim ในหน้าสถานที่ 6 แห่ง เทียบกับ `source_url` ที่ระบุไว้
   เปิดลิงก์ต้นทางอ่านจริง แล้วบอกว่าตรงกันไหม
   ให้เลือก: wat-boromthat, tao-ming, iron-bridge, culture-street, governor-wall, khun-in
2. ตรวจว่ามี claim ไหนที่ status เป็น CONFIRMED แต่แหล่งอ้างอิงไม่ได้ยืนยันชัดขนาดนั้น
   หรือกลับกัน มี claim ที่ยืนยันได้แต่ติดป้ายว่ายังไม่ยืนยัน
3. ตรวจปี พ.ศ. กับ ค.ศ. ในบทความและไทม์ไลน์ · แปลงถูกต้องไหม (พ.ศ. = ค.ศ. + 543)
4. ตรวจว่าลิงก์ `source_url` ทั้งหมดยังเปิดได้ไหม · ลิสต์อันที่ตายแล้ว
5. ตรวจ `data/guide-picks.json` 13 รายการ · ลิงก์ Google Maps เปิดแล้วไปร้านถูกไหม
6. ตรวจว่ามีข้อความไหนในเว็บที่อ้างตัวเลขไม่ตรงกับข้อมูลจริง
   เช่น บอกว่า 59 ร้าน แต่จริง ๆ มี 108 ร้าน

เขียนรายงานที่ `audit/report-facts.md`""".strip()),

    "language": ("agy", SPEC + """งานของคุณ: **ตรวจภาษาและการใช้คำ**

1. ตรวจภาษาไทยทั้งเว็บ · คำผิด คำซ้ำ ประโยคที่อ่านไม่รู้เรื่อง ประโยคที่ขาดหาย
2. ตรวจว่ามี em-dash หรือ en-dash หลงเหลือไหม (เว็บนี้ใช้ · แทน)
   แต่ระวัง คำสมาสอย่าง ชิโน-โปรตุกีส ใช้ยัติภังค์ถูกแล้ว ไม่ใช่ปัญหา
3. ตรวจว่ามีคำโฆษณาเกินจริงหลงเข้ามาไหม เช่น ดีที่สุด ห้ามพลาด สวยที่สุด ที่เดียวในโลก
   เว็บนี้ตั้งใจไม่ใช้คำพวกนี้
4. ตรวจหน้าอังกฤษ 6 หน้า · ภาษาอังกฤษอ่านลื่นไหม มีที่แปลแล้วความหมายเพี้ยนไหม
   หน้าที่ต้องตรวจ: /en/ /en/places/tao-ming/ /en/stories/city/ /en/rest/ /en/eat/ /en/map/
5. ตรวจว่าชื่อสถานที่ทับศัพท์อังกฤษใช้ระบบเดียวกันทั้งเว็บไหม
   เช่น Takua Pa กับ Takuapa ใช้ปนกันตรงไหนบ้าง ควรใช้แบบไหนเป็นหลัก
6. ตรวจคำบรรยายรูปทุกใบ · ตรงกับสิ่งที่อยู่ในรูปไหม (ดู `data/photo-registry.json` ประกอบ)

เขียนรายงานที่ `audit/report-language.md`""".strip()),
}


def run(name):
    runner, prompt = JOBS[name]
    for attempt in range(3):
        if runner == "codex":
            argv = [CODEX, "exec", "-m", "gpt-5.6-luna", "--skip-git-repo-check",
                    "--dangerously-bypass-approvals-and-sandbox", "-"]
            stdin = prompt
        else:
            argv = [AGY, "--dangerously-skip-permissions", "--model", "gemini-3.1-pro-high", "-p", prompt]
            stdin = None
        p = subprocess.run(argv, input=stdin, cwd=PROJECT, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=3000)
        log = (p.stdout or "") + "\n--ERR--\n" + (p.stderr or "")
        open(os.path.join(HERE, name + ".log"), "w", encoding="utf-8").write(log)
        out = os.path.join(HERE, "report-" + name.split('-')[0] + ".md")
        if "quota reached" in log or "usage limit" in log:
            time.sleep(600)
            continue
        return name, f"{runner} rc={p.returncode}"
    return name, "quota"


only = set(sys.argv[1:])
names = [n for n in JOBS if not only or n in only]
print("งานตรวจ %d ชุด" % len(names), flush=True)
with ThreadPoolExecutor(max_workers=4) as ex:
    for f in as_completed({ex.submit(run, n): n for n in names}):
        print("  %s: %s" % f.result(), flush=True)
print("done")
