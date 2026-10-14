# System Patterns

## How This System Works

`rattlinator.par` is the source. `rattlinator.stl` is the mesh exported from that part. There is no generated model and no second part that has to match it.

A change is a save in Solid Edge, then a new STL export over the same names. Git commits are the version history. Do not put a revision number in the filename.

The geometry is the print from 2025-03-30, which was called 0.13 when the only record was a new filename. `Rattlinator 0.14.par` was left in the old folder. It is a different file, it has no STL, and it was not copied.

## It has to get out of the way

The part stops the handle from rattling, and it also has to let the extinguisher be used while it is still on. A change that makes it rigid, or that blocks the trigger, fails the product. Print it in TPU 95 so it can deform.
