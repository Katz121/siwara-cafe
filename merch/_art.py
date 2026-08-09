# -*- coding: utf-8 -*-
"""Hand-drawn line-art SVG primitives for Siwara Cafe merch.
Every primitive draws inside a 0..100 x 0..100 local box (house: 0..200 x 0..120)
so it can be placed with transform="translate(x,y) scale(s)".
"""

INK = "#241d19"
BRICK = "#b4451f"
TEAK = "#8a5a2b"
PAPER = "#f4ece0"

DEFS = f"""
<defs>
  <filter id="rough" x="-6%" y="-6%" width="112%" height="112%">
    <feTurbulence type="fractalNoise" baseFrequency="0.024" numOctaves="3" seed="17" result="n"/>
    <feDisplacementMap in="SourceGraphic" in2="n" scale="2.1"
      xChannelSelector="R" yChannelSelector="G"/>
  </filter>
  <filter id="rough2" x="-6%" y="-6%" width="112%" height="112%">
    <feTurbulence type="fractalNoise" baseFrequency="0.013" numOctaves="4" seed="5" result="n"/>
    <feDisplacementMap in="SourceGraphic" in2="n" scale="2.6"
      xChannelSelector="R" yChannelSelector="G"/>
  </filter>
  <filter id="rough3" x="-6%" y="-6%" width="112%" height="112%">
    <feTurbulence type="fractalNoise" baseFrequency="0.031" numOctaves="2" seed="41" result="n"/>
    <feDisplacementMap in="SourceGraphic" in2="n" scale="3.2"
      xChannelSelector="R" yChannelSelector="G"/>
  </filter>
  <filter id="grain" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="4" seed="3"/>
    <feColorMatrix type="saturate" values="0"/>
  </filter>
</defs>
"""

PAPER_TEXTURE = (
    '<rect width="100%" height="100%" fill="{p}"/>'
    '<rect width="100%" height="100%" filter="url(#grain)" opacity="0.13"'
    ' style="mix-blend-mode:multiply"/>'
).format(p=PAPER)


def _rng(seed):
    """tiny deterministic LCG -> floats in [0,1)"""
    s = [seed * 7919 + 13]

    def nxt():
        s[0] = (s[0] * 1103515245 + 12345) % 2147483648
        return s[0] / 2147483648
    return nxt


def _hatch(x1, y1, x2, y2, n, dx, dy, w=0.8, col=INK, op=0.75, seed=3):
    """n hand-scribbled strokes stepped by (dx,dy) · spacing, length and weight all wobble."""
    r = _rng(seed)
    out = []
    for i in range(n):
        j = (r() - 0.5) * (abs(dx) + abs(dy)) * 0.55        # uneven spacing
        ox, oy = dx * i + j, dy * i + j * 0.4
        t0 = r() * 0.12                                     # short of the start
        t1 = 1 - r() * 0.14 + 0.06                          # overshoot the end
        ax, ay = x1 + (x2 - x1) * t0, y1 + (y2 - y1) * t0
        bx, by = x1 + (x2 - x1) * t1, y1 + (y2 - y1) * t1
        ww = w * (0.7 + r() * 0.75)
        out.append(
            f'<line x1="{ax+ox:.1f}" y1="{ay+oy:.1f}" x2="{bx+ox:.1f}" y2="{by+oy:.1f}"'
            f' stroke="{col}" stroke-width="{ww:.2f}" opacity="{op*(0.75+r()*0.35):.2f}"/>'
        )
    return "".join(out)


def sketch(inner, seed=1, dx=0.45, dy=-0.35, rot=0.22, op=0.3, filt="rough"):
    """Make a clean group look drawn by a person: a faint offset under-drawing of the same
    shapes (the 'gone over it twice' look) plus a wobble filter, seeded per group so not
    every part of the poster shakes identically."""
    f2 = {"rough": "rough2", "rough2": "rough3", "rough3": "rough"}[filt]
    return (
        f'<g filter="url(#{f2})" opacity="{op}" transform="translate({dx},{dy}) rotate({rot} 50 50)"'
        f' stroke-linecap="round">{inner}</g>'
        f'<g filter="url(#{filt})">{inner}</g>'
    )


