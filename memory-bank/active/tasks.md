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
