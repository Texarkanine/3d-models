# 3d-models

Publishable models. Someone who wants one model downloads it from Cults, or from that model's GitHub release. This repository is the workshop: the source, the printable files, and one release per directory.

## Where things are

| Path | What it is |
| --- | --- |
| `models/` | One directory per model. Each directory's README says what that model is and where its files are. The directories are the list. |
| `author.yaml` | The shared Cults nickname and listing text. |
| `release-please-config.json`, `.release-please-manifest.json` | Which directories get a release, and the version of each. |
| `memory-bank/` | How the catalog publishes: versions, the Cults deploy, and how to add a model. |

## Releases

A conventional commit on `main` that touches one model directory opens a release pull request for that directory. Merging it creates the tag `<directory>-vX.Y.Z` and the GitHub release. Publishing that release sends the model's listing to Cults.

The version rules, how to add a model, and how to publish an older tag again are in [`memory-bank/systemPatterns.md`](memory-bank/systemPatterns.md); this repository is intended to be read and written primarily by AI agents.
