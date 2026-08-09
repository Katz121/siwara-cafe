# -*- coding: utf-8 -*-
"""Round 4 · hand-drawn sketches of the SEVEN real angles in D:\\Siwaracafeweb\\siwarahome.
Each prompt was written after looking at that exact photo, so the sketch matches the angle.
Sequential only.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from _run_codex2 import HUMAN, NOTEXT  # noqa: E402
from _run_codex2 import run  # noqa: E402

JOBS = [
    # ---------------------------------------------------------------- exterior, from the lawn
    ("f01_angle_lawn_view.png", "1024x1536",
     "a loose hand-drawn ink and watercolour sketchbook page of a Thai teak wooden cafe seen across "
     "its front lawn from the left: on the left a two-storey teak block with a wide gable, a "
     "terracotta tiled roof with a decorative wooden bargeboard, three tall casement windows upstairs "
     "under the gable and a wooden louvre vent in the gable peak; in front of it a lower gabled porch "
     "with its big folding teak doors wide open so you can see dark shadow and a couple of bar stools "
     "inside; the building steps down to the right into a lower single-storey wing with a tiled roof, "
     "small casement windows and a dark open doorway; old wall lanterns beside the doors; a wide gravel "
     "drive curving away to the right with a big spreading mango tree over it; a low white fence and "
     "green hills in the far distance; a broad sweep of lawn filling the whole bottom third of the "
     "page drawn with just a few horizontal pencil strokes and left mostly bare paper; heavy monsoon "
     "clouds suggested by three or four loose wet washes at the top. "
     + HUMAN + ". " + NOTEXT),

    # ---------------------------------------------------------------- the house BEFORE restoration
    ("f02_angle_before_1932.png", "1024x1536",
     "a hand-drawn pencil and sepia ink wash sketch, made to look like a drawing of an old photograph "
     "of the same house long before it was restored: a tall two-storey Thai wooden house, the upper "
     "floor slightly cantilevered out over the lower one, roofed with old corrugated metal sheets "
     "instead of tiles, a plain wide gable with no decoration, upstairs wooden louvre shutters and one "
     "small window with vertical iron bars, downstairs tall wooden panelled windows and shutters, "
     "everything weathered and dark; to the right a lower lean-to wing with a corrugated roof, an open "
     "double door showing a dark interior with a bench, and a small barred window; the whole house "
     "sitting on a raised plastered plinth with a couple of concrete steps; a big earthen water bowl "
     "and two buckets on the bare dirt yard in front; scrubby grass, a bamboo clump on the right, an "
     "empty pale sky; drawn entirely in graphite with thin sepia washes, all the tone put in with loose "
     "irregular pencil hatching and smudged fingertips. "
     + HUMAN + ". " + NOTEXT),

    # ---------------------------------------------------------------- interior wide, the main room
    ("f03_angle_interior_wide.png", "1024x1536",
     "a loose ballpoint pen sketch of the inside of a Thai teak house cafe, drawn standing in the "
     "doorway looking across the room: a teak plank ceiling running away in perspective with two small "
     "downlights, teak plank walls everywhere; on the left wall a large framed painting of a crowded "
     "town in warm tones with a sprig of white orchid propped on its corner, and a big rubber plant in "
     "a white pot on the floor in the foreground corner; a tall open doorway in the middle left showing "
     "another room beyond with a row of bar stools at a counter and daylight from its windows; in the "
     "centre of the far wall a tall window with a coloured pressed-glass transom above it, a white "
     "vertical grille, its wooden casement pushed open, trailing vines hanging either side, a hanging "
     "rattan basket, and a grid of small postcards pinned on the wall beside it; below the window a "
     "plain teak table with a small vase of pink flowers and two wooden benches, one bench pulled out "
     "onto a woven rug; on the right a small glass-fronted wooden cabinet with a coffee grinder and a "
     "pleated-shade table lamp glowing on it, and beyond it an open door to the bright garden; the "
     "floorboards drawn with fast scribbled ballpoint lines, the right hand third of the drawing left "
     "unfinished. " + HUMAN + ". " + NOTEXT),

    # ---------------------------------------------------------------- the lonely window counter
    ("f04_angle_window_counter.png", "1024x1536",
     "a hand-drawn fineliner and loose watercolour sketch of a quiet corner of a Thai teak house cafe: "
     "on the left a long teak counter fixed under a run of folding casement windows that are pushed "
     "wide open, three tall wooden bar stools tucked under it, a wooden rack of paperback books and a "
     "small tissue box standing on the counter; through the open windows you can see the tiled roof of "
     "the neighbouring house and big banana leaves against a pale sky; a leaning mirror propped in the "
     "far left corner and a monstera in a white pot beside it; in the middle of the room a small dark "
     "round pedestal table with three turned-leg stools around it and a glass vase of white tulips on "
     "top; behind that a low glass-fronted wooden cabinet with a small lamp and a radio on it; on the "
     "right wall a tall window with three panes of coloured pressed glass in the transom, green blue "
     "and pink, painted with three flat loose watercolour patches, a white vertical grille below it "
     "and the wooden wall painted a soft sage green under the sill; a pleated-shade floor lamp at the "
     "far right edge, two flat floor cushions on the boards; wide teak floorboards drawn with a few "
     "long uneven lines running away from the viewer. " + HUMAN + ". " + NOTEXT),

    # ---------------------------------------------------------------- the signature window, frontal
    ("f05_angle_signature_window.png", "1024x1536",
     "a pencil and coloured-pencil sketchbook drawing looking straight at the most beautiful corner of "
     "a Thai teak house: a tall wooden window set in a teak plank wall, its transom made of two panes "
     "of patterned pressed glass, one amber yellow and one dusty pink, drawn with soft coloured-pencil "
     "scribble that goes over the lines; below the transom the window is open with a white painted "
     "vertical grille, and beyond it bright daylight, a paved courtyard, potted shrubs, a motorbike, a "
     "banana clump and the roof of a low building, all drawn very faintly so the outside looks blown "
     "out with light; a strand of vine hangs down each side of the window and a string of small "
     "hanging ornaments dangles down the middle; on the left wall a loose grid of little postcards and "
     "small paintings pinned up, drawn as quick rectangles with a few marks inside instead of real "
     "pictures; on the right wall a woven rattan basket hanging from a peg and a pleated lampshade "
     "entering the frame; a low teak ledge across the bottom with two tiny framed paintings and a "
     "small cactus in a pot; teak plank ceiling above; graphite hatching for the dark wood, the whole "
     "drawing slightly crooked. " + HUMAN + ". " + NOTEXT),

    # ---------------------------------------------------------------- lounge with the chandelier
    ("f06_angle_lounge.png", "1024x1536",
     "a loose ink and grey wash hand-drawn sketch of the lounge room of a Thai teak house cafe, drawn "
     "from a corner so the perspective sweeps to the right: a teak plank ceiling with a small brass "
     "chandelier of five lamp shades hanging on the left and a wooden ceiling fan further right; along "
     "the far wall tall teak lattice screens with panes of coloured pressed glass in blue green pink "
     "and yellow above them, drawn with quick flat washes; against that wall a teak settee and two "
     "matching teak armchairs with floral cushions, and a long low teak coffee table with a glass top "
     "in front of them; a small round teak table with two stools in the near foreground with a tissue "
     "box on it; on the left wall an antique dark wooden pendulum clock and a flat dark screen, and a "
     "wooden cabinet in the near left corner with a big bunch of pink and white flowers on it; at the "
     "far end of the room, smaller in the distance, a counter with tall bar stools and a bright window "
     "full of garden greenery, and a standing lamp with a pleated shade; wide dark floorboards drawn "
     "with long fast strokes, a patch of sunlight on the floor left as bare paper. "
     + HUMAN + ". " + NOTEXT),

    # ---------------------------------------------------------------- the roses on the table
    ("f07_angle_roses_table.png", "1024x1024",
     "a small quick watercolour and ink still life sketch on cream paper: two full pale pink garden "
     "roses with yellow centres on green stems with a few leaves, standing in a slender fluted clear "
     "glass vase on a polished dark teak table top; beside the vase a little wooden flip calendar "
     "block; the background is only three or four loose wet washes suggesting warm wood and a blurred "
     "chair, no detail at all; the roses are the only thing drawn carefully and even they are a bit "
     "lopsided, petals drawn with single wobbly strokes and pink washes that bleed outside the lines "
     "and pool at one edge, the table drawn with two lines and a smudge. "
     + HUMAN + ". The only text is JUN 18 hand-lettered small and imperfect on the little calendar "
     "block, and there is no other text anywhere"),
]

if __name__ == "__main__":
    only = sys.argv[1:]
    for name, size, brief in JOBS:
        if only and name not in only:
            continue
        run(name, size, brief)
