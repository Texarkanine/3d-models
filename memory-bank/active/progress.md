# Progress

Design and publish-ready a slide-on TPU 95A grip for the curved handle of a Commercial Electric wire stripper. It lives in a new catalog model, `models/commercial-electric-wire-stripper-grips/`, whose outside design the straight grip will share later.

**Complexity:** Level 1

The first cycle (2026-10-31) was Level 3. The 2026-11-01 rework is Level 1.

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

## 2026-10-31 - PREFLIGHT - COMPLETE

* Work completed
    - Checked the plan against the codebase: TDD encoding, conventions, dependencies, conflicts and completeness. Ran two numeric probes outside the repository: a slide-on sweep and arc against chord placement.
    - First line of `.preflight-status`: `PASS WITH ADVISORY`. No plan edits.
* Decisions made
    - The plan is acceptable as it stands. The 12 advisories and the radical idea are listed in `.preflight-status` for the operator to weigh before `/niko-build`.
* Insights
    - The bore cannot slide along the steel as a rigid copy, because the curve is not uniform (radius about 175 mm in the middle, nearly straight at both ends). With the grip settled in its best pose, the W ribs rub over about the last 27 mm of travel, never harder than when seated, and the bore walls never touch the steel.
    - The ribs bite along the whole grip, so the full grip needs about 83/FIT_LEN times the fit test's force to seat and hold. A fit test that feels tight predicts a grip that will not go on by hand.
    - At D2 the rib tip clears the hole by only about 0.08 mm on the mock, which is less than the uncertainty in W there. The creative doc's claim that the ribs clear the hole "even at W 6.3" is wrong.

## 2026-10-31 - BUILD - COMPLETE

* Work completed
    - `steel.py` (the measured steel as a `Handle`), `grips.py` (bore, gable roof, glue-key ribs, flared and domed outside, print transform, fit test), `README.md`, and `tools/overhang.py`. `plot_curve.py` now draws from `steel.py`; `reduce_curve.py` is gone.
    - Outputs: `curved_grip` and `curved_grip_fit_test`, as STEP and STL, standing on the open end. Grip: 92.6 tall, 19.3 × 21.3 at the open end, 14.9 cm³.
    - Ad hoc verification in `.scratch/wirestripper-grip/` (`verify.py`, `render.py`): every check passes; details in `activeContext.md`.
* Decisions made
    - Operator direction at build: no `publish.yaml` changes, the ribs are glue keys, and no committed tests while the shape is prototyped. Plan step 5 and `check_fit.py` were dropped.
    - Readings from A are chords, converted to arc length. The open end is at s = 83.58.
    - One light rib bite (0.1). `CORNER_R` is 4.8, keeping 2 mm over each bore corner. `END_CLEAR` is 1.0, `FIT_LEN` 15.
    - The bore's gable roof is computed in print orientation. The dome starts at the ridge's height.
* Insights
    - CadQuery's smooth loft overshoots where a section changes quickly: a rib fading out over 1 mm bit 0.18 instead of 0.10. Ruled lofts follow the sections exactly, and with sections 4 mm apart on a 175 mm radius they stray only about 0.01.
    - If the dome starts at the bore's end, the T wall at the roof's ridge thins to about 1.3. Starting it at the ridge's height keeps the body's 2.2.
    - W at B is the biggest unknown: 9.7 from the calipers against 10.25 from the tracing. The fit test will show which is right.

## 2026-10-31 - QA - COMPLETE (FAIL, fixable)

* Work completed
    - Semantic review of the build against the plan, the creative docs and the operator's build-time direction.
    - Independent checks:
        - both STLs rebuild byte for byte, and the STEP files differ only in their header;
        - the curve PNG is reproducible;
        - catalog suite 88 OK;
        - overhang: only the ridge strip on the grip, nothing on the fit test;
        - `verify.py` reproduces every number in `activeContext.md`;
        - the fit-test STL matches the grip STL cut at 15 mm to within 0.07 %.
* Decisions made
    - FAIL (fixable), documentation only. Build must rerun:
        - Q1: the README copies `FIT_LEN`;
        - Q2: the model's `systemPatterns.md` copies about 17 tunable `grips.py` values, against the plan's one-home invariant and the h7/h11 rule.
    - Geometry, maths and print orientation are accepted as they are. Six non-blocking advisories are in `tasks.md`, among them the misleading "footprint" in `sizes()` and the `stations` naming overload.
* Insights
    - The operator has said these values will be tuned after each test print. Copies of them in prose go stale at the first retune, which is why the one-home rule exists.

## 2026-10-31 - BUILD (QA rework) - COMPLETE

* Work completed
    - Q1: the README describes the fit test as "the open end alone", without its length.
    - Q2: `systemPatterns.md` rewritten so that each fact has one home. It names parameters and keeps the reasoning, the measured limits (the 9 mm gap, the 5 mm wall at B) and the assertion thresholds. The values stay in `grips.py`, and the readings in `steel.py`.
    - A-1: `sizes()` measures the tessellated part, not the loose bounding box. It reports the height as 92.3 and labels the leaning part's span as a span, not a footprint.
    - A-2: `grips.stations()` renamed `loft_positions()`. A-6: the docstring says the valleys are `BORE_CLEAR` deep. The scratch `verify.py` run line now lists every package it needs.
    - Rebuild: STLs byte-identical, STEP header-only changes restored; catalog suite 88 OK.
