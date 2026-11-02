# Tech Context

Parametric CAD in Python with CadQuery (OpenCascade kernel), as in the bulb storage models. The outputs are 3D-print files: STL for the slicer, STEP for CAD.

## Environment Setup

- No dependency manifest is committed. Run each script from this directory with `uv run --no-project --with <each package> python <script>`; uv caches the packages.
- Pin CadQuery for builds: `--with cadquery==2.8.0 --with cadquery-ocp==7.9.3.1.1` (the README's command). The committed STL files are exactly what was printed and found to fit, and these versions rebuild them byte for byte. Another version may move the tessellation.
- `steel.py` is pure Python. `grips.py` needs `cadquery`. `tools/plot_curve.py` needs `pillow`. `tools/overhang.py` needs `trimesh`, `shapely`, `rtree`, `networkx` and `scipy`.

## Build Tools

- `python grips.py` regenerates `curved_grip`, `straight_grip` and their fit tests (`.step` and `.stl`) in place, standing on the open end, and prints each grip's main sizes and the gap left with the tool shut. It takes about a minute. Outputs are committed; regenerate and commit them with any change to `grips.py` or `steel.py`. Each run rewrites STEP headers (a timestamp); if a STEP file's only changes are in its header, restore it rather than commit it.
- `python steel.py` prints, for each handle, the centre line's fit to the tracing and the traced widths against the model's (the curved handle's caliper widths, the straight handle's line), each station's chord and arc position, W and T at the holes, A and B, and the tip's shape. For the straight handle it also prints the differences from the curved handle at A and B, and its tip against the old straight grip's floor.
- `python tools/plot_curve.py` redraws `reference/curve-rebuilt.png` from `steel.py`, to compare with the tracing photo.
- Lofts: the bore and the outside are smooth lofts through cross-sections square to the centre line, every `SECTION_STEP` or less. The ribs, the roof and the open end (flare, bevel and round) are ruled lofts: a smooth loft overshoots where a rib fades out, and rings through the round. `Wire.fillet2D` needs every corner radius under half the shorter side; `grips.rrect` caps it below that, so sections that shrink (the dome) keep a valid radius.

## Testing Process

- The final test is a TPU print slid onto the operator's tool. The fit test comes first, then the full grip. A design change that alters an STL needs a new print before it ships.
- `grips.py`'s assertions catch impossible parameters: the tip's corner radius (0 to half the tip's W), `END_CLEAR` (a length past A, or `None`), the roof's angle (at least 45), a tip-seated roof's slopes meeting their own corners of the tip and closing only above it (`tip_roof()`), the ribs' fade length, corner clearance, material over the bore corners, the gap left between the two grips with the tool shut (`shut_gap`), the open end's bevel and round (they fit before `FLARE_LEN`, leave three extrusion lines over the bore's corners on the bed, and are steep enough to print), the dome, rib placement. `grip()` asserts one valid solid.
- To see a change of hundredths, compare CAD sections (the STEP files), not STL slices. The STL export strays up to about 0.1 from its own CAD on the lofted bore.
- `tools/overhang.py <file.stl>` lists faces that need support in print orientation (copied from the H11 model). Exported STLs should be watertight.
- There are no committed tests for the shapes: checks are ad hoc in `.scratch/`, and the test print decides. Run each check for both grips; the builder is shared, but each handle's steel is different. Useful ad hoc checks: the mock steel (`grips.steel_solid`) never inside the bore wall; each rib bites `RIB_BITE` in cross-sections; the thinnest wall between the bore's and the outside's faces; for a tip-seated closed end, the mock steel's rounded tip `BORE_CLEAR` from the bore up to where the roof's slopes take over, and nowhere nearer; a rebuild in a temporary folder compared with the committed STLs byte for byte; horizontal slices of the STL just above the bed, for the angle where the outside meets the bed and the open end's profile; the face normals near the bed all the way round, so that the bevel's angle is checked at the corners, not only on the flats.
