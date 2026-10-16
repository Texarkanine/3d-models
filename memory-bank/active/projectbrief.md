# Project Brief

## User Story

As the operator, I want an update deploy to leave the public Cults gallery showing exactly the tag's images and one preview per STL, so that deleted photos and previews do not stay on the page.

## Use-Case(s)

### Update an existing listing

A tag that already has a Cults creation is published again. The publisher updates the listing, adds the tag's files and photos, and removes the previous ones. The public page should then match that final set.

## Requirements

As described in [issue 4](https://github.com/Texarkanine/3d-models/issues/4):

1. After the old assets are removed, make one field change that Cults counts as an update, so the gallery rebuilds from the final asset set.
2. An update deploy leaves the public page gallery showing exactly the tag's images plus one preview per STL, with no manual step.

## Constraints

1. `createIllustration` and `destroyIllustration` do not change `updatedAt`.
2. `updateCreation` with unchanged values does not change `updatedAt`. A real field change does.
3. Editing `details` to `"."` and back to `""` bumped `updatedAt` and the next page load matched the API.
4. Points the issue leaves open: whether one call can bump `updatedAt` without a visible edit; whether a bump before new STL previews exist leaves the gallery without them; an optional read-back that fails the deploy unless blueprints and illustrations match the tag.

## Acceptance Criteria

1. An update deploy leaves the public page gallery showing exactly the tag's images plus one preview per STL, with no manual step.
