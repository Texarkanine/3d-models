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
