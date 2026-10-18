# Tech Context

Parametric CAD in Python with CadQuery (OpenCascade kernel). The outputs are 3D-print files: STL for the slicer, STEP for CAD (Solid Edge Community Edition).

## Environment Setup

- The model needs only `cadquery`; the scripts in `tools/` also need `trimesh`, `shapely`, `rtree`, `matplotlib`, `networkx` and `scipy`. No dependency manifest is committed. Run any script from this directory with `uv run --no-project --with <each package> python <script>`; uv caches the packages, so no virtual environment is kept.

## Build Tools

- `python h7_led_cover.py` regenerates every output in place, already turned to print orientation: `h7_cover` and `h7_fit_test` at this directory, and one `clips/h7_clip_flange_<band>mm` per entry in `CLIP_VARIANTS`, each as `.step` and `.stl`. Clips are exported from `printed_clip()` (arms spread as printed); `clip()` is the clip as held in use.
- Each run rewrites STEP headers: the timestamp in `FILE_NAME`, and an export counter in `PRODUCT` that shifts when the export order changes. If a STEP file's only changes are in its header, restore it (`git checkout -- <file>`) rather than commit it.
- Outputs are committed. Regenerate and commit them with any change to the script.
- `python h7_prong_cover.py` regenerates `h7_prong_cover` (`.step` and `.stl`) in place, slotted face down, and prints its size and the springs' estimated force. It needs only `cadquery`.
- `measure_flange.svg` (flange diagram for users) is drawn by `tools/make_svg.py <output.svg>`. Redraw it when the key or bore parameters change.

## Testing Process

- The model script's assertions catch impossible geometry when it runs.
- `tools/check_fit.py` is the pass/fail suite. Its lettered sections each check one behaviour of the cover, clip and mock bulbs together. Each check prints PASS or FAIL with its numbers; the script exits 1 if any fails. Name sections to run only those (see its docstring). Add a check only for a behaviour that has settled: the operator does not want tests for shapes still being prototyped. Keep the suite lean: for a one-time question (for example, "is this export the clip that was printed?") use a one-off check such as comparing STLs byte for byte, not a new section.
- The other scripts in `tools/` are run from this directory and print numbers that need reading; they do not fail on their own:
  - `overhang.py <file.stl>`: faces that need support in print orientation; flat roofs are labelled as a bridge (held both sides) or a cantilever (held on one side, which needs support).
  - `probe.py`: sizes, volumes and validity of the cover and every clip.
  - `render_sections.py <out_dir>`: section pictures with a mock bulb.
- Exported STLs should be watertight.
- Section M of `check_fit.py` puts mock tabs in the prong cover: nominal, the operator's LED plug, and two extremes. Only the four ridges may touch them, each 0.1 to 0.4 mm in. Test print 2 of the prong cover worked (2026-10-18).
- The final test is a physical print on the operator's bulbs; a `h7_fit_test` print (collar and seat only) checks flange, key and clip quickly.
