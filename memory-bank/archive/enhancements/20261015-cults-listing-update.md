---
task_id: cults-listing-update
complexity_level: 2
date: 2026-10-15
status: completed
---

# TASK ARCHIVE: Cults listing update

## SUMMARY

A later publish updates an existing Cults listing. The text still goes through `updateCreation`. The tag's files are added with `createBlueprint`, the photos with `createIllustration`, and the blueprint and illustration ids that were already on the creation are removed afterwards. The catalog suite passed and QA passed. The pull request is https://github.com/Texarkanine/3d-models/pull/13.

## REQUIREMENTS

- Find the Cults calls that can apply a new tag's model files, text, and photos to an existing listing.
- Implement that path. `updateCreation` cannot carry `fileUrls` or `imageUrls`. The v1.0.2 deploy stopped on that guard on purpose.
- Open a non-draft pull request from `how-to-update-cults`.

## IMPLEMENTATION

`tools/cults_publish.py` reads the chosen creation with `myself.creationsBatch(ids:)`. It adds each printable URL with `createBlueprint` and each photo URL with `createIllustration`, sends the listing text through `updateCreation` with no file or image URLs, then calls `destroyBlueprint` and `destroyIllustration` for the ids from that read. An empty file list, an empty `img/`, a missing asset mutation, or a chosen id that no row carries refuses before any mutation. An error from a create or from the text update stops the run before the destroys.

`memory-bank/systemPatterns.md` records that a later publish removes blueprint and illustration files that are not in the tag.

The plan had widened the name scan to carry those ids. The official schema's `creationsBatch` accepts `ids`, so the build asks for that one creation instead. `creation` takes a slug, and the stored id is a global id.

## TESTING

Publisher tests are in `tests/test_cults_publish.py`. `test_update_without_file_arguments_sends_assets` failed on the old refusal, then passed once the asset calls were in place. The catalog command is `uv run --no-project --with pyyaml python -m unittest discover -s tests`. The suite ended at 47 tests, all passing. QA passed. No live Cults call was made, so the `$ids` variable type and the asset field selections are unproven on the server.

## LESSONS LEARNED

`creation` takes a slug. `myself.creationsBatch(ids:)` is the read that uses the stored id. `Blueprint.fileUrl` is Cults' own URL, so an update replaces the whole set instead of comparing URLs.

A third-party writeup that cites Discord is not the schema. The official introspection is, and it requires the API key.

## PROCESS IMPROVEMENTS

Nothing notable beyond using the official introspection before planning the mutation names.

## TECHNICAL IMPROVEMENTS

`createBlueprints` and `createIllustrations` would send the same URLs in fewer requests. The singular calls are the same design.

## NEXT STEPS

The first real deploy of a tag whose model already has a Cults id is the live check. It has not been run.
