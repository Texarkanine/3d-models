# Progress

Design and publish-ready a slide-on TPU 95A grip for the curved handle of a Commercial Electric wire stripper. It lives in a new catalog model, `models/commercial-electric-wire-stripper-grips/`, whose outside design the straight grip will share later.

**Complexity:** Level 2

The first cycle (2026-10-31) was Level 3. Reworks 1 to 3 (2026-11-01) were Level 1. Rework 4 (2026-11-01) is Level 2.

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

## 2026-11-01 - REWORK - INITIATED (second rework)

* Work completed
    - A second rework was opened on the operator's second test print. The previous cycle was Level 1, and the first was Level 3.
* Decisions made
    - The operator's feedback, with a photo of print 1, print 2 and the stock grip: "I actually really liked the kind of flute that you had going on. We only want to bevel the side that's down towards the bed. We want to keep the more gradual fluting that was on the top side where your hands would connect... if we can combine those so we can print one that's going to look more like the stock one with a flute on the actual grip but then the little bevel on the top so it's not sharp, that would be ideal." Also: commit each iteration, so that old ones can be looked at again.
    - The operator will cut the old straight grip off and measure the steel once this print is done.
* Insights
    - Print 2's lip fixed the sharp edge, but it gave up print 1's gradual flare. The flare is what the hand meets, and the operator prefers it. Print 1 is commit `95e5f61`, print 2 is `da750d8`.

## 2026-11-01 - COMPLEXITY-ANALYSIS - COMPLETE (second rework)

* Decisions made
    - Level 1. One element changes: the outline of the open end in `grips.py`. Print 1's flare comes back, and its edge on the bed is rounded with a printable bevel.

## 2026-11-01 - BUILD - COMPLETE (second rework)

* Work completed
    - The flare is restored. Its bed edge is rounded by `RIM_R` over a bevel at `RIM_ANGLE` (`grips.rim_profile`). The outputs were regenerated, and the model's `systemPatterns.md` and `techContext.md` updated.
    - The slice check now also requires a flute (a gradual fall above the widest point). Both earlier prints' STLs fail it, each on the flaw the operator named; the new STL passes. `verify.py`, `tools/overhang.py` and the catalog suite (88 OK) show no regressions.
* Decisions made
    - The round touches both the bed's plane and the flare, so above it the flare is exactly print 1's. `RIM_R` is small, so the widest point drops from print 1's `FLARE` only by what the round trims.
    - `RIM_STEP` was halved after the first build, because the flare's ruled steps left creases on the surface the hand meets.
* Insights
    - The operator's word "flute" means the flare, not the bead.

## 2026-11-01 - QA - COMPLETE (PASS) (second rework)

* Work completed
    - Semantic review of commit `c585867` against the rework 2 brief.
    - Independent checks:
        - a scratch rebuild gives byte-identical STLs, and the STEP files differ only in their header;
        - `lip.py` fails on print 1's and print 2's STLs, each for the flaw the operator named, and passes on both new STLs;
        - `rim_profile()` is tangent where it should be and never flatter than `RIM_ANGLE`, at the defaults and over a parameter sweep;
        - the rim matches its profile to 0.0000, and the body is within 0.019 of design;
        - `verify.py` reproduces the build's numbers;
        - overhangs are unchanged;
        - catalog suite 88 OK.
* Decisions made
    - PASS. All five rework 2 requirements are met. Advisories A-15 to A-18 are in `tasks.md`; none blocks.
* Insights
    - Print 1's smooth loft through four sections did not follow its own quadratic flare: its STL sat up to 0.045 outside it. The new ruled loft follows `flare()` exactly, so "print 1's flare" now means print 1's design, not its STL. The two differ by far less than a line width.

## 2026-11-01 - WRAP-UP - COMPLETE (second rework)

* Work completed
    - Fixed QA advisories A-15 to A-18. The STLs are byte-identical to `c585867`.
    - Root persistent files: skip. Only this model's outside changed, and no catalog contract changed.
* Decisions made
    - Iteration 3 closes unprinted. The operator, looking at the model, asked for more bevel ("only three or four layers... bring it in a little bit more"). That is rework 3.

## 2026-11-01 - REWORK - INITIATED (third rework)

