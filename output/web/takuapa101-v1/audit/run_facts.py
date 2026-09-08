"""content-facts แตกเป็น 4 งานย่อย · agy หมดเวลาเมื่อรวมเป็นงานเดียว"""
import os, shutil, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor, as_completed
sys.stdout.reconfigure(encoding='utf-8')
HERE=os.path.dirname(os.path.abspath(__file__)); PROJECT=os.path.dirname(HERE)
CODEX=shutil.which("codex") or shutil.which("codex.cmd") or "codex"
SPEC="อ่าน `audit/SPEC.md` ให้ครบก่อนลงมือ แล้วทำตามกฎทุกข้อ โดยเฉพาะข้อที่ห้ามแก้ไฟล์และห้ามแต่งปัญหา\nงานนี้เล็ก ทำให้จบใน 15 นาที ถ้าเปิดลิงก์ไหนไม่ได้ให้เขียนว่าเปิดไม่ได้ แล้วไปข้อถัดไป\n\n"
JOBS={
 "claims-a": SPEC+"""ตรวจ claim ใน `data/places-enriched.json` เฉพาะ 3 แห่งนี้: wat-boromthat, tao-ming, iron-bridge
เปิด `source_url` ของแต่ละ claim อ่านจริง แล้วบอกว่าเนื้อความตรงกันไหม
ชี้เฉพาะอันที่ status เป็น CONFIRMED แต่แหล่งไม่ได้ยืนยันชัดขนาดนั้น หรือกลับกัน
เขียนรายงานที่ `audit/facts-claims-a.md`""",
 "claims-b": SPEC+"""ตรวจ claim ใน `data/places-enriched.json` เฉพาะ 3 แห่งนี้: culture-street, governor-wall, khun-in
เปิด `source_url` ของแต่ละ claim อ่านจริง แล้วบอกว่าเนื้อความตรงกันไหม
ชี้เฉพาะอันที่ status เป็น CONFIRMED แต่แหล่งไม่ได้ยืนยันชัดขนาดนั้น หรือกลับกัน
เขียนรายงานที่ `audit/facts-claims-b.md`""",
 "years": SPEC+"""งานคำนวณล้วน ไม่ต้องเปิดเน็ต
1. หาปี พ.ศ. และ ค.ศ. ทุกจุดใน `data/places-enriched.json` และ `data/stories/*.json`
   ตรวจว่าแปลงถูกไหม (พ.ศ. = ค.ศ. + 543) ลิสต์เฉพาะคู่ที่ผิด
2. ตรวจไทม์ไลน์ทุกแห่ง เรียงปีถูกลำดับไหม มีปีที่เป็นไปไม่ได้ไหม
3. ตรวจตัวเลขที่เขียนบนหน้าเว็บใน `site/` เทียบข้อมูลจริง เช่น จำนวนร้าน จำนวนสถานที่
   นับจากไฟล์ข้อมูลจริงแล้วเทียบ ลิสต์เฉพาะที่ไม่ตรง
เขียนรายงานที่ `audit/facts-years.md`""",
 "links": SPEC+"""งานเช็กลิงก์
1. รวบรวม `source_url` ทั้งหมดจาก `data/places-enriched.json` (ไม่ซ้ำ)
   ยิง HTTP HEAD หรือ GET ด้วย python ตรวจว่าเปิดได้ไหม ลิสต์อันที่ 404 หรือตายแล้ว
2. ตรวจลิงก์ Google Maps ใน `data/guide-picks.json` ทั้ง 13 รายการ
   ว่า URL ประกอบถูกรูปแบบไหม และพิกัดหรือชื่อร้านในลิงก์ตรงกับรายการไหม
เขียนรายงานที่ `audit/facts-links.md`"""}
def run(name):
    p=subprocess.run([CODEX,"exec","-m","gpt-5.6-luna","--skip-git-repo-check",
        "--dangerously-bypass-approvals-and-sandbox","-"],input=JOBS[name],cwd=PROJECT,
        capture_output=True,text=True,encoding="utf-8",errors="replace",timeout=1800)
    open(os.path.join(HERE,"facts-"+name+".log"),"w",encoding="utf-8").write((p.stdout or "")+"\n--ERR--\n"+(p.stderr or ""))
    return name,"rc=%d"%p.returncode
only=set(sys.argv[1:]); names=[n for n in JOBS if not only or n in only]
print("งานย่อย %d ชุด"%len(names),flush=True)
with ThreadPoolExecutor(max_workers=4) as ex:
    for f in as_completed({ex.submit(run,n):n for n in names}):
        print("  %s: %s"%f.result(),flush=True)
print("done")
