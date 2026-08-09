# -*- coding: utf-8 -*-
"""Turn the real Siwara photos into pencil / ink line drawings that keep the EXACT angle.

Text-to-image models invent a different building; this path cannot, because the lines come
out of the photograph itself. Three looks per photo:
  _pencil  · XDoG soft graphite drawing, warm paper, grain
  _ink     · high-contrast ink line drawing (good base for stickers / screen print)
  _wash    · ink lines over a flattened watercolour-ish wash of the real colours

Usage:  python _photo_to_sketch.py            (all photos in siwarahome)
        python _photo_to_sketch.py มุมสวย.jpg
"""
import io
import sys
import unicodedata
from pathlib import Path

import cv2
import numpy as np

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

SRC = Path(r"D:\Siwaracafeweb\siwarahome")
OUT = Path(r"D:\Siwaracafeweb\merch\sketch")
OUT.mkdir(parents=True, exist_ok=True)

PAPER = np.array([244, 236, 224], dtype=np.float32)      # RGB cream
INKC = np.array([36, 29, 25], dtype=np.float32)          # RGB near-black brown

SLUG = {
    "siwara": "g01_lawn_view",
    "siwaraold": "g02_before_restoration",
    "มุมร้าน": "g03_interior_wide",
    "มุมร้าน1": "g04_lounge",
    "มุมเหงาๆ": "g05_window_counter",
    "มุมสวย": "g06_signature_window",
    "ดอกไม้ในร้าน": "g07_roses_table",
}


def fit(img, long_side=1800):
    h, w = img.shape[:2]
    s = long_side / max(h, w)
    if s < 1:
        img = cv2.resize(img, (int(w * s), int(h * s)), interpolation=cv2.INTER_AREA)
    return img


def xdog(gray, sigma=0.9, k=1.7, p=22.0, eps=0.55, phi=12.0):
    """eXtended Difference of Gaussians · the classic 'looks hand-drawn' edge operator."""
    g1 = cv2.GaussianBlur(gray, (0, 0), sigma)
    g2 = cv2.GaussianBlur(gray, (0, 0), sigma * k)
    d = (1 + p) * g1 - p * g2
    d /= 255.0
    out = np.where(d >= eps, 1.0, 1.0 + np.tanh(phi * (d - eps)))
    return np.clip(out, 0, 1)


def paper_grain(shape, seed=7, amount=0.055):
    rng = np.random.default_rng(seed)
    n = rng.normal(0, 1, shape[:2]).astype(np.float32)
    n = cv2.GaussianBlur(n, (0, 0), 1.1)
    fib = cv2.GaussianBlur(rng.normal(0, 1, shape[:2]).astype(np.float32), (0, 0), 5.0)
    g = n * 0.7 + fib * 1.6
    g = g / (np.abs(g).max() + 1e-6)
    return 1.0 + g * amount


def wobble(x, seed=3, amp=1.5):
    """displace the drawing slightly with smooth noise so lines are not photo-straight"""
    h, w = x.shape[:2]
    rng = np.random.default_rng(seed)
    fx = cv2.GaussianBlur(rng.normal(0, 1, (h, w)).astype(np.float32), (0, 0), 26)
    fy = cv2.GaussianBlur(rng.normal(0, 1, (h, w)).astype(np.float32), (0, 0), 26)
    fx = fx / (np.abs(fx).max() + 1e-6) * amp
    fy = fy / (np.abs(fy).max() + 1e-6) * amp
    gx, gy = np.meshgrid(np.arange(w, dtype=np.float32), np.arange(h, dtype=np.float32))
    return cv2.remap(x, gx + fx, gy + fy, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)


def flatten(gray, sigma=55):
    """Flat-field / dodge: divide by the local average so dark teak walls keep their detail
    instead of turning into a solid black mass. This is the whole reason the first pass
    came out looking like a night photo."""
    base = cv2.GaussianBlur(gray, (0, 0), sigma)
    flat = (gray + 1.0) / (base + 1.0) * 150.0
    flat = np.clip(flat, 0, 255).astype(np.uint8)
    flat = cv2.createCLAHE(clipLimit=1.2, tileGridSize=(10, 10)).apply(flat)
    # kill wood grain and fabric texture but keep the real structural edges, otherwise the
    # drawing turns into a field of scribble (teak plank grain is everywhere in these photos)
    rgb = cv2.cvtColor(flat, cv2.COLOR_GRAY2BGR)
    rgb = cv2.edgePreservingFilter(rgb, flags=cv2.RECURS_FILTER, sigma_s=90, sigma_r=0.35)
    rgb = cv2.edgePreservingFilter(rgb, flags=cv2.RECURS_FILTER, sigma_s=45, sigma_r=0.25)
    return cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY).astype(np.float32)


def ink_layer(gray_flat, target=0.10, strength=1.0):
    """dark-line map in 0..1 · eps auto-tuned so ink covers ~target of the page,
    which keeps every photo (bright lawn or dark interior) reading as a drawing on paper."""
    lo, hi, e = 0.12, 0.99, None
    for _ in range(11):
        eps = (lo + hi) / 2
        e1 = 1.0 - xdog(gray_flat, sigma=0.8, k=1.6, p=18, eps=eps, phi=15)
        e2 = 1.0 - xdog(gray_flat, sigma=1.7, k=1.7, p=22, eps=eps + 0.02, phi=11)
        e = np.maximum(e1, e2 * 0.8)
        cov = float((e > 0.35).mean())
        if cov > target:
            hi = eps            # too much ink -> raise threshold
        else:
            lo = eps
    e = wobble(e, amp=1.7)
    return np.clip(e * strength, 0, 1)


