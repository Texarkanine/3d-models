# Project Brief

## User Story

As the owner of the Commercial Electric wire stripper, I want each grip's closed end to have no empty space past the steel tip beyond what printing needs, so that the end of the grip is solid and carries load instead of flexing over a hollow.

## Background (operator, 2026-11-01)

- Straight grip iteration 1 (`3046d4e`) printed and went on the tool. Its open end sits about 2.5 above the curved grip's, up to where the straight steel widens. The operator first asked to shorten it by 2.5, then chose to keep that stagger; the stock grips are staggered too. The open ends do not change.
- The grip's length is not the problem. Hollow space past the steel tip is: it flexes and carries no load.
- The printed straight grip is about 7 longer than the old one, and the printed curved grip about 5 longer than the factory one.
- The old straight grip's inside is 84.8 deep from the mouth at the centre, and about 83.6 near the edge. The printed straight grip reads about 87.7 deep.
- In the model, the bore runs `END_CLEAR` (1.0) past a square-ended tip at full width, and its gable roof rises 4.3 (straight) or 3.7 (curved) more. Both tracings show rounded tips. The old straight grip's 1.2 between centre and edge matches a half-circle tip.

## Requirements

1. The bore's closed end follows the steel's rounded tip with `BORE_CLEAR` all round, the tip included. The extra 1.0 past the tip goes.
2. The roof keeps its slopes at `ROOF_ANGLE` in print, so it still prints without supports.
3. The solid end over the roof stays as thick as now (`DOME_LEN`). The outside follows the roof down, so each grip gets shorter: about 2.9 for the straight grip and about 1.7 for the curved one, as agreed.
4. The tip shapes are steel readings, read on the small side so that the bore cannot come out too tight. The straight tip is a full half circle (corner radius 3.3, about half its W at A). The curved tip has rounded corners (radius 1.5, from its tracing).
5. The operator's new readings go into the dated log, and those the model uses go into `steel.py`.
6. Nothing else changes: the open ends and their stagger, the flare, the bevel, the bore along the body, the walls, and the ribs, except where the ribs must end before the tip's round.
7. This printable iteration (curved grip iteration 6, straight grip iteration 2) is committed on its own.
8. `publish.yaml` stays as it is.

## Constraints

1. Material: TPU 95A. Prints open end down, with no supports.
2. The repository is public: everything committed must be shareable.
3. Task memory bank: `models/commercial-electric-wire-stripper-grips/memory-bank/` (the operator's direction). The earlier curved-grip task's files in the root `memory-bank/active/` belong to that task and stay untouched.

## Acceptance Criteria

1. With the steel's rounded tip modelled, the steel is nowhere inside the grip's wall, and the bore hugs the tip at `BORE_CLEAR` from its sides up to where the roof's slopes take over.
2. The roof's ridge sits about 2.4 (straight) and 3.0 (curved) past the tip, against 5.3 and 4.7 now.
3. The open ends are unchanged, within the loft's few hundredths.
4. `tools/overhang.py` flags only the roof's ridge strip.
5. The catalog tests pass.
