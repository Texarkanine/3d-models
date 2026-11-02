# System Patterns

## How This System Works

Each fact has one home:
- **Readings of the bare steel** live in `steel.py`, which prints them and their cross-checks when run. `reference/measurements.md` is the dated log of how and when each reading was taken, with the photos. A new reading goes into both: a dated entry in the log, and the value in use in `steel.py`.
- **Design values** live in `grips.py` as named parameters at the top. It prints the main sizes on each run.
- **This file** holds the reasoning behind them. It names parameters but does not copy their values, so it stays true when a test print retunes one.

`grips.py` builds a grip from a `steel.Handle`: centre line, W and T along it, and the length A to B. It never assumes curvature. A straight handle is a `Handle` with a constant centre line, so the straight grip reuses the same builder with new steel data.

## Names for places on a handle

- **A** is the tip of the bare steel. Every length along a handle is measured from A.
- **The tip's round:** both tips are rounded in the plane of the handles. `Handle.tip_r` is the radius of the tip's corners: the sides run straight up to `tip_r` from A, then round off into the tip.
- **B** is where the old grip's open end sat. The new grip covers the steel from A to B.
- **W** is the steel's width in the plane the handles swing in, which is across the handle when the tool lies flat. **T** is its thickness at right angles to that plane, straight up off the table.
- **D1, D2** are holes through the steel; D2 is the one near A on both handles. **S1 to S3** are the stations where W and T were measured on the curved handle. **J to M** are the stations where T was measured on the straight handle; M is at B.
- **s** is distance along the centre line from A. The calipers and ruler measure straight lines, so `steel.py` stores each reading as a chord and converts it to s. On a curved handle, B is at s = `Handle.length`, which is longer than the straight distance measured from A. Anything placed "at B" must use `Handle.length`.

## The curved handle

- The steel tapers toward A, strongly in W and barely in T. It is an open channel, filled with a hard ribbed plastic insert that belongs to the tool. The grip fits over the outside of the whole thing.
- It bends about 15 degrees between A and B, in the plane the handles swing in. Most of the bend is in the middle; both ends are nearly straight.
- The curve comes from offsets the operator measured on a pencil tracing. `steel.py` fits a quartic centre line to the traced centre points and takes W and T from the calipers, linear between the stations and extended past them. Take the shape from the tracing and the sizes from the calipers.
- Its tip is a flat end with rounded corners. Their radius comes from the tracing alone and is read on the small side, so a grip's roof cannot come down on the steel. It is the less certain of the two tip readings.
- The biggest unknown is W at B. It lies beyond the last caliper station, and the tracing there reads wider than the calipers' trend. `python steel.py` prints both.
- Squeezed shut, the two handles come closest at B. How much room the grips have there is set by a measured gap; see "The tool must still close" below.

## The straight handle

- The tracing shows it straight, so its centre line is a constant.
- It has no caliper widths. The tracing reads W to the nearest 0.5, so `steel.py` takes W as one straight line through every traced row. A piecewise fit would kink at each half-millimetre step and run off past the last row.
- T comes from the calipers at A, J, K, L and M. A and M are its ends, so T is never extrapolated.
- Its tip is a half circle, read slightly small. The old straight grip's floor agrees: it is deeper at the centre than near the edge by what a half circle gives there (`python steel.py` prints both).
- B is the paper edge of the tracing, where the old grip stopped. The rows are placed from B, one row apart, as on the curved tracing.
- Its readings are within half a millimetre of the curved handle's, and a curved grip slides onto it and works. The straight grip is built from its own readings, with the same clearances and walls, so the two grips match inside and out as closely as the two steels allow. `python steel.py` prints the differences.
- The weakest reading is W near B. If the straight fit test is loose there, caliper widths at J, K, L, M and B replace the traced line.

## How a grip fits

