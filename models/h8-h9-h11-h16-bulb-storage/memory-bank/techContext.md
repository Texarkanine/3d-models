# Tech Context

Parametric CAD in Python with CadQuery (OpenCascade kernel), as in `h7-bulb-storage`. The outputs are 3D-print files: STL for the slicer, STEP for CAD (Solid Edge Community Edition).

## Environment Setup

- No dependency manifest is committed. Run each script from this directory with `uv run --no-project --with <each package> python <script>`; uv caches the packages, so no virtual environment is kept.
- `h11_holder.py` needs `cadquery` and `shapely`. `tools/make_svg.py` needs `shapely`. `tools/overhang.py` needs `trimesh`, `shapely`, `rtree`, `networkx` and `scipy`.

## Build Tools

- `python h11_holder.py` regenerates `h11_holder` and `h11_fit_test` (`.step` and `.stl`) in place, standing on the open end. Outputs are committed; regenerate and commit them with any change to the script. Each run rewrites STEP headers (a timestamp); if a STEP file's only changes are in its header, restore it rather than commit it.
- `python h11_prong_cover.py` regenerates `h11_prong_cover` (`.step` and `.stl`) in place, standing on its back face, and prints how far the teeth reach under the hooks and the arms' force and stress. It needs only `cadquery`.
- `tools/make_svg.py <output.svg>` draws `measure_cap.svg`: the PGJ19 cap at its largest sizes, the letters to measure, and the four wide-fin variants. Redraw it when the standard's numbers or the defaults change.

## Testing Process

- The final test is a physical print on the operator's halogen and LED H11s. `h11_fit_test` (openings, ring, stop and catches only) comes first, as `h7_fit_test` did for H7.
- The model script's assertions catch impossible geometry when it runs.
- `tools/check_fit.py` is the pass/fail suite (needs `cadquery` and `shapely`). Its lettered sections move every bulb type's cap through the openings, onto the wall, along the twist path and past the catches, and check catch strain and force, the wall against the seal, and the head against the body. It also checks that the 3D model matches the 2D shapes it tests. It exits 1 if any check fails; name sections to run only those.
- Tested 2026-10-15: the 0.1 fit test fit the operator's halogen and LED H11s on its first print ("fits like a glove"). The v1 holder's open end is unchanged from 0.1; v1 only rounds the outside of the closed end into a dome (0.1: a 45 degree cone).
- Section G of `check_fit.py` seats the connector cap on mock sockets at the standard's limits, with H11 and with H9 keys. The back plate and insert must touch nothing, and only the teeth may touch the hooks, pressing 0.3 to 1.2 mm into them. Test print 2 of the connector cap worked (2026-10-18).
- `tools/overhang.py <file.stl>` lists faces that need support in print orientation (copied from H7). Exported STLs should be watertight.
- Do not add committed tests for shapes still being prototyped. Verify ad hoc in scratch and let the test print decide; add checks once a shape settles.

## Sources for the defaults

The standards behind each default, with the sheet and page they were read from, and the operator's measured LED H11 are in the docstring of `h11_holder.py`.