* Decisions made
    - A-3 (keep `steel_solid`) and A-5 (`publish.yaml` files stay open) unchanged, per QA and the operator. A-4 (ribs may cross a hole's edge) goes to the reflection.
* Insights
    - CadQuery's `BoundingBox()` on lofted B-spline faces is loose by about 0.3 mm. Measure sizes from a tessellation.

## 2026-10-31 - QA (run 2) - COMPLETE (PASS)

* Work completed
    - Reviewed the build rework against the run 1 findings, then rechecked the whole model.
    - Independent checks:
        - a scratch rebuild gives byte-identical STLs, and the STEP files differ only in their header;
        - `sizes()` reports 92.3 tall, which matches the mesh;
        - catalog suite 88 OK;
        - overhang: only the ridge strip on the grip, nothing on the fit test;
        - `verify.py` runs with its new run line and reproduces every number in `activeContext.md`;
        - no tunable value is copied into the README or the model's memory bank;
        - the reference images carry no metadata.
* Decisions made
    - PASS. Q1, Q2, A-1, A-2 and A-6 are resolved, and A-3 is accepted. A-4 and A-5 go to reflect and archive.
    - Three new non-blocking advisories are in `tasks.md`:
        - A-7: the `steel.py` docstring says it holds all "the numbers the model uses";
        - A-8: `systemPatterns.md` says `RIDGE_W` "is narrower than one extrusion line", which is true only for its current value;
        - A-9: one docstring line is longer than the others.
* Insights
    - The split now matches h7 and h11. Readings live in `steel.py`, design values in `grips.py`, and the reasoning in `systemPatterns.md`. A retune after a test print changes one file.

## 2026-10-31 - REFLECT - COMPLETE

* Work completed
    - Reflection written. QA run 2's wording advisories (A-7 to A-9) fixed. Root persistent files reconciled: no change needed.
* Decisions made
    - Acceptance criterion 4 (`publish.yaml` names its files) stays open at the operator's direction. Criteria 1 to 3 wait on test prints.
* Insights
    - The creative phase turned "texture for glue" into a friction fit, and preflight analysed that fit in depth; the operator reframed the ribs as glue keys at build. Confirm with the operator any requirement a creative decision adds.
    - In this catalog, first-print prototypes get ad hoc checks in `.scratch/` and a fit test. Committed checks wait until a shape survives a print.

## 2026-11-01 - REWORK - INITIATED

* Work completed
    - Rework opened on the operator's first test print. The completed cycle was Level 3.
* Decisions made
    - The operator's feedback: "it's basically perfect. Except, the part that prints on the bed, since it just angles up with no bevel, makes a pretty 'sharp' edge. Can we get a little 'bulge' out from the contact with the bed, then back in, so there's a rounded edge at the top? And also, if you want to make the straight one, it oughta work. Fits like a glove, doesn't even need adhesive!"
    - The straight grip stays a later task: its steel is still unmeasured (`reference/measurements.md`).
* Insights
    - First print: the bore fits the steel from A to B and the grip holds dry, with no glue. Acceptance criterion 1 is met. The flare made the open end's outer edge acute where it met the bed.

## 2026-11-01 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Classified the rework.
* Decisions made
    - Level 1. It fixes one defect found in a print, the sharp edge at the open end. The fix is confined to the outside's open end in `grips.py`; the bore, ribs and dome are unchanged.

## 2026-11-01 - BUILD - COMPLETE

* Work completed
    - A rounded lip replaces the flare at the open end. The outputs were regenerated, and the model's `systemPatterns.md` and `techContext.md` updated.
    - An ad hoc check, `.scratch/wirestripper-grip/lip.py`, reproduced the defect first (71 degrees, widest on the bed). It passes after the fix (130 degrees, crown 1.75 up, back on the body by about 4). The first cycle's `verify.py` and `tools/overhang.py` show no regressions. Catalog suite: 88 OK.
* Decisions made
    - The lip starts flush with the body wall on the bed and stands `LIP` out at the crown. Its maximum matches the old flare's, so the wall facing the other handle stays where `CONVEX_LIMIT` allowed it.
    - The lip is a separate ruled loft fused to the body's smooth loft.
* Insights
    - The old flare had also left the smooth body loft 0.02 to 0.03 over its wall for several millimetres past the flare. Taking the lip out of the smooth loft brought that back to 0.000.
    - The footprint on the bed drops from 231 to 164 mm². The operator should watch bed adhesion on the 92 mm tall print.

## 2026-11-01 - QA - COMPLETE (PASS)

* Work completed
    - Semantic review of the rework against the rework brief and the operator's direction.
    - Independent checks:
        - a scratch rebuild gives byte-identical STLs, and the STEP files differ only in their header;
        - `lip.py` fails on the pre-fix STL and passes on both new STLs;
        - a separate slice check matches `lip_profile()` to within 0.01 on all four sides and both diagonals;
        - `verify.py` reproduces the build's numbers;
        - the body walls are within 0.012 of design;
        - overhangs are unchanged;
        - catalog suite 88 OK.
* Decisions made
    - PASS. All four rework requirements are met. Advisories A-10 to A-14 are in `tasks.md`; none blocks.
* Insights
    - On a leaning part, horizontal STL slices exaggerate small differences. Old and new differ by up to 0.1 locally above the lip, while cross-sections square to the centre line put both builds within 0.015 of design. Check walls square to the centre line.

## 2026-11-01 - WRAP-UP - COMPLETE

* Work completed
    - Fixed QA advisories A-10 to A-13: doc wording, the comment on `d1`, `LIP_STEP` moved, and a new `LIP_ANGLE >= 45` assertion. A-14 (the footprint) is passed to the operator.
    - The rebuild is byte-identical in both STLs.
    - Root persistent files: skip. The rework changed only this model's outside; no catalog contract changed.
* Decisions made
    - Level 1 rework complete. Next is the operator's print of the lipped grip, then `/niko-archive` for the whole task.
