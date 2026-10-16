# Active Context

## Current Task: cults-listing-placeholders
**Phase:** PLAN - COMPLETE

## What Was Done
- Planned four steps: parse the version and build the `blob/main` changelog URL, fill `{version}`, `{changelog_url}`, and `{license_name}` in the description, boilerplate, and manufacturing, wire `publish` so the schema manufacturing argument is filled and `name` is not, then delete `images` from the two publish records and from the system-patterns field list
- Tests stay in `tests/test_cults_publish.py`. The `img/not-uploaded.png` decoy stays in `write_repo`

## Next Step
- Preflight validation
