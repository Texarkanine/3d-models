# Project Brief

## User Story

As the operator, I want a published GitHub release to publish that tag to Cults, and I want a manual run of the current workflow to publish an older tag, so that a release goes out on its own and a fixed publisher can still target a tag that was cut earlier.

## Use-Case(s)

### Use-Case 1

A release pull request merges and GitHub publishes the release. Deploy runs for that release's tag without anyone opening the Run workflow form.

### Use-Case 2

The workflow file and the publisher on an older tag cannot publish. The operator starts Deploy from `main` and supplies that older tag. The run uses the workflow and the publisher from `main`, and it reads the model files from the tag.

## Requirements

1. Publishing a GitHub release starts deploy for that release's tag.
2. The manual Run workflow action stays, including the tag input.
3. A manual run uses the workflow and the publisher from the ref it was started from, and reads the model files from the tag input.
4. The Cults request sends `User-Agent: Texarkanine GitHub CICD for Cults3D`. That header does not contain the Python urllib agent string.
5. Catalog notes that say deploy is only started by hand, and does not run when a release is created, are updated to match this behavior.

## Constraints

1. This work does not publish any tag, including `h7-bulb-storage-v1.0.1`.
2. The manual action is not removed.
3. The automatic path is the default. The manual path is the backup for an older tag.

## Acceptance Criteria

1. The deploy workflow runs when a release is published, and it still accepts a manual tag.
2. A manual run started from `main` with an older tag executes the publisher from `main` and reads that tag's model files.
3. The Cults HTTP request carries `Texarkanine GitHub CICD for Cults3D` and does not carry `Python-urllib`.
4. Tests cover the trigger, the split between the publisher and the tag's files, and the user agent.
5. No live Cults call and no live git push happen in this work.

## Rework

Prior complexity: Level 2.

The HTTP transport tests that assert the User-Agent string, and that `Python-urllib` is absent from the headers, are not tests. Remove them. Do not replace them with another assertion on that header. The publisher still sends `Texarkanine GitHub CICD for Cults3D`.

Acceptance criterion 3, and the user-agent clause of criterion 4, no longer ask for a test.
