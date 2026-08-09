"""agy (Antigravity CLI) writes hand-drawn line-art SVGs for Siwara merch.
3 jobs in parallel max (5 hits rate limits). agy always writes into its scratch dir,
so we sweep the scratch dir afterwards and copy files into merch/agy/.
"""
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

AGY = r"C:\Users\siwat\AppData\Local\agy\bin\agy"
OUT = Path(r"D:\Siwaracafeweb\merch\agy")
SCRATCH = Path(r"C:\Users\siwat\.gemini\antigravity-cli\scratch")
BRIEF = Path(r"D:\Siwaracafeweb\merch\BRIEF.md").read_text(encoding="utf-8")
OUT.mkdir(parents=True, exist_ok=True)

COMMON = (
    "งานนี้ต้องเป็น SVG ที่คุณเขียนเส้นเอง (ห้ามเรียก generate_image ห้ามใช้ bitmap ห้าม embed base64). "
    "พื้นกระดาษครีม #f4ece0 หมึก #241d19 · เน้นได้แค่ #b4451f และ #8a5a2b. "
    "ให้ความรู้สึกวาดมือ: ใช้ path ที่มีจุดหักเล็ก ๆ ไม่สมมาตร, stroke-linecap='round' stroke-linejoin='round', "
    "น้ำหนักเส้นสลับ 1.2-3.2, ลงเงาด้วยเส้น hatching ถี่หรือจุด stippling เท่านั้น ห้ามเทสีแบนทับพื้นที่ใหญ่ ห้าม gradient. "
    "ใส่ filter feTurbulence + feDisplacementMap scale ประมาณ 2 ครอบกลุ่มเส้น เพื่อให้เส้นสั่นเหมือนมือวาด "
    "(แต่ห้ามครอบตัวหนังสือ). ตัวหนังสือไทยใช้ font-family=\"Chonburi, 'Noto Sans Thai', serif\" "
    "ผ่าน @import Google Fonts ใน <style> และสะกดตามที่ brief ให้เป๊ะ. "
    "ต้องวาดรายละเอียดจริงจัง อย่างน้อย 150 path ต่อไฟล์ ไม่ใช่ภาพร่างหยาบ ๆ 20 เส้น. "
    "เขียนไฟล์เดียวจบ ไม่ต้องอธิบายยาว"
)

