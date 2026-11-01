# System Patterns

## How This System Works

Each fact has one home:
- **Readings of the bare steel** live in `steel.py`, which prints them and their cross-checks when run. `reference/measurements.md` is the dated log of how and when each reading was taken, with the photos. A new reading goes into both: a dated entry in the log, and the value in use in `steel.py`.
- **Design values** live in `grips.py` as named parameters at the top. It prints the main sizes on each run.
- **This file** holds the reasoning behind them. It names parameters but does not copy their values, so it stays true when a test print retunes one.

`grips.py` builds a grip from a `steel.Handle`: centre line, W and T along it, and the length A to B. It never assumes curvature. A straight handle is a `Handle` with a constant centre line, so the straight grip reuses the same builder with new steel data.

## Names for places on a handle

- **A** is the tip of the bare steel. Every length along a handle is measured from A.
- **B** is where the old grip's open end sat. The new grip covers the steel from A to B.
- **W** is the steel's width in the plane the handles swing in, which is across the handle when the tool lies flat. **T** is its thickness at right angles to that plane, straight up off the table.
- **D1, D2** are holes through the steel. **S1 to S3** are the stations where W and T were measured.
- **s** is distance along the centre line from A. The calipers and ruler measure straight lines, so `steel.py` stores each reading as a chord and converts it to s. On a curved handle, B is at s = `Handle.length`, which is longer than the straight distance measured from A. Anything placed "at B" must use `Handle.length`.

## The curved handle

- The steel tapers toward A, strongly in W and barely in T. It is an open channel, filled with a hard ribbed plastic insert that belongs to the tool. The grip fits over the outside of the whole thing.
- It bends about 15 degrees between A and B, in the plane the handles swing in. Most of the bend is in the middle; both ends are nearly straight.
- The curve comes from offsets the operator measured on a pencil tracing. `steel.py` fits a quartic centre line to the traced centre points and takes W and T from the calipers, linear between the stations and extended past them. Take the shape from the tracing and the sizes from the calipers.
- The biggest unknown is W at B. It lies beyond the last caliper station, and the tracing there reads wider than the calipers' trend. `python steel.py` prints both.
- With the tool squeezed shut and the old straight grip on, the gap at B is 9 mm. That is the room for the curved grip's wall on the side facing the straight handle. The old grip's wall there was 5 mm.

## How a grip fits

- The bore is the steel plus `BORE_CLEAR` on every side. Its corners (`BORE_CORNER_R`) are tight enough that even a sharp steel corner clears the bore by at least 0.15; `check_design` asserts it.
- Eight lengthwise ribs, two on each face near the corners, reach `RIB_BITE` past the steel face. They are glue keys, not crush ribs (the operator's direction, 2026-10-31). They locate the grip. The valleys between them, `BORE_CLEAR` deep, give glue something to fill and key into, and they survive vapor-smoothing. Glue and air escape along the valleys while the grip is pushed on. Whether a grip also holds dry is for the test prints to show.
- The ribs sit `RIB_INSET` from the corners, so they bear on solid steel near the edges rather than on the insert. A rib may cross the edge of a hole; that only loses contact over the hole's width.
- The bore runs `END_CLEAR` past A, so the steel bottoms out at B, not at the roof.

## The outside

- Walls are measured from the steel face, not from the bore, so retuning the bore never moves the outside. `WALL_SIDE` is in the plane of the handles, and `WALL_FACE` is across it. `CORNER_R` rounds the corners and must leave at least 2 mm over each bore corner; `check_design` asserts it.
- It flares by `FLARE` toward the open end, fading out over `FLARE_LEN`. That gradual flare is what the hand meets, and the operator prefers it, as on the stock grip.
- On the bed, the open end's edge sits `BEVEL` in from the flare's full width. A straight bevel rises from there at `BEVEL_ANGLE`, and a round of radius `RIM_R` blends it into the flare. The edge is neither sharp nor overhanging, and the bevel is tall enough to see and feel. `BEVEL` may bring the edge inside the body wall. `check_design` keeps at least three extrusion lines over the bore's corners on the first layer, and `grips.py` prints the figure. History (2026-11-01):
    - Print 1's flare ran out to the bed and left an acute, sharp edge there.
    - Print 2 swapped the flare for a bead that bulged out and back in. The edge was good, but the flare was lost.
    - Iteration 3 (`c585867`, not printed) kept the flare and rounded its bed edge with a circle that also touched the bed. That left only a few layers of bevel; the operator asked for more, brought further in.
    - The design now sets the bevel directly with `BEVEL`. Iteration 3's shape is the same construction with a smaller `BEVEL`.
- `grips.rim_profile` gives the open end's outline, from the bed to `FLARE_LEN`. It is a ruled loft of closely spaced sections; a smooth loft would ring through the round.
- The open end is a true offset of the body: its corner radius grows and shrinks with the walls (`CORNER_R` plus the outline's grow). The bevel then keeps `BEVEL_ANGLE` at the corners as well as on the flats. Holding the corner radius while the walls come in moves the corners in about 1.4 times as far, and flattens the bevel there below 45 degrees. That happened in iteration 4's first build (`efac921`), and QA caught it. The dome is different: it keeps `CORNER_R`, capped by `grips.rrect` as it shrinks.
- On the side facing the other handle, the wall at the open end is at most `WALL_SIDE + FLARE`. It must stay within the 5 mm the closed tool allows (`CONVEX_LIMIT`, asserted). The bevel and round trim the widest point below that, and `grips.py` prints the actual figure. Constant walls keep the closest approach to the other handle at the open end, where the gap was measured.
- The grip is the same on both sides in W and in T. That is load-bearing: it makes a mirrored tracing harmless.
- The dome starts at the height of the bore's roof ridge and shrinks along a quarter circle of radius `DOME_LEN`. Starting it any lower thins the T wall at the ridge's ends below the body's. The cap over the ridge is then `DOME_LEN`, at least `END`.

## Print orientation is designed in

Each grip prints standing up, open end down on the bed, closed end at the top. The grip leans with the steel's curve, most at the tip. The open end's bevel rises at `BEVEL_ANGLE` above horizontal. Below 45 degrees it would need support, and `tools/overhang.py` would flag it; `check_design` asserts it. The bore's closed end is a gable roof whose two slopes are `ROOF_ANGLE` above horizontal in print, computed from the actual lean. The only face `tools/overhang.py` flags is the ridge strip at the roof's top. `RIDGE_W` must stay narrower than one extrusion line, so the perimeters close it. No supports are needed.

## Test prints

The fit test (`FIT_LEN` of the open end) checks the bore on the steel near B, where the steel is widest. Slide it on from the tip up to B. It does not test the curve; the full grip does. Record each test print's outcome as a SumMem note for this model: what was printed, how it went on, how it held, and what changed.
