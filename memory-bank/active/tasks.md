# Task: cults-listing-placeholders

* Task ID: cults-listing-placeholders
* Complexity: Level 2
* Type: simple enhancement

Replace `{version}`, `{changelog_url}`, and `{license_name}` in the Cults boilerplate and in each model's `description` and `manufacturing`. The changelog URL is the file on `main`, with no fragment. The listing title stays `name`. Remove the unused `images` field from the publish records.


## Test Plan (TDD)

### Behaviors to Verify

- Version from a tag: `version_from_tag("h7-bulb-storage-v1.0.2", "h7-bulb-storage")` → `1.0.2`
- Tag that does not start with `<component>-v`: `version_from_tag("h7-bulb-storage-v1.0.2", "other")` → `ValueError`
- Tag with an empty version: `version_from_tag("widget-v", "widget")` → `ValueError`
- Changelog URL: `changelog_url("Texarkanine/3d-models", "h7-bulb-storage")` → `https://github.com/Texarkanine/3d-models/blob/main/models/h7-bulb-storage/CHANGELOG.md`
- Changelog URL shape: that URL does not contain the tag and does not contain `#`
- Repository that is not `owner/name`: `changelog_url("nope", "widget")` → `ValueError`
- Model description tokens: description `See {changelog_url}#{version} under the {license_name}.` with version `1.0.2`, the changelog URL above, and license name `GNU General Public License` → the description contains the URL, `#1.0.2`, and the license name, and contains none of the three tokens
- Boilerplate tokens: boilerplate `Version {version}. {changelog_url}. {license_name}.` → the joined description contains `Version 1.0.2.`, the changelog URL, and the license name, and contains none of the three tokens
- Manufacturing folded into the description: manufacturing `Notes {version}` with no schema argument → the joined description contains `Notes 1.0.2` and does not contain `{version}`
- Manufacturing sent as a schema argument: `publish()` with manufacturing `Notes {version}` and a `manufacturingNotes` argument → the mutation variable equals `Notes 1.0.2`, and the description does not contain that sentence
- Listing title: `publish()` with name `Example {version}` → the mutation `name` is `Example {version}`
- Existing description behavior stays: license name replacement, manufacturing section present or absent, empty manufacturing, and `img/not-uploaded.png` from an `images` list is not uploaded

### Test Infrastructure

- Framework: `unittest`
- Test location: `tests/test_cults_publish.py`
- Conventions: one `unittest.TestCase` per concern; `write_repo` builds a temporary model; `FakeCults` records GraphQL variables; assertions read those variables
- New test files: none

## Implementation Plan

### 1. [x] Version and changelog URL — executable

- Files: `tools/cults_publish.py`, `tests/test_cults_publish.py`

1. Stub tests: add empty `test_version_from_tag`, `test_tag_must_match_component`, `test_empty_version_is_refused`, `test_changelog_url_is_blob_main`, and `test_changelog_url_refuses_a_bad_repository` on a new `ListingTextTests` class.
2. Stub interface: add `version_from_tag(tag, component)` and `changelog_url(repository, component)` with docstrings and empty bodies. Export them from the test import list.
3. Write tests and run red: assert the version, the exact changelog URL, the absence of the tag and of `#`, and `ValueError` for a mismatched tag, an empty version, and a repository that is not `owner/name`.
4. Write code and run green: `version_from_tag` returns the suffix after `<component>-v` and raises `ValueError` otherwise. `changelog_url` returns `https://github.com/<repository>/blob/main/models/<component>/CHANGELOG.md`, quoting path segments the way `file_url` does, and raises `ValueError` for a repository that is not `owner/name`.

### 2. [x] Fill the three listing texts — executable

- Files: `tools/cults_publish.py`, `tests/test_cults_publish.py`

1. Stub tests: add empty `test_description_fills_version_changelog_and_license`, `test_boilerplate_fills_the_same_tokens`, and `test_manufacturing_in_the_description_is_filled` on `DescriptionTests`.
2. Stub interface: add `fill_listing_text(text, *, version, changelog_url, license_name)`. Add keyword-only `version` and `changelog_url` to `assemble_description`. Update the four existing `assemble_description` calls to pass those keywords.
3. Write tests and run red: assert the operator's deep-link shape `{changelog_url}#{version}` becomes the `blob/main` URL plus `#1.0.2`, and that boilerplate and in-description manufacturing lose their tokens.
4. Write code and run green: `fill_listing_text` replaces `{changelog_url}`, then `{license_name}`, then `{version}`. `assemble_description` fills the model description, the boilerplate, and manufacturing before it joins them.

