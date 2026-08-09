# -*- coding: utf-8 -*-
"""Collect every rendered PNG from all engines into one picker gallery page.
Run last · then open merch/PICKER.html in a browser and pick by code (เช่น D01, F05, M03)."""
import io
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = Path(__file__).parent

TITLES = {
    # codex round 1 (too machine-perfect, kept for comparison)
    "c01": ("ภาพแกะไม้ดิจิทัล · ปฏิเสธแล้ว", "Codex", "เนี้ยบเกินไป ไม่เหมือนลายมือคน"),
    "c02": ("ถนนเมืองเก่า แบบแกะไม้ · ปฏิเสธแล้ว", "Codex", "เนี้ยบเกินไป"),
    # codex round 2 · hand media
    "d01": ("ปากกาลูกลื่นในสมุดสเก็ตช์", "Codex", "โปสเตอร์ · สติกเกอร์ใหญ่"),
    "d02": ("ปากกา + สีน้ำเลอะขอบ", "Codex", "โปสเตอร์ · โปสการ์ด"),
    "d03": ("ดินสอ 2B มีเส้นร่างเหลือ", "Codex", "โปสเตอร์ · เติมตัวหนังสือไทยทับได้"),
    "d04": ("พู่กันหมึกเส้นหนา", "Codex", "เสื้อ · ตราปั๊ม"),
    "d05": ("ปากกาคอแร้ง ถนนเมืองเก่า", "Codex", "โปสเตอร์ · ถุงผ้า"),
    "d06": ("ปากกาเมจิก แผ่นสติกเกอร์", "Codex", "สติกเกอร์"),
    "d07": ("ดินสอ + สีไม้ ในร้าน", "Codex", "โปสเตอร์แขวนร้าน"),
    "d08": ("แผนที่เดินเมืองเก่าวาดมือ", "Codex", "ใบแจก · ที่รองแก้ว"),
    # codex round 3 · more
    "e01": ("ของในร้าน 6 ชิ้น ปากกา+สีไม้", "Codex", "สติกเกอร์"),
    "e02": ("ตึกเมืองเก่า 6 ชิ้น", "Codex", "สติกเกอร์"),
    "e03": ("มาร์กเกอร์ ไม่กี่เส้น", "Codex", "เสื้อ (ง่ายที่สุด)"),
    "e04": ("กาแฟ + บ้าน เป็นลายเดียว", "Codex", "เสื้อ · ตรา"),
    "e05": ("ดินสอ แสงเย็น", "Codex", "โปสเตอร์"),
    "e06": ("สมุดพรรณไม้", "Codex", "โปสเตอร์ · ห่อของ"),
    "e07": ("มุมสงบในร้าน", "Codex", "โปสเตอร์"),
    "e08": ("เคาน์เตอร์ slow bar", "Codex", "โปสเตอร์"),
    "e09": ("ตึกแถวชิโนโปรตุกีส 4 คูหา", "Codex", "โปสเตอร์แนวยาว · เสื้อ"),
    "e10": ("สวนหลังร้าน สีน้ำ", "Codex", "โปสเตอร์"),
    "e11": ("ป้ายร้านเขียนมือ", "Codex", "ป้าย · เสื้อ"),
    # codex round 4 · the real angles
    "f01": ("มุมสนามหน้าร้าน (จากรูปจริง)", "Codex · มุมจริง", "โปสเตอร์หลัก"),
    "f02": ("บ้านเดิมก่อนบูรณะ (จากรูปจริง)", "Codex · มุมจริง", "เล่าเรื่อง then/now"),
    "f03": ("มุมร้านกว้าง (จากรูปจริง)", "Codex · มุมจริง", "โปสเตอร์"),
    "f04": ("มุมเหงา ๆ ริมหน้าต่าง (จากรูปจริง)", "Codex · มุมจริง", "โปสเตอร์"),
    "f05": ("มุมสวย หน้าต่างกระจกสี (จากรูปจริง)", "Codex · มุมจริง", "โปสเตอร์ · โปสการ์ด"),
    "f06": ("มุมโซฟาโคมระย้า (จากรูปจริง)", "Codex · มุมจริง", "โปสเตอร์"),
    "f07": ("กุหลาบบนโต๊ะ (จากรูปจริง)", "Codex · มุมจริง", "การ์ด · สติกเกอร์"),
    # claude SVG
    "m01": ("ชุดตราประจำร้าน 6 แบบ", "Claude SVG", "สติกเกอร์ · ปั๊มถุง · เสื้อ"),
    "m02": ("ตู้สะสมของในร้าน 9 ชิ้น", "Claude SVG", "โปสเตอร์ · สติกเกอร์"),
    "m03": ("โปสเตอร์บ้าน เส้นคม", "Claude SVG", "โปสเตอร์ (ตัวหนังสือคมสุด)"),
    "m04": ("ลายสกรีนเสื้อ + ม็อกอัป", "Claude SVG", "เสื้อ"),
    "b01": ("โปสการ์ด/ดวงตราไปรษณีย์", "Claude SVG", "โปสการ์ด · สติกเกอร์"),
    "b02": ("แบบสถาปนิก", "Claude SVG", "โปสเตอร์"),
    "b03": ("แผ่นสติกเกอร์ 10 ชิ้น", "Claude SVG", "สติกเกอร์"),
    "b04": ("การ์ดเมนูลายเส้น", "Claude SVG", "ใบแจก"),
    "b05": ("ตราวงกลม + ม็อกอัปเสื้อ", "Claude SVG", "เสื้อ"),
    "b06": ("แถบเมืองเก่า สกรีนอก", "Claude SVG", "เสื้อ"),
    # photo -> sketch (real angles, exact)
    "g01": ("มุมสนามหน้าร้าน", "จากรูปจริง", "โปสเตอร์หลัก"),
    "g02": ("บ้านเดิมก่อนบูรณะ", "จากรูปจริง", "เล่าเรื่อง then/now"),
    "g03": ("มุมร้านกว้าง", "จากรูปจริง", "โปสเตอร์"),
    "g04": ("มุมโซฟาโคมระย้า", "จากรูปจริง", "โปสเตอร์"),
    "g05": ("มุมเหงา ๆ ริมหน้าต่าง", "จากรูปจริง", "โปสเตอร์"),
    "g06": ("มุมสวย หน้าต่างกระจกสี", "จากรูปจริง", "โปสเตอร์ · โปสการ์ด"),
    "g07": ("กุหลาบบนโต๊ะ", "จากรูปจริง", "การ์ด · สติกเกอร์"),
    # agy
    "a01": ("บ้าน แนวตั้ง", "agy SVG", "โปสเตอร์"),
    "a02": ("แผ่นสติกเกอร์", "agy SVG", "สติกเกอร์"),
    "a03": ("ตราอกเสื้อ", "agy SVG", "เสื้อ"),
    "a04": ("ถนนเมืองเก่า", "agy SVG", "โปสเตอร์"),
    "a05": ("ในร้าน เส้นบาง", "agy SVG", "โปสเตอร์"),
    "a06": ("กรอบพรรณไม้", "agy SVG", "โปสเตอร์"),
}

