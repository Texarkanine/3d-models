# Measurements

The operator's readings of their own tool, a Commercial Electric CE190205, with calipers, a ruler and pencil tracings. All sizes are in millimetres. The letters are defined in `../memory-bank/systemPatterns.md`.

The values the model uses live in `../steel.py`; this file says how each reading was taken and when. Add a new reading with its date. Keep a photo here only while it holds information not yet captured in numbers.

Distances "from A" were measured straight from A; `steel.py` converts them to distances along the curve.

## Curved handle, bare steel (2026-10-31)

| Item | From A | Reading |
|---|---|---|
| D2 | 7 | 3 mm hole |
| S1 | 16.93 | W 7.13 × T 14.04 |
| S2 | 47.76 | W 8.61 × T 14.24 |
| S3 | 68.17 | W 9.23 × T 14.28 |
| D1 | 76.5 | 3 mm hole |
| B | 83.15 | Where the old grip's open end sat. The operator slid the old grip back on and marked the steel. |

- The holes go through the faces you see with the tool lying flat (`tool-open.jpg`).
- The steel is an open channel holding a hard, ribbed black plastic insert that belongs to the tool (`curved-steel-channel.jpg`). The channel and insert are not measured.

### Curve offsets

`curve-tracing-offsets.jpg` shows the tracing of the bare curved steel, tip up. Two straight reference lines, PA on the left and PB on the right, are 38.5 apart (PW). Rows across them are 10 apart (PU). Row 0 is about 2.3 below the tip, and row 8 is at B. The offsets were measured on the paper itself.

| Row | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|---|
| PA: PA line to the left traced edge | 19 | 16 | 12.5 | 9.5 | 7.5 | 6 | 4.75 | 4 | 3.5 |
| PB: PB line to the right traced edge | 13 | 16 | 18.5 | 20.75 | 22.5 | 24 | 24.5 | 24.75 | 24.75 |

The tracing also shows the tip: a flat end with rounded corners of about 2, in the plane of the handles. `steel.py` reads them as 1.5, on the small side, because a pencil rounds a corner a little. This is the only record of the curved tip's shape.

## Straight handle, bare steel (2026-11-01)

A pencil tracing, tip up, between two straight lines 30 apart, with rows 10 apart. The paper edge is B, where the old grip stopped on the steel. Row 7 is taken to be 10 above the paper edge, as row 8 would be; the photo of the tracing showed 10.2. A is 85.14 above B.

| Row | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| Left line to the left traced edge | 11.5 | 11.5 | 11 | 11 | 10.5 | 10.5 | 10.5 | 10 |
| Right line to the right traced edge | 11.5 | 11.5 | 11 | 11 | 11 | 10.5 | 10.5 | 10 |
| W (30 less both) | 7 | 7 | 8 | 8 | 8.5 | 9 | 9 | 10 |

- The widths come from the tracing alone, to the nearest 0.5. This handle has no caliper widths.
- The traced centre is 15 from the left line on every row except row 4 (14.75). The handle is straight.
- The tip is a half circle in the plane of the handles, square across it. Its radius is half of W where the round starts, about 3.4; `steel.py` reads it as 3.3.

| Item | Where | Reading |
|---|---|---|
| A | The rounded tip | T 13.9 |
| J | Row 0 | T 14.02 |
| K | Row 3 | T 14.09 |
| L | Row 5 | T 14.25 |
| M | B, the paper edge | T 14.53 |
| B | 85.14 from A | Where the old grip stopped |

**Holes:** two 3 mm holes through the faces you see with the tool lying flat. Measured from the rounded tip to each hole's near edge: 6.32 and 76.75, so their centres are 7.82 and 78.25 from A. `steel.py` names them D2 and D1, after the matching holes on the curved handle.

## Old grips

- **Old curved grip** (`old-curved-grip-mouth.jpg`), at the open end:
    - inside 10 × 14.14, outside 19.75 × 20.67;
    - walls 5 on the long sides and 3.25 on the short sides.

  It may have swollen from the chemicals that ruined it.
- **Old straight grip:**
    - inside at the open end: 10.12 wide × 14.6 high;
    - inside depth from the mouth: 84.8 at the centre, and about 83.6 near the edge;
    - outside: 12 to 15.1, flaring to 19.7.

  Its floor sat about on the steel's tip (84.8 against 85.14 from A to B). The 1.2 between centre and edge is what a half-circle tip gives about 0.75 in from the side, which supports the straight tip's shape.

## Tool shut

- **2026-11-01:** with a test curved grip on each handle, the two open ends were about 3.3 apart when the tool was squeezed shut. Those grips' widest point stood 0.47 past the body wall, a smaller flare than the shipped grips'. `grips.py` keeps this as `SHUT_GAP` and `SHUT_WALL`. Shut, the handles come closest at B.
- **2026-11-02:** with the shipped pair on, the tool closes, and the two grips do not touch.
