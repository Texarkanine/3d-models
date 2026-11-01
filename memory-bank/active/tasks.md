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
