# -*- coding: utf-8 -*-
"""Round 3 · more hand-drawn Codex sheets (winning engine for the 'a person drew this' look).
Sequential only. Reuses the HUMAN / SUBJECT anchors from round 2.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from _run_codex2 import HUMAN, SUBJECT, NOTEXT, typo, run  # noqa: E402

JOBS = [
    # --- pure sticker art, one object per drawing, big and clean (best for die-cutting)
    ("e01_stickers_objects.png", "1024x1024",
     f"a notebook page with six separate hand-drawn objects doodled on it with a fine black pen and "
     f"a single terracotta colour pencil, each object drawn big and clear with plenty of white paper "
     f"around it, never overlapping, each at a slightly different tilt: an antique pendulum wall "
     f"clock in a dark wooden case with a tiny horse figure on top, a coffee cup on a saucer with "
     f"steam, an arc floor lamp with a pleated dome shade, a tall glass of iced honey lemon coffee "
     f"with a lemon slice, a slice of homemade cake on a plate, and a coconut flower branch. "
     f"{HUMAN}. {NOTEXT}"),

    ("e02_stickers_house_set.png", "1024x1024",
     f"a notebook page with six separate hand-drawn doodles of small buildings and street things from "
     f"a Thai old town, drawn with a fine black pen and washed lightly with one muddy terracotta "
     f"watercolour, each drawn big with white paper around it and never overlapping: a two-storey "
     f"teak wooden gabled house cafe, a Sino-Portuguese shophouse front with louvre shutters, an old "
     f"street lantern, a leaning electric pole with tangled wires, a wooden bench with a floral "
     f"cushion, and a long teak drawer cabinet. {HUMAN}. {NOTEXT}"),

    # --- t-shirt art: simple, bold, few strokes
    ("e03_tee_minimal_house.png", "1024x1024",
     f"one single simple hand-drawn line drawing of {SUBJECT}, drawn with a thick black marker in "
     f"very few strokes, deliberately simplified and a bit clumsy, the roof done in about eight "
     f"strokes, no shading at all except three or four quick scribbled lines, sitting alone in the "
     f"middle of a big empty cream page, the kind of drawing that would still read clearly printed "
     f"small on the chest of a t-shirt. {HUMAN}. {NOTEXT}"),

    ("e04_tee_coffee_house.png", "1024x1024",
     f"one hand-drawn ink doodle where a coffee cup and the teak wooden gabled cafe house are drawn "
     f"together as a single small motif, the house sitting behind the cup like it is rising out of "
     f"the steam, drawn with a wobbly black brush pen with thick and thin strokes and a couple of ink "
     f"blots, simple enough to screen print in one colour, alone on an empty cream page. "
     f"{HUMAN}. {NOTEXT}"),

    # --- posters with room for Thai type to be set later in HTML
    ("e05_poster_dusk_pencil.png", "1024x1536",
     f"a pencil and sepia colour pencil sketchbook drawing of {SUBJECT} at dusk, warm lantern light "
     f"suggested by leaving small patches of bare paper inside the windows while the rest of the "
     f"drawing is loosely shaded with graphite scribble, a couple of figures walking towards the "
     f"veranda drawn as three or four scruffy lines each, the whole top third of the page left "
     f"completely empty bare paper. {HUMAN}. {NOTEXT}"),

    ("e06_poster_botanical_page.png", "1024x1536",
     f"a botanist's field notebook page drawn by hand in ink and light watercolour: a coconut flower "
     f"branch, a coffee branch with cherries, a monstera leaf and a fern frond arranged loosely down "
     f"the page with white space between them, each with quick uneven stipple shading, the middle of "
     f"the page left clear and empty, the drawings slightly wilting and imperfect, one leaf only half "
     f"finished. {HUMAN}. {NOTEXT}"),

    # --- interior / details, human warmth
    ("e07_interior_corner.png", "1024x1536",
     f"a loose hand-drawn ink and watercolour sketch of one quiet corner inside a teak wooden Thai "
     f"cafe: a wooden bench with floral cushions under a casement window with small panes, a potted "
     f"plant beside it, an antique pendulum wall clock on the panelled wall above, a low wooden table "
     f"with a coffee cup and a paperback on it, afternoon light drawn as a few diagonal pencil lines "
     f"across the floorboards, the edges of the sketch trailing off into bare paper. {HUMAN}. {NOTEXT}"),

    ("e08_counter_slowbar.png", "1024x1536",
     f"a hand-drawn ballpoint sketch of the coffee counter of a small wooden Thai cafe seen from a "
     f"customer standing at it: a teak counter top, a hand pouring a kettle in a slow spiral over a "
     f"filter, a row of glass jars, a scribbled shelf of cups behind, a small chalk board leaning "
     f"against the counter, everything drawn quickly with scribbled ballpoint shading and a wonky "
     f"perspective, the hand drawn a bit badly. {HUMAN}. {NOTEXT}"),

    # --- old town context sheets
    ("e09_shophouse_row.png", "1024x1536",
     f"a hand-drawn ink and light watercolour elevation study of four Sino-Portuguese shophouses in "
     f"a row in a Thai old town, drawn flat-on like a page from a heritage survey notebook but done "
     f"by hand and slightly crooked: stucco air vents, wooden louvre shutters, faded shop signs, "
     f"corrugated awnings, one shop with its roller door half down, a motorbike leaning outside, each "
     f"building a slightly different height and the row not sitting on a straight ground line, small "
     f"pencil notes and measurement ticks in the margin that are just squiggles not readable words. "
     f"{HUMAN}. {NOTEXT}"),

    ("e10_river_garden.png", "1024x1536",
     f"a loose watercolour and ink sketch of the back garden of the teak wooden cafe: a circular lawn "
     f"edged with gravel, round-trimmed topiary bushes, banana and coconut palms, a couple of wooden "
     f"chairs and a small table on the grass, the corner of the wooden house with its terracotta roof "
     f"entering from the right, a green hill behind, the washes loose and blotchy and running past the "
     f"ink lines, one corner of the paper cockled by the water. {HUMAN}. {NOTEXT}"),

    # --- one lettering-led sheet, hand lettered Thai
    ("e11_handlettered_sign.png", "1024x1536",
     f"a hand-lettered sign design drawn on cream paper with a broad black nib and one terracotta "
     f"colour, the kind a shop owner draws before painting their own signboard: a rectangular signboard "
     f"shape drawn slightly crooked with a decorative hand-drawn border of small leaves and coffee "
     f"beans, a small simple line drawing of the teak gabled house in the middle of the board, faint "
     f"pencil guide lines still visible under the lettering. "
     f"{typo('the hand-lettered Thai words ศิวรา คาเฟ่ large across the middle of the board and the smaller hand-lettered Thai word ตะกั่วป่า underneath')}"),
]

if __name__ == "__main__":
    only = sys.argv[1:]
    for name, size, brief in JOBS:
        if only and name not in only:
            continue
        run(name, size, brief)