ORDER = ["g", "f", "d", "e", "m", "b", "a", "c"]


def collect():
    pngs = []
    for d in ("sketch", "codex", "claude", "agy"):
        for f in sorted((ROOT / d).glob("*.png")):
            code = f.stem.split("_")[0].lower()[:3]
            variant = ""
            for v, lab in (("_pencil", "ดินสอ"), ("_ink", "หมึกเส้น"), ("_wash", "หมึก+สีน้ำ")):
                if f.stem.endswith(v):
                    variant = lab
            pngs.append((code, f, variant))
    pngs.sort(key=lambda t: (ORDER.index(t[0][0]) if t[0][0] in ORDER else 9, t[0], t[2]))
    return pngs


CARD = """<figure>
  <a href="{rel}" target="_blank"><img src="{rel}" alt="{code}" loading="lazy"></a>
  <figcaption><b>{code}</b> · {title}<span class="meta">{engine} · ใช้ทำ: {use}</span></figcaption>
</figure>"""

PAGE = """<!DOCTYPE html><html lang="th"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>ศิวรา คาเฟ่ · ลายเส้นให้เลือก</title>
<link href="https://fonts.googleapis.com/css2?family=Chonburi&family=Sarabun:wght@300;400;600&display=swap" rel="stylesheet">
<style>
 *{box-sizing:border-box}
 body{margin:0;background:#efe6d8;color:#241d19;font-family:'Sarabun',sans-serif;padding:38px 30px 90px}
 h1{font-family:'Chonburi',serif;font-size:40px;margin:0 0 6px}
 p.lead{margin:0 0 26px;font-size:17px;opacity:.8;max-width:900px;line-height:1.7}
 .grid{display:grid;gap:26px;grid-template-columns:repeat(auto-fill,minmax(310px,1fr))}
 figure{margin:0;background:#f7f1e6;border:1px solid #cdbfa9;border-radius:6px;overflow:hidden;
        box-shadow:0 2px 0 #d8cab4}
 figure img{width:100%;display:block;background:#f4ece0}
 figcaption{padding:11px 13px 13px;font-size:15px;line-height:1.5;border-top:1px solid #e0d3bd}
 figcaption b{font-family:'Sarabun';letter-spacing:.14em}
 .meta{display:block;font-size:13px;opacity:.62;margin-top:3px}
 .note{margin:34px 0 0;padding:16px 18px;background:#f7f1e6;border-left:4px solid #b4451f;
       font-size:15px;line-height:1.75;max-width:900px}
</style></head><body>
<h1>ศิวรา คาเฟ่ · ลายเส้นให้เลือก</h1>
<p class="lead">@@COUNT@@ แบบ จาก 3 เอนจิน · โค้ด <b>G</b> = ถอดเส้นจากรูปจริงโดยตรง มุมตรงเป๊ะ 100% (p ดินสอ · i หมึก · w หมึก+สีน้ำ) · <b>F</b> = โมเดลวาดใหม่ตามมุมจริง · <b>D/E</b> = ลายมือคนวาด (ปากกา ดินสอ สีน้ำ) · <b>M/B</b> = SVG เส้นคมพร้อมสกรีน คุมตัวหนังสือไทยได้เป๊ะ · <b>A</b> = agy · <b>C</b> = รอบแรกที่เนี้ยบเกินไป เก็บไว้เทียบ<br>คลิกรูปเพื่อดูเต็ม · ชอบอันไหนบอกโค้ดมา เดี๋ยวทำต่อเป็นไฟล์พร้อมพิมพ์ (โปสเตอร์ / สติกเกอร์ die-cut / ฟิล์มสกรีนเสื้อ)</p>
<div class="grid">
@@CARDS@@
</div>
<p class="note">ขั้นต่อไปหลังเลือก: ขยายเป็น 300dpi (A3 โปสเตอร์ / A5 โปสการ์ด) · สติกเกอร์แยกชิ้น + เส้นตัด · ลายเสื้อแยกเป็นสีเดียวสำหรับทำบล็อกสกรีน · เติมตัวหนังสือไทยด้วยฟอนต์จริงทับบนภาพวาดที่เว้นที่ว่างไว้</p>
</body></html>"""

if __name__ == "__main__":
    pngs = collect()
    cards = []
    for code, f, variant in pngs:
        t = TITLES.get(code, ("(ยังไม่ตั้งชื่อ)", "?", "?"))
        title = t[0] + (f" · {variant}" if variant else "")
        label = code.upper() + ({"ดินสอ": "p", "หมึกเส้น": "i", "หมึก+สีน้ำ": "w"}.get(variant, ""))
        cards.append(CARD.format(rel=f.relative_to(ROOT).as_posix(), code=label,
                                 title=title, engine=t[1], use=t[2]))
    out = ROOT / "PICKER.html"
    out.write_text(PAGE.replace("@@COUNT@@", str(len(pngs)))
                       .replace("@@CARDS@@", "\n".join(cards)), encoding="utf-8")
    print(f"{out}  ·  {len(pngs)} designs")
    for c, f, v in pngs:
        print(" ", c.upper(), f.name)
