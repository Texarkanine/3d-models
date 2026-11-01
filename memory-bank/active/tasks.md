# Task: commercial-electric-wire-stripper-curved-grip (rework 4: a stronger flare, and the straight grip)

* Task ID: commercial-electric-wire-stripper-curved-grip
* Complexity: Level 2
* Type: simple enhancement (rework 4)

Three commits, so that each iteration can be looked up on its own (projectbrief "Rework 4"): the straight readings, then curved grip iteration 5, then straight grip iteration 1.

1. **Curved grip, iteration 5:** the open end's widest point stands 1.0 further out than iteration 4's (0.47 past the body wall; the settings below give 0.99 more, which the report states). The bevel on the bed keeps iteration 4's look: the same height to the widest point (about 7 layers) and the bed edge about 0.97 in from the widest. The flare above it stays a flute: its steepest fall stays at most 0.5 per mm, as with print 1's flare, which the operator liked. The tool-closing limit `CONVEX_LIMIT` (5 mm, inferred from the old grip) gives way to the operator's direct measurement: with the tool shut, the open ends of two iteration-4 grips are 3.3 apart. A guard keeps at least `MIN_SHUT_GAP` between the two grips. The operator called 1.5 more each "pushing it" (0.3 left); 1.0 more each leaves about 1.3 between two curved grips. The pair that ships leaves about 1.1 (preflight A1): the 3.3 was measured with a curved grip stretched onto the straight steel, which models 0.47 wider at B, and the straight grip is built for that steel.
2. **Straight grip, iteration 1:** record the straight readings, model the straight handle in `steel.py`, and build `straight_grip` and its fit test with the same design. The builder already takes any `steel.Handle`.

Flare settings found in `.scratch/wirestripper-grip/flare_solve.py` (iteration 4: widest 0.474 at 1.459 above the bed, falling 0.24 per mm above it):

| `FLARE_LEN` | `FLARE` | `BEVEL` | widest | falls, per mm | bed edge |
|---|---|---|---|---|---|
| 5.0 (as now) | 3.55 | 3.07 | 1.473 at 1.46 | 0.82 | +0.48 |
| 7.0 | 2.55 | 2.08 | 1.471 at 1.46 | 0.51 | +0.47 |
| **8.0 (chosen)** | **2.3** | **1.8** | about 1.46 at 1.46 | 0.42 | +0.49 |

Keeping `FLARE_LEN` at 5 would double the flare's steepness (0.82 per mm), which is closer to a ridge than to the flute the operator asked to keep. At 8 the flare is as steep as print 1's (0.4 per mm), and stands out three times as far. On the bed, the first-layer wall over the bore corners rises from 1.55 to about 2.55, which also enlarges the footprint (iteration 4: 132 mm²).

Straight readings (operator, 2026-11-01, confirmed in chat):
- **Tracing, tip up:** two lines 30 apart, rows 10 apart, rows 0 to 7. The paper edge is B, where the old grip stopped. It is assumed to be 10 below row 7 (the photo shows 10.2), so row k is 85.14 − 10·(8 − k) from A.
- **Offsets:** left 11.5, 11.5, 11, 11, 10.5, 10.5, 10.5, 10; right 11.5, 11.5, 11, 11, 11, 10.5, 10.5, 10. W (30 − left − right) is 7, 7, 8, 8, 8.5, 9, 9, 10.
- **T, by calipers:** 13.9 at A; J 14.02 at row 0; K 14.09 at row 3; L 14.25 at row 5; M 14.53 at B.
- **A to B:** 85.14.
- **Holes:** two holes of 3 mm, measured from the tip to each hole's near edge: 6.32 and 76.75. Their centres are 7.82 and 78.25 from A.
- **Old straight grip's opening, inside:** 10.12 × 14.6.
- **Tool shut:** the open ends of the two grips are about 3.3 apart, with an iteration-4 curved grip on each handle.

## Test Plan (TDD)

The operator's standing direction (build of 2026-10-31, `techContext.md`): no committed tests while the shapes are prototyped. Checks are ad hoc scripts in `.scratch/wirestripper-grip/` (gitignored). A check is written or tightened first and run red on the current state, then the code makes it green. The catalog suite guards the repository.

