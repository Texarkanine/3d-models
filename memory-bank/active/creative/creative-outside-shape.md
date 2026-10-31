# Decision: Outside shape

## Context

**What:** The outside of the grip: its cross-section, how its size runs along the length, and what the open and closed ends look like. The straight grip will later use the same definition on different steel.

**Why it matters:** The outside is what the hand feels, what has to clear the other handle when the tool closes, and what stands on the bed while it prints. Once a grip ships, changing the outside is a new release and a reprint.

**Constraints:**
- On the convex side, which faces the straight handle, the wall at B is at most 5.0 mm from the steel face. The old grip's was 5 mm from its bore.
- It prints open end down and leans up to about 15 degrees, without support. Every outside face must narrow going up or overhang by less than 45 degrees.
- It must also work for the straight grip: the definition has to be relative to whatever steel it wraps, not drawn around the curved handle.
- It is comfortable and close in feel to the original. The operator likes the tool; a better outside is welcome but not required.
- The old curved grip at its open end measures about 20 × 20.7 outside: wall 5 in the plane of the handles, 3.25 across it, at a collar. The old straight grip runs from 12 to 15.1, then flares to 19.7 at its open end. Both originals are narrow at the tip and flared at the open end.
- The operator does not want tests for shapes still being prototyped, so the outside must be cheap to change after a test print.

## Options Evaluated

- **A. Steel-offset rounded rectangle:** the outside is the steel's outline grown by a set wall on each side, with large rounded corners. It follows the steel's curve and taper, with a small flare at the open end and a domed closed end.
- **B. Oval:** an ellipse around the steel, with a minimum wall at the steel's corners.
- **C. Sculpted:** a palm swell, finger grooves and a flared guard, shaped for the hand rather than the steel.

## Analysis

| Criterion | A. Offset rounded rectangle | B. Oval | C. Sculpted |
|---|---|---|---|
| Convex wall at B ≤ 5.0 | Set directly (3.8 + 1.0 flare = 4.8) | Hard. An ellipse around a 9.7 × 14.3 rectangle needs about 5 mm at the face centres just to clear the corners with 3 mm of wall | A swell can move the closest point off B, where the gap was not measured |
| Bulk | About 19 × 22 at the open end, near the original | About 20 × 27: an ellipse around a rectangle wastes a lot | Varies |
| Prints standing up | The body follows the steel's lean. The flare is widest at the bed. The dome narrows going up | Same as A | A swell's lower side overhangs gently; finger grooves have overhanging roofs |
| Works on the straight grip | Yes: same walls on other steel | Yes | Must be resculpted per handle |
| Feel versus original | Same family: narrow at the tip, flared at the open end, near-square | Rounder, rolls more in the hand | Fits some hands, fights others |
| Cost to change after a test print | A few parameters | A few parameters | Redesign |

Key insights:
- **An ellipse around a rectangle wastes material.** Keeping 3 mm over the steel's corners pushes the face walls past the 5 mm limit at B. Large corner radii on a rounded rectangle give most of an oval's comfort at a near-original size.
- **Both originals taper toward the tip and flare at the open end.** Following the steel's own taper reproduces that feel for free. The flare also gives a wider footprint for a tall print and a stop that keeps the hand off the latch.
- **The closing gap was measured at B only.** Any outside that grows on the convex side away from B relies on a gap no one measured. Constant walls are the only shape whose closest approach stays where it was measured.

## Decision

**Selected:** A. Steel-offset rounded rectangle.

**Rationale:** It is the only option that meets the 5 mm convex-side limit with margin and stays near the original size and feel. It carries over to the straight grip unchanged and can be retuned after a test print by changing numbers. It needs no shape that relies on clearance nobody measured.

**Tradeoff:** No palm swell or finger shaping. Comfort comes from rounded corners and the original's proportions, not from sculpting. Sculpting can come later, once the closing gap along the whole length is measured.

## Implementation Notes

All walls are measured from the steel face, so changing the bore clearance or ribs does not move the outside. Starting values:

- `WALL_SIDE` 3.8: the walls in the plane of the handles, on the convex and concave sides.
- `WALL_FACE` 2.5: the walls across the plane, on the faces with the holes.
- `CORNER_R` 5.0: outside corner radius. Assert at least 2 mm of material over each relieved bore corner.
- `FLARE` 1.0 per side, over the last `FLARE_LEN` 5.0 mm at the open end, widest at the open end. Assert that the convex wall at B, `WALL_SIDE + FLARE`, is at most 5.0.
- **Closed end:** domed. The sections shrink over the last few millimetres along a quarter-circle law. The dome is built from lofted sections rather than a fillet, because fillets on lofted B-spline faces are unreliable in OpenCascade. The cap stays at least `END` 3.0 thick over the peak of the bore's roof.
- **Construction:** loft the outside sections along the same centre line as the bore, then subtract the bore with its ribs.
- **Resulting size:** about 17.5 × 20 on the body near B, 19.5 × 22 at the open end, and 14.7 × 20 near the tip.