def structure_mask(gray, sigma=6, keep=0.32):
    """A person draws the shapes that matter and only suggests grass and foliage. This keeps
    ink where there is real large-scale structure (walls, frames, roofs) and thins it out in
    fine texture like lawn and leaves, which otherwise turns into salt-and-pepper speckle."""
    g = cv2.GaussianBlur(gray, (0, 0), sigma)
    gx = cv2.Sobel(g, cv2.CV_32F, 1, 0, ksize=5)
    gy = cv2.Sobel(g, cv2.CV_32F, 0, 1, ksize=5)
    m = np.sqrt(gx * gx + gy * gy)
    m = cv2.GaussianBlur(m, (0, 0), 8)
    m /= (np.percentile(m, 88) + 1e-6)
    m = np.clip(m, 0, 1) ** 0.55
    return keep + (1 - keep) * m


def hatch_shadow(gray, angle=32, spacing=9, pct=22, softness=30):
    """diagonal pencil hatching only in the genuinely darkest areas of THIS photo
    (percentile based, so a dark interior does not end up hatched edge to edge)"""
    h, w = gray.shape
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    a = np.deg2rad(angle)
    jitter = cv2.GaussianBlur(np.random.default_rng(5).normal(0, 1, (h, w)).astype(np.float32),
                              (0, 0), 30) * 2.4                        # strokes not perfectly parallel
    band = np.sin((xx * np.cos(a) + yy * np.sin(a) + jitter) * (np.pi / spacing))
    lines = np.clip((np.abs(band) - 0.62) * -5.5, 0, 1)
    thresh = float(np.percentile(gray, pct))
    dark = np.clip((thresh - cv2.GaussianBlur(gray, (0, 0), 4)) / softness, 0, 1)
    return lines * dark


def compose(ink, tone=None, grain_seed=7, ink_col=INKC, tint=None, tone_amt=0.55):
    h, w = ink.shape
    canvas = np.ones((h, w, 3), np.float32) * PAPER
    if tone is not None:
        t = np.clip(tone, 0, 1)[..., None]
        shade = PAPER * (1 - tone_amt * t) + ink_col * (tone_amt * t)
        canvas = shade
    if tint is not None:
        canvas = canvas * (1 - tint[..., 3:4]) + tint[..., :3] * tint[..., 3:4]
    a = ink[..., None]
    canvas = canvas * (1 - a) + ink_col * a
    canvas *= paper_grain((h, w), seed=grain_seed)[..., None]
    return np.clip(canvas, 0, 255).astype(np.uint8)


def watercolour(bgr, levels=6, blur=17):
    """flatten the real colours into a few loose washes that keep the true palette,
    with the chroma pushed up so it reads as deliberate paint rather than a faded photo"""
    # keep the TRUE colours of the room. Earlier attempts blurred and boosted the chroma
    # channels, which smeared teak brown into pink and turned jpeg noise into rainbow blotches.
    # Quantising / mean-shifting invents false colour regions that go lurid the moment you
    # touch saturation. Just soften the real photo colours and lay them under the ink lines,
    # like a colour-pencil tint over a drawing.
    sm = cv2.edgePreservingFilter(bgr, flags=cv2.RECURS_FILTER, sigma_s=150, sigma_r=0.45)
    sm = cv2.GaussianBlur(sm, (0, 0), 4)
    hsv = cv2.cvtColor(sm, cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv[..., 1] = np.clip(hsv[..., 1] * 1.12, 0, 255)
    hsv[..., 2] = np.clip(hsv[..., 2] * 0.98 + 26, 0, 255)
    sm = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
    rgb = sm[:, :, ::-1].astype(np.float32)
    rgb = rgb * 0.86 + PAPER * 0.14                                    # slight lift only
    return np.dstack([rgb, np.full(rgb.shape[:2], 0.9, np.float32)])


def process(path: Path):
    stem = SLUG.get(path.stem, path.stem)
    bgr = fit(cv2.imdecode(np.fromfile(str(path), np.uint8), cv2.IMREAD_COLOR))
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY).astype(np.float32)
    gray = cv2.bilateralFilter(gray.astype(np.uint8), 9, 60, 60).astype(np.float32)

    flat = flatten(gray)
    ink = ink_layer(flat, target=0.13) * structure_mask(gray)
    hatch = hatch_shadow(gray)
    made = []
    print(f"   ink coverage {(ink > 0.35).mean()*100:.1f}%  hatch {(hatch > 0.3).mean()*100:.1f}%")

    # 1 · pencil · lines + a little hatching in the deep shadows, page stays light
    img = compose(np.clip(ink * 0.72 + hatch * 0.55, 0, 1), hatch * 0.5,
                  grain_seed=11, tone_amt=0.22)
    p = OUT / f"{stem}_pencil.png"
    cv2.imencode(".png", img[:, :, ::-1])[1].tofile(str(p)); made.append(p)

    # 2 · ink only (sticker / screen-print base) · no tone at all
    img = compose(np.clip(ink * 1.1, 0, 1), None, grain_seed=23)
    p = OUT / f"{stem}_ink.png"
    cv2.imencode(".png", img[:, :, ::-1])[1].tofile(str(p)); made.append(p)

    # 3 · ink + watercolour wash carrying the real colours of the room
    img = compose(np.clip(ink * 0.85, 0, 1), None, grain_seed=31, tint=watercolour(bgr))
    p = OUT / f"{stem}_wash.png"
    cv2.imencode(".png", img[:, :, ::-1])[1].tofile(str(p)); made.append(p)

    for m in made:
        print("  ✅", m.name, m.stat().st_size // 1024, "KB")
    return made


if __name__ == "__main__":
    names = sys.argv[1:]
    files = [SRC / n for n in names] if names else sorted(SRC.glob("*.jpg"))
    for f in files:
        print(f"\n=== {f.name}")
        process(f)
