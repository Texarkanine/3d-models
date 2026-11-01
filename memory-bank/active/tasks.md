# Task: commercial-electric-wire-stripper-curved-grip (rework 3: a bigger bevel)

## Fix

- **What was short:**
    - Iteration 3 (`c585867`) rounded the bed edge with a circle that touched the bed's plane, so the bevel was a by-product of `RIM_R`. It reached the widest point 0.75 above the bed, about 4 layers.
    - Its bed edge sat only 0.42 in from the widest point.
- **What changed:** `BEVEL` is a parameter: how far the edge on the bed comes in from the flare's full width.
    - A straight bevel rises from the edge at `BEVEL_ANGLE` (renamed from `RIM_ANGLE`).
    - The round `RIM_R` now touches the bevel and the flare, not the bed.
    - Iteration 3's shape is this construction with `BEVEL` about 0.76.
    - New helper `corner_wall(grow)`, used by the body check (at least 2.0) and by a new first-layer check (at least 1.2, three extrusion lines).
    - `check_design` also asserts that the outline's d rises strictly, so the bevel and round fit between the bed and `FLARE_LEN`.
    - The old assertion "foot on or outside the body wall" is dropped: the operator asked for the edge to come further in.
- **Unchanged:** the flare, the bore, ribs, roof, dome and `FIT_LEN`.
- **Failing check first:** `lip.py` now also requires the widest point at least 1.2 above the bed (6 layers), and the bed edge at least 0.8 in from it. Iteration 3's STL fails both (0.75; 0.42). The new STL passes.

## Files

- `models/commercial-electric-wire-stripper-grips/grips.py`
- `models/commercial-electric-wire-stripper-grips/curved_grip.{step,stl}`, `curved_grip_fit_test.{step,stl}` (regenerated)
- `models/commercial-electric-wire-stripper-grips/memory-bank/systemPatterns.md` (bevel, first-layer wall, history)
- `models/commercial-electric-wire-stripper-grips/memory-bank/techContext.md` (lofts and assertions)

## Verification

- **`lip.py`:**
    - bed edge 130 degrees;
    - edge on the bed −0.50 from the body wall, 0.97 in from the widest point;
    - widest 0.47 at 1.5 above the bed (the profile gives 1.46, about 7 layers);
    - straight bevel up to 0.94;
    - above the widest it falls at most 0.24 per mm;
    - on the body by `FLARE_LEN`.
- **`verify.py`:**
    - steel inside the bore wall 0 mm³;
    - rib bites 38.7 mm³ against 38.6;
    - corner gap at least 0.213;
    - thinnest wall 1.393, on the first layer over the bore corners, as `corner_wall` predicts (the body is still 2.05);
    - cap 5.0;
    - both STLs watertight, standing on z = 0;
    - the fit test matches the grip cut at `FIT_LEN`;
    - footprint 128 mm² (prints 1, 2 and 3: 231, 164 and 180). Tell the operator: a brim may be needed on the 92 mm part.
- **`tools/overhang.py`:** only the roof's ridge strip (2.9 mm²); nothing on the fit test.
- **Close-up render** (`.scratch/wirestripper-grip/render-open-end.png`): a clear straight bevel rounding into the flare, matching on the W and T sides.
- **Catalog suite:** 88 OK.

## QA (2026-11-01, rework 3): FAIL (fixable; Build reruns)

Reviewed commit `efac921` against the "Rework 3" section of `projectbrief.md`.

### Blocking

