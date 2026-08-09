# -*- coding: utf-8 -*-
"""Build print-ready A6 postcards (front + back) for Siwara Cafe.

A6 trim 105 x 148 mm · 3 mm bleed all round -> 111 x 154 mm · 300 dpi -> 1311 x 1819 px
Safe area: 5 mm inside the trim (so 8 mm in from the bleed edge).

Outputs into merch/print/postcards/:
  <CODE>_front.png / <CODE>_back.png   300 dpi, bleed included
  SIWARA_postcards_A6_print.pdf        all pages, front then back, ready to send to the printer
  GUIDE.md                             what to tell the print shop
"""
import io
import subprocess
import sys
from pathlib import Path

from PIL import Image

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).parent
SEL = ROOT / "selected"
OUT = ROOT / "print" / "postcards"
OUT.mkdir(parents=True, exist_ok=True)

DPI = 300
MM = DPI / 25.4
W = round(111 * MM)          # 1311 px  (105 + 3 + 3)
H = round(154 * MM)          # 1819 px  (148 + 3 + 3)
BLEED = round(3 * MM)        # 35 px
SAFE = round(8 * MM)         # 94 px from the bleed edge

SHOP = {
    "th": "ศิวรา คาเฟ่",
    "en": "SIWARA CAFE",
    "addr": "53 ถนนราษฎร์บำรุง ต.ตะกั่วป่า อ.ตะกั่วป่า จ.พังงา 82110",
    "hours": "เปิดอังคาร · อาทิตย์  10:00 · 17:00  (ปิดวันจันทร์)",
    "web": "siwara.cafe",
    "social": "FB siwaracafetakuapa   ·   IG @si.wara_cafe   ·   TikTok @siwaracafe",
    "tel": "097 350 1514",
}

CARDS = [
    ("F05", "F05_signature-window.png", "มุมสวย · หน้าต่างกระจกสี",
     "แสงบ่ายผ่านกระจกอัดลายสีเหลืองกับชมพู บนบ้านไม้สักอายุเกือบร้อยปี"),
    ("F07", "F07_roses-table.png", "กุหลาบบนโต๊ะ",
     "ดอกไม้สดบนโต๊ะไม้ เปลี่ยนใหม่ทุกเช้าก่อนเปิดร้าน"),
    ("F08", "F08_oldtown-street.png", "ถนนเมืองเก่าตะกั่วป่า",
     "โคมแดงสองแถวเหนือถนนสายวัฒนธรรม หน้าตึกแถวชิโนโปรตุกีส"),
    ("F13", "F13_street-morning.png", "เมืองเก่าตอนเช้า",
     "แสงเช้าสาดกำแพงตึกแถว ก่อนร้านรวงจะเปิดประตู"),
    ("F14", "F14_songthaew-mural.png", "รถสองแถวบนกำแพงเก่า",
     "ภาพวาดรถสองแถวตะกั่วป่า · เขาหลัก บนผนังคราบกาลเวลา"),
    ("F02", "F02_before-restoration.png", "บ้านหลังนี้เมื่อก่อน",
     "บ้านไม้สักหลังคาสังกะสี ก่อนบูรณะมาเป็นศิวรา คาเฟ่"),
    ("F09", "F09_shrine-lanterns.png", "ศาลเจ้าซินใช่ตึ๋ง",
     "โคมแดงเต็มลานศาลเจ้า หัวใจของเมืองเก่าตะกั่วป่า"),
    ("F11", "F11_elephants-old-street.png", "ตะกั่วป่าเมื่อครั้งเหมืองแร่",
     "ขบวนช้างเดินกลางถนนสายเดียวกับที่คุณเพิ่งเดินผ่าน"),
]

