# Active Context

## Current Task: commercial-electric-wire-stripper-curved-grip
**Phase:** BUILD - READY

## What Was Done
- Operator approved the intent: matched TPU grips for both handles. Curved grip first; straight later, once its glued grip is off and the steel is measured.
- Operator decisions: TPU 95A; inner grooves or texture to key glue (survives vapor-smoothing the outside); print open end down, no supports; outside need not copy the original; the black ribbed insert in the curved channel is hard plastic that belongs to the tool.
- Operator: `.scratch/` is only for temporary files. Planning and design resources live in the model directory, which was set up as `models/commercial-electric-wire-stripper-grips/` (`f834ba2`).
- Creative decisions:
  - Bore: longitudinal crush ribs on a clearance bore, two per face, whose valleys take glue.
  - Outside: a steel-offset rounded rectangle with a mouth flare and a domed end.
- Plan written to `tasks.md`. Preflight: PASS WITH ADVISORY (A1 to A12 in `.preflight-status`).
- Operator direction at `/niko-build` (2026-10-31), which overrides parts of the plan:
  - `publish.yaml` stays as it is (`files: []`). We are on a branch and will print and fit-test long before anything publishes. Plan step 5 is dropped; A8 and A12 are moot for now.
  - The inner ribs exist for adhesive to key into, not for a friction fit. Don't fret over them; get close enough for a first test print and learn from each print. So the crush-rib bite tuning (A1, A2, A3, the grip-zone idea) is set aside.
  - No committed tests against the generated files yet: the shape is still being iterated in meat space. Design it, verify ad hoc that it is what was meant, then the operator prints and reports. `tools/check_fit.py` is dropped; its checks run ad hoc from `.scratch/`.

## Next Step
- Build the curved grip and its fit test, verify ad hoc, hand off for a test print.
