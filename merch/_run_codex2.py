# -*- coding: utf-8 -*-
"""Round 2 · Codex $imagegen — HAND-DRAWN BY A PERSON look (not digital engraving).
Sequential only. Single-paragraph orders only.
Round 1 failed the brief because "engraving / woodblock" prompts produce that
machine-perfect look. Round 2 anchors every prompt to a real drawing medium
(ballpoint, fineliner + watercolour, 2B pencil, brush pen, conte, colour pencil)
and forbids the tells of a digital render.
"""
import hashlib
import io
import subprocess
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

CODEX = r"C:\Users\siwat\AppData\Roaming\npm\codex.cmd"
OUT = Path(r"D:\Siwaracafeweb\merch\codex")
OUT.mkdir(parents=True, exist_ok=True)

HUMAN = (
    "CRITICAL this must look like a real human being sat down and drew it by hand in a "
    "sketchbook, photographed slightly off-square with soft daylight and a faint page shadow: "
    "lines are imperfect and wobbly, line pressure is uneven and lines fade or break where the "
    "pen lifted, strokes overshoot past corners instead of meeting exactly, some lines are drawn "
    "over twice, perspective is a little bit off, verticals are not perfectly vertical, nothing is "
    "symmetrical, hatching is quick and irregular with lines that are not parallel and not evenly "
    "spaced, some areas are left unfinished or only suggested, faint construction lines and eraser "
    "smudges are visible, small ink blots and fingerprint smudges on the paper, the paper has real "
    "visible fibre texture and a soft dog-eared corner. STRICTLY AVOID the look of a digital "
    "illustration, vector art, clip art, a copperplate engraving, a laser-perfect woodcut, evenly "
    "machined hatching, or an architectural CAD render; do NOT draw every single roof tile or every "
    "wood plank individually, suggest them loosely and let some stop halfway"
)

SUBJECT = (
    "a nearly 100-year-old two-storey Thai teak wooden house cafe in Takua Pa old town, "
    "Phang-nga: stacked gable roofs of terracotta clay tiles, a tall central gable with a wooden "
    "louvre air vent under the peak, a lower left wing open as a sitting veranda with a couple of "
    "wooden chairs, a right wing with tall wooden double doors, horizontal lap wooden siding, "
    "casement windows with small panes, an old lantern beside each door, a few round-trimmed "
    "topiary bushes in front and a circular lawn edged with gravel"
)

NOTEXT = (
    "There must be absolutely no text, no letters, no numbers, no signature and no watermark "
    "anywhere in the image"
)


def typo(lines: str) -> str:
    return (
        f"The only text in the image is hand-lettered with the same pen, slightly uneven baseline, "
        f"letters not identical in size: {lines}. TYPOGRAPHY RULE render the Thai exactly character "
        f"for character with correct Thai vowels and tone marks, no invented glyphs, no misspellings, "
        f"no Latin substitutions, and add no other text anywhere"
    )


