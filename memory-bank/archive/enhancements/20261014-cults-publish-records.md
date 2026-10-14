---
task_id: cults-publish-records
complexity_level: 2
date: 2026-10-14
status: completed
---

# TASK ARCHIVE: Cults publish records and docs-as-patch

## SUMMARY

The Cults publish records are written, and a `docs` commit that touches a model directory opens a patch release. Optional listing fields are empty. The upload job is still unwired.

## REQUIREMENTS

- `author.yaml` records nickname `texarkanine`, `locale: EN`, `made_with_ai: true`, and the shared description sentence with `{license_name}`.
- Both `publish.yaml` files set `license_code: gpl`, category Gadget (`Q2F0ZWdvcnkvMjU`), and subcategory Vehicle Accessories (`Q2F0ZWdvcnkvODY`). Names, descriptions, and file lists stay as they were.
- `manufacturing`, `tags`, `images`, and `cults_creation_id` stay empty. One photo per model comes later.
- `release-please-config.json` copies the full default changelog sections and makes `docs` visible.
- The catalog notes record the version convention: `docs` and `fix` are patch, `feat` is minor, a breaking change is major. The version stays `MAJOR.MINOR.PATCH`.
- The Cults upload step stays unwired.

## IMPLEMENTATION

`author.yaml` holds the shared nickname, the AI flag, and the disclaimer. Each `publish.yaml` holds the license and the two category ids. `manufacturing` is an empty scalar. `tags` and `images` are empty lists.

`changelog-sections` replaces the release-please defaults, so the file copies the 17.6.0 list and leaves `docs` unhidden. A visible commit that is not a feature or a breaking change bumps the patch. A package that has never been released still proposes `1.0.0` on its first release. `fire-extinguisher-rattlinator` is already `1.0.0`. `h7-bulb-storage` is still `0.0.0`.

`memory-bank/systemPatterns.md` and `memory-bank/techContext.md` record that convention. `author.yaml` is outside every package, so a commit that touches only that file bumps nothing. The implementation commits were `chore`, so filling the records did not open a release. `AGENTS.md` still tells a new model to leave `license_code` and `category_id` empty until first publish. That sentence describes a new model, so it was left alone.

## TESTING

No catalog test suite exists, and a test of the YAML would be a change-detector. Preflight passed with advisory. QA passed on the build diff and confirmed all six requirements. The patch bump itself runs in GitHub Actions on a later `docs` commit.

## LESSONS LEARNED

In release-please 17.6.0, unhiding a commit type is what makes it count. A custom `changelog-sections` list replaces the defaults, so the full list has to be copied. Hiding `docs` was the only reason a listing commit did not already bump the patch.

## PROCESS IMPROVEMENTS

Nothing notable. The plan's file list and order held, and QA did not ask for a code change.

## TECHNICAL IMPROVEMENTS

A later task could add a schema check that the publish files and the files they name are well formed. That check was out of scope for this records change.

## NEXT STEPS

Commit each photo as `docs` inside its model directory. The rattlinator photo is a patch on `1.0.0`. An H7 photo that lands before the first release is cut ships inside `1.0.0`.