def understroke(inner, op=0.2, dx=-1.4, dy=1.1, rot=-0.6):
    """leftover pencil construction lines showing under the inked lines"""
    return (f'<g opacity="{op}" transform="translate({dx},{dy}) rotate({rot} 50 50)">'
            f'{inner}</g>')


def _stipple(cx, cy, rx, ry, n, seed=1, r=0.55, col=INK, op=0.6):
    """deterministic pseudo-random dots inside an ellipse."""
    out = []
    s = seed * 7919 + 13
    for i in range(n):
        s = (s * 1103515245 + 12345) % 2147483648
        a = (s / 2147483648) * 6.2831853
        s = (s * 1103515245 + 12345) % 2147483648
        rr = (s / 2147483648) ** 0.5
        import math
        x = cx + math.cos(a) * rx * rr
        y = cy + math.sin(a) * ry * rr
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{col}" opacity="{op}"/>')
    return "".join(out)


# ---------------------------------------------------------------- the house
def house(w=2.6, tile=BRICK, bg=PAPER, hills=True, lawn=True):
    """Front elevation of the Siwara teak house. Local box 0..200 x 0..120."""
    p = []
    a = p.append
    S = f'stroke="{INK}" fill="none" stroke-linecap="round" stroke-linejoin="round"'

    if hills:
        a(f'<path d="M2 62 Q 22 44 40 56 Q 52 46 64 58" {S} stroke-width="{w*0.45:.2f}" opacity="0.55"/>')
        a(f'<path d="M136 58 Q 152 42 172 54 Q 186 46 198 60" {S} stroke-width="{w*0.45:.2f}" opacity="0.55"/>')
        a(_hatch(6, 60, 34, 60, 4, 1.2, 2.4, w=0.5, op=0.35))
        a(_hatch(150, 58, 180, 58, 4, 1.0, 2.4, w=0.5, op=0.35))

    # ---- walls (paper fill first so hatching behind windows is hidden)
    a(f'<rect x="66" y="46" width="68" height="58" fill="{bg}"/>')      # centre block
    a(f'<rect x="20" y="70" width="46" height="34" fill="{bg}"/>')      # left wing
    a(f'<rect x="134" y="70" width="46" height="34" fill="{bg}"/>')     # right wing

    # ---- centre gable roof
    a(f'<path d="M60 48 L100 20 L140 48 Z" fill="{bg}"/>')
    a(f'<path d="M59.4 48.6 L100 19.4 L140.6 48.6" {S} stroke-width="{w:.2f}"/>')
    a(f'<line x1="56" y1="48.6" x2="144" y2="48.6" {S} stroke-width="{w*1.15:.2f}"/>')
    for i in range(7):                                                  # tile courses
        y = 24.5 + i * 3.4
        hw = (y - 20) / 28 * 40
        a(f'<line x1="{100-hw:.1f}" y1="{y:.1f}" x2="{100+hw:.1f}" y2="{y:.1f}"'
          f' stroke="{tile}" stroke-width="{w*0.42:.2f}" opacity="0.85"/>')
    a(f'<line x1="100" y1="19.4" x2="100" y2="17" {S} stroke-width="{w*0.8:.2f}"/>')
    a(f'<rect x="93" y="30" width="14" height="10" fill="{bg}" {S} stroke-width="{w*0.5:.2f}"/>')
    a(_hatch(94, 32, 106, 32, 4, 0, 2, w=0.7))                          # louvre vent

    # ---- lower sweeping roof over both wings + veranda
    a(f'<path d="M14 72 L34 58 L166 58 L186 72 Z" fill="{bg}"/>')
    a(f'<path d="M13.6 72.4 L34 57.6 L166 57.6 L186.4 72.4" {S} stroke-width="{w:.2f}"/>')
    a(f'<line x1="12" y1="72.4" x2="188" y2="72.4" {S} stroke-width="{w*1.15:.2f}"/>')
    for i in range(5):
        y = 60.5 + i * 2.6
        pad = (y - 58) / 14 * 20
        a(f'<line x1="{34-pad:.1f}" y1="{y:.1f}" x2="{166+pad:.1f}" y2="{y:.1f}"'
          f' stroke="{tile}" stroke-width="{w*0.4:.2f}" opacity="0.8"/>')

    # ---- wood lap siding
    for i in range(9):                                                  # upper storey
        y = 50 + i * 2.4
        a(f'<line x1="67" y1="{y}" x2="133" y2="{y}" stroke="{TEAK}"'
          f' stroke-width="{w*0.3:.2f}" opacity="0.55"/>')
    for x0, x1 in ((21, 65), (135, 179)):
        for i in range(11):
            y = 74 + i * 2.7
            a(f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="{TEAK}"'
              f' stroke-width="{w*0.3:.2f}" opacity="0.55"/>')

    # ---- upper storey windows (3 casements, 3x2 panes)
    for x in (72, 91, 110):
        a(f'<rect x="{x}" y="51" width="17" height="17" fill="{bg}" {S} stroke-width="{w*0.62:.2f}"/>')
        a(f'<line x1="{x+5.7}" y1="51" x2="{x+5.7}" y2="68" {S} stroke-width="{w*0.34:.2f}"/>')
        a(f'<line x1="{x+11.4}" y1="51" x2="{x+11.4}" y2="68" {S} stroke-width="{w*0.34:.2f}"/>')
        a(f'<line x1="{x}" y1="59.5" x2="{x+17}" y2="59.5" {S} stroke-width="{w*0.34:.2f}"/>')
    a(f'<line x1="66" y1="46" x2="66" y2="104" {S} stroke-width="{w*0.7:.2f}"/>')
    a(f'<line x1="134" y1="46" x2="134" y2="104" {S} stroke-width="{w*0.7:.2f}"/>')

    # ---- ground floor: open veranda in the middle
    a(f'<rect x="70" y="76" width="60" height="28" fill="{bg}" {S} stroke-width="{w*0.7:.2f}"/>')
    a(_hatch(72, 78, 72, 102, 9, 6.4, 0, w=0.55, op=0.5))               # shadowed interior
    a(f'<line x1="82" y1="76" x2="82" y2="104" {S} stroke-width="{w*0.8:.2f}"/>')  # posts
    a(f'<line x1="118" y1="76" x2="118" y2="104" {S} stroke-width="{w*0.8:.2f}"/>')
    a(f'<rect x="92" y="80" width="16" height="24" fill="{bg}" {S} stroke-width="{w*0.6:.2f}"/>')
    a(f'<line x1="100" y1="80" x2="100" y2="104" {S} stroke-width="{w*0.4:.2f}"/>')

    # ---- left wing: wide window + open bay
    a(f'<rect x="26" y="78" width="20" height="15" fill={chr(34)}{bg}{chr(34)} {S} stroke-width="{w*0.6:.2f}"/>')
    a(f'<line x1="32.6" y1="78" x2="32.6" y2="93" {S} stroke-width="{w*0.32:.2f}"/>')
    a(f'<line x1="39.3" y1="78" x2="39.3" y2="93" {S} stroke-width="{w*0.32:.2f}"/>')
    a(f'<line x1="26" y1="85.5" x2="46" y2="85.5" {S} stroke-width="{w*0.32:.2f}"/>')
    a(f'<rect x="51" y="78" width="12" height="26" fill="{bg}" {S} stroke-width="{w*0.6:.2f}"/>')
    a(_hatch(52.5, 80, 52.5, 103, 5, 2.1, 0, w=0.5, op=0.45))

    # ---- right wing: wooden double door + window
    a(f'<rect x="140" y="76" width="18" height="28" fill="{bg}" {S} stroke-width="{w*0.7:.2f}"/>')
    a(f'<line x1="149" y1="76" x2="149" y2="104" {S} stroke-width="{w*0.45:.2f}"/>')
    for i in range(2):
        a(f'<rect x="{142+i*9:.0f}" y="80" width="5" height="9" fill="none" {S} stroke-width="{w*0.3:.2f}"/>')
        a(f'<rect x="{142+i*9:.0f}" y="92" width="5" height="9" fill="none" {S} stroke-width="{w*0.3:.2f}"/>')
    a(f'<rect x="164" y="79" width="12" height="14" fill="{bg}" {S} stroke-width="{w*0.6:.2f}"/>')
    a(f'<line x1="170" y1="79" x2="170" y2="93" {S} stroke-width="{w*0.32:.2f}"/>')
    a(f'<line x1="164" y1="86" x2="176" y2="86" {S} stroke-width="{w*0.32:.2f}"/>')

    # ---- wall lanterns
    for lx in (76, 112, 137, 161):
        a(f'<path d="M{lx} 77 l0 2.6 M{lx-2.2} 79.6 l4.4 0 l-1 5.2 l-2.4 0 Z" {S}'
          f' stroke-width="{w*0.42:.2f}"/>')

    # ---- veranda deck + steps
    a(f'<path d="M64 104 L136 104 L142 110 L58 110 Z" fill="{bg}" {S} stroke-width="{w*0.7:.2f}"/>')
    a(f'<line x1="60" y1="107" x2="140" y2="107" {S} stroke-width="{w*0.4:.2f}"/>')

    # ---- topiary bushes
    for bx, br in ((16, 5.2), (48, 4.2), (68, 3.6), (132, 3.6), (152, 4.6), (184, 5.4)):
        a(f'<path d="M{bx} {104-br*2} q {br*1.5} {-br*0.3} {br*1.4} {br*1.1}'
          f' q {br*0.5} {br*1.1} {-br*1.4} {br*1.2} q {-br*1.9} {br*0.1} {-br*1.5} {-br*1.2}'
          f' q {br*0.1} {-br*1.1} {br*1.5} {-br*1.1} Z" {S} stroke-width="{w*0.5:.2f}"/>')
        a(f'<line x1="{bx}" y1="{104-br*0.1:.1f}" x2="{bx}" y2="104" {S} stroke-width="{w*0.5:.2f}"/>')
        a(_stipple(bx, 104 - br * 1.2, br * 1.1, br * 0.8, 14, seed=int(bx), r=0.45, op=0.5))

    if lawn:
        a(f'<ellipse cx="100" cy="115" rx="62" ry="7" {S} stroke-width="{w*0.5:.2f}"/>')
        a(_stipple(100, 115, 58, 5, 60, seed=9, r=0.4, op=0.4))
    a(f'<line x1="2" y1="104" x2="198" y2="104" {S} stroke-width="{w*0.75:.2f}"/>')
    return "".join(p)