- **Q3: at the four corners the bevel is 43.4 degrees, not `BEVEL_ANGLE`.** That is under the design's 45 degree rule, and `check_design` still passes.
    - **Cause:** `outside()` builds every section with corner radius `CORNER_R + max(grow, 0.0)`. That rule was written for the dome, where grow goes down to −`DOME_LEN`. This build is the first to start the rim inside the body wall (grow −0.5 on the bed). Below the body wall the corner radius stays `CORNER_R`, so the corners move in about 1.41 times as far as the flat sides. The first ruled segment, from grow −0.5 to +0.29 over 0.94 of height, is therefore 50 degrees on the flats but 43.3 on the diagonals.
    - **Measured on the committed STL:** 116 outer faces (19 mm²) under 45 degrees, at z 0.31 to 0.63, all at the four diagonals. The flat sides are 50.0. Iteration 3 (`c585867`) is 49.9 to 50.9 all round, because its grow never went below zero.
    - **It gets worse as `BEVEL` grows,** which the build's insight says is now the one number to tune:

        | `BEVEL` | edge on the bed | corner bevel | first-layer corner wall | `check_design` |
        | --- | --- | --- | --- | --- |
        | 1.00 | +0.00 | 50.0 | 2.05 | passes |
        | 1.25 | −0.25 | 45.5 | 1.73 | passes |
        | 1.50 (built) | −0.50 | 43.3 | 1.39 | passes |
        | 1.75 | −0.75 | 42.1 | 1.06 | fails (wall) |

        A sweep of 964 sets of `BEVEL`, `BEVEL_ANGLE`, `RIM_R`, `FLARE` and `FLARE_LEN` that `check_design` accepts found 258 with a corner bevel under 45 degrees. The worst was 35.3. `tools/overhang.py` flags only faces flatter than about 42.5 degrees, so it does not catch today's 43.4.
    - **The docs are wrong at the corners.** The model's `systemPatterns.md` says the bevel rises at `BEVEL_ANGLE`, that below 45 degrees it would need support, and that `check_design` asserts this. At the corners, neither the angle nor the guard holds.
    - **Fix (Build chooses):**
        - Preferred: give the rim's sections a true offset, with corner radius `CORNER_R + grow` also below zero, and make `corner_wall` match. The bevel is then `BEVEL_ANGLE` all round, and the first-layer corner wall rises from 1.39 to about 1.55. The dome keeps `max(grow, 0)`, since its grow reaches −5.
        - Alternative: keep the rounder corners, and extend the assertion and the docs to the corner angle.

      Either way, regenerate the outputs and re-run the checks, including a check of the corners.
    - **Why the build's checks missed it:** `lip.py` measures only the T extent (the flat sides), and the render was compared on the W and T sides only.

### How each rework 3 requirement stands

1. **A taller bevel, with the edge on the bed further in.** Met. `lip.py`: 130 degrees at the bed edge; the edge is −0.496 from the body wall and 0.968 in from the widest point; widest 0.473 at z 1.50. Iteration 3's STL fails both new conditions (widest at z 0.75; edge 0.421 in).
2. **Print 1's flare above it, the round between, no supports, `CONVEX_LIMIT`.** Met on the flats. Above z ≈ 1.75 the outline matches iteration 3's to 0.001. The wall facing the other handle is 4.27, against the 5.0 limit. No supports by `tools/overhang.py`. The corners, however, break the design's own 45 degree rule (Q3).
3. **Enough first-layer wall.** Met: 1.393 over the bore corners, asserted at least 1.2. The flat T face is 1.7.
4. **Bore, ribs and dome unchanged; its own commit.** Met. The diff leaves `bore()`, `ribs()`, `roof()`, the dome, `steel.py` and `FIT_LEN` alone. The iteration is in `efac921`, like iteration 3 in `c585867`.

### What QA checked independently

- **Rebuild** in the scratchpad, in 22 s:
    - both STLs are byte-identical to the committed files;
    - the STEP files differ only in the `FILE_NAME` timestamp;
    - `sizes()` prints the build's figures.
- **`lip.py`:** FAIL on iteration 3's STL, PASS on the new one. The numbers are given under requirement 1.
- **`rim_profile()` maths:**
    - the bevel's line, the touch condition (`gap`) and the 130 degree start angle are correct;
    - in all 964 accepted sets of the sweep, the round leaves the bevel exactly on its line, and no outward segment of the profile is flatter than `BEVEL_ANGLE`;
    - the new "d rises strictly" assertion catches both ways the bisection can fail to bracket a touch point.
- **`verify.py`:** reproduces the build's numbers:
    - 0 mm³ of steel in the bore wall;
    - rib bites 38.7 against 38.6;
    - thinnest wall 1.393;
    - cap 5.0;
    - watertight STLs;
    - footprint 128 mm²;
    - the fit test matches the grip cut at `FIT_LEN`.
- **Corner angles:** a face-normal scan of the outer faces below z 2.5, in 15 degree sectors around the part. This scan found Q3.
- **`tools/overhang.py`:** the 2.9 mm² ridge strip only; nothing on the fit test.
- **Catalog suite:** 88 OK.
- **Code quality:**
    - `corner_wall()` removes the duplicated corner formula, and is used by `check_design` and `sizes()`;
    - no `RIM_ANGLE` is left anywhere;
    - the README and `publish.yaml` need no change.

