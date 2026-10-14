# Tech Context

Siemens Solid Edge part, edited by hand. No Python, no CadQuery, no dependency manifest.

## Environment Setup

- Open `rattlinator.par` in Solid Edge.

## Build Tools

- Export a binary STL in millimetres when the part changes, and replace `rattlinator.stl`. The export that was printed used a custom chord tolerance of 0.05 mm. That setting is not stored in the part file.
- Print the STL in TPU 95.

## Testing Process

- The test on record is the physical print of the 2025-03-30 export, on the operator's 2.5 pound and 5 pound extinguishers. There is no automated check.
