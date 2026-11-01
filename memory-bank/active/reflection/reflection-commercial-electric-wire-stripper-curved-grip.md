---
task_id: commercial-electric-wire-stripper-curved-grip
date: 2026-10-31
complexity_level: 3
---

# Reflection: Curved grip for the Commercial Electric wire stripper

## Summary

A slide-on TPU 95A grip for the bare curved steel handle, with a fit test, is built from the operator's measurements. It is verified against a mock of the steel and committed as STEP and STL, standing on its open end. Whether it fits the real steel waits on the operator's test prints.

## Requirements vs Outcome

- Requirement 1 (inside follows the curve and taper from A to B): done on the mock steel. The steel never enters the bore wall, and the ribs bite exactly `RIB_BITE` at every section checked. B is placed by arc length, 83.58 along the curve for the measured 83.15 straight from A.
- Requirement 2 (snug, yet slides on by hand): designed but not yet proven: a clearance bore with light ribs. Only a print can settle it.
- Requirement 3 (glue texture): done. Eight lengthwise ribs leave `BORE_CLEAR`-deep valleys that vent glue and air.
- Requirement 4 (a new outside, shared by both grips): done. The builder takes any `steel.Handle` and assumes no curvature.
- Requirement 5 (the tool still closes): designed, and asserted at B against the measured 9 mm gap with the 5 mm limit. Not yet checked on the tool.
- Requirement 6 (open end down, no supports): done. The only flagged overhang is the roof's ridge strip, narrower than one extrusion line.
- Requirement 7 (in the catalog, with source, STL and STEP): done.
- Acceptance criteria 1 to 3 wait on prints. Criterion 4 is half met: the catalog tests pass, but at the operator's direction `publish.yaml` still has `files: []`. This is open, not met.
- Reinterpreted at build, by the operator: the ribs are glue keys, not crush ribs. Allowed by the reinterpretation: a rib may cross a hole's edge (at D2, 1.497 from the face centre line against a hole radius of 1.5). The creative doc had said the ribs stay clear of the holes. With glue keys, losing contact over 3 mm does not matter.

## Plan Accuracy

- The sequence (steel, then plot, grip, outputs, docs) held, and the file list was right apart from the operator's cuts.
- The operator removed two planned pieces at build: `tools/check_fit.py` (sections A to E) and the `publish.yaml` step. The plan had already noted the h7/h11 rule against committed tests for shapes still being prototyped, but it planned the suite anyway, arguing that it pinned requirements rather than shapes. The operator's call followed the established rule. The checks themselves held up: run ad hoc from `.scratch/`, they caught real problems.
- The challenges the plan predicted were the ones that happened. Lofts needed care: the corner radius had to shrink in the dome (preflight A6), and lofted ribs overshot. Mixing arc and chord mattered at B (preflight A4).
- Two surprises:
  - The first dome design thinned the T wall at the ends of the roof's ridge to about 1.3, against 2.2 on the body. The fix was to start the dome at the ridge's height.
  - A smooth loft of the ribs overshot to a 0.18 bite near the tip, where they fade out.

## Creative Phase Review

- **Bore fit and glue key:** the structure held: a clearance bore with tight corners and lengthwise ribs near the corners. The reasoning did not. It built a friction fit, with crush ribs, a W/T bite split and tuning by fit test, from "stays on without glue". The operator's own request had been texture for glue. Preflight then spent effort on the consequences of the friction design: a slide-on sweep, force scaling and margins at the holes. The operator dropped all of it at build.
- **Outside shape:** it held. It turned into code cleanly. The only adjustment was a corner radius of 4.8 instead of 5, so that each bore corner keeps the creative doc's own minimum of 2 mm.

## Build & QA Observations

- **What went well:**
  - The proof of concept (loft along a quartic centre line) carried straight into `grips.py`.
  - The ad hoc `verify.py` (volume intersections, shapely sections, BRep distances between face sets) caught the rib overshoot at once and confirmed each fix in numbers.
  - The rendered sections made the design easy to check by eye.
- **Iterations:**
  - `fillet2D` raised a negative-radius error in the dome.
  - The rib loft overshot.
  - The wall probe read the open-end faces, which the bore and the outside share, as a wall of 0.
  - A rendered section came out upside down.

  Each was found and fixed within one or two runs.
- **QA:**
  - Run 1 failed on documentation. `systemPatterns.md` and the README copied tunable values out of `grips.py`, against a catalog norm already recorded in root SumMem (2026-10-16) and in the h7/h11 docs.
  - Run 1 also found that `sizes()` misreported the footprint, because OpenCascade's bounding box is loose and the part leans.
  - Run 2 passed. Its three wording advisories were fixed before reflect.

## Cross-Phase Analysis

- **Creative → preflight → build:** the creative phase turned the operator's "something for glue" into a friction design. Preflight's three medium findings (A1, A2, A3) all came from that friction design, and the operator's clarification at build made them moot. If the creative phase had confirmed the new requirement it introduced (hold without glue), that analysis would not have been needed.
- **Creative → docs → QA:** the creative docs list starting values next to each decision, which suits a decision record. I then wrote the model's `systemPatterns.md` in the same style, value next to name. That copied the values into a persistent file, and QA run 1 failed on it.
- **Preflight → build:** A4 (arc against chord), A5 (`END_CLEAR`) and A6 (dome corner radius) each saved a build iteration or a wrong part. Without A4, the open end would have landed 0.43 short.