* Work completed
    - A third rework was opened, on the operator's review of iteration 3 in CAD, before it was printed. The previous cycle was Level 1.
* Decisions made
    - The operator's feedback: "a little bit more of a bevel on the top. We basically only have three or four layers of bevel. I think we can do a little bit more... bring it in a little bit more maybe."

## 2026-11-01 - COMPLEXITY-ANALYSIS - COMPLETE (third rework)

* Decisions made
    - Level 1. One element changes: the bevel in `grips.rim_profile`. It becomes its own parameter, how far the bed edge comes in, rather than a by-product of the round's radius.

## 2026-11-01 - BUILD - COMPLETE (third rework)

* Work completed
    - `BEVEL` (how far the bed edge comes in), `BEVEL_ANGLE` and a round `RIM_R` touching the bevel and the flare. Outputs regenerated, model docs updated.
    - `lip.py` now requires 6 layers to the widest point and an edge 0.8 in from it. Iteration 3 fails both; the new STL passes. `verify.py`, `tools/overhang.py` and the catalog suite (88 OK) show no regressions beyond the intended thinner first layer.
* Decisions made
    - `BEVEL` 1.5 with `RIM_R` 0.8. That gives about twice iteration 3's layers, which is what the operator asked for: "a little bit more... bring it in a little bit more". The edge sits 0.5 inside the body wall.
    - The first layer keeps three extrusion lines over the bore's corners; this is asserted.
* Insights
    - The footprint is down to 128 mm². The operator should consider a brim.
    - Iteration 3 is this construction with a smaller `BEVEL`, so the bevel can be tuned with one number from here on.

## 2026-11-01 - QA - COMPLETE (FAIL, fixable) (third rework)

* Work completed
    - Semantic review of commit `efac921` against the rework 3 brief.
    - Independent checks:
        - a scratch rebuild gives byte-identical STLs, and the STEP files differ only in their header;
        - `lip.py` fails on iteration 3's STL and passes on the new one;
        - `rim_profile()` is valid for every accepted parameter set, and its "d rises strictly" guard catches every round that cannot touch the bevel (9,225 sets);
        - `verify.py` reproduces the build's numbers;
        - overhangs are unchanged by `tools/overhang.py`;
        - catalog suite 88 OK.
* Decisions made
    - FAIL (fixable). Build must rerun for Q3: at the four corners the bevel is 43.4 degrees, not `BEVEL_ANGLE`'s 50, which is under the design's 45 degree rule. `check_design` passes, and `systemPatterns.md` claims the rule holds.
    - Advisories A-19 to A-21 are in `tasks.md`; none blocks.
* Insights
    - `outside()`'s corner rule `CORNER_R + max(grow, 0)` was written for the dome. Once the rim goes inside the body wall, the corners move in about 1.41 times as far as the flats, so the bevel there is flatter than its profile. A check of the T extent alone, or of the W and T sides, cannot see it; scan face normals around the whole part.

## 2026-11-01 - BUILD - COMPLETE (third rework, Q3 fix)

* Work completed
    - Fixed QA's Q3. The open end's sections are now a true offset (corner radius `CORNER_R + grow`), so the bevel keeps `BEVEL_ANGLE` at the corners as well. `corner_wall` matches.
    - The all-round normal scan failed on `efac921` (43.4 degrees) and passes now (49.9 degrees at the least). The other checks are unchanged; catalog suite 88 OK.
* Insights
    - The corner rule was written for the dome, where grow is only negative. It became wrong as soon as another feature took grow below zero. A shape rule that sits in a shared helper (`sec`) needs to state what it is for.

## 2026-11-01 - QA - COMPLETE (PASS) (third rework, run 2)

* Work completed
    - Semantic review of commit `87e777c` (the fix for Q3) against QA run 1's findings and the rework 3 brief.
    - Independent checks:
        - a scratch rebuild gives byte-identical STLs, and the STEP files differ only in their header;
        - the all-round normal scan passes at 49.9 degrees at the least (`efac921` failed at 43.4);
        - a separate slice-offset check shows the bevel steps out evenly all round;
        - slices above z 0.95 are identical to `efac921`;
        - a sweep of 4,846 accepted parameter sets keeps the rim a true offset;
        - `lip.py`, `verify.py` and `tools/overhang.py` reproduce the build's numbers;
        - catalog suite 88 OK.
