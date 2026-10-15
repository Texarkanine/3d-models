---
task_id: cults-auto-deploy
date: 2026-10-15
complexity_level: 2
---

# Reflection: Automatic Cults deploy

## Summary

A published GitHub release starts Cults deploy, and Run workflow remains so the publisher on the selected branch can target an older tag. The Cults client sends `User-Agent: Texarkanine GitHub CICD for Cults3D`. QA passed. This work did not publish a tag.

## Requirements vs Outcome

All five requirements shipped. The manual action is still there. A manual run started from `main` checks the model files out from the tag and runs `publisher/tools/cults_publish.py` from `github.sha`. The omit-agent test also requires the header to be present, which is the same behavior: a missing header is how `urllib` sends `Python-urllib`.

## Plan Accuracy

The three-step order held, and the file list was right. The nested-checkout cleanup and the `github.sha` split were anticipated and did not need a redesign. The surprise was in the first red run: scanning header values for `Python-urllib` stayed green while the header was absent, because the banned agent is added by `urlopen`, not stored on the request we build.

## Build & QA Observations

Both executable steps went red, then green, and the suite ended at 38 tests. QA passed without a code change. Preflight and QA both noticed the repeated tag expression. A job-level environment variable cannot fill `steps.*.with.ref`, so the repetition stayed.

## Insights

### Technical

- Assert that the `User-Agent` header is present. `urllib.request.urlopen` adds `Python-urllib` only when the request does not already have one, so a scan of the headers you set will not see it.
- On `workflow_dispatch`, `github.sha` is the ref selected in Use workflow from. Starting that run from the old tag loads the old workflow file, which this change does not rewrite.

### Process

- Nothing notable

### Million-Dollar Question

The split we built is the foundational shape: model files from the tag, publisher from the workflow ref, one expression for the tag. GitHub Actions cannot take that expression from a job environment into `with.ref`, so writing it on each checkout and `TAG` binding is the small form, not a shortcut.
