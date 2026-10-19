# System Patterns

## How This System Works

`jerry-can-buffer.par` is the source. `jerry-can-buffer.stl` is the mesh of one body from that part: the 3/8 in lip. There is no generated model.

The old folder names each variant with a dot where a fraction has a slash. `3.8` is 3/8 in, `1.16` is 1/16 in, `3.32` is 3/32 in, and `1.4` is 1/4 in. This directory is only `1.16 top 3.8 lip 3.32 gap 1in len`. The two 1/4 in lip meshes were not copied.

A change is a save in Solid Edge, then a new STL export over the same name. Git commits are the version history. Do not put a revision or the fraction code in the filename.

The cross-section, in inches, is a channel. The top web is 1/16 thick and 1 5/16 wide. Each return lip is 3/8 long and 1/16 thick. The opening between the underside of the top and the top of the lips is 3/32. The part is 1 long. The mouth between the lip tips is 7/16.

## One body

The part file can show more than one lip. The STL, and any STEP used to check it, has to be this body. On 2026-10-19 a STEP export of the open part matched this STL to within 0.0001 mm, and it did not match the 1/4 in lip meshes. That STEP file is not in this directory.