### Non-blocking advisories

- **A-19 (tell the operator).** The flute's widest point drops from 0.66 (iteration 3) to 0.47. Print 1 was 1.0 on the bed. Above z ≈ 1.75 the outline is unchanged, so the hand meets the same flare, with a lower lip.
    - The build reported 0.47, but not the comparison.
    - "A little bit more" became about twice the layers, and the edge moved in 0.74. It is one number to retune.
    - If the flute feels weaker, `FLARE` has 0.2 of headroom under `CONVEX_LIMIT` (3.8 + 1.2 = 5.0).
- **A-20 (print).** The footprint is down to 128 mm² (prints 1, 2 and 3: 231, 164 and 180). A brim may be needed on the 92 mm part. Add it to `publish.yaml`'s manufacturing notes only if the print shows it is needed.
- **A-21 (print record, as A-18).** Add a model SumMem note "Iteration 4 = <commit>" once the fix for Q3 is committed. `efac921` will no longer be the printable iteration.

## Build (rework 3, after QA FAIL): Q3 fixed

- **Cause:** `outside()` gave every section the corner radius `CORNER_R + max(grow, 0)`. Below the body wall that holds the radius while the flats come in, so the corners move in about 1.41 times as far. The bevel at the corners was 43.4 degrees.
- **Fix:** the open end's sections are a true offset, with corner radius `CORNER_R + grow`. The body and the dome keep `CORNER_R`; the dome's radius is still capped by `rrect` as it shrinks. `corner_wall(grow)` uses the same true offset, so the first-layer wall over the bore corners is 1.55 (it was 1.39).
- **Failing check first:** `.scratch/wirestripper-grip/corner_bevel.py` (QA's `corner_bevel.py`, now with a pass/fail line) scans the face normals all round near the bed. On `efac921`'s STL it fails: 43.4 degrees at a corner, 116 faces under 45. After the fix it passes, at 49.9 to 52.3 degrees in every 15-degree direction.
- **Re-verified:**
    - `lip.py` passes: unchanged on the T side.
    - `verify.py`:
        - steel 0 mm³ in the wall;
        - rib bites 38.7 mm³;
        - thinnest wall 1.553, on the first layer;
        - cap 5.0;
        - watertight STLs;
        - footprint 132 mm²;
        - the fit test matches.
    - `tools/overhang.py`: only the ridge strip.
    - Catalog suite: 88 OK.
- **Docs:** `systemPatterns.md` states the true-offset rule and why the dome differs. `techContext.md` adds the all-round normal scan to the useful ad hoc checks.

## QA (2026-11-01, rework 3, run 2): PASS

Reviewed commit `87e777c` (the fix for Q3) against QA run 1's findings and the "Rework 3" section of `projectbrief.md`.

### Q3: resolved

- `outside()` now builds the open end's sections as a true offset (corner radius `CORNER_R + grow`). The body and the dome keep `CORNER_R`, as before. `corner_wall(grow)` uses the same offset.
- **All-round normal scan** (`corner_bevel.py`):
    - the new grip and the fit test are 49.9 degrees at the least, in every 15 degree direction;
    - `efac921` fails at 43.4, and iteration 3 (`c585867`) passes at 49.9.
- **A separate check by QA** (`offset_check.py` in the QA scratchpad): each slice in the bevel is compared with the slice below it, at 720 points round the outline.
    - The step outward is the same all round: within 3.5 %, and that 3.5 % comes from the part's lean. That gives a slope of 49.9 to 50.9 degrees.
    - On `efac921` the step at the corners was 1.30 times the step on the flats, a slope of 43.4 degrees.
- **The change stays in the bevel:** slices of the new STL and of `efac921` are identical from z 0.95 up to the dome, bore included (symmetric difference 0.0002 mm² or less). Only the first ruled segment changed, from the bed to the bevel's top at 0.94.
- **The fix holds for any accepted parameters:** a sweep over 4,846 parameter sets that `check_design` accepts found none where:
    - a rim corner radius reaches zero;
    - `rrect`'s cap shortens a rim corner (which would break the true offset).

    So `BEVEL_ANGLE >= 45` now also guards the corners.
- **Docs:** `systemPatterns.md` states the true-offset rule and why the dome is different. `techContext.md` adds the all-round scan to the useful checks. The README and `publish.yaml` need no change.

### How each rework 3 requirement stands

1. **A taller bevel, with the edge on the bed further in.** Met. `lip.py`: 130 degrees at the bed edge; the edge is −0.496 from the body wall and 0.968 in from the widest point; widest 0.473 at z 1.50.
2. **Print 1's flare above it, the round between, no supports, `CONVEX_LIMIT`.** Met, now all round:
    - the bevel is at least 49.9 degrees in every direction;
    - `tools/overhang.py` flags only the roof's ridge strip (2.9 mm²), and nothing on the fit test;
    - the wall facing the other handle is 4.27, against the 5.0 limit.
3. **Enough first-layer wall.** Met:
    - 1.553 over the bore corners, measured by `verify.py`, against 1.55 from `corner_wall`;
    - asserted at least 1.2.
4. **Bore, ribs and dome unchanged; its own commit.** Met:
    - `bore()`, `ribs()`, `roof()`, the dome, `steel.py` and `FIT_LEN` are untouched;
    - slices above the bevel are identical to `efac921`;
    - iteration 4 is commit `87e777c`.

### What QA checked independently

- **Rebuild** in the scratchpad (24 s): both STLs are byte-identical to the committed files, and the STEP files differ only in the `FILE_NAME` timestamp. `sizes()` prints the build's figures.
- **`verify.py`:**
    - steel inside the bore wall 0 mm³;
    - rib bites 38.7 mm³ against 38.6;
    - corner gap at least 0.213;
    - thinnest wall 1.553;
    - cap 5.0;
    - both STLs watertight, standing on z = 0;
    - footprint 132 mm²;
    - the fit test matches the grip cut at `FIT_LEN` (2479 against 2480 mm³).
- **`corner_wall()`:** where its corner-arc assumption holds (the outside corner's centre lies inside the bore corner's centre in both directions), a shapely distance check matches it to 0.00003. Otherwise it reports less material than there is, so it is a safe lower bound. That is true of the body check too, and it predates this fix.
- **Catalog suite:** 88 OK.

### Non-blocking advisories

- **A-19, A-20, A-21 still stand.**
    - A-19: tell the operator that the flute's widest point is 0.47, against iteration 3's 0.66.
    - A-20: the footprint is now 132 mm² (it was 128); a brim may be needed.
    - A-21: add the model SumMem note "Iteration 4 = `87e777c`" at wrap-up.
- **A-22 (docs wording).** The new bullet in the model's `systemPatterns.md` ends with process history: "That happened in iteration 4's first build (`efac921`), and QA caught it."
    - "Iteration 4" is not defined in the History list just above it, which stops at iteration 3.
    - The rule and the reason for it are the lasting part.
    - Either drop the sentence, or add iteration 4 to the History list and point to it.
- **A-23 (docs, older than this fix).** The "Print orientation" paragraph of the model's `systemPatterns.md` says a bevel under 45 degrees would be flagged by `tools/overhang.py`.
    - Its `LIMIT` (cos 45° + 0.03) flags only faces flatter than about 42.6 degrees, which is why `efac921`'s 43.4 went unflagged.
    - The guard that holds is `check_design` plus the true offset.
    - Reword: `tools/overhang.py` flags under about 43 degrees, and the all-round normal scan checks the bevel itself.
- **A-24 (code, optional).** In `corner_wall`, `grow` cancels out of `gap_u` and `gap_v`, so the result is `corner_wall(0) + grow`. That is correct, and the current form follows the geometry, so no change is needed. A docstring line could say that it is a lower bound when the corner-arc assumption fails.

### Advisories resolved after QA (rework 3, run 2)

- **A-19, A-20:** told the operator: the widest point is 0.47 (iteration 3: 0.66), and the 132 mm² footprint may need a brim.
- **A-21:** the model's SumMem records "Iteration 4 = `87e777c`". `efac921` is its flawed first build and is not to be printed.
- **A-22:** the `efac921` history moved into the History list as part of iteration 4. The true-offset point now states only the rule and the reason.
- **A-23:** `systemPatterns.md` now says that `check_design` guards the 45-degree rule, and that `tools/overhang.py` flags only faces flatter than about 43 degrees.
- **A-24 (optional):** not taken. The `corner_wall` docstring is unchanged, so no rebuild was needed.