# ------------------------------------------------------------- shop objects
def clock(w=2.2):
    S = f'stroke="{INK}" fill="none" stroke-linecap="round" stroke-linejoin="round"'
    p = [
        f'<path d="M46 8 q4 -3 8 0 M50 5 l0 3" {S} stroke-width="{w*0.5:.2f}"/>',      # horse finial hint
        f'<path d="M42 6 q8 -5 16 0 l3 4 l-22 0 Z" {S} stroke-width="{w*0.55:.2f}"/>',
        f'<path d="M30 10 l40 0 l-3 6 l-34 0 Z" {S} stroke-width="{w*0.7:.2f}"/>',      # pediment
        f'<rect x="33" y="16" width="34" height="70" rx="2" {S} stroke-width="{w:.2f}"/>',
        f'<circle cx="50" cy="34" r="13" {S} stroke-width="{w*0.7:.2f}"/>',
        f'<circle cx="50" cy="34" r="10.5" {S} stroke-width="{w*0.3:.2f}"/>',
        f'<line x1="50" y1="34" x2="50" y2="26" {S} stroke-width="{w*0.6:.2f}"/>',
        f'<line x1="50" y1="34" x2="56" y2="37" {S} stroke-width="{w*0.6:.2f}"/>',
        f'<circle cx="50" cy="34" r="1.2" fill="{INK}"/>',
        f'<rect x="40" y="52" width="20" height="30" {S} stroke-width="{w*0.55:.2f}"/>',
        f'<line x1="50" y1="52" x2="50" y2="72" {S} stroke-width="{w*0.45:.2f}"/>',
        f'<circle cx="50" cy="75" r="4.2" {S} stroke-width="{w*0.6:.2f}"/>',
        f'<path d="M33 86 l34 0 l-4 6 l-26 0 Z" {S} stroke-width="{w*0.6:.2f}"/>',
    ]
    for i in range(12):                                                   # dial ticks
        import math
        a0 = i * 30 * math.pi / 180
        p.append(f'<line x1="{50+math.sin(a0)*9.6:.1f}" y1="{34-math.cos(a0)*9.6:.1f}"'
                 f' x2="{50+math.sin(a0)*8.2:.1f}" y2="{34-math.cos(a0)*8.2:.1f}"'
                 f' stroke="{INK}" stroke-width="{w*0.3:.2f}"/>')
    p.append(_hatch(34, 18, 34, 84, 3, 1.5, 0, w=0.6, op=0.55))
    p.append(_hatch(63, 18, 63, 84, 3, 1.5, 0, w=0.6, op=0.55))
    return "".join(p)


