---
task_id: cults-auto-deploy
complexity_level: 2
date: 2026-10-15
status: completed
---

# TASK ARCHIVE: Automatic Cults deploy

## SUMMARY

Publishing a GitHub release starts Cults deploy for that tag. Run workflow remains, and a manual run uses the publisher from the ref it was started from while the tag input selects the model files. The Cults client sends `User-Agent: Texarkanine GitHub CICD for Cults3D`. This work did not publish a tag. A later rework removed the tests that asserted that header.

## REQUIREMENTS

- A published release starts deploy for that release's tag.
- The manual action stays, including the tag input.
- A manual run uses the workflow and the publisher from the ref it was started from, and reads the model files from the tag.
- The Cults request sends `Texarkanine GitHub CICD for Cults3D`.
- Catalog notes match that behavior.
- Do not publish any tag, including `h7-bulb-storage-v1.0.1`.
- Rework: delete the tests that assert the User-Agent string or the absence of `Python-urllib`. Do not replace them.

## IMPLEMENTATION

`.github/workflows/deploy.yaml` listens for `release` type `published` and still accepts `workflow_dispatch`. The model checkout and `TAG` use the manual tag on a manual run and `github.event.release.tag_name` on a release. A second checkout of `github.sha` lands at `publisher/` with sparse checkout `tools`. The upload runs `publisher/tools/cults_publish.py`. The creation-id step removes `publisher` before it checks out `main`.

`tools/cults_publish.py` sets the User-Agent on the GraphQL request. `tests/test_deploy_workflow.py` locks the trigger, the tag expression, and the publisher checkout. `HttpTransportTests` was added with the header and then deleted. The suite ended at 36 tests.

`README.md`, `memory-bank/productContext.md`, `memory-bank/systemPatterns.md`, and `memory-bank/techContext.md` say a published release starts deploy, and that a manual run starts from the branch that contains the current publisher.

The open pull request is https://github.com/Texarkanine/3d-models/pull/8. Its body says the Actions run is unproven until a smoke test after merge.

## TESTING

Publisher and workflow tests are Python unittest. Command: `uv run --no-project --with pyyaml python -m unittest discover -s tests`. The first build reached 38 tests. After the rework, 36 passed. No live Cults call and no live git push of a creation id. Preflight passed with advisory. Both QA passes were clean. A local unauthenticated probe of `https://cults3d.com/graphql` got Cloudflare 1010 with no User-Agent and Cults' own 401 with the custom agent. That probe was not the Actions runner.

## LESSONS LEARNED

On `workflow_dispatch`, `github.sha` is the ref selected in Use workflow from. Starting the run from an old tag loads that tag's workflow file. The manual rerun of an older tag has to be started from `main`, with the tag in the input.

A job-level environment variable cannot fill `steps.*.with.ref`, so the tag expression is written on the model checkout and on each `TAG` binding.

Do not test the User-Agent string. Asserting the header, or that `Python-urllib` is absent, goes red only when the string changes. The reflection's note to assert that the header is present was withdrawn in the rework.

## PROCESS IMPROVEMENTS

Nothing notable.

## TECHNICAL IMPROVEMENTS

Nothing notable. The split between the tag's model files and the workflow ref's publisher is the shape that was built.

## NEXT STEPS

Merge the pull request. Then, from `main`, run Deploy with tag `h7-bulb-storage-v1.0.1`. That is the smoke test. The org pull-request template was not changed. It still lives in the org `.github` repository.
