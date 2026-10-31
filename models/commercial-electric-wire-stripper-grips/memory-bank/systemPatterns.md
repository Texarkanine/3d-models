# System Patterns

## How This System Works

The operator's measurements of the bare steel are the source data. `reference/measurements.md` records each reading, what it measures, and how it was taken. The photos next to it show the tool, the old grip, and the tracings the curve was read from. Any size in the model cites a reading in that file.

## Names for places on a handle

- **A** is the tip of the bare steel. Every length along a handle is measured from A.
- **B** is where the old grip's open end sat. The new grip covers the steel from A to B.
- **W** is the steel's width in the plane the handles swing in, which is across the handle when the tool lies flat. **T** is its thickness at right angles to that plane, straight up off the table.
- **D1, D2** are holes through the steel. **S1 to S3** are the stations where W and T were measured.

## The curved handle

- The steel tapers from about 6.0 × 13.9 (W × T) at A to about 9.5 × 14.3 at B. It is an open channel, filled with a hard ribbed plastic insert that belongs to the tool. The grip fits over the outside of the whole thing.
- It bends about 15 degrees between A and B, in the plane the handles swing in. Its centre line is never more than 3.6 mm from a straight line drawn from A to B. Most of the bend is between 20 and 70 mm from A.
- The curve comes from offsets the operator measured on a pencil tracing, which match the caliper widths to within 0.5 mm. Take the shape from the tracing and the sizes from the calipers. `tools/reduce_curve.py` does that reduction and prints the cross-checks.
- With the tool squeezed shut and the old straight grip on, the gap at B is 9 mm. That is the room for the curved grip's wall facing the straight handle at B. The old grip's wall there was 5 mm.

## Print orientation is designed in

Each grip prints standing up, open end down on the bed. Its closed end is at the top. The curve leans the part at most about 15 degrees from vertical, so it needs no support.
