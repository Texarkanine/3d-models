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
