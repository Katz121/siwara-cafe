"""รอบตรวจที่ 2 · งานย่อยเล็กลง เพื่อไม่ให้ตัวตรวจหมดเวลากลางทาง"""
import os, shutil, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor, as_completed
sys.stdout.reconfigure(encoding='utf-8')
HERE=os.path.dirname(os.path.abspath(__file__)); PROJECT=os.path.dirname(HERE)
CODEX=shutil.which("codex") or shutil.which("codex.cmd") or "codex"
AGY=r"C:\Users\siwat\AppData\Local\agy\bin\agy.cmd"
if not os.path.exists(AGY): AGY=shutil.which("agy") or "agy"
SPEC=("อ่าน `audit/SPEC.md` ให้ครบก่อนลงมือ แล้วทำตามกฎทุกข้อ โดยเฉพาะข้อห้ามแก้ไฟล์และห้ามแต่งปัญหา\n"
      "งานนี้ขอบเขตแคบ ทำให้จบใน 15 นาที · ถ้าตรวจข้อไหนไม่ได้ ให้เขียนว่าตรวจไม่ได้เพราะอะไร แล้วไปข้อถัดไป\n"
      "เสิร์ฟไฟล์ด้วย `python -m http.server 8799 --directory site` แล้วเปิด http://127.0.0.1:8799 ถ้าต้องใช้เบราว์เซอร์ (Playwright ติดตั้งแล้ว)\n\n")
