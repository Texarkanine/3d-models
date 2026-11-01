# Project Brief

## User Story

As the owner of a Commercial Electric wire stripper and crimper whose rubber grips went sticky from automotive fluids, I want a slide-on TPU grip I can print for the curved handle, so that I can replace the ruined grip now and print a new one whenever I need to.

## Use-Case(s)

### Use-Case 1: Replace the curved grip

The old curved grip is already off. The operator prints the new grip in TPU 95A, slides it onto the bare curved steel as far as the old one went, and uses the tool.

### Use-Case 2: Glue it on

Someone who wants the grip permanent glues it on. The inside has grooves or texture for the glue to key into. The texture is there even if the outside is vapor-smoothed, which removes the print lines.

### Use-Case 3: Matching straight grip (later task)

Once the curved grip works, the same design approach makes a straight grip with the same outside. The straight steel is not measured yet; its old grip is still glued on.

## Requirements

1. The inside fits the bare curved steel from A (the tip) to B (83.15 mm from A), following its measured curve and taper (`models/commercial-electric-wire-stripper-grips/reference/measurements.md`).
2. The fit suits TPU 95A: snug enough to stay on, loose enough to slide on by hand.
3. The inside has grooves or texture that give glue something to grip.
4. The outside is a new, comfortable design meant to be shared by both grips. It does not copy the old grip.
5. With the grip on, the tool still closes fully. At B, with the old straight grip on, the closed tool leaves 9 mm between the bare curved steel and the straight grip.
6. It prints standing up, open end down on the bed, with no supports.
7. The model lives in this catalog as `models/commercial-electric-wire-stripper-grips/`, with source, STL and STEP.

## Constraints

1. This task covers the curved grip only. The straight grip is a later task.
2. Material: TPU 95A (the operator's). The jerry can buffer found TPU 95 stiff to stretch over a part.
3. The steel stays as it is, including the hard plastic insert in its channel.
4. The repository is public: everything committed must be shareable.

## Acceptance Criteria

1. A TPU 95A print slides onto the operator's curved steel to B and stays on in normal use.
2. The tool closes fully with the new curved grip and the old straight grip on.
3. The part prints open end down without supports.
4. The catalog tests pass, and the model's publish record names its printable files.

## Rework (2026-11-01): round the open end

The first TPU 95A print fits the steel "like a glove" and stays on without adhesive. The flare widens all the way to the bed, so the open end's outer edge is acute and feels sharp.

1. Give the open end a rounded lip. From the bed, the outside bulges out and then comes back in, so the edge the hand meets is rounded.
2. It still prints open end down with no supports.
3. The wall at B on the side facing the other handle stays within `CONVEX_LIMIT`.
4. The bore, the ribs, the rest of the outside, and the fit test's length stay as they are.

The straight grip is still a later task. It needs its steel measured once the old glued grip is off.

## Rework 2 (2026-11-01): flare plus a rounded bevel

Print 2's lip fixed the sharp edge, but the operator prefers print 1's gradual flare ("flute") where the hand meets the grip. The stock grip has both: a flare, and a rounded edge at the open end.

1. Bring back print 1's flare along the grip.
2. Round off only the open end's outer edge, the one on the bed, with a small printable bevel so it isn't sharp.
3. It still prints open end down with no supports, and the wall facing the other handle stays within `CONVEX_LIMIT`.
4. The bore, ribs and dome stay as they are.
5. Commit each printable iteration on its own, so that earlier ones can be checked out.
