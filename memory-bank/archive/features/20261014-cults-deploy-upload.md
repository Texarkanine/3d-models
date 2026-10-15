---
task_id: cults-deploy-upload
complexity_level: 3
date: 2026-10-14
status: completed
---

# TASK ARCHIVE: Cults deploy upload

## SUMMARY

The hand-started deploy workflow publishes one model tag to Cults and writes the returned creation id back to `main`. Listing photos are the files in that model's `img/` directory. The rattlinator manufacturing field stays empty, with a comment marking it as the place the operator writes print notes.

## REQUIREMENTS

The operator wants to publish one tag by running the deploy workflow. Cults receives that model's listing from `publish.yaml` and `author.yaml`, including the photos in `img/`. Manufacturing text, when present, is what Cults receives. On the rattlinator the field stays empty until the operator writes the notes. Those notes are meant to cover the Cura support blocker and printing in TPU 95. The agent does not write that text.

The upload had to replace the placeholder that exited 1. The trigger stays a hand-started workflow against one tag. The API key stays in `secrets.CULTS3D_API_KEY`. License, the AI flag, the nickname, and the categories stay as already recorded. A blank `cults_creation_id` means Cults has not returned an id yet.

## IMPLEMENTATION

`tools/cults_publish.py` reads the model's `publish.yaml`, `author.yaml`, and `.gitattributes`. It calls `https://cults3d.com/graphql` with Basic auth. The username is `cults_nick`. The password is the secret, and the publisher does not put that secret in the query.

Printable paths in `files` become `raw.githubusercontent.com` URLs for the repository, tag, and component. A path whose extension `.gitattributes` marks with `filter=lfs` uses `media.githubusercontent.com`. `file_url` is the only place that picks the host. Listing photos are every file in `img/`, not the `images` list. `images` stays empty.

The description is the model text plus the author boilerplate, with `{license_name}` replaced from Cults' license list. Non-empty manufacturing goes on a schema argument whose name contains "manufactur" when introspection finds one, and otherwise into a Manufacturing section of the description. Empty manufacturing adds nothing. `made_with_ai` is sent when the schema has that argument. If it does not, the run refuses before creating or updating. Blank `license_code` or `category_id` refuses before any request. Arguments the schema does not list are dropped. A free listing omits `downloadPrice` unless that argument is non-null, in which case the value is `0`.

Zero name matches create a listing. One match updates it. More than one match stops. A local id updates that id. A local id that disagrees with the single name match stops. If an update cannot carry `fileUrls` and `imageUrls`, the run refuses before a partial update. A non-empty Cults `errors` list fails the run.

`.github/workflows/deploy.yaml` still checks out the tag with Git LFS and resolves the component. It has `contents: write`. The upload step installs PyYAML with `python -m pip install pyyaml` and runs `tools/cults_publish.py` with `COMPONENT`, `TAG`, and `CULTS3D_API_KEY`. A later step fetches `main`, writes the id with `--set-creation-id`, and pushes. The commit uses `git -c user.name` and `git -c user.email`, subject `chore: record Cults creation id`. It is skipped when the id is already on `main`.

The photo files themselves are in `docs: add the listing photos`. That commit used to be a chore, which would not have cut a release, so the tag Cults fetches would not have contained the pictures. It is a `docs` commit now, and it touches both model directories.

Catalog notes in `README.md`, `AGENTS.md`, `memory-bank/systemPatterns.md`, `memory-bank/techContext.md`, and `memory-bank/productContext.md` describe the wired upload, the public GitHub URLs, and the chore id write-back.

## TESTING

Publisher tests live in `tests/` and use Python unittest. PyYAML is installed for the run and is not a committed manifest. Local command: `uv run --no-project --with pyyaml python -m unittest discover -s tests`. The suite was 31 tests, all passing, with a fake Cults transport. No live Cults call and no live git push.

The creative decision was unittest rather than pytest or a script modeled on `h7-bulb-storage/tools/check_fit.py`. Unittest adds no package of its own. The tests pass fakes into functions, so they do not need pytest fixtures. `check_fit.py` stays a geometry check for one model. That choice held through build.

QA passed on the first review. It confirmed the planned behaviors, the secret hygiene, the blank-field refusal, the made-with-AI gate, create versus update versus refuse, and the chore-only id write-back. Two notes were non-blocking. The AI-argument check looks at the create schema before it knows whether the run will update. The id-write step assumes the upload step already installed PyYAML on the shared runner.

## LESSONS LEARNED

A file in `img/` is a listing photo. `images` in `publish.yaml` is not a second inventory of that folder. The plan had said to copy each photo path into `images`, and preflight had called a test of that copy a behavior test. The operator rejected both. A test that fails because someone added a photo they meant to add is a change-detector.

The documented `updateCreation` arguments do not include `fileUrls` or `imageUrls`. This publisher refuses that update when introspection agrees. The refusal has not been tried against the live schema.

A `chore` commit that adds listing photos does not cut a release. The photos have to be in a `docs`, `fix`, or `feat` commit that touches the model directory, or the tag Cults is given will not contain them.

## PROCESS IMPROVEMENTS

When a plan says a test should fail if a folder and a config list disagree, ask whether the folder is already the list. Preflight treated that disagreement as a product break. It was an intended edit.

## TECHNICAL IMPROVEMENTS

`--dry-run` was a preflight sketch for printing the mutation payload without the network or the secret. It was not built. Add it if a review of the payload before the first real tag is worth a workflow step.

The two QA notes are real but small. The update path requires the create schema to have the AI argument, and the id-write step does not install PyYAML itself.

## NEXT STEPS

Merge the branch. Release-please should open a patch release for each model, because `docs: add the listing photos` touches both directories. After those releases merge, run the deploy workflow against the new tags. The operator still has to write the rattlinator print notes in `manufacturing` before a publish that should include them.
