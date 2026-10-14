# Tech Context

The catalog has no CAD toolchain. Each model directory documents its own in that directory's `memory-bank/techContext.md`.

## Environment Setup

- Git. GitHub Actions runs release-please. No local dependency install is required to cut a release.
- The Cults API key will be a GitHub Actions secret. It is not stored in the repository. `author.yaml` holds the Cults nickname and locale.

## Build Tools

- `.github/workflows/release-please.yaml` runs on every push to `main`. It mints a token from the helper GitHub App (`vars.HELPER_APP_ID`, `secrets.HELPER_APP_PRIVATE_KEY`) and passes that token to `googleapis/release-please-action` v5. The app token is what lets pull-request checks run on the release pull request. The action reads `release-please-config.json` and `.release-please-manifest.json`.
- Both packages start at `0.0.0`, which means they have never been released. A `feat` commit that touches a package proposes the next version. A `chore` commit does not.
- The workflow opens a release pull request. The GitHub release and the tag are created when that pull request is merged, not when the model's own pull request is merged.
- `.github/workflows/deploy.yaml` is started by hand with a tag input. It checks out that tag and resolves the model directory. The Cults upload step is still a placeholder and exits with an error.

## Testing Process

- Confirm a merged conventional commit on `main` produces a release-please pull request whose tag name is `<directory>-vX.Y.Z`.
- There is no automated test suite at the catalog root.