def cup(w=2.4):
    S = f'stroke="{INK}" fill="none" stroke-linecap="round" stroke-linejoin="round"'
    return "".join([
        f'<path d="M26 40 l6 32 q1 8 9 8 l18 0 q8 0 9 -8 l6 -32" {S} stroke-width="{w:.2f}"/>',
        f'<ellipse cx="50" cy="40" rx="24" ry="6.4" {S} stroke-width="{w*0.8:.2f}"/>',
        f'<ellipse cx="50" cy="40" rx="19" ry="4.6" {S} stroke-width="{w*0.3:.2f}"/>',
        f'<path d="M74 48 q12 2 11 12 q-1 10 -13 9" {S} stroke-width="{w*0.85:.2f}"/>',
        f'<path d="M18 82 q32 8 64 0" {S} stroke-width="{w*0.7:.2f}"/>',
        f'<ellipse cx="50" cy="84" rx="34" ry="5" {S} stroke-width="{w*0.8:.2f}"/>',
        f'<path d="M42 30 q-5 -7 0 -13 q5 -6 0 -12" {S} stroke-width="{w*0.55:.2f}" opacity="0.8"/>',
        f'<path d="M56 28 q5 -6 0 -12 q-5 -5 0 -10" {S} stroke-width="{w*0.55:.2f}" opacity="0.8"/>',
        _hatch(30, 56, 30, 74, 4, 1.6, 0, w=0.6, op=0.5),
    ])


