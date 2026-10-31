# Progress

Design and publish-ready a slide-on TPU 95A grip for the curved handle of a Commercial Electric wire stripper. It lives in a new catalog model, `models/commercial-electric-wire-stripper-grips/`, whose outside design the straight grip will share later.

**Complexity:** Level 3

## 2026-10-31 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Guided the operator's measurements (annotated photo guide), then reduced the curve offsets and cross-checked them against the calipers.
    - Set up the model directory: release-please config and manifest at 0.0.0, catalog test entry, `AGENTS.md`, memory bank, draft `publish.yaml`, SumMem store, `reference/` and `tools/`.
* Decisions made
    - Level 3.
    - Curved grip first. The straight grip is a later task.
    - Model directory `commercial-electric-wire-stripper-grips`: brand plus tool, as the bulb models name what they fit. It can be renamed cheaply before the first release.
* Insights
    - The tracing's widths match the calipers to within 0.5 mm, and its length from A to B is within 0.7 mm of the measured 83.15. Take the shape from the tracing and the sizes from the calipers.
    - The old grip reached past hole D1. The end of the residue on the steel was not B.

## 2026-10-31 - CREATIVE (bore fit and glue key) - COMPLETE

* Work completed
    - Compared a plain interference bore, longitudinal crush ribs, circumferential rings, and a clearance bore with glue.
* Decisions made
    - Longitudinal crush ribs on a clearance bore whose corners clear the steel. Two ribs per face sit near the corners, clear of the holes and the insert. The valleys carry glue and let air out. W bites harder than T. The fit test tunes `BORE_CLEAR` and the bites.
* Insights
    - The steel's W taper keeps the W ribs from biting until the last few millimetres. T barely tapers, so T contact rubs the whole way and must stay light.

## 2026-10-31 - CREATIVE (outside shape) - COMPLETE

* Work completed
    - Compared a steel-offset rounded rectangle, an oval, and a sculpted outside.
* Decisions made
    - Steel-offset rounded rectangle. Walls are set from the steel face (3.8 in the plane of the handles, 2.5 across it, corner radius 5), with a 1.0 flare at the open end and a lofted dome at the closed end. The same definition will wrap the straight steel.
* Insights
    - An ellipse around a rectangular steel needs too much wall to clear the corners, and breaks the 5 mm convex limit at B.
    - The closing gap was measured only at B. Constant walls keep the closest approach at B, so no shape rests on a gap nobody measured.

## 2026-10-31 - PLAN - COMPLETE

* Work completed
    - Component analysis, test plan (check_fit sections A to E plus the catalog record test), 7-step implementation plan, challenges and pre-mortem.
    - Technology validation: a CadQuery loft of rounded-rectangle sections along a quartic centre line, with a lofted ribbed bore. Result: a valid single solid in 2.7 s, a watertight STL, standing on z = 0.
* Decisions made
    - `steel.py` (pure Python) holds the measured steel as a `Handle`. `grips.py` builds from any `Handle`, so the straight grip reuses it. `reduce_curve.py` is folded into `steel.py` and check_fit section A.
    - The centre line is a quartic least-squares fit (worst residual 0.08 mm). A is placed so the chord from A to B is the measured 83.15.
    - The bore's closed end is a gable computed from the tip's lean, so both faces are at least 45 degrees in print.
    - Ship a fit test: the grip's first `FIT_LEN` mm.
* Insights
    - The grip is symmetric in both W and T, so a mirrored tracing cannot matter.
    - The fit test proves only the open end. The full grip is the test of the curve.
