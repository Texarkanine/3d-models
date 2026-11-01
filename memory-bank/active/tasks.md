# Task: commercial-electric-wire-stripper-curved-grip (rework 2: flare plus a rounded bevel)

## Fix

- **What was wrong:**
    - Print 1 (`95e5f61`) had the flare the operator likes, but its edge on the bed was sharp (71 degrees inside the part).
    - Print 2 (`da750d8`) fixed the edge with a bead, but lost the flare: above its crown it fell back at 0.98 per mm.
- **What changed:** the flare (`FLARE`, `FLARE_LEN`) is back, and only its edge on the bed is rounded.
    - `RIM_R` is a round that touches the bed's plane and the flare.
    - Below the point where the round slopes at `RIM_ANGLE`, a straight bevel runs down to the bed (`grips.rim_profile`).
    - The open end, from the bed to `FLARE_LEN`, is a ruled loft of closely spaced sections (`RIM_STEP`) fused to the smooth body loft.
    - `check_design` asserts:
        - `WALL_SIDE + FLARE` against `CONVEX_LIMIT`;
        - `RIM_R < FLARE_LEN`;
        - the bevel's foot on or outside the body wall;
        - `RIM_ANGLE >= 45`.
    - `sizes()` reports the edge on the bed, the widest point and the wall there.
- **Unchanged:** the bore, ribs, roof, dome and `FIT_LEN`.
- **Failing check first:** `.scratch/wirestripper-grip/lip.py` now also requires the widest point within 2 mm of the bed, and above it a fall of at most 0.5 per mm (a flute, not a bead).
    - Print 1's STL fails it (bed edge 71 degrees, widest on the bed).
    - Print 2's STL fails it (falls 0.98 per mm).
    - The new STL passes.

## Files

- `models/commercial-electric-wire-stripper-grips/grips.py`
- `models/commercial-electric-wire-stripper-grips/curved_grip.{step,stl}`, `curved_grip_fit_test.{step,stl}` (regenerated)
- `models/commercial-electric-wire-stripper-grips/memory-bank/systemPatterns.md` (flare plus rim, and the history of the three prints)
- `models/commercial-electric-wire-stripper-grips/memory-bank/techContext.md` (ruled loft, assertions, slice check)

## Verification

- **`lip.py`:**
    - Bed edge 130 degrees; 0.24 out on the bed.
    - Widest 0.66 at 0.75 above the bed. Above that it falls at most 0.29 per mm.
    - On the body wall by `FLARE_LEN`.
    - Above about 1 mm, the outline is print 1's flare exactly.
- **`verify.py`:**
    - steel inside the bore wall 0 mm³;
    - rib bites 38.7 mm³ against 38.6;
    - corner gap at least 0.213;
    - thinnest wall 2.053;
    - cap over the ridge 5.0;
    - both STLs watertight, standing on z = 0;
    - the fit test matches the grip cut at `FIT_LEN`;
    - footprint 180 mm² (print 1: 231; print 2: 164).
    - The W wall at s = 76.85 reads 3.782 against 3.800. That is ringing in the smooth body loft, whose sections moved when the body loft started at `FLARE_LEN` again. It is 0.02, far under a line width.
- **`tools/overhang.py`:** only the roof's ridge strip (2.9 mm²); nothing on the fit test.
- **Close-up render** (`.scratch/wirestripper-grip/render-open-end.png`): the flare, with the rounded and bevelled edge on the bed, matching on the W and T sides.
- **Catalog suite:** 88 OK.

## QA (2026-11-01, rework 2): PASS

Reviewed commit `c585867` against the "Rework 2" section of `projectbrief.md`.

How each rework 2 requirement is met:
1. **Print 1's flare is back.** `flare()` is print 1's quadratic, with the same `FLARE` and `FLARE_LEN`. Above the round's touch point (1.04 from B), `rim_profile()` follows it exactly.
2. **Only the edge on the bed is rounded, over a small printable bevel.**
    - The round is `RIM_R` 0.8, over a 50 degree bevel. The bed edge is 130 degrees inside the part, the same as print 2's, which the operator liked.
    - It changes the outline only within about 1 mm of the bed.
3. **No supports, and the wall stays within `CONVEX_LIMIT`.**
    - The wall facing the other handle is 4.46 at its widest. `check_design` asserts the bound `WALL_SIDE + FLARE`, which is 4.8, within `CONVEX_LIMIT`.
    - `tools/overhang.py` flags only the 2.9 mm² ridge strip, as before.
4. **The bore, ribs and dome are unchanged.** The diff leaves `bore()`, `ribs()`, `roof()`, the dome, `steel.py` and `FIT_LEN` alone.
5. **Iteration 3 is its own commit** (`c585867`). Prints 1 and 2 stay at `95e5f61` and `da750d8`.