## Insights

### Technical
- In OpenCascade, a smooth loft (`makeLoft(ruled=False)`) overshoots wherever the cross-sections change quickly. A rib fading out over 1 mm bit 0.18 where 0.10 was meant. Use ruled lofts for such features. With sections 4 mm apart on a 175 mm radius, a ruled loft strays only about 0.01. (Recorded as a root SumMem note.)
- On a capped tube, start the outside's dome at the height of the inner roof's peak, not at the end of the bore. Otherwise the wall at the roof's corners thins by the dome's shrink at that height.
- CadQuery's `BoundingBox()` is about 0.3 loose on lofted B-spline faces. Measure sizes from a tessellation.
- Calipers measure chords. On a curved part, convert every "from the tip" reading to arc length before placing anything along the curve.

### Process
- For a first-print prototype in this catalog, plan ad hoc verification in `.scratch/` plus a fit test from the start. Plan committed checks only after the shape survives a print. The rule already existed in h7 and h11; arguing past it cost planning and preflight effort.
- When a creative decision adds a functional requirement the operator did not state (here, holding without glue), confirm it with the operator before building the design around it.
- Model docs name parameters and give the reasoning; they never copy values. This catalog norm was already in SumMem and was still missed. Check the model's `README.md` and `memory-bank/` for copied numbers before QA.

---

# Reflection: Rework 4 (2026-11-01, Level 2): a stronger flare, and the straight grip

## Summary

Curved grip iteration 5 (`e1b3528`) stands the open end's widest point 0.99 further out, at the same height, with its flare no steeper than print 1's. Its tool-closing guard now uses the operator's measured gap. Straight grip iteration 1 (`3046d4e`) is built from the operator's straight readings (`db5cbfd`) with the same design. QA passed. Whether both print and fit waits on the operator.

## Requirements vs Outcome

- **Flare:** met. The widest point is 0.99 further out (asked: 1.0), at z 1.50. The flare falls at most 0.42 per mm, the bevel is at least 49.9 degrees all round, and 1.08 is left with the tool shut, against at least 0.8.
    - Reinterpreted: "one millimeter out flare" was taken at the widest point, since the operator reasoned in terms of the gap.
    - Added: `FLARE_LEN` grew from 5 to 8, to keep print 1's slope. The operator did not ask for this and should judge it in hand.
- **Readings:** met. The log, both photos and `steel.py`. The one assumption, row 7 at 10 from B, is recorded.
- **Straight grip:** met as designed. Its walls and open end are identical to the curved grip's, and its bore follows its own readings: 0.34 to 0.47 wider in W than the curved grip's, 0.22 taller at B. "Match inner and outer dimensions" was read as the same design on its own steel.
- **One commit per iteration:** met, with three commits.
- **`publish.yaml`:** unchanged.

## Plan Accuracy

- **Preflight run 1** found two real flaws:
    - B3 could not pass, because `FLARE_LEN` moves every section of the body loft;
    - the gap guard modelled the wrong pair of grips.

  Fixing the second reordered the plan (straight steel first) and split the work into three commits. After that the plan held.
- **Surprises:**
    - `shapely.polygonize` cannot close rings from raw mesh-plane segments;
    - a 9 µm extra rib bite where the straight T profile kinks between loft sections;
    - "leaning" in the size report.

## Build & QA Observations

- The regression guards made the `Handle` change safe to do quickly: the curved report diff, a pixel diff of the plot, and byte-identical STLs across every rebuild.
- QA found one wrong sentence (A-25), fixed. Its checks reproduced every figure.
- One process slip: `tail` on a red run's output. The green runs were read whole.

## Insights

### Technical
- **A measurement taken on a stand-in must be translated to the part that ships.** The 3.3 gap was measured with a curved grip on the straight steel. Walls measured from the steel do not carry across when the two steels differ, so the guard needed the W difference at B. Preflight caught it, not the plan.
- **Moving one end of a smooth loft's section range moves every section,** so "unchanged elsewhere" checks need a geometric tolerance, not equality.
- **trimesh's welded `section().to_2D(to_2D=identity)` is the reliable way to get slice polygons for comparison.** Raw `mesh_plane` segments do not share exact endpoints.

### Process
- **Typing hand-written readings back in chat before building** settled three questions in one round trip: the paper edge is B, the holes' datum, and where J to L sit. Do it for every measurement sheet.

### Million-Dollar Question

The open end would be set in the operator's own terms: the widest point's reach and height, plus the flare's slope. `FLARE` and `BEVEL` would be derived from those by a solver, which today lives in the scratch `flare_solve.py`. The tool-closing guard would then be a direct limit on that reach. "A bit more flare" becomes one number, and the next print's change is exactly what the operator asked for. Preflight run 2 proposed this. It was not taken here, because the operator had already named the change and the current parameters deliver it, but it is the natural next refactor if the open end is retuned again.