def lamp(w=2.2):
    S = f'stroke="{INK}" fill="none" stroke-linecap="round" stroke-linejoin="round"'
    p = [
        f'<ellipse cx="62" cy="94" rx="16" ry="4" {S} stroke-width="{w*0.8:.2f}"/>',
        f'<path d="M62 92 q0 -34 -6 -50 q-6 -18 -22 -20" {S} stroke-width="{w:.2f}"/>',
        f'<path d="M18 24 q16 -2 26 14 l-34 0 q-2 -12 8 -14 Z" {S} stroke-width="{w*0.9:.2f}"/>',
        f'<path d="M10 38 q17 6 34 0" {S} stroke-width="{w*0.7:.2f}"/>',
    ]
    for i in range(6):                                                    # pleats
        x = 13 + i * 5.4
        p.append(f'<path d="M{x} 37.5 q{(24-x)*0.14:.1f} -8 {(24-x)*0.3:.1f} -13"'
                 f' {S} stroke-width="{w*0.32:.2f}" opacity="0.8"/>')
    p.append(f'<path d="M14 43 l-3 6 M27 44 l0 7 M40 43 l3 6" {S} stroke-width="{w*0.4:.2f}" opacity="0.7"/>')
    return "".join(p)


def bench(w=2.2):
    S = f'stroke="{INK}" fill="none" stroke-linecap="round" stroke-linejoin="round"'
    p = [
        f'<path d="M8 30 q0 -8 8 -8 l68 0 q8 0 8 8 l0 26 l-84 0 Z" {S} stroke-width="{w:.2f}"/>',
        f'<rect x="6" y="56" width="88" height="12" rx="3" {S} stroke-width="{w:.2f}"/>',
        f'<path d="M12 68 l0 20 M88 68 l0 20 M26 68 l0 14 M74 68 l0 14" {S} stroke-width="{w*0.8:.2f}"/>',
        f'<path d="M6 62 q44 6 88 0" {S} stroke-width="{w*0.35:.2f}"/>',
    ]
    for i in range(9):                                                    # back slats
        x = 14 + i * 9
        p.append(f'<line x1="{x}" y1="26" x2="{x}" y2="56" {S} stroke-width="{w*0.42:.2f}"/>')
    p.append(f'<path d="M10 56 q40 -10 80 0" {S} stroke-width="{w*0.5:.2f}" opacity="0.8"/>')
    for i in range(6):                                                    # floral cushion dots
        x = 16 + i * 13
        p.append(f'<path d="M{x} 60 q2 -3 4 0 q-2 3 -4 0" {S} stroke-width="{w*0.35:.2f}"/>')
    return "".join(p)


