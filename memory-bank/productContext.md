# Product Context

## Target Audience

- The operator. This repository is the workshop for models they intend to publish.
- Someone who wants a single model downloads it from Cults, or from that model's GitHub release. They do not clone this repository.

## Use Cases

- Keep each publishable model under version control, whatever tool authored it.
- Cut a separate GitHub release for each model from conventional commits in that model's directory.
- Publish one tag to Cults by running the deploy workflow by hand against that tag.

## Key Benefits

- One author record and one release path serve every model.
- A model directory can hold a Solid Edge part, a Python script, or any other source. The catalog does not require one of them.

## Success Criteria

- A conventional commit merged to `main` that touches a model directory causes release-please to open a release pull request for that directory.
- Merging the release pull request creates a GitHub release and a tag named `<directory>-vX.Y.Z`.

## Key Constraints

- Models that are not for publication do not belong in this repository.
- Facts that belong to one model live in that directory, including `publish.yaml`. Facts that belong to the author live in `author.yaml`.
- The repository is AGPL-3.0. The license on a Cults listing is chosen per model in `publish.yaml`.
