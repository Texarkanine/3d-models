# Active Context

## Current Task: commercial-electric-wire-stripper-curved-grip
**Phase:** BUILD - COMPLETE

## What Was Done
- Earlier phases: intent approved (matched TPU 95A grips; curved first). Creative: a clearance bore with lengthwise ribs, and a steel-offset rounded-rectangle outside. Plan in `tasks.md`. Preflight: PASS WITH ADVISORY.
- Operator direction at `/niko-build` (2026-10-31), which overrides parts of the plan:
  - `publish.yaml` stays as it is (`files: []`); fit testing comes long before any publish.
  - The ribs are glue keys, not a friction fit. Get close enough for a first test print and learn from each print.
  - No committed tests against generated files while the shape is iterated in meat space. Verify ad hoc; the operator prints and reports.
- Files created or modified in `models/commercial-electric-wire-stripper-grips/`:
  - New: `steel.py`, `grips.py`, `README.md`, `tools/overhang.py` (copied from H11), and the outputs `curved_grip.{step,stl}` and `curved_grip_fit_test.{step,stl}`.
  - Changed: `tools/plot_curve.py` (draws from `steel.py`), `reference/curve-rebuilt.png`, `reference/measurements.md` (now a dated log), `memory-bank/systemPatterns.md`, `memory-bank/techContext.md`.
  - Deleted: `tools/reduce_curve.py`.
- Build decisions not in the creative docs:
  - Every reading from A is treated as a chord and converted to arc length. B is at s = 83.58 (preflight A4).
  - One `RIB_BITE` of 0.1 replaces the separate W and T bites, because the ribs are glue keys.
  - `CORNER_R` is 4.8, not 5, so that each bore corner keeps the creative doc's 2 mm (2.05).
  - The dome keeps its corner radius, capped at 0.45 of the shorter side (preflight A6).
  - `END_CLEAR` is 1.0 (preflight A5) and `FIT_LEN` is 15.
  - The bore roof is a ruled gable whose ridge comes from the lean at A, with both slopes at 50 degrees in print. The dome starts at the ridge's height, so the T wall over the roof never drops below the body's 2.2.
  - The ribs are ruled lofts, because a smooth loft overshot to a 0.18 bite near the tip.
- Deviations from the plan: step 5 (`publish.yaml`) and `tools/check_fit.py` were dropped at the operator's direction. Their checks ran ad hoc in `.scratch/wirestripper-grip/verify.py`.
- Verification:
  - The steel is never inside the bore wall (0 mm³).
  - Rib bites total 38.7 mm³ against 38.6 expected; at each of 7 sections they are 0.100–0.104.
  - The steel corners clear the bore by at least 0.213.
  - The thinnest wall is 2.03, at the corners. The cap over the ridge is 5.0.
  - Both STLs are watertight and stand on z = 0, with a 231 mm² footprint.
  - Overhang: only the 0.2 mm ridge strip (2.9 mm²).
  - The fit-test STL matches the grip STL cut at 15 mm to within 0.1 %.
  - Catalog suite: 88 OK. A rebuild reproduces the committed STLs exactly.

## Next Step
- QA (subagent), then reflect. After that, the operator prints the fit test and then the full grip, and reports back.
