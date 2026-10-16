---
task_id: cults-listing-placeholders
date: 2026-10-15
complexity_level: 2
---

# Reflection: cults-listing-placeholders

## Summary

The publisher now replaces `{version}`, `{changelog_url}`, and `{license_name}` in the shared boilerplate and in each model's description and manufacturing. The listing title is unchanged, and `images` is no longer a publish field. QA passed.

## Requirements vs Outcome

The approved brief is what shipped. `{changelog_url}` is the changelog on `main`, with no tag and no fragment, which overrides issue #2's "URL at that tag". `{version}` still comes from the tag. `tags` stayed. No leftover-token guard was added. Preflight offered one, and the build left unknown `{token}` text literal on purpose.

## Plan Accuracy

The four-step plan held. Preflight's one blocking finding was real: `PublishTests` passed `h7-bulb-storage-v1.0.0` with component `widget`, so a strict tag check would have failed the existing suite. The revised step gave those tests `widget-v1.0.0` before the new tests went red. The challenges that were written down (replace order, manufacturing sent as its own argument, hardcoded `main`) were the ones that mattered.

## Build & QA Observations

The red runs failed for the reasons the tests named. The full suite was 79 tests, all passing. QA passed with advisories only. The awkward spot was committing the `images` deletion without the operator's uncommitted h7 manufacturing prose. That prose is still unstaged.

## Insights

### Technical

- A shared `TAG` in `tests/test_cults_publish.py` is not safe to reuse once the tag must match the component. `FileUrlTests` still use the h7 tag. `PublishTests` use `widget-v1.0.0`.

### Process

- Nothing notable

### Million-Dollar Question

Fill each string once, in `publish`, and let `assemble_description` only join parts it is given. The license replacement used to live inside the joiner, so the plan filled manufacturing in both places. The second pass finds no tokens. One fill at the boundary is the smaller shape.