JOBS = [
    ("a01_house_portrait.svg", 1080, 1350,
     "โปสเตอร์แนวตั้ง ภาพประธานคือตัวบ้านไม้สักของร้าน วาดแบบ elevation เกือบตรงหน้า เต็มความกว้าง "
     "อยู่ช่วงกลางถึงล่างของภาพ · เห็นกระเบื้องดินเผาเป็นแถวๆ ทีละตับ, ช่องลมระแนงใต้จั่ว, ผนังไม้ตีนอน, "
     "หน้าต่างลูกฟัก 3x2 หลายบาน, ประตูไม้บานคู่, โคมไฟผนัง, พุ่มไม้กลมเรียงหน้าบ้าน, สนามหญ้าวงกลม+กรวด, "
     "เนินเขาป่าเป็นเส้น hatching บางๆ ด้านหลัง · ด้านบนเว้นที่ให้หัวเรื่อง 'ศิวรา คาเฟ่' (ใหญ่) "
     "และบรรทัดรอง 'บ้านไม้สักเกือบ 100 ปี ในเมืองเก่าตะกั่วป่า' · ล่างสุด 'SIWARA CAFE · EST. 2475'"),

    ("a02_sticker_sheet.svg", 1080, 1350,
     "แผ่นสติกเกอร์ 10 ชิ้น แต่ละชิ้นมีเส้นตัด dashed รอบตัวเอง (die-cut) เรียงเป็นตะแกรงหลวมๆ เว้นช่องชัด "
     "ห้ามชิ้นทับกัน · ชิ้นที่ต้องมี: (1) ตัวบ้านไม้ทรงจั่วของร้าน (2) นาฬิกาแขวนโบราณตู้ไม้ ลูกตุ้ม มีม้าเล็กบนยอด "
     "(3) แก้วกาแฟร้อนบนจานรอง ไอน้ำม้วน (4) โคมไฟก้านโค้งหัวโคมโดมผ้าจีบ (5) ม้านั่งไม้เบาะลายดอก "
     "(6) เค้กหนึ่งชิ้น (7) แก้วกาแฟฮันนี่เลม่อนใส่น้ำแข็ง มีมะนาวฝาน (8) ช่อดอกมะพร้าว "
     "(9) ลูกเต๋าบอร์ดเกมกับตัวหมาก (10) ตราวงกลมมีคำว่า 'ศิวรา' กับ 'ตะกั่วป่า' โค้งตามวง · "
     "ทุกชิ้นต้องอ่านออกตอนย่อเหลือ 3 ซม. เส้นอย่าบางเกินไป"),

    ("a03_tee_emblem.svg", 1080, 1350,
     "ลายสกรีนอกเสื้อ วางกลางภาพในกรอบสี่เหลี่ยมจัตุรัสประมาณ 760x760 (ที่เหลือปล่อยว่าง) "
     "เป็นตราวงกลมเส้นหนา สกรีนได้จริง: วงกลมสองชั้น, ในวงคือตัวบ้านไม้ทรงจั่วเส้นหนักแบบแกะไม้ "
     "hatching หลังคาเป็นเส้นหนา, ใต้บ้านมีริบบิ้นเส้นหมึกเขียน 'EST. 2475', "
     "ข้อความไทย 'ศิวรา คาเฟ่' โค้งตามขอบวงด้านบน (ใช้ textPath) และ 'ตะกั่วป่า' โค้งตามขอบวงด้านล่าง, "
     "รอบวงโรยเมล็ดกาแฟกับใบไม้เล็ก · ห้ามมีเส้นบางกว่า 2.2 · ใช้แค่ 2 สี"),

    ("a04_oldtown_street.svg", 1080, 1350,
     "ฉากถนนเมืองเก่าตะกั่วป่าแนวตั้ง มุมมองคนเดินถนน: ซ้ายเป็นตึกแถวชิโนโปรตุกีสสองชั้น 3 คูหา "
     "มีช่องลมปูนปั้น หน้าต่างบานเกล็ดไม้ ป้ายร้านเก่า กันสาดสังกะสี · ขวาเป็นบ้านไม้สักของร้านศิวรา "
     "มีป้าย OPEN เล็กๆ · กลางภาพมีเสาไฟฟ้าเอียง สายไฟพาดข้ามฟ้า จักรยานจอด ต้นไม้ริมถนน "
     "พื้นถนนมีเส้นเปอร์สเปกทีฟวิ่งเข้าไปหาจุดลับตา · ลงเงาด้วย cross-hatch แน่นในเงาใต้กันสาด "
     "ล่างสุดมีคำว่า 'ตะกั่วป่า' เล็กๆ กับ 'SIWARA CAFE'"),

    ("a05_interior_scene.svg", 1080, 1350,
     "ฉากภายในร้านแบบเส้นบางประณีต โปร่ง มีที่ว่างเยอะ: ผนังไม้ตีระแนงนอน, ตู้ลิ้นชักไม้สักยาวมีบานตะแกรงลายตาราง, "
     "นาฬิกาแขวนโบราณสองเรือนขนาบภาพวาดทิวทัศน์ในกรอบ, แจกันกุหลาบกับแถวหนังสือบนตู้, "
     "ต้นไม้กระถางด้านหน้าซ้าย, โคมไฟก้านโค้งหัวโดมผ้าจีบโน้มลงเหนือม้านั่งไม้เบาะลายดอก, "
     "หน้าต่างไม้บานเปิดมีแสงบ่ายเข้ามา ตีเส้นแสงเป็นเส้นเฉียงบางๆ · ล่างขวามีบรรทัดเล็ก "
     "'Here, every moment feels like home.'"),

    ("a06_botanical_frame.svg", 1080, 1350,
     "โปสเตอร์กรอบพฤกษศาสตร์: กรอบรอบภาพทำจากพรรณไม้เขียนเส้นแบบตำราพฤกษศาสตร์ "
     "(ใบมอนสเตอรา ทางมะพร้าว ช่อดอกมะพร้าว กิ่งกาแฟมีผลเชอร์รี่ ใบเฟิน) เรียงต่อกันรอบสี่ด้าน "
     "มีเส้นใบและเงา stippling ละเอียด · กลางกรอบเป็นวงรีที่ข้างในวาดบ้านไม้สักของร้านขนาดกลาง "
     "และใต้วงรีเป็นข้อความ 'ศิวรา คาเฟ่' กับบรรทัดเล็ก 'SLOW BAR · COZY CORNER · WARM COFFEE · GOOD TIME'"),
]


def run(job):
    name, w, h, spec = job
    dest = OUT / name
    prompt = (
        f"อ่าน brief นี้ก่อน:\n\n{BRIEF}\n\n"
        f"งานของคุณ: เขียนไฟล์ SVG หนึ่งไฟล์ที่ path นี้ให้สำเร็จ: {dest.as_posix()}\n"
        f"ชื่อไฟล์: {name} · viewBox=\"0 0 {w} {h}\" width={w} height={h}\n\n"
        f"เนื้อหาภาพ: {spec}\n\n{COMMON}"
    )
    print(f"--- start {name}", flush=True)
    p = subprocess.run(
        [AGY, "--dangerously-skip-permissions", "--model", "gemini-3.1-pro-high",
         "--effort", "high", "-p", prompt],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        cwd=str(OUT), timeout=1800,
    )
    if not dest.exists():
        for stray in SCRATCH.rglob(name):
            shutil.copy(stray, dest)
            break
    print(f"--- done {name} exit={p.returncode} exists={dest.exists()} "
          f"size={dest.stat().st_size if dest.exists() else 0}", flush=True)
    if not dest.exists():
        print((p.stdout or "")[-800:], flush=True)
    return dest


if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=3) as ex:
        list(ex.map(run, JOBS))
    print("\n=== results ===")
    for f in sorted(OUT.glob("*.svg")):
        print(f.stat().st_size // 1024, "KB", f.name)
