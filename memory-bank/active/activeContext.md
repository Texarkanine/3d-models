# Active Context

## Current Task: cults-listing-placeholders
**Phase:** BUILD - COMPLETE

## What Was Done
- Filled `{version}`, `{changelog_url}`, and `{license_name}` in the boilerplate, the model description, and manufacturing
- The changelog URL is `https://github.com/<repository>/blob/main/models/<component>/CHANGELOG.md`
- `version_from_tag` runs before any Cults request and requires `<component>-v<version>`
- `name` is sent unchanged
- Deleted `images` from both publish records in `e40ac14`. The operator's uncommitted h7 manufacturing prose is still unstaged
- Files modified:
  - `/home/mobaxterm/git/3d-models/tools/cults_publish.py`
  - `/home/mobaxterm/git/3d-models/tests/test_cults_publish.py`
  - `/home/mobaxterm/git/3d-models/memory-bank/systemPatterns.md`
  - `/home/mobaxterm/git/3d-models/models/h7-bulb-storage/publish.yaml`
  - `/home/mobaxterm/git/3d-models/models/fire-extinguisher-rattlinator/publish.yaml`

## Next Step
- QA review
