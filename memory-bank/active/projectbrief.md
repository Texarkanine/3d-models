# Project Brief

## User story

Move each publishable model from the repository root into `models/<component>/` per [issue #1](https://github.com/Texarkanine/3d-models/issues/1).

## Requirements

- Keep the release-please **component** name and tag prefix (`<component>-vX.Y.Z`) unchanged.
- Update every path that assumes models live at the root: release-please package keys and manifest, deploy tag resolution, Cults file URLs, tests, and catalog documentation.
- Land before Cults `{changelog_url}` work (#2).