* Decisions made
    - PASS. Q3 is resolved, and all four rework 3 requirements are met.
    - A-19 to A-21 still stand. New advisories A-22 to A-24 (two doc wordings and an optional docstring note) are in `tasks.md`; none blocks.
    - Iteration 4 is commit `87e777c`.
* Insights
    - A true offset of a rounded rectangle needs no separate assertion at the corners: as long as the corner radius stays positive and `rrect`'s cap does not apply, the corners follow the flats' profile exactly. Then `BEVEL_ANGLE >= 45` guards the whole outline.

## 2026-11-01 - WRAP-UP - COMPLETE (third rework)

* Work completed
    - QA run 2 passed on `87e777c`. Advisories A-19 to A-23 are handled; A-24 (optional) is not taken. Iteration 4's commit is recorded in the model's SumMem.
    - Root persistent files: skip. Only this model's outside changed, and no catalog contract changed.
* Decisions made
    - Iteration 4 (`87e777c`) is ready to print. Next: the operator prints it, cuts off the old straight grip, and measures the straight steel. Then `/niko-archive`, or another rework.

## 2026-11-01 - REWORK - INITIATED (fourth rework)

* Work completed
    - A fourth rework was opened on the operator's print of iteration 4 and their readings of the bare straight steel. The previous cycle was Level 1.
    - The straight readings were typed back in chat and confirmed by the operator against the paper.
* Decisions made
    - The operator's feedback: iteration 4 fits. "The hand feel of the most recent iteration, I would like a bit more of a flare out." With the tool shut and a curved grip on each handle, the open ends are about 3.3 apart. "Each one could do 1.5, but that'd be pushing it, so let's actually go one millimeter out flare on each side, not just one half."
    - The straight grip: "we technically don't need to make the straight one, but we're going to make it anyway for completeness' sake." It "should match inner and outer dimensions the same as the other side." A curved grip already slides onto the straight handle and works.

## 2026-11-01 - COMPLEXITY-ANALYSIS - COMPLETE (fourth rework)

* Decisions made
    - Level 2: a self-contained enhancement of this one model. The straight grip reuses the builder, which was written for any `steel.Handle`; it needs a second handle in `steel.py`, a `Handle` that takes W and T at different places, and a second set of outputs. The flare change retunes three parameters and replaces the tool-closing limit with the measured gap. No design question needs a creative phase.

## 2026-11-01 - PLAN - COMPLETE (fourth rework)

* Work completed
    - Plan in `tasks.md`: six steps, B1 to B9 checked ad hoc.
* Decisions made
    - The flare is measured at the widest point, since the operator reasoned in terms of the gap. `FLARE_LEN` goes from 5 to 8, so that the flare stays as steep as print 1's (0.42 per mm against 0.4), rather than twice as steep. `FLARE` 2.3 and `BEVEL` 1.8 keep iteration 4's bevel height and its bed edge, 0.97 in from the widest point.
    - The 5 mm limit (`CONVEX_LIMIT`) gives way to the measured 3.3 gap between two iteration-4 grips, with at least `MIN_SHUT_GAP` left.
    - The straight W is a least-squares line through the tracing, which reads to 0.5. T comes from the calipers at A, J, K, L and M.

## 2026-11-01 - PREFLIGHT - COMPLETE (fourth rework)

* Work completed
    - Checked the plan against the codebase: the TDD encoding, conventions, dependencies, conflicts and completeness. Probes in the session scratchpad built iteration 5 and the straight grip from the plan's values; both build, and pass `lip.py`, `corner_bevel.py` and `tools/overhang.py`. Catalog suite 88 OK.
    - First line of `.preflight-status`: `FAIL (fixable)`. No plan edits.
