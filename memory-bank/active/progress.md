# Progress

Replace `{version}`, `{changelog_url}`, and `{license_name}` in the Cults boilerplate and in each model's `publish.yaml` description and manufacturing. The changelog URL is the file on `main`, with no fragment. Remove the unused `images` field. Leave `tags` and the listing title.

**Complexity:** Level 1

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

## 2026-10-15 - PREFLIGHT - COMPLETE

* Work completed
    - Re-ran Level 2 preflight against the revised `tasks.md`, the publisher, the tests, the publish-record tests, the workflow, and both publish records
    - Verified the prior blocking finding is resolved: `PUBLISH_TAG = "widget-v1.0.0"`, an overridable `_publish` tag, and repointed URL assertions are scheduled before the red run
    - First line of `.preflight-status`: `PASS WITH ADVISORY`
* Decisions made
    - No plan edits: the TDD ordering check found nothing to swap or strike
    - Unit 4 owes no tests: the publisher never reads `images`, and `test_publish_records.py` asserts only on `files` and release-please registration
* Insights
    - The operator's uncommitted h7 manufacturing prose and the `images: []` deletion are separate diff hunks, so `git add -p` can keep the prose out of the `chore` commit
    - Advisory: a leftover-token guard (`{verison}`-style typos refuse the deploy) would strengthen the "no tokens remain" criterion; recorded for the operator, not added to the plan

## 2026-10-15 - BUILD - COMPLETE

* Work completed
    - `version_from_tag` and `changelog_url` parse the tag and build the `blob/main` URL
    - `fill_listing_text` replaces the three tokens in the description, boilerplate, and manufacturing
    - `publish` fills the schema manufacturing argument and leaves `name` literal
    - Removed `images` from both `publish.yaml` files and from the system-patterns field list
    - Full suite: 79 tests passed
* Decisions made
    - The placeholder commit is `feat` and does not touch a model directory
    - The `images` removal is a separate `chore` so release-please does not cut a model release
    - No leftover-token guard. An unknown `{token}` stays literal
* Insights
    - `PublishTests` needed `widget-v1.0.0` once the tag must match the component
    - `write_repo` quotes fields with `json.dumps` so `{version}` is valid YAML

## 2026-10-15 - QA - COMPLETE

* Work completed
    - Reviewed the publisher, tests, system patterns, and both publish records against the plan and brief
    - Full suite: 79 tests passed
    - Wrote `.qa-validation-status`: PASS
* Decisions made
    - Three advisories, none blocking
* Insights
    - The double fill of manufacturing is idempotent because the built changelog URL and the version hold no tokens

## 2026-10-15 - REFLECT - COMPLETE

* Work completed
    - Wrote `memory-bank/active/reflection/reflection-cults-listing-placeholders.md`
    - Checked the persistent memory bank. `systemPatterns.md` already records the tokens, the untouched title, and the dropped `images` field
* Decisions made
    - Leave the double fill in place. The smaller shape is one fill in `publish` and a joiner that does not substitute
* Insights
    - `PublishTests` and `FileUrlTests` no longer share one tag

## 2026-10-15 - REWORK - INITIATED

* Work completed
    - The operator chose rework
* Decisions made
    - Complexity before this reclassification: Level 2
* Insights
    - On the Cults edit form, the manufacturing text is inside the 3D model description, under a Manufacturing heading. Settings and manufacturing instructions is empty

## 2026-10-15 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Classified the rework as Level 1
* Decisions made
    - It is a bug in one publisher: the manufacturing text is appended to the description
* Insights
    - The publisher only sends manufacturing to a schema argument whose name contains "manufactur". Otherwise it writes a Manufacturing section into the description

## 2026-10-15 - BUILD - COMPLETE

* Work completed
    - A failing update test expected manufacturing in `details` and not in the description
    - `_manufacturing_argument` now returns `details` when no name contains "manufactur"
    - Full suite: 80 tests passed
* Decisions made
    - An argument whose name contains "manufactur" still wins over `details`
* Insights
    - The gallery refresh reads `details` after the text update, so restoring it puts the manufacturing text back

## 2026-10-15 - QA - COMPLETE

* Work completed
    - Reviewed the `details` fallback, description omission, and gallery refresh against the task and brief rework note
    - Full suite: 80 tests passed
    - Wrote `.qa-validation-status`: PASS
* Decisions made
    - PASS with two advisories, none blocking
* Insights
    - Empty manufacturing on update preserves pre-existing `details`; the plan scoped files to the publisher and its tests, so no pattern-doc change was required
