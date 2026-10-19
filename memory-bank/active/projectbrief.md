# Project Brief

## User Story

As the operator, I want an update deploy to select the Cults design whose `creation.id` is the stored `cults_creation_id`, including when that design is not the newest, so a bulb listing publishes instead of failing because the newest design is a different one.

## Use-Case(s)

### Update an older listing

The account has more than one design. The design being published is not the newest. The deploy updates that design.

### Reject a different design

The read used to find the stored design returns some other design. The deploy stops before `updateCreation`.

## Requirements

1. Select the design whose `creation.id` equals the stored `cults_creation_id`.
2. Do not use `creationsBatch(ids:)` to make that choice.
3. Keep sending `creation.id` to `updateCreation`.
4. A regression fails when the read returns a different design.

## Constraints

1. The stored id stays `creation.id`. `creation.identifier` is not written into `publish.yaml` and is not sent to `updateCreation`.
2. The change stays in the Cults publisher and its tests.

## Acceptance Criteria

1. An update whose stored id is not the newest design still selects that design and sends that id to `updateCreation`.
2. A read that returns a different design fails before `updateCreation`.
3. The catalog test suite passes.
