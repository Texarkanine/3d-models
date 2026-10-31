# Tech Context

Parametric CAD in Python with CadQuery (OpenCascade kernel), as in the bulb storage models. The outputs are 3D-print files: STL for the slicer, STEP for CAD.

## Environment Setup

- No dependency manifest is committed. Run each script from this directory with `uv run --no-project --with <each package> python <script>`; uv caches the packages.
- `steel.py` is pure Python. `grips.py` needs `cadquery`. `tools/plot_curve.py` needs `pillow`. `tools/overhang.py` needs `trimesh`, `shapely`, `rtree`, `networkx` and `scipy`.

## Build Tools

- `python grips.py` regenerates `curved_grip` and `curved_grip_fit_test` (`.step` and `.stl`) in place, standing on the open end, and prints the main sizes. It takes about 15 seconds. Outputs are committed; regenerate and commit them with any change to `grips.py` or `steel.py`. Each run rewrites STEP headers (a timestamp); if a STEP file's only changes are in its header, restore it rather than commit it.
- `python steel.py` prints the centre line's fit to the tracing, the traced widths against the caliper widths, each station's chord and arc position, and W and T at A, the holes and B.
- `python tools/plot_curve.py` redraws `reference/curve-rebuilt.png` from `steel.py`, to compare with the tracing photo.
- Lofts: the bore and the outside are smooth lofts through cross-sections square to the centre line, every `SECTION_STEP` or less. The ribs and the roof are ruled lofts; a smooth loft overshoots where a rib fades out. `Wire.fillet2D` needs every corner radius under half the shorter side; `grips.rrect` caps it below that, so sections that shrink (the dome) keep a valid radius.

## Testing Process

- The final test is a TPU print slid onto the operator's tool. The fit test comes first, then the full grip.
- `grips.py`'s assertions catch impossible parameters: corner clearance, material over the bore corners, the wall at B, the dome, rib placement. `grip()` asserts one valid solid.
- `tools/overhang.py <file.stl>` lists faces that need support in print orientation (copied from the H11 model). Exported STLs should be watertight.
- Do not add committed tests for shapes still being prototyped. Verify ad hoc in `.scratch/` and let the test print decide; add checks once a shape settles. Useful ad hoc checks: the mock steel (`grips.steel_solid`) never inside the bore wall; each rib bites `RIB_BITE` in cross-sections; the thinnest wall between the bore's and the outside's faces; the steel's tip below the roof in print orientation.
