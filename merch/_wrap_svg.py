# -*- coding: utf-8 -*-
"""Inline any .svg into a 1080x1350 HTML page so render_covers_png.py can shoot it
(and so Google Fonts referenced by the SVG actually load)."""
import re
import sys
from pathlib import Path

TPL = """<!DOCTYPE html><html lang="th"><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Chonburi&family=Sarabun:wght@300;400;600;700&family=Noto+Sans+Thai:wght@300;400;600;700&display=swap" rel="stylesheet">
<style>html,body{margin:0;padding:0;background:#f4ece0;overflow:hidden}
svg{display:block;width:1080px;height:1350px}</style></head><body>
%s
</body></html>"""


def wrap(svg_path: Path) -> Path:
    svg = svg_path.read_text(encoding="utf-8", errors="replace")
    svg = re.sub(r"^.*?(?=<svg)", "", svg, flags=re.S)          # drop xml/doctype preamble
    out = svg_path.with_name(svg_path.stem + "_view.html")
    out.write_text(TPL % svg, encoding="utf-8")
    return out


if __name__ == "__main__":
    for pat in sys.argv[1:]:
        for f in sorted(Path().glob(pat)) or [Path(pat)]:
            if f.suffix.lower() == ".svg":
                print(wrap(f))
