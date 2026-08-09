# -*- coding: utf-8 -*-
"""Copy the approved designs into merch/selected/ with print-friendly names + an index page."""
import io
import shutil
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = Path(__file__).parent
OUT = ROOT / "selected"
OUT.mkdir(exist_ok=True)

# code, source file, new name, Thai title, what it is for
PICKS = [
    ("F01", "codex/f01_angle_lawn_view.png", "F01_lawn-view.png",
     "มุมสนามหน้าร้าน", "โปสเตอร์หลัก · ปกเพจ"),
    ("F02", "codex/f02_angle_before_1932.png", "F02_before-restoration.png",
     "บ้านเดิมก่อนบูรณะ", "คู่กับ F01 เล่าเรื่อง แล้ว/ตอนนี้ · โปสเตอร์"),
    ("F04", "codex/f04_angle_window_counter.png", "F04_window-counter.png",
     "มุมเหงา ๆ ริมหน้าต่าง", "โปสเตอร์ · โปสการ์ด"),
    ("F05", "codex/f05_angle_signature_window.png", "F05_signature-window.png",
     "มุมสวย หน้าต่างกระจกสี", "โปสเตอร์ตัวเด่น · โปสการ์ด"),
    ("F06", "codex/f06_angle_lounge.png", "F06_lounge.png",
     "มุมโซฟาโคมระย้า", "โปสเตอร์"),
    ("F07", "codex/f07_angle_roses_table.png", "F07_roses-table.png",
     "กุหลาบบนโต๊ะ", "การ์ดเล็ก · สติกเกอร์ · ที่รองแก้ว"),
    ("D07", "codex/d07_interior_sketch.png", "D07_interior-pencil.png",
     "ในร้าน ดินสอ + สีไม้", "โปสเตอร์แขวนในร้าน"),
    ("E01", "codex/e01_stickers_objects.png", "E01_stickers-objects.png",
     "ของในร้าน 6 ชิ้น", "แผ่นสติกเกอร์ (ตัดแยกชิ้น)"),
    ("E02", "codex/e02_stickers_house_set.png", "E02_stickers-oldtown.png",
     "ตึกเมืองเก่า 6 ชิ้น", "แผ่นสติกเกอร์ (ตัดแยกชิ้น)"),
    ("E09", "codex/e09_shophouse_row.png", "E09_shophouse-row.png",
     "ตึกแถวชิโนโปรตุกีส 4 คูหา", "โปสเตอร์แนวยาว · ลายสกรีนเสื้อ · ถุงผ้า"),
    ("F08", "codex/f08_angle_oldtown_street.png", "F08_oldtown-street.png",
     "ถนนเมืองเก่าตะกั่วป่า โคมจีนแดง", "โปสเตอร์ · โปสการ์ด"),
    ("G08w", "sketch/g08_oldtown_street_wash.png", "G08w_oldtown-street-wash.png",
     "ถนนเมืองเก่า หมึก+สีน้ำ (จากรูปจริง)", "โปสเตอร์ · โปสการ์ด · มุมเป๊ะตามรูป"),
    ("G08i", "sketch/g08_oldtown_street_ink.png", "G08i_oldtown-street-ink.png",
     "ถนนเมืองเก่า หมึกเส้น (จากรูปจริง)", "สติกเกอร์ · สกรีนเสื้อสีเดียว"),
    ("F09", "codex/f09_shrine_lanterns.png", "F09_shrine-lanterns.png",
     "ศาลเจ้าซินใช่ตึ๋ง โคมแดงเต็มลาน", "โปสเตอร์ · โปสการ์ด"),
    ("F10", "codex/f10_street_from_above.png", "F10_street-from-above.png",
     "ถนนเมืองเก่ามองจากระเบียง หลังฝน", "โปสเตอร์"),
    ("F11", "codex/f11_elephants_old_street.png", "F11_elephants-old-street.png",
     "ขบวนช้างบนถนนสมัยเหมืองแร่", "โปสเตอร์เล่าประวัติ · คู่กับ F12"),
    ("F12", "codex/f12_songthaew_1950s.png", "F12_songthaew-1950s.png",
     "รถโดยสารไม้ยุค 2490 หน้าตึกแถว", "โปสเตอร์เล่าประวัติ · ขาวดำ"),
    ("F13", "codex/f13_street_morning.png", "F13_street-morning.png",
     "ถนนเมืองเก่าตอนเช้า แสงส้ม", "โปสเตอร์ · โปสการ์ด"),
    ("F14", "codex/f14_songthaew_mural.png", "F14_songthaew-mural.png",
     "ภาพวาดรถสองแถวบนกำแพงเก่า", "การ์ด · สติกเกอร์ · ที่รองแก้ว"),
]