def cake(w=2.3):
    S = f'stroke="{INK}" fill="none" stroke-linecap="round" stroke-linejoin="round"'
    return "".join([
        f'<path d="M22 78 l16 -46 l38 0 l8 46 Z" {S} stroke-width="{w:.2f}"/>',
        f'<path d="M27 62 q22 5 45 0 M25 70 q24 5 48 0" {S} stroke-width="{w*0.5:.2f}"/>',
        f'<path d="M38 32 q10 -6 20 -1 q10 5 18 1" {S} stroke-width="{w*0.7:.2f}"/>',
        f'<circle cx="54" cy="26" r="4.6" {S} stroke-width="{w*0.7:.2f}"/>',
        f'<path d="M54 21 q3 -5 7 -4" {S} stroke-width="{w*0.5:.2f}"/>',
        f'<ellipse cx="50" cy="80" rx="36" ry="6" {S} stroke-width="{w*0.8:.2f}"/>',
        f'<path d="M16 82 q34 8 68 0" {S} stroke-width="{w*0.5:.2f}"/>',
        _hatch(30, 40, 30, 74, 5, 1.8, 0, w=0.55, op=0.45),
    ])


def iced_coffee(w=2.3):
    S = f'stroke="{INK}" fill="none" stroke-linecap="round" stroke-linejoin="round"'
    p = [
        f'<path d="M32 20 l4 68 q1 6 7 6 l14 0 q6 0 7 -6 l4 -68" {S} stroke-width="{w:.2f}"/>',
        f'<ellipse cx="50" cy="20" rx="18" ry="5.2" {S} stroke-width="{w*0.8:.2f}"/>',
        f'<path d="M36 44 q14 5 28 0" {S} stroke-width="{w*0.5:.2f}" opacity="0.8"/>',
        f'<path d="M58 16 l10 -14" {S} stroke-width="{w*0.9:.2f}"/>',
        f'<circle cx="44" cy="30" r="7" {S} stroke-width="{w*0.55:.2f}"/>',
    ]
    for i in range(9):                                                    # lemon slice
        import math
        a0 = i * 40 * math.pi / 180
        p.append(f'<line x1="44" y1="30" x2="{44+math.cos(a0)*6.4:.1f}"'
                 f' y2="{30+math.sin(a0)*6.4:.1f}" stroke="{INK}" stroke-width="{w*0.3:.2f}"/>')
    p.append(f'<rect x="38" y="52" width="10" height="10" rx="1.5" {S} stroke-width="{w*0.45:.2f}"/>')
    p.append(f'<rect x="52" y="62" width="9" height="9" rx="1.5" {S} stroke-width="{w*0.45:.2f}"/>')
    p.append(_hatch(37, 70, 37, 86, 4, 1.7, 0, w=0.55, op=0.5))
    return "".join(p)


