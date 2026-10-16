# Progress

Replace `{version}`, `{changelog_url}`, and `{license_name}` in the Cults boilerplate and in each model's `publish.yaml` description and manufacturing. The changelog URL is the file on `main`, with no fragment. Remove the unused `images` field. Leave `tags` and the listing title.

**Complexity:** Level 2

## 2026-10-15 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Classified the task as Level 2 from the approved intent
* Decisions made
    - `{changelog_url}` is `https://github.com/Texarkanine/3d-models/blob/main/models/<component>/CHANGELOG.md`, not the tag and not a fragment
    - The same three tokens are replaced in `publish.yaml` `description` and `manufacturing`
    - `name` stays literal
    - Drop `images` from `publish.yaml`; keep `tags`
* Insights
    - Photos already come from each model's `img/` directory. The publisher does not read `images`
    - `tags` is sent as `tagNames` when the list is non-empty

## 2026-10-15 - PLAN - COMPLETE

* Work completed
    - Wrote the Level 2 plan in `memory-bank/active/tasks.md`
    - Mapped tests to `tests/test_cults_publish.py`
* Decisions made
    - `version_from_tag` requires the tag to start with `<component>-v`
    - `fill_listing_text` replaces `{changelog_url}`, then `{license_name}`, then `{version}`
    - The `images` decoy stays in the test fixture. No test asserts that the publish records lack the key
* Insights
    - A manufacturing schema argument bypasses the joined description, so `publish` must fill that string itself

## 2026-10-15 - PREFLIGHT - COMPLETE

* Work completed
    - Ran Level 2 preflight against `tasks.md`, the publisher, the tests, the workflow, and both publish records
    - First line of `.preflight-status`: `FAIL (fixable)`
* Decisions made
    - No plan edits: the TDD ordering check found nothing to swap or strike
* Insights
    - `PublishTests` pass `TAG = "h7-bulb-storage-v1.0.0"` with component `widget`, so `version_from_tag` would fail every existing publish test; the plan needs a unit-level substep that gives those tests a matching tag

## 2026-10-15 - PLAN - COMPLETE

* Work completed
    - Revised step 3 so `PublishTests` use `widget-v1.0.0` and `_publish` can override the tag
    - Scheduled the version check before any Cults request
    - Scheduled the token contract in `systemPatterns.md`, and a `chore` commit that deletes only `images`
* Decisions made
    - Keep ordered `str.replace`. Do not switch to `re.sub`
    - Do not stage the operator's uncommitted h7 manufacturing prose
* Insights
    - A `{changelog_url}#{version}` fragment will not scroll to a release-please heading. The publisher still adds no fragment