BACK_TPL = """<!DOCTYPE html><html lang="th"><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Chonburi&family=Sarabun:wght@300;400;600&display=swap" rel="stylesheet">
<style>
  @page{{size:{W}px {H}px;margin:0}}
  *{{box-sizing:border-box}}
  html,body{{margin:0;padding:0;width:{W}px;height:{H}px;overflow:hidden;background:#f4ece0}}
  .sheet{{position:relative;width:{W}px;height:{H}px;
         font-family:'Sarabun',sans-serif;color:#241d19}}
  /* everything inside .safe is guaranteed not to be cut off */
  .safe{{position:absolute;left:{SAFE}px;top:{SAFE}px;
        width:{IW}px;height:{IH}px}}
  .head{{display:flex;align-items:baseline;gap:14px;
        border-bottom:1.5px solid #241d19;padding-bottom:10px}}
  .th{{font-family:'Chonburi',serif;font-size:40px;line-height:1}}
  .en{{font-size:17px;letter-spacing:.26em;opacity:.7}}
  .caption{{margin-top:14px;font-size:23px;font-weight:600}}
  .desc{{margin-top:5px;font-size:17px;line-height:1.55;opacity:.78;max-width:560px}}
  .divider{{position:absolute;left:{DIVX}px;top:{DIVT}px;width:1.5px;height:{DIVH}px;
           background:#241d19;opacity:.55}}
  .lines{{position:absolute;left:0;top:{LT}px;width:{LW}px}}
  .lines div{{height:1px;background:#241d19;opacity:.2;margin-bottom:{LGAP}px}}
  .stamp{{position:absolute;right:0;top:{LT}px;width:{STW}px;height:{STH}px;
         border:1.5px dashed #241d19;opacity:.55;border-radius:3px;
         display:flex;align-items:center;justify-content:center;
         font-size:13px;letter-spacing:.12em;text-align:center;line-height:1.5;padding:6px}}
  .addr{{position:absolute;right:0;top:{AT}px;width:{AW}px}}
  .addr div{{height:1px;background:#241d19;opacity:.2;margin-bottom:{AGAP}px}}
  .addr .lbl{{height:auto;background:none;opacity:.5;font-size:13px;letter-spacing:.14em;
             margin-bottom:16px}}
  .foot{{position:absolute;left:0;bottom:0;width:{IW}px;
        border-top:1.5px solid #241d19;padding-top:9px;font-size:14.5px;line-height:1.7}}
  .foot b{{font-weight:600}}
  .foot .row2{{opacity:.72}}
  .code{{position:absolute;right:0;bottom:0;font-size:12px;opacity:.45;letter-spacing:.16em}}
</style></head><body>
<div class="sheet">
  <div class="divider"></div>
  <div class="safe">
    <div class="head"><span class="th">{shop_th}</span><span class="en">{shop_en}</span></div>
    <div class="caption">{caption}</div>
    <div class="desc">{desc}</div>

    <div class="lines">{LROWS}</div>

    <div class="stamp">ติด<br>แสตมป์</div>
    <div class="addr">
      <div class="lbl">ถึง / TO</div>
      <div></div><div></div><div></div><div></div>
    </div>

    <div class="foot">
      <div><b>{addr}</b></div>
      <div class="row2">{hours}  ·  โทร {tel}</div>
      <div class="row2">{web}  ·  {social}</div>
      <div class="code">{code}</div>
    </div>
  </div>
</div>
</body></html>"""


