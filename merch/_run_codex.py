"""Sequential Codex $imagegen runs (gpt-image-2) for Siwara merch line art.
Sequential ONLY (parallel = race condition, files overwrite each other).
Each prompt MUST be a single paragraph or codex receives an empty prompt.
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

STYLE = (
    "hand-drawn ink line art on warm cream paper (#f4ece0) with visible paper grain, "
    "dark sepia-black ink (#241d19) lines with uneven organic hand-wobble line weight, "
    "shading only by cross-hatching and stippling, at most two accent colors: "
    "terracotta brick (#b4451f) and teak brown (#8a5a2b), vintage warm quiet mood, "
    "no gradients, no 3D, no photorealism, no flat modern vector look"
)

SUBJECT = (
    "a nearly 100-year-old two-storey Thai teak wooden house cafe in Takua Pa old town, "
    "Phang-nga: stacked gable roofs of terracotta clay tiles, a tall central gable with a "
    "wooden louvre air vent under the peak, a lower left wing open as a sitting veranda, "
    "a right wing with tall wooden double doors, horizontal lap wooden siding, casement "
    "windows with small glass panes in a 3x2 grid, antique wall lanterns beside every door, "
    "small round-trimmed topiary bushes in front, a circular lawn edged with gravel, and "
    "green forested hills behind"
)

TYPO = (
    "TYPOGRAPHY RULE render the Thai text exactly character for character with correct Thai "
    "vowels and tone marks, no invented glyphs, no misspellings, no Latin substitutions, "
    "and do not add any text that is not listed"
)

JOBS = [
    ("c01_botanical_ink.png", "1024x1536",
     f"a vertical poster of {SUBJECT}, framed by hand-drawn botanical branches, monstera and "
     f"coconut fronds along the top corners and bottom edge, the house centred in the lower two "
     f"thirds, generous empty cream space at the top for a headline, style: {STYLE}. "
     f"Text in the poster: the Thai heading 'ศิวรา คาเฟ่' large at the top, below it the smaller "
     f"Thai line 'บ้านไม้สักเกือบ 100 ปี ในเมืองเก่าตะกั่วป่า', and at the very bottom the small "
     f"Latin line 'SIWARA CAFE · EST. 2475'. {TYPO}"),

    ("c02_engraving_street.png", "1024x1536",
     f"a vertical vintage copperplate-engraving style illustration of Takua Pa old town street: "
     f"a row of two-storey Sino-Portuguese shophouses with stucco air vents, wooden louvre "
     f"shutters and faded old shop signs on the left, and on the right {SUBJECT}, with a leaning "
     f"electric pole and sagging wires crossing the sky, a bicycle parked on the footpath, dense "
     f"fine engraving hatch lines describing every surface, style: {STYLE}. "
     f"Text: only the small Thai line 'ตะกั่วป่า' bottom centre and 'SIWARA CAFE' below it. {TYPO}"),

    ("c03_sticker_sheet.png", "1024x1024",
     f"a square hand-drawn sticker sheet on cream paper, nine separate small ink drawings each "
     f"surrounded by its own dashed die-cut outline, arranged in a loose three by three grid with "
     f"clear space between them: an antique pendulum wall clock in a dark wooden case with a tiny "
     f"horse figure on top, a coffee cup on a saucer with curling steam, an arc floor lamp with a "
     f"pleated dome shade, a long teak drawer cabinet, a wooden bench with a floral cushion, a "
     f"slice of homemade cake, a glass of iced honey lemon coffee with a lemon slice, a coconut "
     f"flower branch, and the small teak gabled cafe house, style: {STYLE}. "
     f"Text: no text at all except the small Thai word 'ศิวรา' inside one round badge sticker. {TYPO}"),

    ("c04_interior_thin_line.png", "1024x1536",
     f"a vertical delicate thin-line pen illustration of the quiet interior of a teak wooden Thai "
     f"cafe: a long teak drawer cabinet against a wood-panelled wall, two tall antique pendulum "
     f"wall clocks hanging one on each side of a framed landscape painting, a vase of roses and a "
     f"row of books on the cabinet, a potted plant in the foreground, an arc floor lamp with a "
     f"pleated dome shade leaning over a wooden bench with floral cushions, soft afternoon light "
     f"from a casement window, very fine sparse hatching, lots of breathing white space, "
     f"style: {STYLE}. Text: only the small Latin line 'Here, every moment feels like home.' "
     f"at the bottom. {TYPO}"),

    ("c05_woodblock_tee.png", "1024x1024",
     f"a square bold woodblock print emblem designed to be screen printed on a t-shirt chest, "
     f"two inks only on cream: a thick confident carved outline drawing of the teak gabled cafe "
     f"house inside a circular badge, chunky carved hatch marks for the roof tiles, a ring of "
     f"coffee beans and small leaves around the circle, deliberately rough carved edges, no line "
     f"thinner than a woodcut gouge, style: bold Japanese mokuhanga woodblock, ink #241d19 with "
     f"terracotta #b4451f accents on cream #f4ece0, no fine detail, no hatching finer than 2mm. "
     f"Text arched inside the circular badge: the Thai words 'ศิวรา คาเฟ่' across the top arc and "
     f"'ตะกั่วป่า' across the bottom arc. {TYPO}"),

    ("c06_map_zine.png", "1024x1536",
     f"a vertical hand-drawn illustrated walking map of Takua Pa old town in the style of a "
     f"traveller's ink sketchbook page: a winding street drawn as a soft curving ribbon, tiny "
     f"line-drawn shophouses and a temple and a river along it, a dotted walking route, a small "
     f"hand-drawn compass rose, and at the end of the route a slightly larger drawing of {SUBJECT} "
     f"marked with a little pin, coffee-ring stain on the paper, style: {STYLE}. "
     f"Text: the Thai heading 'เมืองเก่าตะกั่วป่า' at the top, the small Thai label 'ศิวรา คาเฟ่' "
     f"beside the pinned house, and nothing else. {TYPO}"),
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
        capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=1500,
    )
    tail = (p.stdout or "")[-600:]
    print(tail, flush=True)
    if p.returncode != 0:
        print(f"!! exit {p.returncode}: {(p.stderr or '')[-400:]}", flush=True)
    print(f"exists={dest.exists()}", flush=True)


if __name__ == "__main__":
    only = sys.argv[1:]
    for name, size, brief in JOBS:
        if only and name not in only:
            continue
        run(name, size, brief)

    print("\n=== md5 check (duplicates = race/regen needed) ===")
    for f in sorted(OUT.glob("*.png")):
        print(hashlib.md5(f.read_bytes()).hexdigest()[:12], f.stat().st_size // 1024, "KB", f.name)