CARD = """<figure>
  <a href="{f}" target="_blank"><img src="{f}" loading="lazy" alt="{code}"></a>
  <figcaption><b>{code}</b> · {title}<span>{use}</span><span class="px">{w} x {h} px</span></figcaption>
</figure>"""

PAGE = """<!DOCTYPE html><html lang="th"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>ศิวรา คาเฟ่ · แบบที่เลือกไว้</title>
<link href="https://fonts.googleapis.com/css2?family=Chonburi&family=Sarabun:wght@300;400;600&display=swap" rel="stylesheet">
<style>
 *{box-sizing:border-box}
 body{margin:0;background:#efe6d8;color:#241d19;font-family:'Sarabun',sans-serif;padding:38px 30px 90px}
 h1{font-family:'Chonburi',serif;font-size:38px;margin:0 0 6px}
 p.lead{margin:0 0 28px;font-size:17px;opacity:.82;max-width:880px;line-height:1.7}
 .grid{display:grid;gap:26px;grid-template-columns:repeat(auto-fill,minmax(320px,1fr))}
 figure{margin:0;background:#f7f1e6;border:1px solid #cdbfa9;border-radius:6px;overflow:hidden;
        box-shadow:0 2px 0 #d8cab4}
 figure img{width:100%;display:block;background:#f4ece0}
 figcaption{padding:11px 13px 13px;font-size:15px;line-height:1.55;border-top:1px solid #e0d3bd}
 figcaption b{letter-spacing:.14em}
 figcaption span{display:block;font-size:13px;opacity:.62;margin-top:2px}
 .px{font-variant-numeric:tabular-nums}
</style></head><body>
<h1>ศิวรา คาเฟ่ · แบบที่เลือกไว้</h1>
<p class="lead">@@N@@ แบบที่ผ่านการเลือก เก็บไว้ในโฟลเดอร์ <b>merch/selected/</b> · ไฟล์ต้นฉบับความละเอียดเดิมยังอยู่ใน merch/codex/ ทั้งหมด<br>ขั้นต่อไปที่ทำได้: ขยาย 300dpi สำหรับ A3/A5 · แยกสติกเกอร์เป็นชิ้น ๆ พร้อมเส้นตัด · แปลงเป็นลายสกรีนสีเดียว · วางตัวหนังสือไทยด้วยฟอนต์จริงทับ</p>
<div class="grid">
@@CARDS@@
</div>
</body></html>"""

if __name__ == "__main__":
    from PIL import Image
    cards, rows = [], []
    for code, src, new, title, use in PICKS:
        s = ROOT / src
        d = OUT / new
        shutil.copy2(s, d)
        w, h = Image.open(d).size
        cards.append(CARD.format(f=new, code=code, title=title, use=use, w=w, h=h))
        rows.append(f"{code}  {new}  {w}x{h}  {d.stat().st_size//1024} KB  · {title}")
    (OUT / "INDEX.html").write_text(
        PAGE.replace("@@N@@", str(len(PICKS))).replace("@@CARDS@@", "\n".join(cards)),
        encoding="utf-8")
    readme = ["# แบบที่เลือกไว้ · ศิวรา คาเฟ่", "",
              "เปิด `INDEX.html` เพื่อดูทั้งหมด · ไฟล์ต้นฉบับเดิมอยู่ที่ `../codex/`", ""]
    for code, src, new, title, use in PICKS:
        readme.append(f"- **{code}** `{new}` · {title} · ใช้ทำ: {use}")
    (OUT / "README.md").write_text("\n".join(readme) + "\n", encoding="utf-8")
    print(f"selected/ · {len(PICKS)} files")
    for r in rows:
        print(" ", r)
