# -*- coding: utf-8 -*-
"""Claude-side hand-drawn SVG merch sheets for Siwara Cafe (print-controlled Thai type)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _art import (DEFS, PAPER_TEXTURE, INK, BRICK, TEAK, PAPER, house, clock, lamp, bench,
                  cabinet, cup, cake, iced_coffee, coconut_flower, board_game, coffee_beans,
                  leaf_sprig, tee_mock, sketch, understroke, _hatch, _stipple)

OUT = Path(__file__).parent / "claude"
OUT.mkdir(exist_ok=True)
W, H = 1080, 1350

HEAD = """<!DOCTYPE html><html lang="th"><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Chonburi&family=Sarabun:wght@300;400;600&display=swap" rel="stylesheet">
<style>
  html,body{{margin:0;padding:0;background:{paper};overflow:hidden}}
  svg{{display:block}}
  .th{{font-family:'Chonburi',serif;fill:{ink}}}
  .sb{{font-family:'Sarabun',sans-serif;fill:{ink}}}
  .lat{{font-family:'Sarabun',sans-serif;letter-spacing:.22em;fill:{ink}}}
</style></head><body>
<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">
{defs}{paper_tex}
""".format(paper=PAPER, ink=INK, w=W, h=H, defs=DEFS, paper_tex=PAPER_TEXTURE)

FOOT = "</svg></body></html>"

S = f'stroke="{INK}" fill="none" stroke-linecap="round" stroke-linejoin="round"'


def wobbly_rect(x, y, w, h, sw=2.2, o=6):
    """rectangle whose corners overshoot, drawn as four separate pen strokes"""
    return (
        f'<path d="M{x-o} {y+1.5} L{x+w+o} {y-1}" {S} stroke-width="{sw}"/>'
        f'<path d="M{x+w+1} {y-o} L{x+w-1.5} {y+h+o}" {S} stroke-width="{sw*0.95:.2f}"/>'
        f'<path d="M{x+w+o} {y+h+1} L{x-o} {y+h-1.5}" {S} stroke-width="{sw}"/>'
        f'<path d="M{x-1} {y+h+o} L{x+1.5} {y-o}" {S} stroke-width="{sw*0.95:.2f}"/>'
    )


def dashed_cut(x, y, w, h, r=18):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="none"'
            f' stroke="{INK}" stroke-width="1.5" opacity="0.45"'
            f' stroke-dasharray="11 7 6 8 14 6"/>')


def place(inner, x, y, s, box=100):
    return f'<g transform="translate({x},{y}) scale({s})">{inner}</g>'


# ============================================================ m01 · badge set
def m01():
    p = [HEAD]
    a = p.append
    a(f'<g class="th"><text x="{W/2}" y="150" font-size="72" text-anchor="middle">'
      f'ตราศิวรา</text></g>')
    a(f'<g class="sb"><text x="{W/2}" y="196" font-size="27" text-anchor="middle" opacity="0.82">'
      f'ชุดตราลายเส้น สำหรับสติกเกอร์ · ปั๊มถุงกระดาษ · สกรีนอกเสื้อ</text></g>')
    a(f'<path d="M{W/2-190} 218 q190 7 380 -2" {S} stroke-width="1.6" opacity="0.6"/>')

    cells = [(70, 250), (560, 250), (70, 620), (560, 620), (70, 990), (560, 990)]
    cw, ch = 450, 340
    labels = ["๐๑ ตราวงกลม", "๐๒ ตราโล่จั่วบ้าน", "๐๓ ตราแก้วกาแฟ",
              "๐๔ ตราอักษร ศ", "๐๕ ตราปั๊มไปรษณีย์", "๐๖ ตราริบบิ้น"]

    defs_extra = []
    for i, (cx0, cy0) in enumerate(cells):
        a(dashed_cut(cx0, cy0, cw, ch))
        mx, my = cx0 + cw / 2, cy0 + ch / 2 - 12
        seed = i + 2
        filt = ["rough", "rough2", "rough3"][i % 3]

        if i == 0:      # ---------------- circle badge, arched Thai
            r = 132
            defs_extra.append(
                f'<path id="arcT{i}" d="M{mx-r+16} {my+6} a {r-16} {r-16} 0 0 1 {2*(r-16)} 0"/>'
                f'<path id="arcB{i}" d="M{mx+r-24} {my+18} a {r-24} {r-24} 0 0 1 {-2*(r-24)} 0"/>')
            ring = (f'<path d="M{mx-r} {my} a {r} {r} 0 1 1 {2*r} 0 a {r} {r} 0 1 1 {-2*r} 0" '
                    f'{S} stroke-width="3"/>'
                    f'<path d="M{mx-r+11} {my+2} a {r-11} {r-13} 0 1 1 {2*(r-11)} -3 '
                    f'a {r-11} {r-11} 0 1 1 {-2*(r-11)} 3" {S} stroke-width="1.5"/>')
            a(sketch(ring, seed, filt=filt))
            a(f'<g filter="url(#{filt})">{place(house(w=2.0, lawn=False, hills=False), mx-96, my-6, 0.96)}</g>')
            a(f'<text class="th" font-size="34" text-anchor="middle">'
              f'<textPath href="#arcT{i}" startOffset="50%">ศิวรา คาเฟ่</textPath></text>')
            a(f'<text class="sb" font-size="25" text-anchor="middle" letter-spacing="2">'
              f'<textPath href="#arcB{i}" startOffset="50%">ตะกั่วป่า</textPath></text>')

        elif i == 1:    # ---------------- shield with gable
            sh = (f'<path d="M{mx-104} {my-118} L{mx+104} {my-122} L{mx+100} {my+52} '
                  f'Q{mx} {my+142} {mx-100} {my+48} Z" {S} stroke-width="3"/>'
                  f'<path d="M{mx-92} {my-108} L{mx+92} {my-111} L{mx+88} {my+44} '
                  f'Q{mx} {my+126} {mx-88} {my+41} Z" {S} stroke-width="1.4"/>')
            a(sketch(sh, seed, filt=filt))
            gable = (f'<path d="M{mx-74} {my-14} L{mx} {my-78} L{mx+74} {my-14}" {S} stroke-width="3.4"/>'
                     f'<line x1="{mx-84}" y1="{my-12}" x2="{mx+84}" y2="{my-12}" {S} stroke-width="3.4"/>'
                     + "".join(
                         f'<line x1="{mx-(k+1)*10.4}" y1="{my-70+(k+1)*8.2}" '
                         f'x2="{mx+(k+1)*10.4}" y2="{my-70+(k+1)*8.2}" stroke="{BRICK}" '
                         f'stroke-width="1.9" opacity="0.85"/>' for k in range(7))
                     + f'<rect x="{mx-14}" y="{my-46}" width="28" height="20" {S} stroke-width="1.6"/>'
                     + _hatch(mx - 11, my - 42, mx + 11, my - 42, 4, 0, 4.2, w=1.1, seed=7)
                     + f'<rect x="{mx-52}" y="{my-6}" width="104" height="46" {S} stroke-width="2.4"/>'
                     + f'<line x1="{mx}" y1="{my-6}" x2="{mx}" y2="{my+40}" {S} stroke-width="1.6"/>')
            a(sketch(gable, seed + 5, filt="rough2"))
            a(f'<text class="lat" x="{mx}" y="{my+82}" font-size="22" text-anchor="middle">EST. 2475</text>')

        elif i == 2:    # ---------------- oval, coffee cup
            a(sketch(f'<ellipse cx="{mx}" cy="{my}" rx="150" ry="112" {S} stroke-width="3"/>'
                     f'<ellipse cx="{mx}" cy="{my+1}" rx="139" ry="102" {S} stroke-width="1.4"/>',
                     seed, filt=filt))
            a(f'<g filter="url(#{filt})">{place(cup(2.4), mx-72, my-78, 1.45)}</g>')
            a(f'<text class="th" x="{mx}" y="{my+84}" font-size="30" text-anchor="middle">ศิวรา คาเฟ่</text>')

        elif i == 3:    # ---------------- big letter ศ with leaves
            box = (f'<path d="M{mx-118} {my-104} L{mx+108} {my-108} L{mx+120} {my+98} '
                   f'L{mx-108} {my+104} Z" {S} stroke-width="3"/>')
            a(sketch(box, seed, filt=filt))
            a(f'<text class="th" x="{mx}" y="{my+56}" font-size="168" text-anchor="middle">ศ</text>')
            a(f'<g filter="url(#{filt})">{place(leaf_sprig(1.7), mx-124, my-30, 0.62)}</g>')
            a(f'<g filter="url(#{filt})">{place(leaf_sprig(1.7, flip=True), mx+64, my-30, 0.62)}</g>')
            a(f'<text class="lat" x="{mx}" y="{my+92}" font-size="17" text-anchor="middle" '
              f'opacity="0.85">SIWARA CAFE</text>')

        elif i == 4:    # ---------------- rubber postal stamp with clock
            st = (wobbly_rect(mx - 132, my - 108, 264, 216, sw=3.2, o=9)
                  + wobbly_rect(mx - 120, my - 96, 240, 192, sw=1.5, o=5))
            a(sketch(st, seed, filt=filt))
            a(f'<g filter="url(#{filt})">{place(clock(2.2), mx-52, my-84, 1.04)}</g>')
            a(f'<text class="sb" x="{mx-96}" y="{my+70}" font-size="21" letter-spacing="3">'
              f'ตะกั่วป่า · พังงา</text>')
            a(f'<path d="M{mx-114} {my+88} q52 -9 104 2 q50 10 102 -3" {S} stroke-width="1.5" '
              f'opacity="0.6"/>')

        else:           # ---------------- ribbon with coconut flower
            rb = (f'<path d="M{mx-146} {my+52} l292 -6 l-22 40 l-250 5 Z" {S} stroke-width="2.8"/>'
                  f'<path d="M{mx-146} {my+52} l-16 22 l14 24 M{mx+146} {my+46} l18 20 l-16 26" '
                  f'{S} stroke-width="2.2"/>')
            a(sketch(rb, seed, filt=filt))
            a(f'<g filter="url(#{filt})">{place(coconut_flower(2.0), mx-62, my-116, 1.35)}</g>')
            a(f'<text class="th" x="{mx}" y="{my+82}" font-size="27" text-anchor="middle">'
              f'ศิวรา · ตะกั่วป่า</text>')

        a(f'<text class="sb" x="{cx0+16}" y="{cy0+ch-8}" font-size="18" opacity="0.6">'
          f'{labels[i]}</text>')

    a(f'<defs>{"".join(defs_extra)}</defs>')
    a(FOOT)
    return "".join(p)


# ================================================== m02 · specimen catalogue
def m02():
    items = [
        (house(w=1.9, lawn=False, hills=False), "บ้านไม้สัก", 0.86, -34, 14),
        (clock(2.1), "นาฬิกาโบราณ", 1.62, 12, 2),
        (lamp(2.1), "โคมไฟโดม", 1.60, 8, 4),
        (bench(2.1), "ม้านั่งไม้", 1.62, 4, 22),
        (cabinet(2.1), "ตู้ลิ้นชักไม้สัก", 1.62, 4, 18),
        (cup(2.3), "กาแฟร้อน", 1.60, 8, 10),
        (cake(2.2), "เค้กโฮมเมด", 1.58, 10, 8),
        (iced_coffee(2.2), "ฮันนี่เลม่อน", 1.60, 12, 4),
        (coconut_flower(2.0), "ช่อดอกมะพร้าว", 1.56, 14, 6),
    ]
    nums = ["๐๑", "๐๒", "๐๓", "๐๔", "๐๕", "๐๖", "๐๗", "๐๘", "๐๙"]
    p = [HEAD]
    a = p.append
    a(f'<g filter="url(#rough)">{wobbly_rect(46, 46, W-92, H-92, sw=2.4, o=10)}</g>')
    a(f'<text class="th" x="{W/2}" y="150" font-size="70" text-anchor="middle">ศิวรา คาเฟ่</text>')
    a(f'<text class="sb" x="{W/2}" y="196" font-size="26" text-anchor="middle" opacity="0.82">'
      f'ของในบ้านไม้เกือบ 100 ปี · เมืองเก่าตะกั่วป่า</text>')
    a(f'<path d="M300 220 q240 8 480 -3" {S} stroke-width="1.6" opacity="0.55"/>')

    x0, y0, cw, ch = 96, 252, 296, 318
    for i, (art, cap, s, ox, oy) in enumerate(items):
        cx = x0 + (i % 3) * cw
        cy = y0 + (i // 3) * ch
        filt = ["rough", "rough2", "rough3"][i % 3]
        a(f'<g filter="url(#{filt})">{wobbly_rect(cx, cy, 258, 236, sw=1.7, o=5)}</g>')
        a(f'<g filter="url(#{filt})">{place(art, cx+ox+8, cy+oy+10, s)}</g>')
        a(f'<text class="sb" x="{cx+129}" y="{cy+268}" font-size="25" text-anchor="middle">{cap}</text>')
        a(f'<text class="sb" x="{cx+129}" y="{cy+294}" font-size="19" text-anchor="middle" '
          f'opacity="0.55">{nums[i]}</text>')
    a(f'<text class="lat" x="{W/2}" y="{H-72}" font-size="20" text-anchor="middle">'
      f'SLOW BAR · COZY CORNER · WARM COFFEE · GOOD TIME</text>')
    a(FOOT)
    return "".join(p)


# ============================================== m03 · house hero + type poster
def m03():
    p = [HEAD]
    a = p.append
    a(f'<g filter="url(#rough2)">{wobbly_rect(52, 52, W-104, H-104, sw=2.6, o=12)}</g>')
    a(f'<g filter="url(#rough)">{wobbly_rect(66, 66, W-132, H-132, sw=1.2, o=4)}</g>')
    a(f'<g filter="url(#rough3)">{place(leaf_sprig(1.9), 60, 150, 1.5)}</g>')
    a(f'<g filter="url(#rough3)">{place(leaf_sprig(1.9, flip=True), 830, 150, 1.5)}</g>')

    a(f'<text class="th" x="{W/2}" y="270" font-size="112" text-anchor="middle">ศิวรา คาเฟ่</text>')
    a(f'<text class="sb" x="{W/2}" y="330" font-size="32" text-anchor="middle" opacity="0.88">'
      f'บ้านไม้สักเกือบ 100 ปี ในเมืองเก่าตะกั่วป่า</text>')
    a(f'<path d="M330 366 q108 8 216 0 q108 -8 216 3" {S} stroke-width="1.6" opacity="0.5" '
      f'transform="translate(-108,0)"/>')

    hs = 4.62                                   # 200 * 4.62 = 924 wide
    a(understroke(place(house(w=2.3), 78, 470, hs), op=0.16))
    a(f'<g filter="url(#rough2)">{place(house(w=2.3), 78, 470, hs)}</g>')

    a(f'<g filter="url(#rough)">{place(coffee_beans(2.0, 3), 430, 1130, 0.72)}</g>')
    a(f'<text class="lat" x="{W/2}" y="{H-142}" font-size="21" text-anchor="middle">'
      f'SLOW BAR · COZY CORNER · WARM COFFEE · GOOD TIME</text>')
    a(f'<text class="sb" x="{W/2}" y="{H-104}" font-size="24" text-anchor="middle" opacity="0.8">'
      f'Here, every moment feels like home.</text>')
    a(f'<text class="lat" x="{W/2}" y="{H-72}" font-size="18" text-anchor="middle" opacity="0.7">'
      f'SIWARA CAFE · TAKUA PA · EST. 2475</text>')
    a(FOOT)
    return "".join(p)


# ================================================== m04 · tee print lockups
def m04():
    p = [HEAD]
    a = p.append
    a(f'<text class="th" x="{W/2}" y="128" font-size="60" text-anchor="middle">ลายสกรีนเสื้อ</text>')
    a(f'<text class="sb" x="{W/2}" y="172" font-size="25" text-anchor="middle" opacity="0.8">'
      f'เส้นหนาสกรีนได้ · 2 สี · กว้าง 28 ซม.</text>')

    # --- print A : house over arched type
    a(dashed_cut(64, 210, 452, 470))
    mx, my = 290, 430
    a(f'<defs><path id="teeArc" d="M{mx-176} {my+150} a 176 176 0 0 0 352 0"/></defs>')
    hero = place(house(w=3.4, lawn=False), mx - 176, my - 150, 1.76)
    a(understroke(hero, op=0.14))
    a(f'<g filter="url(#rough2)">{hero}</g>')
    a(f'<text class="th" x="{mx}" y="{my+206}" font-size="52" text-anchor="middle">ศิวรา คาเฟ่</text>')
    a(f'<text class="sb" x="{mx}" y="{my+246}" font-size="25" text-anchor="middle" '
      f'letter-spacing="5">ตะกั่วป่า · พังงา</text>')
    a(f'<text class="sb" x="80" y="668" font-size="18" opacity="0.6">แบบ ก · บ้าน + ตัวหนังสือ</text>')

    # --- print B : circular seal
    a(dashed_cut(564, 210, 452, 470))
    cx2, cy2, r2 = 790, 420, 178
    seal = (f'<path d="M{cx2-r2} {cy2} a {r2} {r2} 0 1 1 {2*r2} 0 a {r2} {r2} 0 1 1 {-2*r2} 0" '
            f'{S} stroke-width="4.6"/>'
            f'<path d="M{cx2-r2+14} {cy2+3} a {r2-14} {r2-16} 0 1 1 {2*(r2-14)} -4 '
            f'a {r2-14} {r2-14} 0 1 1 {-2*(r2-14)} 4" {S} stroke-width="2.4"/>')
    a(sketch(seal, 9, filt="rough3"))
    a(f'<defs>'
      f'<path id="sealT" d="M{cx2-r2+34} {cy2+8} a {r2-34} {r2-34} 0 0 1 {2*(r2-34)} 0"/>'
      f'<path id="sealB" d="M{cx2+r2-44} {cy2+16} a {r2-44} {r2-44} 0 0 1 {-2*(r2-44)} 0"/>'
      f'</defs>')
    a(f'<g filter="url(#rough2)">{place(house(w=3.2, lawn=False, hills=False), cx2-122, cy2-76, 1.22)}</g>')
    a(f'<text class="th" font-size="40" text-anchor="middle">'
      f'<textPath href="#sealT" startOffset="50%">ศิวรา คาเฟ่</textPath></text>')
    a(f'<text class="sb" font-size="28" text-anchor="middle" letter-spacing="3">'
      f'<textPath href="#sealB" startOffset="50%">ตะกั่วป่า</textPath></text>')
    a(f'<g filter="url(#rough)">{place(coffee_beans(2.2, 2), cx2-58, cy2+94, 0.5)}</g>')
    a(f'<text class="sb" x="580" y="668" font-size="18" opacity="0.6">แบบ ข · ตราวงกลม</text>')

    # --- shirt mockups
    a(f'<path d="M120 726 q420 9 840 -4" {S} stroke-width="1.5" opacity="0.5"/>')
    for i, (tx, lab) in enumerate(((110, "แบบ ก"), (420, "แบบ ข"), (730, "แบบ ข · เล็ก"))):
        filt = ["rough", "rough2", "rough3"][i]
        a(f'<g filter="url(#{filt})">{place(tee_mock(2.6), tx, 760, 2.4)}</g>')
        if i == 0:
            a(f'<g filter="url(#rough2)">{place(house(w=3.6, lawn=False, hills=False), tx+82, 858, 0.44)}</g>')
            a(f'<text class="th" x="{tx+120}" y="936" font-size="17" text-anchor="middle">ศิวรา คาเฟ่</text>')
        else:
            s = 0.30 if i == 2 else 0.40
            ccx, ccy = tx + 120, 900
            rr = 62 * (s / 0.40)
            a(f'<g filter="url(#rough3)"><path d="M{ccx-rr} {ccy} a {rr} {rr} 0 1 1 {2*rr} 0 '
              f'a {rr} {rr} 0 1 1 {-2*rr} 0" {S} stroke-width="2.6"/></g>')
            a(f'<g filter="url(#rough2)">{place(house(w=4.0, lawn=False, hills=False), ccx-rr*0.78, ccy-rr*0.42, rr*0.0078*100/100*0.78)}</g>')
        a(f'<text class="sb" x="{tx+120}" y="1006" font-size="19" text-anchor="middle" '
          f'opacity="0.7">{lab}</text>')

    a(f'<path d="M120 1046 q420 8 840 -3" {S} stroke-width="1.5" opacity="0.5"/>')
    a(f'<text class="sb" x="{W/2}" y="1096" font-size="24" text-anchor="middle" opacity="0.85">'
      f'เส้นทุกเส้นหนาอย่างน้อย 2.2 · สกรีนซิลค์ 2 สีได้เลย</text>')
    a(f'<text class="lat" x="{W/2}" y="1140" font-size="19" text-anchor="middle" opacity="0.7">'
      f'SIWARA CAFE · TAKUA PA · EST. 2475</text>')
    a(f'<g filter="url(#rough)">{place(leaf_sprig(1.8), 96, 1160, 1.1)}</g>')
    a(f'<g filter="url(#rough)">{place(leaf_sprig(1.8, flip=True), 872, 1160, 1.1)}</g>')
    a(f'<text class="sb" x="{W/2}" y="1266" font-size="22" text-anchor="middle" opacity="0.75">'
      f'บ้านไม้สักเกือบ 100 ปี ในเมืองเก่าตะกั่วป่า</text>')
    a(FOOT)
    return "".join(p)


if __name__ == "__main__":
    for name, fn in (("m01_badge_set", m01), ("m02_specimen", m02),
                     ("m03_house_poster", m03), ("m04_tee_lockups", m04)):
        f = OUT / f"{name}.html"
        f.write_text(fn(), encoding="utf-8")
        print("wrote", f, len(f.read_text(encoding='utf-8')) // 1024, "KB")
