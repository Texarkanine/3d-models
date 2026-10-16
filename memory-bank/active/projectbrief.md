# Project Brief

## User Story

As the operator, I want the Cults listing text to fill in the version, the changelog URL, and the license name, so that shared and per-model text can name the release and link the changelog while the listing title stays stable.

## Use-Case(s)

### Use-Case 1

Publishing a tag appends `author.yaml` `boilerplate.description` to every Cults listing. Placeholders in that boilerplate are replaced before the text is sent.

### Use-Case 2

The same placeholders in a model's `publish.yaml` `description` and `manufacturing` are replaced the same way. The operator can write a deep link themselves, for example `Changelog: [click here]({changelog_url}#{version})`.

## Requirements

1. Replace `{version}`, `{changelog_url}`, and `{license_name}` in `author.yaml` `boilerplate.description`.
2. Apply the same substitution to `description` and `manufacturing` in each model's `publish.yaml`.
3. `{version}` is the version being published (`1.0.2` from the tag `h7-bulb-storage-v1.0.2`).
4. `{changelog_url}` is the changelog on the default branch, with no tag and no fragment: `https://github.com/Texarkanine/3d-models/blob/main/models/<component>/CHANGELOG.md`.
5. The publisher does not add a URL fragment.
6. `name` stays literal. That string is the listing title, and a later publish finds the existing Cults listing by it.
7. Remove the unused `images` field from `publish.yaml`. Photos continue to come from each model's `img/` directory.
8. Leave `tags`. A non-empty list is sent to Cults as `tagNames`.

## Constraints

1. Issue [#2](https://github.com/Texarkanine/3d-models/issues/2) is the source for the boilerplate placeholders. The operator overrode the issue's "URL at that tag": the changelog URL is the file on `main`, not on the tag.
2. The changelog path is `models/<component>/CHANGELOG.md`.
3. `{license_name}` stays the token the boilerplate already uses.

## Acceptance Criteria

1. A published description contains the version, the `blob/main` changelog URL, and the license name wherever those tokens appeared in the boilerplate, the model description, or manufacturing.
2. None of `{version}`, `{changelog_url}`, or `{license_name}` remain in the text sent to Cults.
3. The changelog URL has no fragment and does not contain the tag.
4. The listing title equals `publish.yaml` `name`, with no substitution.
5. `publish.yaml` files no longer have an `images` field. `tags` remains.
6. Photos still upload from `img/`.

## Rework

The manufacturing text belongs in Cults' "Settings and manufacturing instructions" field. On the listing the operator opened, that field is empty and still shows the placeholder "3D printing or CNC / Laser cutting settings in English". The same text is inside the 3D model description, under a Manufacturing heading, after the boilerplate.
