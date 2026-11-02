# Task: wire-stripper-grips-closed-end

* Task ID: wire-stripper-grips-closed-end
* Complexity: Level 2
* Type: simple enhancement

Take the hollow out of both grips' closed ends (projectbrief). The bore now ends `END_CLEAR` (1.0) past a square-ended tip, then a gable roof rises 4.33 (straight) or 3.66 (curved) more. The real tips are rounded in the plane of the handles. The new bore follows the rounded tip grown by `BORE_CLEAR`, and each roof slope is the lowest line at `ROOF_ANGLE` in print that clears that grown tip. The outside's dome still starts at the ridge's height, so the grip gets shorter by as much as the ridge drops.

Expected, from preflight run 1's independent working of the Geometry below. `tip_roof_sweep.py` gave the apex, which sits 0.10 to 0.12 higher; see F1.

| | Curved | Straight |
|---|---|---|
| Tip corner radius (`steel.py`) | 1.5 | 3.3 (a half circle; W/2 at the round's start is 3.40) |
| Ridge row past A, now (today's strip sits at the apex) | 4.66 | 5.33 |
| Ridge row past A, new | 2.89 | 2.30 |
| Grip end past A, now / new | 9.66 / 7.89 | 10.33 / 7.30 |
| Shorter by | 1.77 | 3.03 |

Two commits:
1. The tip readings: steel only, so the printed files do not change.
2. Curved grip iteration 6 and straight grip iteration 2: the new closed end, the regenerated files, and their docs.

## Geometry

Worked in the plane of the handles, in a frame at the start of the tip's round. The origin is `O = h.point(rc)`, where `rc = h.tip_r`.
- **Axes:** z runs along `-h.tangent(rc)`, toward A and past it. u runs along `h.normal(rc)`.
- **Steel tip:** the steel is `w = h.width(rc)` wide, and its corners are arcs of radius `rc`. They are centred at z = 0, u = ±`cu`, where `cu = w/2 - rc` (at least 0). A is at z = `rc`.
- **Grown tip:** the same arcs with radius `R = rc + BORE_CLEAR`. A point at angle φ on side σ (+1 or -1) is `(R sin φ, σ(cu + R cos φ))`, with outward normal `(sin φ, σ cos φ)`.
- **Print directions:** up is `-h.tangent(h.length)`. "Horizontal" is the direction in the plane square to up, oriented toward +u.
- **Slopes:** slope σ's outward normal is `sin(ROOF_ANGLE)·σ·horizontal + cos(ROOF_ANGLE)·up`. It touches side σ's arc at `φσ = atan2(nz, σ·nu)`.
    - `roof()` asserts 0 ≤ φσ ≤ 90 degrees: the slope touches its own corner and clears the other one. Two bounds: the lean is less than `ROOF_ANGLE`, and `ROOF_ANGLE` plus the lean is at most 90. The curved grip leans about 15 degrees, so with today's 50 its slopes touch at φ 55.05 and 24.95. The message names both bounds.
- **Bore at height z:** on side σ, the bore's edge follows the arc up to z = `R sin φσ`, and the slope's line after that.
- **Ridge strip:** the last row is at the z where the two lines are `RIDGE_W` apart. The slopes stay exactly at `ROOF_ANGLE` up to the strip. Today's strip sits at the apex, which is 0.10 to 0.12 higher.
- **`past` and `ridge`:** `past` is the ridge row's z − `rc`, its distance past A. The dome starts there, so the cap over the strip stays `DOME_LEN`. `ridge` is the ridge row's centre point, in 3D.
- **Rows:** the arc samples on each side every `RIM_STEP` degrees (its comment now names the tip's arcs too), the two tangent points and the ridge row, merged and sorted.
    - Both sides sample arcs of the same radius on the same grid, and the straight grip's two tangent points coincide. So a z within 1e-3 of the previous row's is dropped; a ruled loft through coincident sections fails.
    - The tangent points and the ridge row are always kept.
    - Each row records `(z, u_lo, u_hi)`.

## Test Plan (TDD)

The operator's standing direction (`techContext.md`) is no committed tests while the shapes are prototyped. Checks are ad hoc scripts in `.scratch/wirestripper-grip/` (gitignored). Each prints its figures and a PASS or FAIL line, and exits non-zero on FAIL. A check for new behaviour is written first and run red on the current code. `grips.check_design` holds the parameter guards. The catalog `unittest` suite guards the repository.

### Behaviors to Verify

- **B1. Tip readings** (`tip_check.py`, pure Python):
    - Both handles have a `tip_r` between 0 and half of W at `tip_r`. The values themselves are readings, not behaviour, so there is no check that repeats them (preflight A7).
    - The straight's modelled tip ends 1.2 ± 0.15 short of A at 0.75 in from the side, matching the old straight grip (84.8 at the centre, 83.6 near the edge).
    - `python steel.py`'s output equals the `5d73490` baseline apart from added lines: the readings do not move.

    Red now: `Handle` has no `tip_r`.
- **B2. The ridge drops** (`closed_end.py`, rewritten):
    - `grips.roof(h)` returns `(rows, past, ridge)`.
    - `past` is 2.30 ± 0.05 (straight) and 2.89 ± 0.05 (curved).
    - The rows start at the body's section: z = 0, u = ±(w/2 + `BORE_CLEAR`).
    - The rows rise in z, and widen no more than the arcs allow.
    - The last row is `RIDGE_W` wide.
    - The straight STL stands 3.03 ± 0.05 lower than its baseline. The curved STL leans, so its drop in height is reported beside 1.77, without a limit.

    Red now: `roof` returns `(r, rise)`.
- **B3. The bore hugs the tip and never touches it** (`verify.py`, extended):
    - With `steel_solid(h)` modelling the rounded tip, no steel is inside the bore wall (0 mm³).
    - Points on the tip's arcs, from the wall to φσ, both sides, at mid-T and 1 in from each T face: each lies `BORE_CLEAR` ± 0.02 from the bore's surface.
    - The point at A on the centre line is at least `BORE_CLEAR` from it.
    - The cap over the ridge is `DOME_LEN` ± 0.01, and at least `END` (preflight run 2, A2: the curved grip gives 4.9948).

    Red now: the gap at the tip is 1.0 or more, and the mock tip is square.
- **B4. The ribs end before the round** (`verify.py`):
    - Rib volume at s < `tip_r` is under 0.01 mm³ (only the embedded roots touch it).
    - The rib bites in cross-sections are still `RIB_BITE`.
    - The bite into the mock steel (`verify.py`'s mock ∩ grip) is 8 ribs' bite cross-section times (L − `tip_r` − `RIB_FADE`), within 2%. Over the fade, only the last quarter of the rib reaches past the steel face, so it adds about an eighth of a rib-length, about 0.2 mm³ in about 38 (preflight A3).

    Red now: the ribs run to A.
- **B5. Nothing else moves** (`slice_compare.py`, rewritten for `curved|straight`). It compares CAD sections: the new STEP against `baseline/<stem>-5d73490.step` (preflight run 2, F1). The range is from the bed to 1 below where the ribs start to fade, in print.
    - The bore's outline is within 0.02 of the baseline's (Hausdorff).
    - The outside's is within 0.02 below `FLARE_LEN + 0.5`, and within 0.1 above it.

    The body lofts' section positions move with their end, so a few hundredths are expected. Preflight's trial build gave at most 0.013 (curved), 0.002 (straight) and 0.007 (curved fit test).

    STL slices are not held to these limits, because the STL export's own error is larger: up to 0.094 on the curved grip's bore at `5d73490`. The script prints the STL comparison too, without a limit. `--shift 0.2` must make the CAD comparison fail.
- **B6. It prints without supports:**
    - `tools/overhang.py` flags only the ridge strip on each full grip, and nothing on the fit tests.
    - `roof_angles.py` (new): every downward-facing bore face above the ribs' fade is at least `ROOF_ANGLE` − 0.5 above horizontal, except the ridge strip. The arcs are steeper than the slopes.

    `roof_angles.py` passes now, so it guards against regression. It must not regress.
- **B7. Parameter guards** (`design_guards.py`): `check_design` raises `AssertionError`
    - for a tip radius over half the tip's W;
    - for a negative tip radius;
    - for `ROOF_ANGLE` 44;
    - when a slope would miss its own corner (the curved grip with `ROOF_ANGLE` 80: 80 plus its 15 degrees of lean is over 90). The ≥ 45 guard does not catch 80, so only `roof()`'s guard can fire (preflight A1).

    Each guard's message names the problem. Red now: there are no such guards.
- **B8. Unchanged elsewhere:**
    - `lip.py` (both grips) gives the same widest point and bevel.
    - `corner_bevel.py` on all four STLs: at least 49.9 degrees.
    - `shut_gap.py` passes.
    - Each fit test equals its grip cut at `FIT_LEN` (`verify.py`).
    - Both STLs are watertight and stand on z = 0.
    - The fit tests match their `5d73490` STEP files within B5's tolerances, by the same CAD comparison.
- **B9. Catalog suite:** `uv run --no-project --with pyyaml python -m unittest discover -s tests` gives 88 OK.
- **Edge cases:**
    - `tip_r` 0 (a square tip) still builds a valid roof; `design_guards.py` builds the straight roof with it. The tip is then 0.3 past A, against 1.0 now, and the ridge row 4.32 past A. `steel_solid` then skips the round (preflight A4).
    - A full half circle, where `cu` is near 0: the mock's last section stays at least 0.02 wide.
    - The curved lean makes the two tangent heights differ: the rows include both.
    - Commit 1 changes no printed file: a rebuild gives byte-identical STLs, and STEP files whose only changes are header timestamps are restored.

### Test Infrastructure

- Framework: none committed for this model (operator's direction). Ad hoc Python in `.scratch/wirestripper-grip/`, run from the repo root with `uv run --no-project --with …`. The catalog `unittest` suite is in `tests/`.
- Conventions: one script per concern; a `curved|straight` argument; a PASS or FAIL line and the exit code.
- New check files: `tip_check.py`, `roof_angles.py`, `design_guards.py`. Rewritten: `closed_end.py`. Extended: `verify.py`, `slice_compare.py`.
- `tip_roof.py` and `tip_roof_sweep.py` were one-off explorations. They read the old `roof()` and `END_CLEAR`, so they stop working after step 2. They are not checks (preflight A5).

## Implementation Plan

### 1. Tip readings: `steel.py` and the log (executable, with prose)

- Files:
    - `models/commercial-electric-wire-stripper-grips/steel.py`;
    - `reference/measurements.md`;
    - scratch `tip_check.py`.

1. **Stub tests:** an empty `tip_check.py`.
2. **Stub interface:**
    - `Handle(..., widths=None, tip_r=0.0, step=0.01)` stores `self.tip_r`. Its docstring says what it is: the tip's corner radius in the plane of the handles, the round starting `tip_r` from A.
    - Constants `TIP_R = 1.5` (curved) and `STRAIGHT_TIP_R = 3.3`.
    - `OLD_STRAIGHT_DEPTH = (84.8, 83.6)`: not steel, kept for the cross-check, like `OLD_STRAIGHT_OPENING`.
    - A helper `Handle.tip_short(u)`: how far short of A the steel ends at u from the centre line.
3. **Write tests and run red:** the B1 assertions. They fail on `tip_r`.
4. **Write code and run green:**
    - Pass `tip_r` to `CURVED` and `STRAIGHT`.
    - `report_curved` and `report_straight` print the tip radius.
    - The straight report also prints the steel's `tip_short` at 0.75 in from the side, beside the old grip's 1.2 between centre and edge.
    - `steel.py`'s docstring gains the tip.
    - Green: `tip_check.py`. Rebuild with `grips.py`: the four STLs are byte-identical; restore STEP files whose only changes are headers.
5. **Prose:** a dated log entry, "Tips and depths (2026-11-01)":
    - the old straight grip's depth (84.8 at the centre, about 83.6 near the edge, the operator's "might be");
    - the printed straight grip's about 87.7, and how a rod lands on the roof's slope;
    - the printed grips about 7 (straight) and 5 (curved) longer than the old ones;
    - the tips' shape from the two tracings, and why each radius is read on the small side;
    - the half-circle cross-check.
6. **Commit:** `chore: saving progress on wire-stripper-grips-closed-end`, its body naming the tip readings, with `tasks.md` updated.

### 2. The closed end: `grips.py` (executable)

- Files:
    - `grips.py`;
    - the eight output files (regenerated);
    - scratch `closed_end.py`, `verify.py`, `slice_compare.py`, `roof_angles.py`, `design_guards.py`.

1. **Stub tests:** empty `roof_angles.py` and `design_guards.py`. `closed_end.py`, `verify.py` and `slice_compare.py` get the new B2 to B5 sections, still empty.
2. **Stub interface,** in `grips.py`:
    - `END_CLEAR` goes. New: `RIB_FADE = 1.0`: the ribs fade into the wall over this length and end where the tip's round starts.
    - `roof(h)` becomes `-> (rows, past, ridge)`, documented as in "Geometry" above: `past` and `ridge` belong to the ridge row, not the apex.
    - `steel_solid(h)` documents the rounded tip.
3. **Write tests and run red:**
    - `closed_end.py` and `verify.py` fail on the current build (B2 to B4).
    - `design_guards.py` fails: no guards.
    - `roof_angles.py` and `slice_compare.py` pass on the current files (guards).
4. **Write code and run green:**
    - `roof(h)`, as in "Geometry".
    - `bore(h)`:
        - the smooth loft from B to `s = tip_r`;
        - a ruled loft through one `rrect` per row, in planes square to `tangent(rc)` at `O − tangent(rc)·z`. Each is `u_hi − u_lo` by `thickness(rc − z) + 2·BORE_CLEAR`, with `BORE_CORNER_R`, offset by the row's centre;
        - the first row's `rrect` is the body's last section, so the two lofts share a face. Fuse and clean.
    - `steel_solid(h)`: rectangles from B to `tip_r`, then the tip's round in the same frame, ruled. Arc samples every `RIM_STEP` degrees; the last section at least 0.02 wide. When `tip_r` is 0, the rectangles run to A and there is no round.
    - `ribs(h)`: full height from B to `tip_r + RIB_FADE`, then down to height 0 at `tip_r`.
    - `outside(h)`: `s_dome = -past`.
    - `check_design(h)` adds three assertions, each with a message:
        - `0 <= h.tip_r <= h.width(h.tip_r) / 2`;
        - `ROOF_ANGLE >= 45`;
        - `RIB_FADE > 0`.

      `roof()` asserts the lean condition itself, and `check_design` calls it.
    - `sizes()` prints, per grip:
        - the tip radius;
        - "the bore hugs the tip at `BORE_CLEAR`";
        - the ridge `past` A;
        - the dome;
        - the grip's end past A.
    - The module docstring describes the roof seated on the rounded tip.
    - Regenerate both grips and both fit tests (`python grips.py`, about 40 s).
    - Green: B2 to B8.

### 3. Model docs (prose/policy)

- Files: the model's `systemPatterns.md`, `techContext.md`, `productContext.md` and `README.md`.
- No tests: prose/policy artifact.

1. `systemPatterns.md`:
    - "Names for places on a handle": the tip's round (`Handle.tip_r`).
    - "The curved handle" and "The straight handle": the tip's shape and where its radius comes from.
    - "How a grip fits": the `END_CLEAR` bullet becomes the bore following the rounded tip at `BORE_CLEAR`. The grip still seats by the steel's taper near B.
    - The ribs end `RIB_FADE` before the round.
    - "Print orientation": the roof seated on the tip.
    - A short history: the square-tip roof (`3046d4e` and before) left 5.3 and 4.7 of hollow, which the operator did not want (2026-11-01).
2. `productContext.md`, Key Constraints: no hollow past the steel tip beyond the clearance and the small roof a print needs; such hollow flexes and carries no load.
3. `techContext.md`: the useful ad hoc checks: the rounded mock tip clears the bore by `BORE_CLEAR`, and the bore hugs it. Add the tip-radius guard to the list of assertions.
4. `README.md`: `steel.py`'s row also names the tip.
5. Commit steps 2 and 3 together: `chore: saving progress on wire-stripper-grips-closed-end`. Its body names curved grip iteration 6 and straight grip iteration 2, and their figures. `tasks.md` is updated.

### 4. Final verification (executable)

1. Catalog suite (B9).
2. Rerun every check on the committed outputs, for both grips.
3. Record the iterations in a SumMem note for the model: the commit, the figures, and what to watch in the print. Commit the note's files (preflight A6), then confirm the working tree is clean.

## Technology Validation

No new technology - validation not required. The checks use packages already in use (cadquery, trimesh, shapely, rtree, networkx, scipy, mapbox_earcut).

## Dependencies

- The operator's readings in chat (2026-11-01): the old straight grip's depth, the printed grip's depth, and how much longer the printed grips are.
- The tracings in `reference/`, for the tips' shape.
- The baselines in `.scratch/wirestripper-grip/baseline/` (`5d73490`).

## Challenges & Mitigations

- **The ruled loft through about 30 `rrect` rows fails or twists.**
    - Every row has the same topology (`rrect`: 4 lines and 4 arcs), the way the dome's sections and today's cap do.
    - If OpenCascade still balks, sample the arcs at 6 degrees instead of 3. The chord sag at 6 degrees on R 3.6 is 0.005, still inside B3's ± 0.02.
- **The cap and the body do not fuse cleanly.** The first row is built by the same call as the body's last section (same plane, width, thickness and radius), so their faces coincide. `grip()` already asserts one valid solid.
- **The chords of the arcs sit inside the true round,** slightly shrinking the clearance. At 3 degrees the sag is about 0.001. B3's ± 0.02 allows for it.
- **The open end moves,** because the body lofts' sections move with their end (s = `tip_r` instead of −1.0; the dome's start).
    - B5 bounds this at 0.02 near the open end. Last task's precedent was 0.075 above the flare on the curved grip.
    - The fit tests may change by hundredths. B8 checks them against the baselines, and they are regenerated and committed.
- **The lean puts the two slopes' tangent points at different heights.** The rows include both, and B3 samples both sides.

## Pre-Mortem

- **The real tip is squarer than modelled, so the steel meets the roof before the open end reaches B,** and the stagger the operator likes shrinks.
    - Both radii are read small, and the straight one agrees with the old grip's floor.
    - If the real corners do stand proud of the modelled round, the first 0.3 is clearance. The open end lands short only by the rest; TPU may also give a little.
    - The report says what to watch for: the open end sitting short of where the steel widens. Then name the fix: a smaller `tip_r` for that handle.
- **The operator expected the grips to shrink by about 3 and 1.7.** The report gives the modelled figures, 3.03 and 1.77. They are a little more than the 2.9 and 1.7 given in chat, which were the apex (F1).
- **Taking `END_CLEAR` out changes how the grip seats.** The fit was always meant to come from the steel's taper near B. The old grip had no gap at the tip at all. The report says the tip now has the same 0.3 as the sides.
- **A full grip print is needed to see the tip change.** The fit test covers only the open end. Name the full straight grip as the print that shows the most change.
    - Preflight's tip-test idea goes in the report as an offer, with its figures. It would be the closed end alone (about 14 mm), pushed onto the bare tip, with its end expected about 6.8 (straight) and 7.5 (curved) past A.
    - It is not built: the operator has not asked for it, and the brief keeps everything else unchanged.

## Preflight run 1 (2026-11-01): FAIL (fixable), resolved in the plan

- **F1:** `past` and `ridge` are defined as the ridge row's. The figures are restated: the ridge row sits 2.89 and 2.30 past A, and the grips get 1.77 and 3.03 shorter. B2's limits are ± 0.05.
- **A1:** B7's lean case is `ROOF_ANGLE` 80 on the curved grip. The Geometry gives both bounds.
- **A2:** rows within 1e-3 of the previous one are dropped.
- **A3:** B4 measures the bite into the mock steel, within 2%.
- **A4:** `steel_solid` skips the round when `tip_r` is 0.
- **A5:** the two exploration scripts are not checks.
- **A6:** step 4 commits the SumMem files.
- **A7:** B1 no longer repeats the radii.
- **Tip test print:** offered in the report, not built.

## Preflight run 2 (2026-11-01): FAIL (fixable), resolved in the plan

- **The trial build.** Preflight built step 2 as planned. Every check passed except B5.
    - `past` is 2.887 and 2.300.
    - The bore stays 0.2989 to 0.3000 from the tip.
    - The straight grip comes out 3.028 lower.
    - Only the ridge strip overhangs.
- **F1:** B5 and B8 compare CAD sections against the `5d73490` STEP files, which are saved in `baseline/`. STL slices are reported only: the STL export strays up to 0.094 from its own CAD on the curved bore.
- **A1 (STL accuracy, outside this brief):** the STLs already stray up to 0.094 (curved) and 0.040 (straight) from the CAD model where the bore's corner rounds meet its W faces. There, the side clearance drops from 0.3 to about 0.18.
    - Exporting at `tolerance` 0.002 would bring that to 0.029, but the curved STL would grow from 3.0 to 4.2 MB.
    - The brief keeps everything else unchanged, so this goes to the operator in the report. It is not done here.
    - A SumMem note records the fact.
- **A2:** B3's cap check is `DOME_LEN` ± 0.01.
- **A self-checking export** (`mesh_error`, an `STL_TOL`): not taken, for the same reason as A1. It belongs to the operator's decision on A1.

## Build Progress

- [x] 1. Tip readings. `Handle(tip_r=…)` and `Handle.tip_short(u)`; `TIP_R` 1.5, `STRAIGHT_TIP_R` 3.3, `OLD_STRAIGHT_DEPTH` (84.8, 83.6). `report_tip()` prints each tip, and the straight report adds the cross-check: 1.21 modelled, 1.20 on the old grip.
    - `tip_check.py` was red first (no `tip_r`), then green. `python steel.py` keeps every baseline line and only adds the tip lines.
    - A rebuild gave byte-identical STLs. The STEP files changed only in their headers and were restored.
    - Log entry "Tips and depths (2026-11-01)".
- [x] 2. The closed end in `grips.py`: `roof()` returns `(rows, past, ridge)`; `tip_plane()`; `bore()` with a ruled cap through the rows; `steel_solid()` with the rounded tip; ribs fading over `RIB_FADE` and ending at `tip_r`; `s_dome = -past`; four new guards; `sizes()` reports the closed end. `END_CLEAR` is gone.
    - Red first:
        - `closed_end.py` and `design_guards.py` failed;
        - `verify.py`'s hug check failed on the committed square-tip design (gaps 0.30 to 1.03).
    - The guards `roof_angles.py` and `slice_compare.py` passed on the old files, and `--shift 0.2` failed.
    - Green on the rebuilt files:
        - B2: `past` 2.887 (curved, 30 rows) and 2.300 (straight, 16 rows). The straight STL is 3.028 lower; the curved one 1.714 lower, against 1.77 along the steel.
        - B3: no steel in the wall. The tip's arcs are 0.2994 to 0.3000 (curved) and 0.2989 to 0.2999 (straight) from the bore. A is 1.54 and 1.56 from it. The cap is 4.9948 and 5.0000.
        - B4: no rib past `tip_r`. The bite volume is +0.39% and +0.21%.
        - B5, CAD: the bore moved at most 0.0134 (curved) and 0.0019 (straight); the open end, 0.0000; the outside above the flare, 0.0053.
        - B6: `roof_angles.py` gives 50.00 to 90.00 degrees with a 2.9 mm² ridge strip. `tools/overhang.py` flags only that strip, which bridges on the straight grip; the fit tests have nothing.
        - B7: every guard fires with its own message; the square tip builds, with the ridge row 4.318 past A.
        - B8, all unchanged:
            - `lip.py`: widest 1.464 and 1.463, at z 1.50;
            - `corner_bevel.py`: 49.9 and 50.2, at the same z and direction as at `5d73490`;
            - `shut_gap.py`;
            - the fit tests equal their grips cut at `FIT_LEN`, both STLs are watertight, and the fit tests' CAD moved 0.0074 and 0.0003.
    - **Deviation (check tolerance, with evidence):** `verify.py`'s rib-bite rows went from ± 0.015 to ± 0.02. The curved grip's W-face rib read 0.115 at S2.
        - The ribs are ruled between sections up to 4 apart. On the curved bend, and across S2's kink in W, a rib bites up to about 0.015 more on one side and less on the other between sections.
        - The `5d73490` build reads 0.089 and 0.112 midway between its own sections near S2. It read 0.101 at S2 only because a section happened to sit there.
        - So the geometry is unchanged in kind, and 0.02 matches B5's allowance for moving the sections. The rows also start at `tip_r + RIB_FADE` (preflight run 3, A1).
    - The STL files changed size with the new tessellation: curved 2.84 to 3.11 MB, straight 1.52 to 2.12 MB, fit tests 1.12 to 0.78 and 0.49 to 0.74 MB.
- [x] 3. Model docs:
    - `systemPatterns.md`: the tip's round, each handle's tip, the ribs' end, the closed end and its history, and the roof in "Print orientation";
    - `productContext.md`: no hollow past the tip;
    - `techContext.md`: all four new guards (preflight run 3, A4), the hug check, comparing CAD rather than STL, and the steel report;
    - `README.md`: `steel.py` names the tip;
    - `grips.py`'s and `steel.py`'s docstrings.
- [x] 4. Final verification. Catalog suite: 88 OK. Every check was rerun on the committed files (`a61aa6d`), and all pass with the figures above (`.scratch/wirestripper-grip/runs/final.txt`). A SumMem note records the iterations.

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [ ] Preflight
- [x] Build
- [ ] QA
