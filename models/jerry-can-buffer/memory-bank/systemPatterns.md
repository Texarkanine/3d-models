# System Patterns

## How This System Works

`jerry-can-buffer.par` is the source. `jerry-can-buffer.stl` and `jerry-can-buffer.step` are two exports of that one body. There is no generated model.

The old folder names each variant with a dot where a fraction has a slash. `3.8` is 3/8 in, `1.16` is 1/16 in, `3.32` is 3/32 in, and `1.4` is 1/4 in. This directory is only `1.16 top 3.8 lip 3.32 gap 1in len`. The two 1/4 in lip meshes were not copied.

A change is a save in Solid Edge, then a new STL export and a new STEP export over the same names. Git commits are the version history. Do not put a revision or the fraction code in the filename.

The cross-section, in inches, is a channel. The top web is 1/16 thick and 1 5/16 wide. Each return lip is 3/8 long and 1/16 thick. The opening between the underside of the top and the top of the lips is 3/32. The mouth between the lip tips is 7/16. The part is 1 long.

In the exports, that 1 inch length is Z, and the channel outline lies on XY. The listing tells people to stretch the length and to print it standing up. An export that puts the length on X or Y makes that scale the channel instead of the rail.

## One body

The part file can show more than one lip. Both exports have to be this body. On 2026-10-20 the STEP and the STL were the same 24 corners, 25.4 mm along Z.
