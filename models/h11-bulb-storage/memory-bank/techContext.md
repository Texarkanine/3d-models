# Tech Context

Parametric CAD in Python with CadQuery (OpenCascade kernel), as in `h7-bulb-storage`. The outputs are 3D-print files: STL for the slicer, STEP for CAD (Solid Edge Community Edition).

## Environment Setup

- No dependency manifest is committed. Run each script from this directory with `uv run --no-project --with <each package> python <script>`; uv caches the packages, so no virtual environment is kept.
- `h11_holder.py` needs `cadquery` and `shapely`. `tools/make_svg.py` needs `shapely`. `tools/overhang.py` needs `trimesh`, `shapely`, `rtree`, `networkx` and `scipy`.

## Build Tools

- `python h11_holder.py` regenerates `h11_holder` and `h11_fit_test` (`.step` and `.stl`) in place, standing on the open end. Outputs are committed; regenerate and commit them with any change to the script. Each run rewrites STEP headers (a timestamp); if a STEP file's only changes are in its header, restore it rather than commit it.
- `tools/make_svg.py <output.svg>` draws `measure_cap.svg`: the PGJ19 cap at its largest sizes, the letters to measure, and the four wide-fin variants. Redraw it when the standard's numbers or the defaults change.

## Testing Process

- The final test is a physical print on the operator's halogen and LED H11s. `h11_fit_test` (openings, ring, stop and catches only) comes first, as `h7_fit_test` did for H7.
- The model script's assertions catch impossible geometry when it runs.
- `tools/check_fit.py` is the pass/fail suite (needs `cadquery` and `shapely`). Its lettered sections move every bulb type's cap through the openings, onto the wall, along the twist path and past the catches, and check catch strain and force, the wall against the seal, and the head against the body. It also checks that the 3D model matches the 2D shapes it tests. It exits 1 if any check fails; name sections to run only those.
- Tested 2026-10-15: the 0.1 fit test fit the operator's halogen and LED H11s on its first print ("fits like a glove").
- `tools/overhang.py <file.stl>` lists faces that need support in print orientation (copied from H7). Exported STLs should be watertight.
- Do not add committed tests for shapes still being prototyped. Verify ad hoc in scratch and let the test print decide; add checks once a shape settles.

## Sources for the defaults

- Cap: IEC 60061-1 sheet 7004-110-2 (PGJ19), read from GOST IEC 60061-1-2014, PDF pages 230 to 232. Nose A1 19.0 max; fin tip radius r8 12.15 to 12.25; fin block F 4.0 max in front of the fins' back face; E 3.0 min from that face to the plate the seal sits on (cap notes 5 and 10); C 25.1 to 25.5, the diameter of that face; plate G 31.4 to 31.6; nose and relaxed spring Z 21.4 max. Narrow fins: one straight edge B 7.8 to 8.0 from the centre line, the other B1 3.3 to 3.5 from the 60 degree line. Wide fin: B3 8.0 (-1), B5 6.0 + B6 4.0 (-2 and -5), B4 10.0 (-3).
- Socket: IEC 60061-2 sheet 7005-110-3, read from GOST IEC 60061-2-2017, PDF pages 197 to 199. Hole Z 19.5 to 20.0; opening radius r8 12.4 to 12.5; wall E at least 2.2 (2.4 for PGJ19-3), from the face the seal presses on to three bearing pads about 3 by 3 mm, with no maximum; a cup of bore C 31.9 to 32.1 around the bulb's plate; retaining bump H 0.25 to 0.35. The bulb's spring pushes the nose into a V-support with at least 10 N, then at least 5 N presses the fins onto the socket.
- Head: UNECE R37 sheet H8/1 maximum outline, read from GOST R 41.37-99, page 91: Ø25 for the first 4.0 mm, then Ø19, glass Ø15, at most 44.0 mm long from the fins' back face. H8 and H11 share this outline; confirm against the operator's bulbs.

## The operator's bulbs

Measured 2026-10-15 on the operator's LED H11, with the letters of `measure_cap.svg`:

- F, fin thickness: 1.0 mm.
- E, back face of the fins to the plate, seal off: 3.33 mm. In spec (3.0 min).
- With the seal on, its face is about 1.38 mm behind the back face of the fins, so the seal stands about 1.95 mm proud of the plate. A wall thicker than 1.38 mm squeezes it.
- L, back face of the fins to the tip: about 32 mm. Shorter than the halogen limit of 44.

The car's socket already limits the LED's fin width, fin reach and nose diameter, so those were not measured. The halogen was not measured: the holder follows the socket standard, which takes every bulb in spec.
