# Progress

A published GitHub release publishes that tag to Cults. The manual workflow remains so the current publisher on `main` can target an older tag. The Cults client sends `User-Agent: Texarkanine GitHub CICD for Cults3D`. This work does not publish any tag.

**Complexity:** Level 2

## 2026-10-15 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Restated the request and recorded the operator's confirmation
    - Moved this checkout from `add-photos` to `main` at `8cc4f59`, then cut `cults-auto-deploy`
    - Classified the work as Level 2
* Decisions made
    - Level 2: one deploy path, a specified design, and no new subsystem
    - Do not republish `h7-bulb-storage-v1.0.1` in this work
    - A manual run uses the publisher from the ref the workflow was started from, and the model files from the tag input
* Insights
    - Checking out the tag replaces `tools/cults_publish.py` with the copy on that tag, which is why an older tag cannot publish until the manual run keeps the current publisher

## 2026-10-15 - PLAN - COMPLETE

* Work completed
    - Wrote the Level 2 plan in `memory-bank/active/tasks.md`
    - Mapped tests to `tests/test_cults_publish.py` and `tests/test_deploy_workflow.py`
* Decisions made
    - Listen only to `release` type `published`
    - Model files come from the manual tag or `github.event.release.tag_name`
    - The publisher is a second checkout of `github.sha` at `publisher/`
    - The creation-id step removes `publisher` before it checks out `main`
* Insights
    - PyYAML loads the workflow `on` key as `True`
    - On a release, `github.sha` is the tagged commit. On a manual run, it is the ref selected in Use workflow from

## 2026-10-15 - PREFLIGHT - COMPLETE (PASS WITH ADVISORY)

* Work completed
    - Validated implementation plan in `memory-bank/active/tasks.md` against codebase reality
    - Preflight status written to `memory-bank/active/.preflight-status`: PASS WITH ADVISORY
* Decisions made
    - Plan confirmed ready for Build phase without blocking changes
* Insights
    - Both executable units strictly enforce TDD step ordering
    - Tag resolution expression and publisher checkout can optionally be streamlined with job-level env or workspace isolation

## 2026-10-15 - BUILD - COMPLETE

* Work completed
    - Set the Cults user agent and covered it in `tests/test_cults_publish.py`
    - Start deploy on a published release, keep the manual tag, and run the publisher from `github.sha`
    - Updated the README and the root catalog notes
    - 38 tests passed
* Decisions made
    - A missing `User-Agent` counts as the banned agent, because `urllib` supplies `Python-urllib`
    - No lint or build command exists in this repository. The unittest suite is the check
* Insights
    - On a manual run, `github.sha` is the ref selected in Use workflow from, so the operator starts that run from `main`

## 2026-10-15 - QA - COMPLETE (PASS)

* Work completed
    - Reviewed implementation of `tools/cults_publish.py`, `.github/workflows/deploy.yaml`, `tests/test_cults_publish.py`, `tests/test_deploy_workflow.py`, `README.md`, and root `memory-bank/` files against the plan
    - Verified all 38 unit tests pass
    - Wrote `PASS` status to `memory-bank/active/.qa-validation-status` and recorded QA results in `memory-bank/active/tasks.md`
* Decisions made
    - Approved implementation as-is with `PASS` verdict
* Insights
    - Both the `User-Agent` header enforcement and the workflow checkout split (`github.sha` publisher vs. tag model checkout) match the planned design cleanly without regressions

## 2026-10-15 - REFLECT - COMPLETE

* Work completed
    - Wrote `memory-bank/active/reflection/reflection-cults-auto-deploy.md`
    - Compared the plan with the build and the QA pass
* Decisions made
    - The repeated tag expression stays. A job environment cannot supply `steps.*.with.ref`
* Insights
    - A test that only searches existing header values misses the `Python-urllib` agent `urlopen` adds when `User-Agent` is absent

## 2026-10-15 - REWORK - INITIATED

* Work completed
    - Operator chose rework over archive
* Decisions made
    - Prior complexity was Level 2
    - Remove the HTTP transport tests that assert the User-Agent string and the absence of `Python-urllib`
    - Do not replace them. The publisher still sends the header
* Insights
    - Those assertions lock a string. They do not show that Cults or Cloudflare accepts the request

## 2026-10-15 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Classified the rework as Level 1
* Decisions made
    - One test class. No new assertion replaces it
* Insights
    - A test that the header equals a constant goes red only when that constant is edited

## 2026-10-15 - BUILD - COMPLETE

* Work completed
    - Removed `HttpTransportTests` from `tests/test_cults_publish.py`
    - Suite is 36 tests, all passing
* Decisions made
    - No replacement test. The header stays in `tools/cults_publish.py`
* Insights
    - Level 1's failing-test step does not fit a deletion the operator asked for by name

## 2026-10-15 - QA - COMPLETE (PASS)

* Work completed
    - Evaluated removal of `HttpTransportTests` and unused imports in `tests/test_cults_publish.py` against plan and project brief requirements
    - Verified all 36 unit tests pass with `uv run --no-project --with pyyaml python -m unittest discover -s tests`
    - Recorded QA results in `memory-bank/active/tasks.md` and wrote `PASS` to `memory-bank/active/.qa-validation-status`
* Decisions made
    - QA validation passed without blocking findings
* Insights
    - Eliminating change-detector assertions that do not verify integration behavior aligns with TDD and testing best practices while leaving production HTTP headers intact


