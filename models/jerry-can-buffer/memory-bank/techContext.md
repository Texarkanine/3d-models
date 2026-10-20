# Tech Context

Siemens Solid Edge ordered part, edited by hand. No Python, no CadQuery, no dependency manifest.

## Environment Setup

- Open `jerry-can-buffer.par` in Solid Edge.

## Build Tools

- When the part changes, export a binary STL in millimetres and a STEP in millimetres, and replace `jerry-can-buffer.stl` and `jerry-can-buffer.step`.
- The 1/4 in lip meshes in the old folder were exported in inches. This body's exports are millimetres. An inch export of this body is 25.4 times too small.
- A typed protrusion distance is kept by pressing Enter in the distance box before Finish. Leaving the box without Enter restores the old distance.

## Testing Process

- There is no automated check.
- The print on the operator's cage is the photos in `img/`.
