"""Optimize the heavy editorial assets in site/assets.

Safe to run repeatedly: source JPEGs are only removed after their WebP has
been written successfully, and existing optimized files are reused.
"""
from pathlib import Path
from PIL import Image, ImageOps
import json

ROOT = Path(__file__).parent
ASSETS = ROOT / "site" / "assets"

def optimize_guides():
    rows = []
    for src in sorted((ASSETS / "guide").glob("*.jpg")):
        dst = src.with_suffix(".webp")
        before = src.stat().st_size
        with Image.open(src) as im:
            im = ImageOps.exif_transpose(im).convert("RGB")
            im.thumbnail((1600, 1600), Image.Resampling.LANCZOS)
            if not dst.exists():
                im.save(dst, "WEBP", quality=82, method=6)
        if dst.exists():
            src.unlink()
            rows.append((src.relative_to(ROOT).as_posix(), before, dst.relative_to(ROOT).as_posix(), dst.stat().st_size))
    return rows

def optimize_og():
    rows = []
    for src in sorted((ASSETS / "og").glob("*.png")):
        before = src.stat().st_size
        with Image.open(src) as im:
            im = ImageOps.exif_transpose(im).convert("RGB")
            if im.size != (1200, 630):
                im = ImageOps.contain(im, (1200, 630), Image.Resampling.LANCZOS)
                canvas = Image.new("RGBA", (1200, 630), (255, 255, 255, 255))
                canvas.alpha_composite(im, ((1200-im.width)//2, (630-im.height)//2))
                im = canvas
            # Palette PNG keeps the original format and preserves crisp text.
            im = im.quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
            im.save(src, "PNG", optimize=True)
        rows.append((src.relative_to(ROOT).as_posix(), before, src.stat().st_size))
    return rows

def optimize_map():
    src = ASSETS / "municipal-map.png"
    if not src.exists():
        return None
    before = src.stat().st_size
    with Image.open(src) as im:
        im = ImageOps.exif_transpose(im)
        # A lossless rewrite is the first choice.
        im.save(src, "PNG", optimize=True)
        png_size = src.stat().st_size
        webp = src.with_suffix(".webp")
        if png_size > before * 0.70:
            if not webp.exists():
                im.save(webp, "WEBP", quality=90, method=6)
        elif webp.exists():
            webp.unlink()
    return ("site/assets/municipal-map.png", before, src.stat().st_size,
            "site/assets/municipal-map.webp" if webp.exists() else None,
            webp.stat().st_size if webp.exists() else None)

def main():
    guides = optimize_guides()
    og = optimize_og()
    mp = optimize_map()
    print(json.dumps({"guides": guides, "og": og, "map": mp}, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