* Decisions made
    - F1, a required fix: B3 (curved slices above the flare within 0.001 mm² of iteration 4's) cannot pass. Raising `FLARE_LEN` moves every body loft section, so the outside moves by up to 0.07 mm. The re-plan must give B3 a geometric tolerance and drop the claim that only the flare changes.
    - Advisories A1 to A8 and the radical idea (a flare sampler plate) are in `.preflight-status`. The most important: the shut gap for the shipped pair (curved + straight) is about 1.1, not 1.3, because the straight steel is 0.47 wider at B (A1). Four caliper W readings on the straight steel would settle that steel's biggest unknown (A3).
* Insights
    - The body loft's section positions depend on `FLARE_LEN`, so any change to the flare's length moves the whole outside by a few hundredths. A check of "unchanged" geometry needs a tolerance, not equality.
    - The 3.3 gap was measured with a curved grip on the straight handle. A gap model that uses walls measured from the steel must account for the steel each grip sits on.

## 2026-11-01 - PLAN - COMPLETE (fourth rework, revised after preflight run 1)

* Work completed
    - Fixed F1: B3 now allows the outside 0.1 of movement above the flare; the bore stays identical.
    - Folded in A1 to A8 (see "Preflight (run 1)" in `tasks.md`).
    - Saved the operator's two photos to `.scratch/` (A4).
* Decisions made
    - Reordered: the straight handle comes first, then curved iteration 5, then the straight grip, as three commits. `shut_gap()` needs both handles' W at B.
    - The gap guard models the pair that ships, about 1.1 left. `MIN_SHUT_GAP` is 0.8.
    - A3: build the straight bore from the traced W now. Recommend the fit test first, and offer caliper widths if it is loose.
    - The flare sampler is not taken; it can be offered later.

## 2026-11-01 - PREFLIGHT - COMPLETE (fourth rework, run 2)

* Work completed
    - Checked the revised plan against the codebase: the TDD encoding, conventions, dependencies, conflicts and completeness. A probe built iteration 5 and applied the restated B3: the bore's symmetric difference is at most 0.00029 mm², and the outside above the flare moves at most 0.075. `lip.py` and `corner_bevel.py` pass. B2's figures are 1.080, 3.063 and 0.063. Catalog suite 88 OK.
    - First line of `.preflight-status`: `PASS WITH ADVISORY`. No plan edits.
* Decisions made
    - Run 1's F1 is resolved. Advisories A1 to A6 and the radical idea are in `.preflight-status`. The most useful: iteration 5's commit should also update the `CONVEX_LIMIT` bullet in `systemPatterns.md` and the "wall at the open end" assertion in `techContext.md` (A1), and `SHUT_WALL` is 4.274 (A4).
* Insights
    - The restated B3 has real margin: 0.075 against 0.1 on the outside, and 0.0003 against 0.001 on the bore.
    - During the 3.3 reading, the curved grip on the straight handle sat about 0.4 short of the straight B, because its bore is shorter than the straight A to B. The shipped straight grip sits at B. The effect on the gap was not measured, and is likely under 0.1.

## 2026-11-01 - BUILD - COMPLETE (fourth rework)

* Work completed
    - Six steps, in three commits:
        - `db5cbfd`: the straight readings in `steel.py`, the log and the photos;
        - `e1b3528`: curved grip iteration 5;
        - `3046d4e`: straight grip iteration 1, with the docs.
    - Each check ran red before its code: `straight_check.py`, `lip.py`, `shut_gap.py` and `verify.py straight`. The regression guards were shown able to fail: `slice_compare.py` fails on a 0.2 shift.
    - All green on the committed outputs. Catalog suite 88 OK.
* Decisions made
    - Curved iteration 5: widest 1.464, against iteration 4's 0.473, at z 1.50; the flare falls at most 0.42 per mm; the bevel is at least 49.9 degrees all round; the footprint is 197 mm² (it was 132).
    - The gap with the tool shut is modelled for the shipped pair: 1.08, with at least 0.8 asserted. The operator's "pushing it" case gives 0.08 and is refused.
    - Straight grip: its open end and walls are identical to the curved grip's. Its bore is 0.34 wider at A and 0.47 wider at B, from the traced W, and 0.22 taller at B, from the calipers.
* Insights
    - Raw `mesh_plane` segments do not share exact endpoints, so `shapely.polygonize` finds no rings. trimesh's `section().to_2D(to_2D=identity)` welds them and keeps the mesh's own x and y.
    - A loft samples its sections every `SECTION_STEP`, so a kink in a readings profile between samples is cut across. Here the straight T rises steeply from A to J, which adds a 9 µm rib bite at J. That is harmless, but worth knowing before readings get denser.
