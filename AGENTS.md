# Agent context

This repository is a catalog of publishable models. Each model is a directory. The repository root owns shared author data, release-please, and the catalog memory bank in `memory-bank/`. A model's own memory bank is that directory's `memory-bank/`.

Read the root `memory-bank/` for how the catalog publishes. When the task names a model, read that directory's `memory-bank/productContext.md`, `systemPatterns.md`, and `techContext.md` before changing it.

## Add a model

1. Create a directory whose name is the release-please component. Use lowercase words separated by hyphens.
2. Put the source and the printable files in that directory. This repo does not require a language, a script, or a particular CAD format.
3. Add `memory-bank/productContext.md`, `systemPatterns.md`, and `techContext.md` for that model.
4. Add `publish.yaml` in the directory. Its `files` list is what a Cults publish will ship. `license_code` and `category_id` stay empty until the first publish. `cults_creation_id` stays empty until Cults returns one.
5. Register the same directory in `release-please-config.json` (`release-type` `simple`, `component` equal to the directory name, `include-component-in-tag` true, and the shared pull-request header) and in `.release-please-manifest.json` at version `0.0.0`.

Release-please does not discover `publish.yaml` on its own. A directory is onboarded only when both files name it. Conventional commits that touch the directory drive that component's release pull request. Merging the pull request on `main` tags `<directory>-vX.Y.Z`.

Author-wide facts (Cults nickname, locale) live in `author.yaml`. The Cults API key is a GitHub Actions secret. A Cults upload job is not in this repo yet.
