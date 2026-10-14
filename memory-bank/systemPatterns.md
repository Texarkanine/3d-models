# System Patterns

## How This System Works

A directory at the repository root is one model and one release-please package. The directory name, the `component` in `release-please-config.json`, and the key in `.release-please-manifest.json` are the same string.

`publish.yaml` in that directory is the only per-model publish record. Tooling that uploads to Cults will read it and nothing else in the directory for the listing. The fields are the name, the description, `license_code`, `category_id`, the `files` list, `images`, and `cults_creation_id`. A blank `license_code` or `category_id` means the model is not ready to publish. A blank `cults_creation_id` means Cults has not returned an id yet.

Release-please does not discover `publish.yaml`. A model is onboarded when `publish.yaml` exists and the directory is registered in both release-please files. Conventional commits whose paths fall inside the directory drive that package. `separate-pull-requests` gives each package its own release pull request.

The root `memory-bank/` describes the catalog. Each model directory has its own `memory-bank/` describing that model. An agent working on a model reads the model's files. An agent changing publish or release behavior reads the root files.

## Adding a model

Create the directory, its memory bank, and `publish.yaml`. Register it in `release-please-config.json` with `release-type` `simple`, `include-component-in-tag` true, and the shared pull-request header. Register it in `.release-please-manifest.json` at `0.0.0`.

Cutting a release and publishing that release are different workflows. Release-please opens the release pull request and, when that pull request is merged, creates the tag and the GitHub release. Deploy is a separate workflow, started by hand against one tag. It does not run because a release was created.
