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
