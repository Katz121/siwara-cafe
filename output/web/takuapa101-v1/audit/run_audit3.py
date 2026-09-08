"""รอบตรวจที่ 3 · ตรวจสถานะหลังแก้ทั้งหมด เน้นหาของที่พังเพิ่มจากการแก้"""
import os, shutil, subprocess, sys
from concurrent.futures import ThreadPoolExecutor, as_completed
sys.stdout.reconfigure(encoding='utf-8')
HERE=os.path.dirname(os.path.abspath(__file__)); PROJECT=os.path.dirname(HERE)
CODEX=shutil.which("codex") or shutil.which("codex.cmd") or "codex"
SPEC=("อ่าน `audit/SPEC.md` ก่อน · ห้ามแก้ไฟล์ · ห้ามแต่งปัญหา · ทุกข้อต้องมีหลักฐาน\n"
      "รอบนี้เว็บเพิ่งถูกแก้หนัก งานคุณคือหาของที่ **พังเพิ่มจากการแก้** ไม่ใช่ทวนของเดิม\n"
      "ขอบเขตแคบ ทำให้จบใน 15 นาที · เสิร์ฟด้วย `python -m http.server 8798 --directory site`\n\n")
J={
"regress-th":SPEC+"""ตรวจหน้าไทยว่ามีอะไรพังจากการแก้รอบล่าสุด
สิ่งที่เพิ่งแก้: ลิงก์แหล่งอ้างอิงที่ตายกลายเป็นข้อความ, คำบรรยายรูปดึงจากทะเบียน,
ตัวเลขร้านคำนวณใหม่, เขียนบทเปิด architecture ใหม่, แยกย่อหน้ายาว, แปลง dash

1. เปิด 12 หน้าไทยด้วย Playwright · หา console error, request 4xx/5xx, การล้นแนวนอนที่ 390 และ 1440
2. ตรวจว่ามีข้อความที่ขาดหาย เพี้ยน หรือมีวงเล็บ/เครื่องหมายค้างจากการแก้ dash ไหม
   ค้นหาคำว่า "ถึง" ทุกจุดบนหน้าเว็บ · อ่านแล้วสมเหตุสมผลทุกจุดไหม
   (ช่วงเวลาใช้ "ถึง" ถูก · แต่ถ้าเป็นตัวคั่นชื่อแหล่งแล้วใช้ "ถึง" คือผิด)
3. ตรวจว่าแหล่งอ้างอิงที่กลายเป็นข้อความ ยังอ่านรู้เรื่องและยังบอกที่มาได้ไหม
4. ตรวจตัวเลขทุกตัวบนหน้าเว็บว่าตรงกันทั้งเว็บไหม (สถานที่ ประเพณี ร้าน รายหมวด)
5. ตรวจว่าบทความ 5 บทยังอ่านต่อเนื่อง ไม่มีย่อหน้าที่ตัดค้างหรือซ้ำจากการแยกย่อหน้า
เขียนที่ `audit/a3-regress-th.md`""",

"regress-en":SPEC+"""ตรวจหน้าอังกฤษว่ามีอะไรพังจากการแก้รอบล่าสุด
สิ่งที่เพิ่งแก้: บั๊ก translate_attrs (เดิมไม่เคยแปล attribute ได้เลย ตอนนี้แปลได้แล้ว),
เพิ่มคำแปล UI 30 กว่ารายการ, เขียนประโยคอังกฤษใหม่ 9 จุด, เติมลิงก์แผนที่ให้ร้าน 59 ร้าน

1. เปิด 10 หน้าอังกฤษด้วย Playwright · console error, request 4xx/5xx, ล้นแนวนอน
2. **ตรวจว่า attribute ที่แปลแล้วไม่มีเครื่องหมายคำพูดเกินหรือ HTML พัง**
   ค้นหา `=""` ซ้อน และ tag ที่โครงสร้างเสีย
3. ตรวจว่าคำแปล UI ใหม่ถูกวางถูกที่ไหม · มี aria-label ไหนที่แปลแล้วความหมายผิดบริบทไหม
4. ตรวจลิงก์ Google Maps 59 เส้นว่า URL ถูกรูปแบบและ encode ถูกไหม · สุ่มเปิด 5 เส้น
5. ตรวจว่าหน้าอังกฤษยังมี hreflang, canonical, title, description ครบและถูกไหม
เขียนที่ `audit/a3-regress-en.md`""",

"regress-assets":SPEC+"""ตรวจไฟล์ภาพและ asset หลังการบีบขนาด
สิ่งที่เพิ่งทำ: แปลง guide/*.jpg เป็น webp, บีบ og/*.png เป็น palette 256 สี,
ย้ายฟอนต์ .ttf ออกจาก site/, สร้างการ์ด og ใหม่ด้วยการตัดคำไทย

1. ตรวจว่าทุก src ใน HTML ชี้ไฟล์ที่มีอยู่จริง · ลิสต์ที่หาย
2. ตรวจว่า og:image ทุกหน้าชี้ไฟล์ที่มีจริง ขนาด 1200x630 จริง
3. เปิดการ์ด og ทั้ง 28 ใบด้วย Pillow · ตรวจว่ามีใบไหนตัวอักษรล้นขอบภาพไหม
   หรือมีใบไหนข้อความหายไปเลยไหม
4. ตรวจว่าฟอนต์ woff2 ยัง build ได้และหน้าเว็บโหลดฟอนต์ครบ 3 ไฟล์
5. ตรวจว่าไม่มี .ttf หรือไฟล์ที่ไม่ควร deploy หลงเหลือใน site/
6. รายงานขนาดรวมของ site/ และไฟล์ที่ยังใหญ่เกิน 300KB
เขียนที่ `audit/a3-regress-assets.md`""",

"regress-build":SPEC+"""ตรวจโค้ดหลังการแก้หลายมือ
รอบที่แล้วมี codex หลายตัวแก้ไฟล์เดียวกันขนานกัน อาจทับกันได้

1. รัน `python build_site.py` แล้ว `python build_en.py` จาก state สะอาด · error/warning ไหม
2. ตรวจไฟล์ Python ทุกไฟล์ · มีฟังก์ชันหรือตัวแปรนิยามซ้ำสองที่ไหม
   มีโค้ดที่ import แล้วไม่ได้ใช้ หรือใช้แล้วไม่ได้ import ไหม
3. ตรวจว่ามีการแก้ที่ทับกันจนได้ผลแปลก ๆ ไหม
   ดูโดยเฉพาะ `build_en.py`, `design.py`, `build_site.py`, `stories.py`, `place_pages.py`
4. `node --check` ทุกไฟล์ JS รวม worker/
5. รัน `python -m unittest test_translate_attrs` · ผ่านไหม
6. ตรวจว่ามี mojibake หรือ ??? ในไฟล์ไหนไหม (เคยเกิดจากเซฟเป็น cp1252)
7. ตรวจว่า sitemap มี 88 URL และตรงกับหน้าที่มีจริง 88 หน้า
เขียนที่ `audit/a3-regress-build.md`""",
}
def run(n):
    q=subprocess.run([CODEX,"exec","-m","gpt-5.6-luna","--skip-git-repo-check",
        "--dangerously-bypass-approvals-and-sandbox","-"],input=J[n],cwd=PROJECT,
        capture_output=True,text=True,encoding="utf-8",errors="replace",timeout=2400)
    open(os.path.join(HERE,"a3-"+n+".log"),"w",encoding="utf-8").write((q.stdout or "")+"\n--ERR--\n"+(q.stderr or ""))
    return n,"rc=%d"%q.returncode
only=set(sys.argv[1:]); names=[n for n in J if not only or n in only]
print("รอบสาม %d งาน"%len(names),flush=True)
with ThreadPoolExecutor(max_workers=4) as ex:
    for f in as_completed({ex.submit(run,n):n for n in names}):
        print("  %s: %s"%f.result(),flush=True)
print("done")
