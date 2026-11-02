# Active Context

## Current Task: wire-stripper-grips-closed-end
**Phase:** BUILD - COMPLETE

Memory bank: `models/commercial-electric-wire-stripper-grips/memory-bank/` (the operator's direction, 2026-11-01).

## What Was Done
- `0e75770`: the tip readings (`steel.py`, the log). No printed file changed.
- `a61aa6d`: curved grip iteration 6 and straight grip iteration 2. The roof sits on the rounded tip, and the grips are 1.77 and 3.03 shorter.
- Files changed, under `/home/mobaxterm/worktrees/Texarkanine/3d-models/3d-models-wirestripper-handle/models/commercial-electric-wire-stripper-grips/`:
    - `steel.py`, `grips.py`;
    - `curved_grip.{step,stl}`, `curved_grip_fit_test.{step,stl}`, `straight_grip.{step,stl}`, `straight_grip_fit_test.{step,stl}`;
    - `reference/measurements.md`, `README.md`;
    - `memory-bank/systemPatterns.md`, `memory-bank/techContext.md`, `memory-bank/productContext.md`;
    - `.summem/notes/` (the iteration's note).
- Key decisions:
    - `past` and `ridge` belong to the ridge row (preflight run 1).
    - B5 compares CAD, not STL (run 2).
    - The rib-bite rows start at `tip_r + RIB_FADE` (run 3).
- Deviation: `verify.py`'s rib-bite tolerance is ± 0.02, not ± 0.015. The evidence is in `tasks.md`, Build Progress, step 2: the `5d73490` build already read 0.089 and 0.112 between its sections near S2.

## Next Step
- QA, in a subagent.
