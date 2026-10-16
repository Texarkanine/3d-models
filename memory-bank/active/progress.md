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