def coconut_flower(w=2.1):
    S = f'stroke="{INK}" fill="none" stroke-linecap="round" stroke-linejoin="round"'
    p = [f'<path d="M50 92 q-4 -34 -2 -58 q1 -12 6 -20" {S} stroke-width="{w:.2f}"/>']
    for i in range(9):                                                    # dangling florets
        y = 24 + i * 7
        d = 6 + i * 2.6
        p.append(f'<path d="M{50-(i*0.4):.1f} {y} q{-d} 6 {-d*1.2:.1f} 18" {S} stroke-width="{w*0.45:.2f}"/>')
        p.append(f'<path d="M{50+(i*0.4):.1f} {y+3} q{d} 6 {d*1.2:.1f} 17" {S} stroke-width="{w*0.45:.2f}"/>')
    p.append(_stipple(50, 56, 26, 30, 46, seed=4, r=0.5, op=0.55))
    return "".join(p)


def board_game(w=2.3):
    S = f'stroke="{INK}" fill="none" stroke-linecap="round" stroke-linejoin="round"'
    p = [
        f'<path d="M20 62 l20 -12 l20 12 l-20 12 Z" {S} stroke-width="{w:.2f}"/>',
        f'<path d="M20 62 l0 16 l20 12 l0 -16 M60 62 l0 16 l-20 12" {S} stroke-width="{w:.2f}"/>',
        f'<path d="M58 46 l14 -8 l14 8 l-14 8 Z" {S} stroke-width="{w*0.85:.2f}"/>',
        f'<path d="M58 46 l0 11 l14 8 l0 -11 M86 46 l0 11 l-14 8" {S} stroke-width="{w*0.85:.2f}"/>',
        f'<path d="M44 32 q-5 -2 -5 -7 q0 -6 6 -6 q6 0 6 6 q0 5 -5 7 l3 10 l-8 0 Z" {S}'
        f' stroke-width="{w*0.8:.2f}"/>',
    ]
    for cx, cy in ((30, 62), (40, 68), (50, 62), (34, 78), (46, 78)):
        p.append(f'<circle cx="{cx}" cy="{cy}" r="1.9" fill="{INK}"/>')
    for cx, cy in ((66, 46), (78, 46), (72, 51)):
        p.append(f'<circle cx="{cx}" cy="{cy}" r="1.5" fill="{INK}"/>')
    p.append(_hatch(22, 68, 22, 76, 4, 4.5, 0, w=0.55, op=0.45))
    return "".join(p)


