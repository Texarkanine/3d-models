# System Patterns

## How This System Works

The operator's measurements of the bare steel are the source data. `steel.py` is the one home of the numbers the model uses. `reference/measurements.md` is the dated log of how and when each reading was taken, with the photos. Add new readings to both: the log gets a dated entry, and `steel.py` gets the value in use.

`grips.py` builds a grip from a `steel.Handle`: centre line, W and T along it, and the length A to B. It never assumes curvature. A straight handle is a `Handle` with a constant centre line, so the straight grip reuses the same builder with new steel data.

## Names for places on a handle

- **A** is the tip of the bare steel. Every length along a handle is measured from A.
- **B** is where the old grip's open end sat. The new grip covers the steel from A to B.
- **W** is the steel's width in the plane the handles swing in, which is across the handle when the tool lies flat. **T** is its thickness at right angles to that plane, straight up off the table.
- **D1, D2** are holes through the steel. **S1 to S3** are the stations where W and T were measured.
- **s** is distance along the centre line from A. The calipers and ruler measure straight lines, so `steel.py` stores each reading as a chord and converts it to s. B is at s = `Handle.length` (83.58 on the curved handle), not at the 83.15 measured straight from A. Anything placed "at B" must use `Handle.length`.

## The curved handle

- The steel tapers from about 6.3 × 13.9 (W × T) at A to about 9.7 × 14.3 at B. It is an open channel, filled with a hard ribbed plastic insert that belongs to the tool. The grip fits over the outside of the whole thing.
- It bends about 15 degrees between A and B, in the plane the handles swing in. Its centre line is never more than 3.8 mm from a straight line drawn from A to B. Most of the bend is between 20 and 70 mm from A.
- The curve comes from offsets the operator measured on a pencil tracing. `steel.py` fits a quartic centre line to the traced centre points (worst miss 0.08 mm) and takes W and T from the calipers, linear between the stations. The traced widths agree with the calipers to within about 0.7 mm. The biggest unknown is W at B: the calipers, extended past S3, give 9.7, while the tracing gives 10.25.
- With the tool squeezed shut and the old straight grip on, the gap at B is 9 mm. That is the room for the curved grip's wall on the side facing the straight handle. The old grip's wall there was 5 mm.

## How a grip fits

- The bore is the steel plus `BORE_CLEAR` (0.3) on every side, with tight corners (radius 0.5), so even a sharp steel corner clears it by 0.2.
- Eight lengthwise ribs, two on each face near the corners, reach `RIB_BITE` (0.1) past the steel face. They are glue keys, not crush ribs. They locate the grip, and the 0.3 valleys between them give glue something to fill and key into, which survives vapor-smoothing. Glue and air escape along the valleys while the grip is pushed on. Whether a grip also holds dry is for the test prints to show.
- The ribs sit `RIB_INSET` (1.5) from the corners, so they bear on solid steel near the edges rather than on the insert. A rib may cross the edge of a hole; that only loses contact over 3 mm.
- The bore runs `END_CLEAR` (1.0) past A, so the steel bottoms out at B, not at the roof.

## The outside

- Walls are measured from the steel face, not from the bore, so retuning the bore never moves the outside. `WALL_SIDE` (3.8) is in the plane of the handles, and `WALL_FACE` (2.5) is across it. Corners are rounded with `CORNER_R` (4.8), which leaves at least 2 mm over each bore corner.
- It flares by `FLARE` (1.0) over the last `FLARE_LEN` (5) at the open end. On the side facing the other handle, the wall at B is therefore 4.8, under the 5 mm the closed tool allows. Constant walls keep the closest approach to the other handle at B, where the gap was measured.
- The grip is the same on both sides in W and in T. That is load-bearing: it makes a mirrored tracing harmless.
- The dome starts at the height of the bore's roof ridge and shrinks along a quarter circle of radius `DOME_LEN` (5). So the wall over the roof is never thinner than the body's, and the cap over the ridge is `DOME_LEN`.

## Print orientation is designed in

Each grip prints standing up, open end down on the bed, closed end at the top. The grip leans with the steel's curve, about 15 degrees at the tip. The flare is widest on the bed. The bore's closed end is a gable roof whose two slopes are `ROOF_ANGLE` (50 degrees) above horizontal in print, computed from the actual lean. The only face that `tools/overhang.py` flags is the 0.2 mm ridge strip at its top, which is narrower than one extrusion line. No supports are needed.

## Test prints

The fit test (`FIT_LEN` 15 mm of the open end) checks the bore on the steel near B, where the steel is widest. Slide it on from the tip up to B. It does not test the curve; the full grip does. Record each test print's outcome as a SumMem note for this model: what was printed, how it went on, how it held, and what changed.