What QA checked independently:
- **Rebuild:** a scratch rebuild in 22 s.
    - Both STLs are byte-identical to the committed files.
    - The STEP files differ only in the `FILE_NAME` timestamp.
    - `sizes()` prints:
        - 0.24 out on the bed;
        - widest 0.66 at 0.80 from B;
        - wall 4.46 against the 5.0 limit.
- **Red, then green:** `lip.py` gives:
    - print 1's STL: FAIL (bed edge 71 degrees, widest on the bed);
    - print 2's STL: FAIL (it falls back at 0.98 per mm);
    - the new grip and fit-test STLs: PASS (bed edge 130 degrees; widest 0.663 at z 0.75; falls at most 0.29 per mm).
- **`rim_profile()` maths, checked by hand and numerically:**
    - The construction circle's centre sits `RIM_R` above the bed.
    - The circle is tangent to the flare at the touch point.
    - The bevel leaves it tangent, at exactly `RIM_ANGLE`.
    - d rises strictly along the outline, and the outline ends at (`FLARE_LEN`, 0).
    - No segment that leans outward is flatter than `RIM_ANGLE`.
- **Parameter sweep:** QA tried every combination of these values:
    - `RIM_R` from 0.2 to 4.9;
    - `RIM_ANGLE` from 45 to 89;
    - `FLARE` from 0.3 to 2;
    - `FLARE_LEN` from 3 to 8.

  Whenever `check_design` accepts a combination, the outline is valid. The two new assertions (`RIM_R < FLARE_LEN`, and the bevel's foot on or outside the body wall) are the right guards: the first is exactly what the bisection needs to find a touch point.
- **Walls square to the centre line:**
    - Over 99 sections in the rim, the built outside matches `WALL + rim_profile()` to 0.0000.
    - Over 158 body sections, it is within 0.019 of design: at most −0.019 on the W side at d ≈ 6, where the smooth body loft rings after the rim ends. The build reported this. It is a twentieth of a layer, and accepted.
- **`verify.py`:** gives the same numbers as the build:
    - 0 mm³ of steel in the bore wall;
    - rib bites 38.7 against 38.6;
    - thinnest wall 2.053;
    - cap 5.0;
    - watertight STLs;
    - footprint 180 mm²;
    - the fit test matches the grip cut at `FIT_LEN`.
- **Catalog suite:** 88 OK.
- **No leftovers:** no `LIP`, `lip_profile` or lip wording remains in the model's code or docs, apart from the deliberate history in `systemPatterns.md`. `publish.yaml` and the README needed no change.

### Non-blocking advisories

- **A-15 (DRY, minor).** `rim_profile()`'s inner `slope()` is the derivative of `flare()`, written out by hand. If the flare's shape changes, both must change, and nothing would catch a mismatch: the round would no longer be tangent, and the result would be a small crease. A docstring saying "derivative of `flare()`" would tie them together.
- **A-16 (a build claim to state precisely in the reflection).** The build's line "Above about 1 mm, the outline is print 1's flare exactly" is true of the design (`flare()`), not of print 1's printed file. Print 1 lofted four sections smoothly, and its STL sat outside its own quadratic:
    - by up to 0.045 between 1.25 and 3 mm (z 2.25: print 1 0.348, quadratic 0.303, new 0.307);
    - by 0.02 to 0.03 past `FLARE_LEN`.

  So iteration 3 is up to 0.045 slimmer than print 1 in that band. That is about a tenth of a line width and should not be felt, but the record should say "print 1's designed flare".
- **A-17 (wording, the same class as A-8).** In the model's `systemPatterns.md`, "The round trims the widest point a little below that" depends on `RIM_R` against `FLARE`. At the current values it trims a third (1.0 to 0.66). `sizes()` already prints the figure, so "a little" can go.
- **A-18 (print record, for requirement 5).** When the operator prints iteration 3, add a model SumMem note "Print 3 = <commit>", as was done for prints 1 and 2. Today that commit is `c585867`. If any wrap-up edit regenerates the outputs, the commit printed will be a later one.

### Advisories resolved after QA (rework 2)

- **A-15:** `flare(d)` now returns the extra wall and its slope together, so the two cannot drift apart. The rebuilt STLs are byte-identical, and the STEP files changed only in their header, so they were restored.
- **A-16:** the claim is corrected. Above about 1 mm, the outline is print 1's *designed* flare. Print 1's STL sat up to 0.045 outside its own quadratic, because a smooth loft was used.
- **A-17:** `systemPatterns.md` drops "a little"; `grips.py` prints the actual figure.
- **A-18:** iteration 3 (`c585867`) is recorded in the model's SumMem. The operator reviewed it in CAD and asked for a bigger bevel before printing, so it goes into rework 3.