J={
"a11y":("codex",SPEC+"""ตรวจการเข้าถึง (accessibility) ด้วย Playwright ที่ 390px และ 1440px
หน้าที่ต้องตรวจ: / /places/ /places/tao-ming/ /stories/city/ /map/ /trip/
1. ทุก img มี alt ที่มีความหมายไหม (alt ว่างใช้ได้เฉพาะภาพประดับ)
2. ปุ่มและลิงก์ที่เป็นไอคอนล้วน มี aria-label ไหม
3. contrast ของตัวอักษรกับพื้นหลัง ผ่าน WCAG AA ไหม ทั้งโหมดสว่างและโหมดกลางคืน
   (สลับโหมดด้วยปุ่ม [data-theme-toggle])
4. เดินด้วย Tab ทั้งหน้า · focus มองเห็นไหม มีกับดัก focus ไหม เมนูมือถือปิดด้วย Esc ได้ไหม
5. พื้นที่กดบนมือถือเล็กกว่า 44x44px ตรงไหนบ้าง
เขียนรายงานที่ `audit/a2-a11y.md`"""),
"perf":("codex",SPEC+"""ตรวจน้ำหนักและความเร็ว
1. ขนาดไฟล์ทุกอย่างใน `site/assets/` · ไฟล์ไหนใหญ่เกิน 300KB บ้าง ลดได้ไหมและลดยังไง
2. รูปทุกใบมี width/height กำกับไหม (กันหน้าเด้ง) และมี loading=lazy ตรงที่ควรมีไหม
3. หน้าไหน HTML ใหญ่ผิดปกติ · ลิสต์ 5 อันดับพร้อมขนาด
4. วัดด้วย Playwright: จำนวน request, ขนาดรวม, และเวลา DOMContentLoaded ของ / และ /map/
5. ฟอนต์ · โหลดกี่ไฟล์ ซ้ำซ้อนไหม มี preload ที่ไม่ได้ใช้ไหม
เขียนรายงานที่ `audit/a2-perf.md`"""),
"jsrt":("codex",SPEC+"""ตรวจ JavaScript ตอนรันจริงด้วย Playwright ทุกหน้าใน `site/` ที่ไม่ใช่ /en/
1. เก็บ console error และ warning ทุกหน้า · ลิสต์พร้อมชื่อหน้า
2. เก็บ request ที่ตอบ 404 หรือ 5xx ทุกหน้า
3. ทดสอบฟังก์ชัน: ค้นหา (Ctrl+K), ตัวกรองใน /places/ และ /eat/, ปุ่มธีม, ตะกร้าทริป
   ทำงานถูกต้องไหม · จำค่าข้ามหน้าไหม
4. ตรวจว่ามี event listener ที่ผูกซ้ำสองรอบไหม (เคยเจอ trip.js โหลดซ้ำมาแล้ว)
เขียนรายงานที่ `audit/a2-jsrt.md`"""),
"data":("codex",SPEC+"""ตรวจความสอดคล้องของไฟล์ข้อมูล (งานอ่านไฟล์ล้วน ไม่ต้องเปิดเน็ต)
1. `data/*.json` ทุกไฟล์ parse ผ่านไหม มีไฟล์ว่างหรือ BOM ไหม
2. id ของสถานที่ที่อ้างถึงใน stories, routes, guide-picks, map-points
   มีอยู่จริงใน `places-enriched.json` ทุกตัวไหม · ลิสต์ id ที่อ้างถึงแต่ไม่มี
3. `data/photo-registry.json` · ไฟล์รูปที่อ้างถึงมีอยู่จริงใน `site/assets/` ทุกใบไหม
   และมีรูปใน assets ที่ไม่ได้อยู่ในทะเบียนแต่ถูกใช้บนหน้าเว็บไหม
4. ตรวจว่ามีสถานที่ไหนไม่มี geo, ไม่มีรูป, หรือไม่มี source เลย · ลิสต์ให้ครบ
5. ตรวจว่าจำนวนที่เขียนบนหน้าเว็บ (20 สถานที่, 7 ประเพณี, 59 รายการ) ตรงกับข้อมูลจริงไหม
เขียนรายงานที่ `audit/a2-data.md`"""),
"seo2":("codex",SPEC+"""ตรวจ SEO รอบสอง เน้นสิ่งที่รอบแรกยังไม่ได้ดู
1. `site/sitemap.xml` และ `robots.txt` · ถูกต้องและสอดคล้องกันไหม
2. JSON-LD ทุกหน้า parse ผ่านไหม · @type เหมาะกับเนื้อหาไหม · มี field ว่างหรือ null ไหม
3. Open Graph และ Twitter card ครบทุกหน้าไหม · og:image ชี้ไฟล์ที่มีจริงไหม ขนาดเหมาะไหม
4. title และ description · ยาวเกิน 60/160 ตัวอักษรตรงไหน · ซ้ำกันตรงไหน (ทั้งไทยและอังกฤษ)
5. ลิงก์ภายในไปยัง siwaracafe.com · กี่เส้น anchor text หลากหลายไหม ดูเป็นธรรมชาติไหม
   หรือดูเหมือนยัด backlink · ให้ความเห็นตรงไปตรงมา
6. คีย์เวิร์ด ตะกั่วป่า / takuapa / Takua Pa · กระจายเป็นธรรมชาติไหม หรือถี่จนดูเป็นการยัดคำ
เขียนรายงานที่ `audit/a2-seo.md`"""),
"news":("codex",SPEC+"""ตรวจระบบข่าวอัตโนมัติใน `worker/`
1. อ่าน `worker/src/index.js`, `filter.js`, `recheck.js` · หา bug เชิงตรรกะ
   โดยเฉพาะ: การกันข่าวซ้ำ, การแกะลิงก์จริงออกจากลิงก์ห่อของ Bing, การจัดการ error
2. ถ้า feed ต้นทางล่มหรือคืน 503 ระบบจะพังทั้งระบบไหม หรือข้ามไปตัวถัดไปได้
3. ถ้า AI คืนคำตอบผิดรูปแบบ จะเกิดอะไรขึ้น · มีทางที่ข่าวผิดหลุดขึ้นเว็บไหม
4. ยิง https://takuapa101-news.siwatid-99.workers.dev/api/news ดูข้อมูลที่คืนมาจริง
   ลิงก์ในผลลัพธ์เปิดไปถึงบทความจริงไหม (สุ่มเช็ก 5 เส้นด้วย HTTP)
5. มีข้อมูลลับหรือคีย์หลุดในโค้ดที่ deploy ไหม
เขียนรายงานที่ `audit/a2-news.md`"""),
"readth":("codex",SPEC+"""ตรวจคุณภาพการอ่านภาษาไทย เฉพาะ 5 บทความใน `data/stories/*.json`
อ่านทั้ง 5 บทจริง แล้วตอบตรงไปตรงมา
1. บทไหนเปิดเรื่องได้ดี บทไหนเปิดแล้วน่าเบื่อ · ยกประโยคมาให้เห็น
2. มีย่อหน้าไหนยาวจนอ่านยากบนมือถือไหม · ระบุบทและย่อหน้า
3. มีการเล่าซ้ำข้อมูลเดิมข้ามบทไหม · ระบุว่าซ้ำตรงไหน
4. น้ำเสียงสม่ำเสมอทั้ง 5 บทไหม หรือบางบทหลุดเป็นภาษาราชการ
5. ถ้าจะแก้แค่ 3 จุดให้ทั้งเว็บอ่านดีขึ้นชัดเจน ควรแก้ตรงไหน
เขียนรายงานที่ `audit/a2-readth.md`"""),
"enq":("codex",SPEC+"""ตรวจคุณภาพภาษาอังกฤษ 8 หน้าใน `site/en/`
/en/ /en/places/ /en/places/tao-ming/ /en/places/iron-bridge/
/en/stories/city/ /en/rest/ /en/eat/ /en/trip/
1. ประโยคไหนอ่านแล้วรู้ว่าแปลมา ไม่ใช่ภาษาอังกฤษที่เจ้าของภาษาเขียน · ยกมาให้เห็น
2. มีที่แปลแล้วความหมายเพี้ยนไปจากไทยไหม
3. มีข้อความไทยตกค้างที่ไม่ใช่ชื่อหน่วยงานราชการไหม (ชื่อหน่วยงานตั้งใจคงไว้ ไม่ใช่ปัญหา)
4. ปุ่มและป้ายกำกับ · ใช้คำอังกฤษที่คนต่างชาติเข้าใจทันทีไหม
เขียนรายงานที่ `audit/a2-enq.md`"""),
"ux":("codex",SPEC+"""ตรวจการใช้งานจริงในมุมนักท่องเที่ยว (ไม่ต้องเขียนโค้ด อ่าน HTML และเปิดเว็บดู)
สมมุติสถานการณ์แล้วเดินตามจริง แล้วบอกว่าติดตรงไหน
1. นักท่องเที่ยวไทยมาถึงตะกั่วป่าตอนเช้า มีเวลาครึ่งวัน · จากหน้าแรกกี่คลิกถึงจะได้แผน
2. ชาวต่างชาติเปิด /en/ อยากรู้ว่ากินอะไรได้บ้างและร้านอยู่ตรงไหน · ทำได้ไหม ติดตรงไหน
3. คนอยากรู้ว่าเทศกาลกินผักปีนี้จัดวันไหน · หาเจอไหม ใช้เวลากี่ขั้น
4. อะไรบนหน้าแรกที่ไม่จำเป็นและควรตัดทิ้ง · ตอบตรง ๆ
เขียนรายงานที่ `audit/a2-ux.md`"""),
"photo":("codex",SPEC+"""ตรวจการใช้ภาพทั้งเว็บเทียบ `data/photo-registry.json`
กฎของเว็บนี้: รูปหนึ่งใบใช้ได้เฉพาะหน้าที่มันเป็นภาพของสิ่งนั้นจริง และคำบรรยายต้องมาจากทะเบียนเท่านั้น
1. ไล่ทุก img ในหน้า `site/` ที่ไม่ใช่ /en/ · รูปไหนถูกใช้บนหน้าที่ไม่อยู่ใน allowed_on
2. คำบรรยายบนหน้าเว็บตรงกับ caption_th ในทะเบียนทุกใบไหม · อันไหนถูกเขียนใหม่
3. รูปเดียวกันถูกใช้ซ้ำเกิน 3 หน้าไหม · ลิสต์พร้อมจำนวน
4. ภาพวาดที่ใช้แทนภาพถ่าย · มีจุดไหนที่ผู้อ่านอาจเข้าใจผิดว่าเป็นภาพถ่ายจริงไหม
เขียนรายงานที่ `audit/a2-photo.md`"""),
}
def run(n):
    r,p=J[n]
    for _ in range(2):
        if r=="codex":
            argv=[CODEX,"exec","-m","gpt-5.6-luna","--skip-git-repo-check","--dangerously-bypass-approvals-and-sandbox","-"]; si=p
        else:
            argv=[AGY,"--dangerously-skip-permissions","--model","gemini-3.1-pro-high","-p",p]; si=None
        try:
            q=subprocess.run(argv,input=si,cwd=PROJECT,capture_output=True,text=True,encoding="utf-8",errors="replace",timeout=1800)
        except subprocess.TimeoutExpired:
            open(os.path.join(HERE,"a2-"+n+".log"),"w",encoding="utf-8").write("timeout"); return n,"timeout"
        log=(q.stdout or "")+"\n--ERR--\n"+(q.stderr or "")
        open(os.path.join(HERE,"a2-"+n+".log"),"w",encoding="utf-8").write(log)
        if "quota reached" in log or "usage limit" in log: time.sleep(420); continue
        return n,"%s rc=%d"%(r,q.returncode)
    return n,"quota"
only=set(sys.argv[1:]); names=[n for n in J if not only or n in only]
print("รอบสอง %d งาน"%len(names),flush=True)
with ThreadPoolExecutor(max_workers=5) as ex:
    for f in as_completed({ex.submit(run,n):n for n in names}):
        print("  %s: %s"%f.result(),flush=True)
print("done")