### Behaviors to Verify

- **B1. Stronger flare (curved).** `lip.py curved` on the new STL must pass:
    - the widest point at least iteration 4's + 0.95 (≥ 1.42) past the body wall;
    - the widest point at least 1.2 above the bed;
    - the bed edge at least 0.8 in from the widest point, at an angle over 100 degrees inside the part;
    - above the widest point, a fall of at most 0.5 per mm;
    - back on the body by the end of the profile, with no step.

    Iteration 4's STL (`87e777c`) fails the first condition.
- **B2. The tool still closes.** `grips.shut_gap()` returns `SHUT_GAP − 2 × (WALL_SIDE + widest − SHUT_WALL) − max(0, (STRAIGHT W at B − CURVED W at B) / 2)`. The last term: the measured curved grip sat stretched on the straight steel with its bore built for the curved W, and its wall moves out by at most half the difference. The straight grip's wall sits a full half-difference out. `check_design` asserts the gap is at least `MIN_SHUT_GAP` = 0.8. That value lies between the operator's "pushing it" (0.3) and their choice (about 1.3, or 1.1 for the shipped pair), with room for the "about" in the 3.3 reading.
    - New settings: about 1.08, passes.
    - Settings putting the widest point 1.5 further out (the operator's "pushing it"): about 0.07, and `check_design` raises.
    - Iteration 4's settings: about 3.07, the measurement less the straight term.

    `.scratch/wirestripper-grip/shut_gap.py` covers all three.
- **B3. The curved grip changes at the open end, and barely elsewhere.** Restated after preflight F1: `FLARE_LEN` moves the body loft's first section, and with it every section of the smooth loft (preflight measured up to 0.07 of movement). `.scratch/wirestripper-grip/slice_compare.py` checks:
    - the bore's outline at every height is iteration 4's, symmetric difference ≤ 0.001 mm² per slice;
    - above the new flare (z ≥ `FLARE_LEN` + 0.5), the outside's outline stays within 0.1 of iteration 4's (Hausdorff distance per slice).
- **B4. The bevel prints without supports, all round.** `corner_bevel.py` passes (≥ 47 degrees in every 15-degree direction) on each new grip and each fit test. `tools/overhang.py` flags only the roof's ridge strip.
- **B5. The straight handle is modelled from its readings.** `.scratch/wirestripper-grip/straight_check.py` (pure Python) checks `steel.STRAIGHT`:
    - its length is 85.14;
    - its bend is 0, and its centre line stays within 0.3 of every traced centre;
    - W at each traced row is within 0.35 of the traced width (the tracing reads to 0.5);
    - T at A, J, K, L and M equals the calipers at chords 0, 5.14, 35.14, 55.14 and 85.14;
    - the holes' centres are at 7.82 (`D2`, near A) and 78.25 (`D1`, near B), both 3 mm. The names follow the curved handle, so the scratch scripts that look holes up by name work on both;
    - W at B is within 0.1 of the old straight grip's inside opening (10.12), and T at B is under 14.6.

    It fails now: `steel` has no `STRAIGHT`.
- **B6. The curved handle is untouched by the `Handle` change.**
    - The curved part of `python steel.py`'s output is identical to the baseline saved before the change.
    - `tools/plot_curve.py` redraws `reference/curve-rebuilt.png` pixel for pixel.
    - The curved STL rebuilt after step 1, with iteration 4's settings, is byte-identical to `87e777c`'s. Rebuilt after step 4, it is byte-identical to iteration 5's.
- **B7. The straight grip is what the builder means.** `verify.py straight` must show:
    - the mock steel never inside the bore wall (0 mm³);
    - the rib bites match `RIB_BITE`;
    - the thinnest wall is as `corner_wall` predicts;
    - the cap over the ridge is at least `END`;
    - both STLs are watertight and stand on z = 0;
    - the fit test is the grip cut at `FIT_LEN`;
    - the tip lies below the roof.

    It fails now: there is no `straight_grip.stl`.
- **B8. Same inside and outside design as the curved grip.** `sizes()` prints the steel, the bore, the rib tips and the outside at B, at the widest point and at A, for both grips.
    - Bore and outside are steel plus the shared clearances and walls.
    - The straight bore differs from the curved one only by the difference in the readings: expected at most 0.5 in W and 0.25 in T.
    - The report gives the figures to the operator.
- **Edge cases:**
    - A straight handle has no lean. `roof()` must give a symmetric gable with both slopes at `ROOF_ANGLE` (checked in `verify.py` by the tip below the roof, and by `tools/overhang.py`).
    - `Handle` with W and T given at different places, in lists of different lengths.
    - T stations at both ends (A and M at B), so T is never extrapolated. The W line covers A to B.
    - The tracing's 0.5 steps: a least-squares line, not a piecewise fit that would add kinks and extrapolate wildly past row 7 (rows 6 to 7 alone would put 11 at B).
- **B9. No regression in the catalog:** `uv run --no-project --with pyyaml python -m unittest discover -s tests`, 88 OK.

### Test Infrastructure

- Framework: none committed for this model, by the operator's direction. Ad hoc Python scripts in `.scratch/wirestripper-grip/`, run with `uv run --no-project --with …`. Catalog `unittest` suite in `tests/`.
- Test location: `.scratch/wirestripper-grip/` (gitignored).
- Conventions: one script per concern, printing figures and a PASS or FAIL line, with a non-zero exit on failure (`lip.py`, `corner_bevel.py`).
- New check files:
    - `shut_gap.py`;
    - `slice_compare.py`;
    - `straight_check.py`.

  `lip.py`, `verify.py` and `corner_bevel.py` gain a `curved|straight` argument.

## Implementation Plan

Reordered after preflight: the straight handle comes first, because `shut_gap()` needs both handles' W at B (A1). The docs for the straight grip go in its commit (A7).

### 1. Straight handle in `steel.py` — executable

- Files:
    - `models/commercial-electric-wire-stripper-grips/steel.py`;
    - scratch `straight_check.py`.

1. **Stub tests.**
    - Empty `straight_check.py`.
    - The baselines are already saved in `.scratch/wirestripper-grip/baseline/`: `python steel.py`'s output, `curve-rebuilt.png`, and iteration 4's STLs.
2. **Stub interface.** In `steel.py`:
    - `Handle(name, coeffs, y_a, y_b, stations, holes, widths=None)`. `stations` stay the named readings (name, chord, W, T), and W or T may be `None` where only one was read. `widths`, when given, is a list of (chord, W) that replaces the stations' W as the width profile. Keeping `stations` keeps `tools/plot_curve.py`, `verify.py` and `render.py` working (A6).
    - The straight readings as `STRAIGHT_*` constants.
    - `STRAIGHT`.
    - `report()` split into `report_curved()` and `report_straight()`.
3. **Write tests and run red.** The B5 assertions; they fail on `steel.STRAIGHT`.
4. **Write code and run green.**
    - `Handle` builds its W and T profiles from the stations that have them, or W from `widths`.
    - The straight handle:
        - its centre line is a constant x, the mean of the traced centres;
        - y runs as on the curved tracing, with row 0 at y = 0 and B at y = 80;
        - its stations are A, J, K, L and M, with T only;
        - its `widths` are the least-squares line through the eight traced widths, given at A and at B;
        - its holes are `D2` and `D1`, each centred at its near-edge reading plus 1.5.
    - Green:
        - `straight_check.py`;
        - B6's diff of the curved report and the redrawn plot;
        - a rebuild of the curved grip, byte-identical to `87e777c`'s STLs (restore the STEP files if only their headers change).

### 2. Straight readings in the log — prose/policy

- Files:
    - `reference/measurements.md`;
    - `reference/straight-tracing.jpg`, `reference/straight-holes.jpg`: the operator's two photos, copied to `.scratch/wirestripper-grip/straight-photos/` (A4) and re-encoded as JPEG like the others. The pre-commit hook strips their metadata.
    - the model's `systemPatterns.md` (the straight handle).
- No tests: prose/policy artifact.

1. Add a dated entry, "Straight handle, bare steel (2026-11-01)":
    - the tracing table, the T readings, A to B and the old straight grip's opening;
    - the holes, quoting the sheet ("Hole bottom from bd. edge") and the operator's reading of it: from the rounded tip to each hole's near edge. Give both the near edge and the centre;
    - the gap with the tool shut;
    - the assumption that row 7 is 10 from B;
    - that the widths come only from the tracing, to 0.5;
    - that a curved grip slides onto the straight handle.

   The 2026-10-31 "Not measured yet" note stays as history, marked superseded.
2. In `systemPatterns.md`, describe how the straight handle is modelled: W as a line through the tracing, T from the calipers, and the stations named J to M.
3. Commit the readings, with `tasks.md` updated: `chore: saving progress on commercial-electric-wire-stripper-curved-grip`, its body naming the straight readings.

### 3. Curved grip, iteration 5: the stronger flare — executable

- Files:
    - `models/commercial-electric-wire-stripper-grips/grips.py`;
    - `curved_grip.{step,stl}`, `curved_grip_fit_test.{step,stl}` (regenerated);
    - the model's `systemPatterns.md`;
    - scratch `lip.py`, `shut_gap.py`, `slice_compare.py`.

1. **Stub tests.**
    - `lip.py` takes `curved|straight` and an optional STL path, and gains the B1 widest-point condition (iteration 4's 0.474 + 0.95).
    - Empty `shut_gap.py`.
    - Empty `slice_compare.py` (new STL against the iteration 4 baseline).
2. **Stub interface.** In `grips.py`:
    - `SHUT_GAP`, `SHUT_WALL` and `MIN_SHUT_GAP` replace `CONVEX_LIMIT`. The comments say where the gap was measured and on what, and that `SHUT_WALL` describes the measured grips, so it stays fixed if `WALL_SIDE` changes;
    - `widest()` returns the rim profile's widest (d, grow);
    - `shut_gap()` returns the gap with the tool shut, for the shipped pair (B2).
3. **Write tests and run red.**
    - `lip.py curved` on iteration 4's STL: FAIL on the widest point.
    - `shut_gap.py`: the three B2 cases. It fails while `shut_gap()` is a stub.
    - `slice_compare.py`: the B3 assertions.
4. **Write code and run green.**
    - `FLARE` 2.3, `FLARE_LEN` 8.0, `BEVEL` 1.8.
    - `check_design` asserts `shut_gap() >= MIN_SHUT_GAP` in place of `WALL_SIDE + FLARE <= CONVEX_LIMIT`.
    - `sizes()` prints the gap left with the tool shut, and uses `widest()`.
    - Regenerate the curved outputs.
    - Green: `lip.py`, `shut_gap.py`, `slice_compare.py`, `corner_bevel.py`, `verify.py curved` and `tools/overhang.py`.
    - In `systemPatterns.md`: the flare history (iteration 5), and the shut-gap rule in place of the "9 mm gap with the old straight grip" point.
    - Add a model SumMem note correcting the earlier "0.5 wider": the operator then asked for 1.0 (A5).
    - Commit iteration 5 on its own, with `tasks.md` updated: `chore: saving progress on commercial-electric-wire-stripper-curved-grip`, its body naming curved grip iteration 5 (the stronger flare).

### 4. Straight grip, iteration 1 — executable

- Files:
    - `grips.py`: `build(h, stem, out)`; the main block builds both grips;
    - `straight_grip.{step,stl}`, `straight_grip_fit_test.{step,stl}` (new);
    - scratch `verify.py`, `corner_bevel.py`, `render.py`.

1. **Stub tests.** `verify.py`, `corner_bevel.py` and `render.py` take `curved|straight`.
2. **Stub interface.** `grips.build(h, stem, out)`: `check_design`, the grip, both exports and `sizes`.
3. **Write tests and run red.** `verify.py straight` fails: there is no `straight_grip.stl`.
4. **Write code and run green.**
    - The main block builds `(steel.CURVED, "curved_grip")` and `(steel.STRAIGHT, "straight_grip")`.
    - Green:
        - `verify.py straight`;
        - `lip.py straight`;
        - `corner_bevel.py` on both straight files;
        - `tools/overhang.py` on both;
        - the curved STLs byte-identical to iteration 5's (B6), with STEP header-only changes restored.

### 5. Model docs — prose/policy

- Files:
    - `README.md`;
    - `memory-bank/productContext.md`, `memory-bank/techContext.md`, `memory-bank/systemPatterns.md`;
    - `grips.py`'s and `steel.py`'s docstrings.
- No tests: prose/policy artifact.

1. **README:** both grips exist; the file table lists `straight_grip.*`; the build writes both.
2. **productContext:** a success criterion for the straight grip (slides on to B, 85 from the tip).
3. **techContext:** `grips.py` builds both grips (about a minute); `steel.py` reports both handles; the scratch checks take a handle.
4. **systemPatterns:** the print orientation for a straight grip (no lean, symmetric roof). No copied values (catalog norm).
5. `publish.yaml` is unchanged.
6. Commit steps 4 and 5 together as straight grip iteration 1, with `tasks.md` updated: `chore: saving progress on commercial-electric-wire-stripper-curved-grip`, its body naming straight grip iteration 1 (A7).

### 6. Final verification — executable

1. Catalog suite (B9).
2. Rerun every scratch check on the committed outputs, and confirm the working tree is clean.

## Technology Validation

No new technology - validation not required. The scratch checks use packages already in use (cadquery, trimesh, shapely, rtree, networkx, scipy, mapbox_earcut, pillow).

## Dependencies

- The operator's straight readings and photos. The photos are saved in `.scratch/wirestripper-grip/straight-photos/`, because the session's image cache does not survive a restart.
- Iteration 4's outputs at `87e777c`, the baseline for B1 and B3.
- The pre-commit image hook (ExifTool) for the two new photos.

## Challenges & Mitigations

- **The tuned flare trips an existing guard** (d rising strictly, the first-layer wall, the 45-degree bevel). The exploration ran `rim_profile()` with these settings: the profile is valid and the first-layer corner wall is about 2.55. `check_design` runs on every build.
- **`SHUT_WALL` is a fact about the measured grips, not a design value.** If `WALL_SIDE` changes later, `SHUT_WALL` must stay what was measured. Say so in its comment and in `systemPatterns.md`.
- **The `Handle` change silently moves the curved grip.** B6 compares the steel report and the plot, and the curved STL bytes across steps 2 to 4.
- **The W line misreads the straight steel** (preflight A3). The tracing reads to 0.5, and the curved calipers show a slight curve. On the curved handle, the tracing read up to 0.56 too wide near B. If the straight tracing does the same, its bore is about 0.4 loose there, and its side ribs do not touch.
    - **Decision:** build from the tracing now. Under the operator's standing direction, the first print should be close enough to learn from, and a curved grip, built 0.47 narrower at B, already works on this steel.
    - **What supports the line:** its residuals are at most 0.35; W at B lands within 0.04 of the old grip's opening; in the middle rows it agrees with the curved handle's calipers.
    - **Report:** recommend the straight fit test first. Give W at A and at B next to the curved handle's. Offer caliper W at J, K, L, M and B as the fix if the fit is loose.
- **The row positions are assumed** (row 7 at 10 from B). A 1 mm error moves W by about 0.04. Record the assumption.
- **The straight roof without lean.** `roof()` with equal heights gives `xr` at the midpoint and no division by zero. `verify.py`'s tip check and `tools/overhang.py` confirm it.
- **Photo commits.** The hook rewrites images and stops the commit once; stage again and recommit.
- **Build time doubles** (two grips, about a minute). Acceptable; the build runs in the background, and the timing goes in techContext.

## Pre-Mortem

- **The operator meant 1.0 on the nominal `FLARE`, not at the widest point.** Their reasoning was in gap terms (3.3 apart, 1.5 each would be pushing it), and the gap is set by the widest point, so the widest point is the right measure. The report states the widest point (0.99 further out) and the gap left (about 1.1 for the shipped pair), so a mismatch is visible at once.
- **The longer flare changes the hand feel more than "a bit more of a flare out".** The report names the trade: `FLARE_LEN` 8 keeps print 1's steepness, while 5 would be twice as steep. Either is one parameter for the next print.
- **The straight grip fits differently from the curved grip on the straight steel** (the operator's working reference). The report gives the straight bore against the curved one at A and B, and recommends the fit test first.
- **A guard written for one handle breaks on the other.** For example, the dome check uses W at A, which differs between the handles. `check_design` runs per handle in `build()`.

## Preflight (run 1, 2026-11-01): FAIL (fixable), resolved in the plan

- **F1:** B3 could not pass, because `FLARE_LEN` moves the body loft's sections. B3 is restated with a 0.1 tolerance on the outside; the bore stays identical.
- **A1:** the gap is modelled for the pair that ships. `shut_gap()` subtracts half the straight handle's extra W at B, which comes to about 1.1, not 1.3.
- **A2:** `MIN_SHUT_GAP` is 0.8, with its reason in B2.
- **A3:** proceed with the traced W. See Challenges.
- **A4:** the photos are saved in `.scratch/`. The log quotes "Hole bottom from bd. edge" next to the operator's reading of it.
- **A5:** step 3 adds a correcting SumMem note.
- **A6:** `Handle` keeps `stations`. The straight holes are named `D2` and `D1`.
- **A7:** the straight grip's docs go in its commit.
- **A8:** the report gives 0.99.
- **The flare sampler** (three fit tests on a plate at +0.5, +1.0 and +1.5) is not taken. The operator chose 1.0 explicitly. The report can offer it if the feel is off.

## Build Progress

- [x] 1. Straight handle in `steel.py`. B5 passes. B6: the curved report is identical to the baseline, the plot is pixel-identical, and the curved STLs rebuild byte-identical to `87e777c`'s (the STEP files changed only in their headers and were restored).
- [x] 2. Straight readings in the log, with the two photos; the straight handle in `systemPatterns.md`. `steel.py`'s docstring and techContext's steel report line updated (preflight run 2, A2).
- [x] 3. Curved grip, iteration 5: `FLARE` 2.3, `FLARE_LEN` 8, `BEVEL` 1.8. The widest point is 1.464 at z 1.50, which is 0.99 further out than iteration 4's. The shut gap is 1.08 against `MIN_SHUT_GAP` 0.8, and `SHUT_WALL` is 4.274. Green:
    - `lip.py` (red first on iteration 4);
    - `shut_gap.py` (red first while `shut_gap()` was a stub);
    - `slice_compare.py`: bore 0.00029 mm², outside 0.075. It passes on iteration 4 against itself and fails when shifted 0.2;
    - `corner_bevel.py`, at least 49.9 degrees;
    - `verify.py curved`: 0 mm³ of steel in the wall, ribs 38.7 mm³, thinnest wall 2.05, footprint 197 mm², the fit test matches;
    - `tools/overhang.py`: the ridge strip only.

  The `CONVEX_LIMIT` prose is replaced in `systemPatterns.md` and `techContext.md` (preflight run 2, A1). A SumMem correction to "0.5" is recorded (run 1, A5).
- [x] 4. Straight grip, iteration 1: `grips.build(h, stem, out)`; the main block builds both grips in about 40 s. `verify.py straight` was red first (no STL), then green:
    - steel 0 mm³ in the wall; ribs 39.4 mm³ against 39.4. One T-face rib bites 0.109 at J, because the loft's sections miss that station's kink in T; that is 9 µm;
    - thinnest wall 2.05; cap 5.0; watertight; the fit test matches; footprint 202 mm²;
    - `lip.py straight`: widest 1.463 at z 1.50;
    - `corner_bevel.py`: at least 50.2 degrees;
    - `tools/overhang.py`: only the 0.2 ridge, which bridges.

  The curved STLs stayed byte-identical to iteration 5's; the STEP files changed only in their headers and were restored. `verify.py` and `render.py` take `curved|straight`. The size report no longer says "leaning" for the straight grip.
- [x] 5. Model docs: the README, productContext (the straight success criterion), techContext (the build of both grips; run every check for both), systemPatterns (print orientation and the fit test for both grips), and the `grips.py` docstring. `publish.yaml` is unchanged.
- [ ] 6. Final verification

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [ ] Preflight
- [ ] Build
- [ ] QA