- The bore is the steel plus `BORE_CLEAR` on every side. Its corners (`BORE_CORNER_R`) are tight enough that even a sharp steel corner clears the bore by at least 0.15; `check_design` asserts it.
- Eight lengthwise ribs, two on each face near the corners, reach `RIB_BITE` past the steel face. They are glue keys, not crush ribs (the operator's direction, 2026-10-31). They locate the grip. The valleys between them, `BORE_CLEAR` deep, give glue something to fill and key into, and they survive vapor-smoothing. Glue and air escape along the valleys while the grip is pushed on. Whether a grip also holds dry is for the test prints to show.
- The ribs end `RIB_FADE` short of the tip's round, fading into the wall over that length, so none stands in the roof.
- The ribs sit `RIB_INSET` from the corners, so they bear on solid steel near the edges rather than on the insert. A rib may cross the edge of a hole; that only loses contact over the hole's width.
- The bore's closed end follows the steel's rounded tip at `BORE_CLEAR`, as everywhere else, and a small roof closes it (see "Print orientation is designed in"). No hollow is left past the tip but that clearance and the roof: the operator does not want hollow there, because it flexes and carries no load (2026-11-01). The grip still seats on the steel's taper near B. The old grips had no gap at the tip at all.
- History (2026-11-01): up to `3046d4e`, the bore ran a millimetre past a square tip, and the roof rose from there. That left about 5 of hollow past the tip at the centre, against about 2.5 once the roof sat on the rounded tip. Each grip got as much shorter, because the dome follows the roof.

## The outside

- Walls are measured from the steel face, not from the bore, so retuning the bore never moves the outside. `WALL_SIDE` is in the plane of the handles, and `WALL_FACE` is across it. `CORNER_R` rounds the corners and must leave at least 2 mm over each bore corner; `check_design` asserts it.
- It flares by `FLARE` toward the open end, fading out over `FLARE_LEN`. That gradual flare is what the hand meets, and the operator prefers it, as on the stock grip.
- On the bed, the open end's edge sits `BEVEL` in from the flare's full width. A straight bevel rises from there at `BEVEL_ANGLE`, and a round of radius `RIM_R` blends it into the flare. The edge is neither sharp nor overhanging, and the bevel is tall enough to see and feel. `BEVEL` may bring the edge inside the body wall. `check_design` keeps at least three extrusion lines over the bore's corners on the first layer, and `grips.py` prints the figure. History (2026-11-01):
    - Print 1's flare ran out to the bed and left an acute, sharp edge there.
    - Print 2 swapped the flare for a bead that bulged out and back in. The edge was good, but the flare was lost.
    - Iteration 3 (`c585867`, not printed) kept the flare and rounded its bed edge with a circle that also touched the bed. That left only a few layers of bevel; the operator asked for more, brought further in.
    - Iteration 4 sets the bevel directly with `BEVEL`. Iteration 3's shape is the same construction with a smaller `BEVEL`. Its first build (`efac921`) held the corner radius as the edge came in, so the bevel flattened at the corners; see the next point. The fix is `87e777c`. Printed: it fits, and a curved grip also works on the straight handle. The operator asked for the flare to stand a millimetre further out, to stop the fingers sliding.
    - Iteration 5 (2026-11-01) stands the widest point about a millimetre further out at the same height, so the bevel keeps iteration 4's look. `FLARE_LEN` grew with `FLARE`, so the flare above it is no steeper than print 1's, which the operator liked; at the old length it would have been twice as steep, nearer a ridge than a flute.
- `grips.rim_profile` gives the open end's outline, from the bed to `FLARE_LEN`. It is a ruled loft of closely spaced sections; a smooth loft would ring through the round.
- The open end is a true offset of the body: its corner radius grows and shrinks with the walls (`CORNER_R` plus the outline's grow). The bevel then keeps `BEVEL_ANGLE` at the corners as well as on the flats. Holding the corner radius while the walls come in moves the corners in about 1.4 times as far, and flattens the bevel there below 45 degrees. The dome is different: it keeps `CORNER_R`, capped by `grips.rrect` as it shrinks.
- Constant walls keep the closest approach to the other handle at the open end's widest point, where the gap was measured.
- The grip is the same on both sides in W and in T. That is load-bearing: it makes a mirrored tracing harmless.
- The dome starts at the height of the bore's roof ridge (the ridge strip) and shrinks along a quarter circle of radius `DOME_LEN`. Starting it any lower thins the T wall at the ridge's ends below the body's. The cap over the ridge is then `DOME_LEN`, at least `END`.

## The tool must still close

- The first limit was inferred: with the old straight grip on, the gap at B was 9, and the old curved grip's wall there was 5 (measurement F). The operator has since measured the real thing. With an iteration-4 grip on each handle and the tool shut, the two open ends were `SHUT_GAP` apart, with a wall of `SHUT_WALL` at the widest point on each.
- `grips.shut_gap()` works out the gap for the grips built now. Each grip's wall at the widest point moves out by its change from `SHUT_WALL`, which is why `SHUT_WALL` stays what was measured even if `WALL_SIDE` or the open end changes. One more term: the grip measured on the straight handle was a curved grip, built for the curved steel, which is narrower at B. On the straight steel its bore still cleared, but its ribs bit harder, so its wall may have moved out by up to half the difference in W. The straight grip, built for its own steel, sits a full half-difference further out than that grip's wall would have without the ribs pushing. The worst case counts it in full.
- `check_design` asserts at least `MIN_SHUT_GAP` left. The operator called 0.3 "pushing it" and chose about a millimetre each side. `grips.py` prints the gap on each build.

## Print orientation is designed in

Each grip prints standing up, open end down on the bed, closed end at the top. The curved grip leans with the steel's curve, most at the tip; the straight grip stands upright. The open end's bevel rises at `BEVEL_ANGLE` above horizontal. Below 45 degrees it would need support. `check_design` asserts that it isn't. `tools/overhang.py` is no substitute: it flags only faces flatter than about 43 degrees. The bore's closed end is a gable roof seated on the steel's rounded tip (`grips.roof`).
- Each slope is the lowest line at `ROOF_ANGLE` above horizontal in print that clears the tip grown by `BORE_CLEAR`, computed from the actual lean.
- Below that, the bore follows the tip's round, which is steeper than the roof there.
- The ridge strip is where the two slopes are `RIDGE_W` apart, and the dome starts at its height.
- `roof()` asserts that each slope meets its own corner of the tip: the lean is less than `ROOF_ANGLE`, and the two together are under 90.
- With no lean, as on the straight grip, the roof is symmetric.

The only face `tools/overhang.py` flags is the ridge strip at the roof's top. `RIDGE_W` must stay narrower than one extrusion line, so the perimeters close it. No supports are needed.

## Test prints

Each grip's fit test (`FIT_LEN` of the open end) checks the bore on the steel near B, where the steel is widest and, on the straight handle, least certain. Slide it on from the tip up to B. It does not test the curve; the full curved grip does. Record each test print's outcome as a SumMem note for this model: what was printed, how it went on, how it held, and what changed.
