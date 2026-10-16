---
task_id: cults-listing-placeholders
complexity_level: 2
date: 2026-10-15
status: completed
---

# TASK ARCHIVE: cults-listing-placeholders

## SUMMARY

The Cults publisher replaces `{version}`, `{changelog_url}`, and `{license_name}` in the shared boilerplate and in each model's description and manufacturing. The changelog URL is the file on `main`, with no tag and no fragment. The listing title stays `name`. `images` is no longer a publish field. A rework then sent manufacturing text to Cults `details` instead of a Manufacturing heading in the description.

## REQUIREMENTS

- Replace those three tokens in `author.yaml` `boilerplate.description` and in `publish.yaml` `description` and `manufacturing`.
- `{version}` comes from the tag (`1.0.2` from `h7-bulb-storage-v1.0.2`). `{changelog_url}` is `https://github.com/Texarkanine/3d-models/blob/main/models/<component>/CHANGELOG.md`. The publisher adds no fragment.
- `name` stays literal, because a later publish finds the listing by that title.
- Remove unused `images`. Leave `tags`.
- Rework: manufacturing text belongs in Settings and manufacturing instructions, not in the description.

## IMPLEMENTATION

`version_from_tag` requires the tag to start with `<component>-v`. `changelog_url` builds the `blob/main` URL. `fill_listing_text` replaces `{changelog_url}`, then `{license_name}`, then `{version}`. `publish` fills the description, the boilerplate, and manufacturing, and does not fill `name`.

`_manufacturing_argument` still prefers a schema name that contains "manufactur". Otherwise it uses `details`. The gallery refresh changes `details` and restores the manufacturing text.

`images` was removed from both publish records in a `chore` commit so that deletion does not cut a model release. Photos still come from `img/`.

Key files: `tools/cults_publish.py`, `tests/test_cults_publish.py`, `memory-bank/systemPatterns.md`.

## TESTING

Publisher tests are in `tests/test_cults_publish.py`. The placeholder work ended at 79 tests. The rework added one update test and the suite ended at 80, all passing. Both QA reviews passed. No live Cults call was made for the rework, so the next publish is what moves an existing listing's notes into `details`.

## LESSONS LEARNED

`PublishTests` and `FileUrlTests` must not share one tag once the tag has to match the component. The publish tests use `widget-v1.0.0`. The file URL tests keep `h7-bulb-storage-v1.0.0`.

A `{changelog_url}#{version}` fragment does not scroll to a release-please heading. Those headings look like `## [1.0.2](…) (date)`, and the GitHub anchor is not `#1.0.2`.

An unknown token such as `{verison}` stays literal. That was left on purpose.

## PROCESS IMPROVEMENTS

Nothing notable. Preflight caught the shared test tag before the build.

## TECHNICAL IMPROVEMENTS

Fill each listing string once, in `publish`, and let `assemble_description` only join parts it is given. Manufacturing is filled in both places today. The second pass finds no tokens.

## NEXT STEPS

Publish a tag after this merges so the live listing picks up `details` and the filled boilerplate.
