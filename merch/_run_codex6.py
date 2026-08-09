# -*- coding: utf-8 -*-
"""Round 6 · hand-drawn versions of the six remaining photos in siwarahome.
Written after looking at each photo, so the angle and the content match. Sequential only.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from _run_codex2 import HUMAN, NOTEXT  # noqa: E402
from _run_codex2 import run  # noqa: E402

JOBS = [
    # ------------------------------------------------ Chinese shrine, hundreds of red lanterns
    ("f09_shrine_lanterns.png", "1024x1536",
     "a loose hand-drawn ink and watercolour sketchbook page of a Chinese shrine in a Thai old "
     "town seen head on across its brick paved forecourt: dozens and dozens of round red paper "
     "lanterns strung on wires that sweep in long curves from the top corners of the page down "
     "towards the shrine, the near lanterns big and the far ones tiny, each one just a quick red "
     "wash with a wobbly outline and a little tassel, the ones nearest the top edge cropped off; "
     "the shrine itself with a tiered red tiled roof, upturned ridge ends with dragon shapes, a "
     "carved and painted timber facade with three open doorways, thick round columns and a small "
     "sign board over the middle door; rows of tall yellow ceremonial banners standing along both "
     "sides of the forecourt; two small figures in white walking near the doors and a couple of "
     "parked motorbikes far left; a bright blue sky with a few loose cloud washes; the paved "
     "forecourt left as bare paper except for scattered dots of lantern shadow. "
     + HUMAN + ". " + NOTEXT),

    # ------------------------------------------------ street seen from a balcony, rain, monks
    ("f10_street_from_above.png", "1024x1536",
     "a hand-drawn ink and grey wash sketch looking down the length of an old Thai shophouse "
     "street from a first floor balcony after rain, steep downward view with the wet road running "
     "away to a pale empty sky: on the left tall Sino-Portuguese shophouses with stained mould "
     "streaked walls, arched openings, wrought iron balcony railings, louvre shutters and a "
     "hanging shop sign; on the right lower buildings with corrugated roofs, one with fresh "
     "terracotta tiles, air conditioning boxes and a green tarpaulin; a forest of leaning power "
     "poles and cables sagging across the whole scene drawn in fast single strokes; two monks in "
     "orange robes walking on the right footpath painted with two loose orange washes, a woman in "
     "a red shirt on the left footpath, a child in pale blue at the bottom right, one motorbike "
     "and a couple of parked cars far down the street, tiny in the distance; the wet road left "
     "almost bare with a few long reflected streaks. " + HUMAN + ". " + NOTEXT),

    # ------------------------------------------------ heritage: elephants up the old street
    ("f11_elephants_old_street.png", "1024x1536",
     "a hand-drawn sepia ink and wash sketch made to look like a drawing of a very old "
     "photograph of a Thai tin mining town street, drawn looking down the street from above: a "
     "line of about seven working elephants walking up the middle of the road towards the viewer, "
     "each with a mahout sitting on its neck and bundles of gear roped on its back, the nearest "
     "elephant big and the furthest small, drawn loosely with soft graphite shading and not quite "
     "correct anatomy; two old high sided wooden bodied lorries and a small vintage car parked "
     "further up the street; rows of two-storey shophouses down both sides with tiled roofs, "
     "wooden shutters, awnings on props and open shopfronts, people standing in the shade "
     "watching, a child running in the road; tall coconut palms and a low hill behind the far end "
     "of the street; a pale washed out sky; everything in warm sepia with faded corners like an "
     "old print, the drawing trailing off unfinished at the bottom edge. "
     + HUMAN + ". " + NOTEXT),

    # ------------------------------------------------ heritage: 1950s songthaew truck
    ("f12_songthaew_1950s.png", "1024x1536",
     "a hand-drawn graphite pencil sketch made to look like a drawing of a black and white "
     "photograph from the nineteen fifties: a row of three old wooden bodied passenger trucks "
     "parked at an angle along a Thai old town street, the nearest one a rounded nineteen forties "
     "American pickup cab with a big chrome grille, round headlamps, a wooden roof rack loaded "
     "with planks, an open sided passenger body behind, and a number plate on the front bumper; a "
     "young man in shorts standing beside the cab and another leaning out of the doorway, two men "
     "talking in the dark open shopfront behind; the shophouses above have deep wooden balconies "
     "with turned balusters, corrugated iron awnings, weathered louvre shutters and a brick end "
     "wall; further down the street more balconies recede into haze and a coconut palm leans over "
     "the roofline; a big open sky with loose cloud shading; all tone made with irregular pencil "
     "hatching and smudged graphite, no colour at all. " + HUMAN + ". " + NOTEXT),

    # ------------------------------------------------ street level, morning light, lanterns
    ("f13_street_morning.png", "1024x1536",
     "a loose hand-drawn ink and light watercolour sketch standing in the middle of an old Thai "
     "shophouse street early in the morning, one point perspective with the road running away to "
     "a small bright vanishing point: two-storey Sino-Portuguese shophouses down both sides, the "
     "left ones catching warm sunlight on their stucco pilasters, arched windows, wrought iron "
     "balcony railings and a hanging street lamp, the right ones in cool shadow with roller "
     "shutters down, wall lamps and a tangle of cables and meter boxes; one long line of small red "
     "lanterns strung across the street receding into the distance, each a single red dab; leaning "
     "power poles with a great mess of wires crossing the sky; potted plants and a blue no parking "
     "sign on the left footpath, a dark pickup and a motorbike parked on the right, a few tiny "
     "cars far away; a pale blue sky with one small cloud; the road left as bare paper with three "
     "or four long strokes and a soft shadow across it. " + HUMAN + ". " + NOTEXT),

    # ------------------------------------------------ the songthaew wall mural
    ("f14_songthaew_mural.png", "1024x1024",
     "a hand-drawn ink and watercolour sketch of a piece of street art in a Thai old town: an old "
     "local passenger truck painted life size onto a badly weathered concrete wall, the truck "
     "bright blue with a yellow painted wooden passenger body and a yellow roof rack, drawn with "
     "wobbly outlines and flat loose washes of blue and yellow that run outside the lines; the "
     "wall around it is a beautiful mess of damp stains, flaking render and black mould streaks, "
     "suggested with loose grey and ochre washes and quick scribbled hatching rather than drawn in "
     "detail; a row of small dark lamp fittings along the top of the wall and a few bare wires; a "
     "plain rough wooden bench standing on the concrete paving in front of the mural at the left, "
     "and a couple of small uplights on the ground; a branch of leaves entering the frame at the "
     "bottom right corner drawn much more roughly than the rest. " + HUMAN + ". " + NOTEXT),
]

if __name__ == "__main__":
    only = sys.argv[1:]
    for name, size, brief in JOBS:
        if only and name not in only:
            continue
        run(name, size, brief)