### 3. [x] Wire publish — executable

- Files: `tools/cults_publish.py`, `tests/test_cults_publish.py`

1. Stub tests: add empty `test_manufacturing_argument_is_filled` and `test_listing_name_is_not_filled` on `PublishTests`. Extend `write_repo` so a test can set `name`, `description`, and the boilerplate. Before those new tests are implemented, give `PublishTests` a tag that matches component `widget`: `PUBLISH_TAG = "widget-v1.0.0"`. Leave `TAG = "h7-bulb-storage-v1.0.0"` for `FileUrlTests`. Change `_publish` to `kwargs.setdefault("tag", PUBLISH_TAG)` and stop passing `tag=TAG`, so a caller can override the tag. Point the `PublishTests` URL assertions that interpolate `TAG` next to `models/widget` at `PUBLISH_TAG`. Run the existing `PublishTests` and confirm they stay green. Do that before the new tests are filled in.
2. Stub interface: no new public function. `publish` will call `version_from_tag`, `changelog_url`, and `fill_listing_text`.
3. Write tests and run red: call `_publish(..., tag="widget-v1.0.2")`. A `manufacturingNotes` variable is `Notes 1.0.2` when the yaml says `Notes {version}`. A name of `Example {version}` is sent unchanged. The description still contains the filled boilerplate.
4. Write code and run green: at the top of `publish`, before `_mutation_arguments` or any other Cults request, derive the version and changelog URL. Pass them into `assemble_description`, fill manufacturing before assigning the schema argument, and assign `name` from the yaml with no substitution. Run the existing `PublishTests` with the new tests and confirm the old ones stay green.

### 4. [x] Drop the unused images field — prose/policy

- Files: `models/h7-bulb-storage/publish.yaml`, `models/fire-extinguisher-rattlinator/publish.yaml`, `memory-bank/systemPatterns.md`
- No tests: prose/policy artifact

1. Delete only the `images` key from both `publish.yaml` files. In `models/h7-bulb-storage/publish.yaml`, leave the operator's uncommitted `manufacturing` prose as it is. Do not revert it, reformat the file, or stage that prose in this task's commit.
2. In `memory-bank/systemPatterns.md`, stop listing `images` as a publish field. Keep the statement that listing photos are the files in `img/`. Record that `{version}`, `{changelog_url}`, and `{license_name}` are replaced in the boilerplate, the model description, and manufacturing, and that `name` is not replaced because a later publish finds the listing by it.
3. Leave the `images: img/not-uploaded.png` decoy in `write_repo`. `test_publish_returns_the_creation_id` already asserts that path is not uploaded.
4. Commit the `images` removal with `chore` so release-please does not cut a model release for deleting an unread field. Keep that commit separate from a commit whose subject would bump a model.

## Technology Validation

No new technology - validation not required

## Dependencies

- `publish` already receives `tag`, `repository`, and `component`
- `deploy.yaml` already resolves the tag as `<component>-v<version>` before it runs the publisher
- Cults license names still come from `_license_name`

## Challenges & Mitigations

- `{changelog_url}#{version}` only works if `{version}` is replaced after `{changelog_url}`: `fill_listing_text` replaces in that order, and the built URL contains none of the tokens
- A tag suffix that does not belong to this component would publish the wrong version: `version_from_tag` requires the tag to start with `<component>-v` and refuses an empty suffix
- Manufacturing sent as a Cults argument never passes through the joined description: step 3 fills that string in `publish` before the payload assignment
- The changelog URL hardcodes `main`: that is the approved URL. A renamed default branch would 404 until this string changes
- `PublishTests` today pass `h7-bulb-storage-v1.0.0` with component `widget`: step 3 points those tests at `widget-v1.0.0` and runs them green before `publish` starts refusing a mismatched tag
- `{changelog_url}#{version}` does not scroll to a release-please heading. Those headings look like `## [1.0.2](…) (date)`, so the GitHub anchor is not `#1.0.2`. The publisher still adds no fragment. The operator writes the fragment
- Keep `str.replace` in the planned order. A single-pass `re.sub` is not part of this plan

## Pre-Mortem

- The joined description is filled and the schema manufacturing argument is not: step 3 is a separate red test on `manufacturingNotes`
- The implementation follows issue #2 and pins the URL to the tag: the changelog test asserts `blob/main` and asserts the tag is absent
- A test that the yaml files lack `images` would fail on an intended edit: step 4 adds no such test
- Substituting inside `name` would make the next publish miss the existing listing: step 3 asserts the name is sent unchanged

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [x] Preflight
- [x] Build
- [ ] QA