def front(src: Path, dst: Path):
    """Portrait artwork is cover-cropped to fill the card. Square or landscape artwork is
    fitted whole onto the cream page instead, because cropping it to portrait chops the
    subject in half (F14 lost the back of the truck that way)."""
    im = Image.open(src).convert("RGB")
    sw, sh = im.size
    if sw / sh <= 0.75:                                   # portrait enough to fill
        scale = max(W / sw, H / sh)
        nw, nh = round(sw * scale), round(sh * scale)
        im = im.resize((nw, nh), Image.LANCZOS)
        left, top = (nw - W) // 2, (nh - H) // 2
        out = im.crop((left, top, left + W, top + H))
    else:                                                 # fit whole, cream margin
        pad = round(6 * MM)
        scale = min((W - 2 * pad) / sw, (H - 2 * pad) / sh)
        nw, nh = round(sw * scale), round(sh * scale)
        im = im.resize((nw, nh), Image.LANCZOS)
        out = Image.new("RGB", (W, H), (244, 236, 224))
        out.paste(im, ((W - nw) // 2, round((H - nh) * 0.42)))
    out.save(dst, dpi=(DPI, DPI))
    return out


def build_backs(cards):
    html_dir = OUT / "_html"
    html_dir.mkdir(exist_ok=True)
    files = []
    inner_w, inner_h = W - 2 * SAFE, H - 2 * SAFE
    for code, _src, caption, desc in cards:
        # the writing zone starts just under the caption block and runs down to the footer,
        # so the card does not have a dead band across its middle
        top = round(inner_h * 0.20)
        bottom = round(inner_h * 0.87)
        nlines = 9
        lgap = round((bottom - top) / nlines)
        addr_top = top + round(34 * MM) + 26
        agap = round((bottom - addr_top) / 4)
        html = BACK_TPL.format(
            W=W, H=H, SAFE=SAFE, IW=inner_w, IH=inner_h,
            DIVX=W // 2, DIVT=SAFE + top - round(4 * MM), DIVH=bottom - top + round(8 * MM),
            LT=top, LW=round(inner_w * 0.44), LGAP=lgap, AGAP=agap,
            LROWS='<div></div>' * nlines,
            STW=round(24 * MM), STH=round(30 * MM),
            AT=addr_top, AW=round(inner_w * 0.44),
            shop_th=SHOP["th"], shop_en=SHOP["en"], caption=caption, desc=desc,
            addr=SHOP["addr"], hours=SHOP["hours"], tel=SHOP["tel"],
            web=SHOP["web"], social=SHOP["social"], code=code,
        )
        f = html_dir / f"{code}_back.html"
        f.write_text(html, encoding="utf-8")
        files.append(f)
    cmd = [sys.executable, r"D:\workFull\scripts\render_covers_png.py",
           "--width", str(W), "--height", str(H), *[str(f) for f in files]]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    print((r.stdout or "")[-500:])
    for f in files:
        png = f.with_suffix(".png")
        im = Image.open(png).convert("RGB")
        if im.size != (W, H):                       # render script shoots at 2x device scale
            im = im.resize((W, H), Image.LANCZOS)
        dst = OUT / png.name
        im.save(dst, dpi=(DPI, DPI))
    return [OUT / (f.stem + ".png") for f in files]


if __name__ == "__main__":
    pages = []
    for code, src, caption, desc in CARDS:
        f = OUT / f"{code}_front.png"
        front(SEL / src, f)
        print(f"  front {f.name}")
    build_backs(CARDS)
    for code, *_ in CARDS:
        pages.append(Image.open(OUT / f"{code}_front.png").convert("RGB"))
        pages.append(Image.open(OUT / f"{code}_back.png").convert("RGB"))
    pdf = OUT / "SIWARA_postcards_A6_print.pdf"
    pages[0].save(pdf, save_all=True, append_images=pages[1:], resolution=DPI)
    print(f"\n  PDF {pdf.name} · {len(pages)} หน้า ({len(CARDS)} ลาย หน้า-หลัง)")

    guide = f"""# โปสการ์ดศิวรา คาเฟ่ · ไฟล์พร้อมส่งโรงพิมพ์

## สั่งพิมพ์แบบนี้
- ขนาดสำเร็จ **A6 · 105 x 148 มม.** (แนวตั้ง)
- กระดาษ **อาร์ตการ์ด 300 แกรม** · เคลือบด้าน (ถ้าอยากให้เขียนปากกาได้ บอกโรงพิมพ์ว่า "เคลือบด้านเฉพาะหน้าหน้า" หรือไม่เคลือบหลัง)
- พิมพ์ **4 สี 2 หน้า**
- **ตัดตก (bleed) 3 มม. มีมาให้ในไฟล์แล้ว** ไฟล์จริงคือ 111 x 154 มม.
- ความละเอียด **300 dpi**
- จำนวนแนะนำ: เริ่ม 100 ใบต่อลาย

## ไฟล์
- `SIWARA_postcards_A6_print.pdf` · ส่งไฟล์นี้ไฟล์เดียวจบ · เรียงหน้า-หลัง สลับกัน {len(CARDS)} ลาย
- `<CODE>_front.png` / `<CODE>_back.png` · ถ้าโรงพิมพ์ขอเป็นไฟล์ภาพแยก

## ลายในชุดนี้
""" + "\n".join(f"- **{c}** · {cap}" for c, _s, cap, _d in CARDS) + """

## ข้อควรรู้
- ไฟล์เป็น **RGB** โรงพิมพ์ดิจิทัลรับได้ปกติ · ถ้าเป็นออฟเซ็ตแล้วเขาขอ CMYK ให้เขาแปลงให้ (เขามีโปรไฟล์สีของเครื่องตัวเอง แปลงเองจะตรงกว่า)
- สีจริงบนกระดาษจะหม่นกว่าบนจอเล็กน้อยเป็นเรื่องปกติ · ขอ **ปรู๊ฟดิจิทัล 1 ใบ** ก่อนพิมพ์จริงทุกครั้ง
- อย่าขยับข้อความเข้าใกล้ขอบมากกว่านี้ · ทุกอย่างวางอยู่ในเขตปลอดภัย 5 มม. จากรอยตัดแล้ว
"""
    (OUT / "GUIDE.md").write_text(guide, encoding="utf-8")
    print(f"  GUIDE.md")
