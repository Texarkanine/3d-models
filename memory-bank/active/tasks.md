# Task: commercial-electric-wire-stripper-curved-grip (rework: round the open end)

## Fix

- **What broke:** the first TPU 95A print's open end has a sharp outer edge where it stood on the bed.
- **Why:** the outside flared by `FLARE` toward the open end, widest on the bed. The outside met the bed at about 71 degrees inside the part, an acute corner.
- **What changed:** a rounded lip replaces the flare (`LIP`, `LIP_R`, `LIP_ANGLE`, `LIP_STEP`; `grips.lip_profile`).
    - On the bed the lip starts flush with the body wall.
    - Its underside rises at `LIP_ANGLE` above horizontal to a crown of radius `LIP_R` that stands `LIP` out. A curve of the same radius blends back into the body.
    - The edge on the bed is now a 130-degree bevel.
    - The lip is a ruled loft fused to the smooth body loft. `check_design` asserts the crown's wall against `CONVEX_LIMIT` and that the underside starts no lower than the body wall. `sizes()` reports the crown.
- **Unchanged:** the bore, the ribs, the dome, `FIT_LEN`, and the convex-side wall's maximum (`WALL_SIDE + LIP` equals the old `WALL_SIDE + FLARE`).
- **Operator direction (from the first cycle):** no committed tests while the shape is iterated in meat space. The failing check is ad hoc: `.scratch/wirestripper-grip/lip.py` slices the STL above the bed. Before the fix it failed (71 degrees, widest on the bed); after it, it passes.

## Files

- `models/commercial-electric-wire-stripper-grips/grips.py`
- `models/commercial-electric-wire-stripper-grips/curved_grip.{step,stl}`, `curved_grip_fit_test.{step,stl}` (regenerated)
- `models/commercial-electric-wire-stripper-grips/memory-bank/systemPatterns.md` (the lip replaces the flare; print orientation)
- `models/commercial-electric-wire-stripper-grips/memory-bank/techContext.md` (the lip is a ruled loft; the bed-edge slice check; build time)

## Verification

- `lip.py`:
    - bed edge 130 degrees;
    - widest 0.999 at 1.75 above the bed;
    - back on the body wall by about 4, at 0.000, where the old flare left the smooth loft 0.02 to 0.03 over;
    - steepest slope 0.98 per mm. Same on the fit test.
- `verify.py`:
    - steel inside the bore wall 0 mm³;
    - rib bites 38.7 mm³ against 38.6;
    - corner gap at least 0.213;
    - thinnest wall 2.052;
    - cap over the ridge 5.0;
    - both STLs watertight, standing on z = 0;
    - the fit test matches the grip cut at `FIT_LEN`.
    - The footprint is 164 mm², down from 231, because the bed edge now sits on the body wall instead of the flare's widest point.
- `tools/overhang.py`: only the roof's ridge strip (2.9 mm²), as before. The lip's underside is not flagged.
- Close-up render, `.scratch/wirestripper-grip/render-lip.png`: the bevel, crown and blend, matching on the W and T sides.
- Catalog suite: 88 OK.

## QA (2026-11-01): PASS

Reviewed commit `36508f1` against the rework section of `projectbrief.md`.

What QA checked independently:
- **Rebuild:** QA rebuilt both parts in a scratch directory outside the repository, in 22 s. Both STLs are byte-identical to the committed files. The STEP files differ only in the `FILE_NAME` timestamp.
- **Red, then green:** `lip.py` fails on the pre-fix grip STL from `95e5f61`: 71 degrees, widest on the bed. It passes on both committed STLs, with the numbers listed above.
- **All sides, not just T:** `lip.py` reads only the T extent. A separate QA slice check also measured W and both diagonals, which cross the rounded corners. At every height from the bed to 6 mm, the STL matches `grips.lip_profile()` to within 0.01.
- **The rest unchanged (rework requirement 4):** the diff leaves `bore()`, `ribs()`, `roof()`, `steel.py` and `FIT_LEN` untouched. `verify.py` reproduces every number listed above. QA cut cross-sections square to the centre line every 0.5 mm. The body walls are within 0.012 of `WALL_SIDE` and `WALL_FACE`; the old build was within 0.015.
- **Overhangs:** `tools/overhang.py` flags only the 2.9 mm² ridge strip on the grip, and nothing on the fit test. Both are watertight.
- **Catalog suite:** 88 OK.
- **No leftovers:** no `FLARE` or `FLARE_LEN` is left in committed code or in the model's docs. The SumMem note for test print 1 is committed.

The `lip_profile()` maths is correct, checked by hand:
- The underside from (0, 0) is tangent to the crown at 180° − `LIP_ANGLE`.
- The blend circle touches the crown from outside, at angle `m`.
- The blend ends tangent to the body wall.
- The new `check_design` assertion is exactly the condition that the tangent point sits on or outside the body wall.

Building the lip as a separate ruled loft is justified. It also removed the 0.02 to 0.03 overshoot that the old flare left in the smooth body loft.

### Non-blocking advisories

- **A-10 (wording, same class as A-8).** The model's `systemPatterns.md`, under "Print orientation", says the lip's underside "overhangs at `LIP_ANGLE` above horizontal, less steeply than the 45 degrees `tools/overhang.py` flags". This has two problems:
    - The claim holds only while `LIP_ANGLE` is above 45, and nothing asserts that.
    - The sentence counts its angle from horizontal, so "less steeply" reads backward.

  Suggested fix: state it as a rule ("`LIP_ANGLE` must stay above 45 degrees, or `tools/overhang.py` flags the underside"), or add that rule as a `check_design` assertion. "The crown sits a couple of millimetres from B" also depends on the current values, and `sizes()` already prints that distance.
- **A-11 (docs).** In the model's `techContext.md`, "Testing Process" lists what the assertions in `grips.py` catch. It still says "the wall at B" and leaves out the new check that the lip's underside starts on or outside the body wall.
- **A-12 (comment).** In `lip_profile()`, the comment on `d1` says it is "the distance at which the underside from (0, 0) meets it". In fact `d1` is the crown centre's distance. The underside touches the crown lower down, at `d1 − LIP_R·cos(LIP_ANGLE)`, which is 0.77 now. Suggested wording: "placed so the underside from (0, 0) is tangent to the crown".
- **A-13 (nit).** `LIP_STEP` sets loft resolution, like `SECTION_STEP`, but it sits under "Outside" instead of "Build".
- **A-14 (operator, print risk).** The footprint on the bed drops from 231 to 164 mm² (−29 %) on a 92 mm part that leans. That follows from what the operator asked for: contact with the bed narrower than the bulge. Build already flagged it. Watch adhesion on the next print; a brim is the usual remedy.

### Advisories resolved after QA

- **A-10:** `systemPatterns.md` now states the rule:
    - below 45 degrees the lip's underside needs support, and `check_design` asserts `LIP_ANGLE >= 45`;
    - the crown's distance from B is left to `sizes()`.
- **A-11:** `techContext.md` lists the assertions on the lip's crown and underside.
- **A-12:** the `d1` comment now says the crown centre is placed so that the underside is tangent to the crown.
- **A-13:** `LIP_STEP` has moved to the Build parameters.
- **A-14:** the operator is told about the smaller footprint and the brim.
- **After the rebuild:** the STLs are byte-identical, and the STEP files changed only in their header timestamp, so they were restored.