JOBS = [
    # ---- 1. ballpoint sketchbook, with lettering
    ("d01_ballpoint_house.png", "1024x1536",
     f"a page from a traveller's sketchbook drawn with a single blue-black ballpoint pen on warm "
     f"cream paper, loose and quick: {SUBJECT}, drawn scrappily with scribbled ballpoint shading "
     f"that goes outside the lines, the bushes just fast scribbled loops, the hills behind only a "
     f"few wandering lines, plenty of bare paper left around the drawing. {HUMAN}. "
     f"{typo('the Thai words ศิวรา คาเฟ่ written by hand under the drawing and the small Thai word ตะกั่วป่า below that')}"),

    # ---- 2. fineliner + loose watercolour wash
    ("d02_watercolour_house.png", "1024x1536",
     f"a hand-painted sketchbook page: {SUBJECT} drawn first with a wobbly black fineliner then "
     f"washed with very loose watercolour in only two muddy colours, terracotta for the roof tiles "
     f"and warm ochre brown for the teak walls, the washes are uneven with visible brush edges, "
     f"water blooms and hard drying lines, and they clearly bleed outside the ink lines and leave "
     f"parts of the drawing unpainted white paper, a stray drip runs down one corner. {HUMAN}. "
     f"{typo('the Thai words ศิวรา คาเฟ่ hand-written small at the bottom left')}"),

    # ---- 3. soft pencil, no text (Thai typography added later in HTML)
    ("d03_pencil_house.png", "1024x1536",
     f"a soft 2B graphite pencil drawing on off-white sketch paper of {SUBJECT}, drawn lightly with "
     f"visible under-drawing boxes and guide lines still showing through the finished lines, "
     f"graphite smudged with a fingertip for the shadows under the roof eaves, an eraser patch where "
     f"something was corrected, the bottom third of the paper left almost empty. {HUMAN}. {NOTEXT}"),

    # ---- 4. brush pen bold sketch for a t-shirt, no text
    ("d04_brushpen_house.png", "1024x1024",
     f"a bold quick brush-pen ink drawing on cream paper of {SUBJECT}, drawn in maybe twenty "
     f"confident thick-and-thin strokes where the brush tip splits and skips, dry-brush texture, a "
     f"couple of fat ink blobs where the brush paused, shapes simplified almost to a signature so it "
     f"would still read printed small on a shirt, loads of empty paper around it. {HUMAN}. {NOTEXT}"),

    # ---- 5. old town street, dip pen and ink, loose
    ("d05_dippen_street.png", "1024x1536",
     f"a loose dip-pen and sepia-ink sketchbook drawing of a Sino-Portuguese old town street in "
     f"Takua Pa, Thailand: a row of two-storey shophouses with stucco air vents, wooden louvre "
     f"shutters, faded old shop signs and corrugated awnings on the left, and on the right the teak "
     f"wooden cafe house with a small OPEN board, a leaning electric pole with sagging wires across "
     f"the sky, a bicycle propped against a wall, the road drawn with a few fast lines running away "
     f"to a vanishing point that is slightly wrong, deep shadows scribbled in quickly under the "
     f"awnings, ink getting drier and scratchier towards the edges of the page, the bottom right "
     f"corner of the drawing just trailing off unfinished. {HUMAN}. "
     f"{typo('the small hand-written Thai word ตะกั่วป่า in the lower right corner')}"),

    # ---- 6. sticker sheet of shop objects, felt pen
    ("d06_marker_stickers.png", "1024x1024",
     f"a sketchbook page of ten small separate hand-drawn objects each roughly circled by a wobbly "
     f"hand-drawn dashed cutting line, drawn with a fine felt pen and lightly touched with one "
     f"terracotta colour pencil: an antique pendulum wall clock in a wooden case with a tiny horse on "
     f"top, a coffee cup on a saucer with steam, an arc floor lamp with a pleated dome shade, a long "
     f"teak drawer cabinet, a wooden bench with a floral cushion, a slice of cake, a tall glass of "
     f"iced honey lemon coffee with a lemon slice, a coconut flower branch, two dice with a wooden "
     f"game pawn, and the little teak gabled cafe house, arranged loosely and crookedly with clear "
     f"space between them and never overlapping, each one drawn at a slightly different tilt and "
     f"size like they were doodled at different moments. {HUMAN}. {NOTEXT}"),

    # ---- 7. interior, quiet pencil + one colour
    ("d07_interior_sketch.png", "1024x1536",
     f"a quiet unfinished sketchbook drawing of the inside of a teak wooden Thai cafe, drawn in "
     f"pencil with a little sepia colour pencil on top: a long teak drawer cabinet against a "
     f"wood-panelled wall, two tall antique pendulum wall clocks hanging either side of a small "
     f"framed landscape painting, a vase of roses and a row of books on the cabinet, a potted plant "
     f"in the foreground drawn much more roughly than the rest, an arc floor lamp with a pleated dome "
     f"shade leaning over a wooden bench with floral cushions, afternoon light suggested by leaving "
     f"the paper bare, the right hand side of the drawing fading out into blank paper mid-object. "
     f"{HUMAN}. {NOTEXT}"),

    # ---- 8. crooked hand-drawn walking map
    ("d08_handmap_oldtown.png", "1024x1536",
     f"a crooked hand-drawn walking map of Takua Pa old town in a notebook, the kind a shop owner "
     f"draws for a customer: the main street as one wandering wobbly line, tiny lopsided line-drawn "
     f"shophouses and a temple and a river along it, a dotted walking route drawn with uneven dots, "
     f"a small badly drawn compass rose, an arrow and a little starred box at the end of the route "
     f"where a slightly bigger drawing of the teak wooden cafe house sits, a real coffee cup ring "
     f"stain overlapping the map, one corner of the page torn. {HUMAN}. "
     f"{typo('the hand-written Thai heading เมืองเก่าตะกั่วป่า at the top and the small hand-written Thai label ศิวรา คาเฟ่ next to the starred house')}"),
]


def run(name: str, size: str, brief: str) -> None:
    dest = OUT / name
    order = (
        f"สร้างภาพด้วย image_gen (gpt-image-2) ขนาด {size} คุณภาพสูง แล้วบันทึกไฟล์ที่ "
        f"{dest.as_posix()} · เนื้อหาภาพ: {brief} · บันทึกไฟล์ให้สำเร็จก่อนตอบ"
    )
    print(f"\n=== {name} ({size}) ===", flush=True)
    p = subprocess.run(
        [CODEX, "exec", "--skip-git-repo-check",
         "--dangerously-bypass-approvals-and-sandbox", order],
        capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=1800,
    )
    print((p.stdout or "")[-400:], flush=True)
    if p.returncode != 0:
        print(f"!! exit {p.returncode}: {(p.stderr or '')[-300:]}", flush=True)
    print(f"exists={dest.exists()}", flush=True)


if __name__ == "__main__":
    only = sys.argv[1:]
    for name, size, brief in JOBS:
        if only and name not in only:
            continue
        run(name, size, brief)
    print("\n=== md5 check ===")
    for f in sorted(OUT.glob("*.png")):
        print(hashlib.md5(f.read_bytes()).hexdigest()[:12], f.stat().st_size // 1024, "KB", f.name)
