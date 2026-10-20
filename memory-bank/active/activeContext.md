# Active Context

## Current Task: svg-comment-mask
**Phase:** BUILD - COMPLETE

## What Was Done
- Classified the approved fix as Level 1: one bug in `tools/strip_svg_metadata.py`, isolated to the comment mask.
- A `<!--` inside CDATA or a processing instruction is copied through. A real `<metadata>` element after it is removed.
- Two new tests failed on the old mask and pass now. Full suite: 88 tests, OK.

## Next Step
- Level 1 QA.