def cabinet(w=2.2):
    S = f'stroke="{INK}" fill="none" stroke-linecap="round" stroke-linejoin="round"'
    p = [
        f'<rect x="6" y="30" width="88" height="12" rx="2" {S} stroke-width="{w:.2f}"/>',
        f'<rect x="8" y="42" width="84" height="36" {S} stroke-width="{w:.2f}"/>',
        f'<path d="M12 78 l0 12 M88 78 l0 12" {S} stroke-width="{w*0.8:.2f}"/>',
    ]
    for i in range(4):                                                    # drawers
        x = 10 + i * 21
        p.append(f'<rect x="{x}" y="44" width="19" height="12" {S} stroke-width="{w*0.5:.2f}"/>')
        p.append(f'<circle cx="{x+9.5}" cy="50" r="1.6" {S} stroke-width="{w*0.4:.2f}"/>')
    for i in range(3):                                                    # lattice panels
        x = 12 + i * 27
        p.append(f'<rect x="{x}" y="58" width="24" height="18" {S} stroke-width="{w*0.5:.2f}"/>')
        p.append(_hatch(x, 58, x + 24, 58 + 18, 5, 4.8, 0, w=0.4, op=0.55))
        p.append(_hatch(x, 76, x + 24, 58, 5, 4.8, 0, w=0.4, op=0.55))
    return "".join(p)


def coffee_beans(w=2.0, n=3):
    S = f'stroke="{INK}" fill="none" stroke-linecap="round" stroke-linejoin="round"'
    p = []
    for i in range(n):
        cx = 30 + i * 20
        p.append(f'<ellipse cx="{cx}" cy="50" rx="9" ry="12" {S} stroke-width="{w*0.8:.2f}"'
                 f' transform="rotate({-18+i*16} {cx} 50)"/>')
        p.append(f'<path d="M{cx} 39 q-3 11 0 22" {S} stroke-width="{w*0.5:.2f}"'
                 f' transform="rotate({-18+i*16} {cx} 50)"/>')
    return "".join(p)


def leaf_sprig(w=1.8, flip=False):
    S = f'stroke="{INK}" fill="none" stroke-linecap="round" stroke-linejoin="round"'
    p = [f'<path d="M10 90 q26 -24 44 -70" {S} stroke-width="{w*0.7:.2f}"/>']
    for i in range(6):
        t = i / 6
        x = 10 + 44 * (t ** 0.8)
        y = 90 - 70 * (t ** 1.15)
        p.append(f'<path d="M{x:.1f} {y:.1f} q10 -8 18 -2 q-8 8 -18 2 Z" {S}'
                 f' stroke-width="{w*0.55:.2f}" transform="rotate({-24+i*6} {x:.1f} {y:.1f})"/>')
        p.append(f'<path d="M{x:.1f} {y:.1f} q-10 -8 -18 -2 q8 8 18 2 Z" {S}'
                 f' stroke-width="{w*0.55:.2f}" transform="rotate({24-i*6} {x:.1f} {y:.1f})"/>')
    g = "".join(p)
    return f'<g transform="scale(-1,1) translate(-100,0)">{g}</g>' if flip else g


def tee_mock(w=2.4, label=""):
    """Line-drawn crew-neck t-shirt. Local box 0..100 x 0..100, chest print area
    is the rect x 30..70, y 34..70 (place art with translate/scale there)."""
    S = f'stroke="{INK}" fill="none" stroke-linecap="round" stroke-linejoin="round"'
    return "".join([
        f'<path d="M36 14 q14 8 28 0 l14 6 q8 4 10 12 l-8 6 l-4 -5 l0 55'
        f' q-22 5 -42 0 l0 -55 l-4 5 l-8 -6 q2 -8 10 -12 Z" {S} stroke-width="{w:.2f}"/>',
        f'<path d="M36 14 q14 12 28 0" {S} stroke-width="{w*0.7:.2f}"/>',
        f'<path d="M38 18 q12 9 24 0" {S} stroke-width="{w*0.35:.2f}" opacity="0.7"/>',
        f'<path d="M32 88 q18 4 36 0" {S} stroke-width="{w*0.5:.2f}" opacity="0.8"/>',
        _hatch(30, 40, 30, 80, 3, 1.4, 0, w=0.5, op=0.35),
    ])
