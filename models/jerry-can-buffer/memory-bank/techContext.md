# Tech Context

Siemens Solid Edge part, edited by hand. No Python, no CadQuery, no dependency manifest.

## Environment Setup

- Open `jerry-can-buffer.par` in Solid Edge.

## Build Tools

- Export a binary STL in millimetres when the part changes, and replace `jerry-can-buffer.stl`. The export copied here used a custom chord tolerance of 0.05 mm. That setting is not stored in the part file.
- The 1/4 in lip meshes in the old folder were exported in inches. This file is millimetres. Exporting this body in inches makes a part 25.4 times too small.

## Testing Process

- There is no automated check and no recorded test print.
- A one-off compare on 2026-10-19 showed the STEP export and this STL are the same 24 vertices. The 1/4 in lip meshes differ by 1/8 in, which is 3/8 minus 1/4.
