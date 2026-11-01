# Measurements

The operator took these on their own tool on 2026-10-31, with calipers, a ruler and a pencil tracing. All sizes are in millimetres. The letters are defined in `../memory-bank/systemPatterns.md`.

This file is a dated log: add new readings as new dated entries rather than editing old ones. The values the model uses live in `../steel.py`. Distances "from A" were measured straight from A; `steel.py` converts them to distances along the curve.

Material: TPU 95A. The old rubber grips were fairly firm.

## Curved handle, bare steel

| Item | From A | Reading |
|---|---|---|
| D2 | 7 | 3 mm hole |
| S1 | 16.93 | W 7.13 × T 14.04 |
| S2 | 47.76 | W 8.61 × T 14.24 |
| S3 | 68.17 | W 9.23 × T 14.28 |
| D1 | 76.5 | 3 mm hole |
| B | 83.15 | Where the old grip's open end sat. The operator slid the old grip back on and marked the steel. |

- An earlier pass gave W 6.79, 8.65 and 9.10 at S1 to S3. The table holds the later, deliberate cross-section readings.
- The holes go through the faces you see with the tool lying flat (`tool-open.jpg`).
- The channel holds a hard, ribbed black plastic insert that belongs to the tool (`curved-steel-channel.jpg`).
- **F:** with the tool squeezed fully shut and the old straight grip still on, the narrowest gap between the bare curved steel and the straight grip is 9, exactly at B.

## Curve offsets

`curve-tracing-offsets.jpg` shows the tracing of the bare curved steel, tip up. Two straight reference lines, PA on the left and PB on the right, are 38.5 apart (PW). Rows across them are 10 apart (PU). Row 0 is about 2.3 below the tip, and row 8 is at B.

| Row | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|---|
| PA: PA line to the left traced edge | 19 | 16 | 12.5 | 9.5 | 7.5 | 6 | 4.75 | 4 | 3.5 |
| PB: PB line to the right traced edge | 13 | 16 | 18.5 | 20.75 | 22.5 | 24 | 24.5 | 24.75 | 24.75 |

`curve-tracing-ruler.jpg` is the same tracing beside a ruler. The ruler sits above the paper, so its scale in the photo is not exactly the paper's. Use the offsets above, which were measured on the paper itself.

`curve-rebuilt.png` is the outline that `tools/plot_curve.py` rebuilds from these numbers. The operator compared it with the tracing and judged it close enough to start (2026-10-31).

## Old curved grip

`old-curved-grip-mouth.jpg` shows the open end.

- Inside at the open end: 10 × 14.14. Outside at the open end: 19.75 × 20.67.
- Wall at the open end: 5 on the long sides, 3.25 on the short sides.
- The old grip may have swollen from the chemicals that ruined it.

## Straight handle

Not measured yet. The old straight grip is still glued on. (Superseded by the 2026-11-01 entry below.)

- **G:** its outside measures 12 to 15.1, then flares to 19.7. The new grips will not copy the old outsides.

## Straight handle, bare steel (2026-11-01)

The operator cut the old straight grip off and measured the bare steel with calipers and a pencil tracing. The readings were typed back in chat, and the operator checked them against the sheets.

`straight-tracing.jpg` shows the tracing, tip up, between two straight lines 30 apart. The rows are 10 apart (the "10mm" mark on the sheet). The paper edge is B, where the old grip stopped on the steel (M on the sheet). Row 7 is taken to be 10 above the paper edge, as row 8 would be; the photo shows 10.2. A is 85.14 above B.

| Row | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| Left line to the left traced edge | 11.5 | 11.5 | 11 | 11 | 10.5 | 10.5 | 10.5 | 10 |
| Right line to the right traced edge | 11.5 | 11.5 | 11 | 11 | 11 | 10.5 | 10.5 | 10 |
| W (30 less both) | 7 | 7 | 8 | 8 | 8.5 | 9 | 9 | 10 |

- The widths come from the tracing alone, to the nearest 0.5. This handle has no caliper widths.
- The traced centre is 15 from the left line on every row except row 4 (14.75). The handle is straight.

| Item | Where | Reading |
|---|---|---|
| A | The rounded tip | T 13.9 |
| J | Row 0 | T 14.02 |
| K | Row 3 | T 14.09 |
| L | Row 5 | T 14.25 |
| M | B, the paper edge | T 14.53 |
| B | 85.14 from A | Where the old grip stopped |

**Holes** (`straight-holes.jpg`):
- The sheet reads "Hole bottom from bd. edge: 76.75, 6.32".
- The operator's reading of it: measured from the rounded tip to the near edge (the "bottom") of each hole.
- Both are 3 mm holes, like the curved handle's, so their centres are 7.82 and 78.25 from A.
- `steel.py` names them D2 and D1, after the matching holes on the curved handle.

**Other readings:**
- **Old straight grip, inside at the open end:** 10.12 wide × 14.6 high. The operator: the new straight grip "should match inner and outer dimensions the same as the other side".
- **A curved grip on the straight handle:** an iteration-4 curved grip also slides onto the straight handle and works.
- **Tool shut:** with an iteration-4 curved grip on each handle and the tool squeezed shut, the two open ends are about 3.3 apart. For the design, this replaces F.
