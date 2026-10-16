# Active Context

## Current Task: cults-listing-placeholders
**Phase:** PLAN - COMPLETE

## What Was Done
- Planned four steps: parse the version and build the `blob/main` changelog URL, fill the three tokens, wire `publish`, then delete `images`
- Revised step 3 after preflight: `PublishTests` use `widget-v1.0.0`, and `_publish` can override the tag, before `publish` refuses a mismatched tag
- Tests stay in `tests/test_cults_publish.py`. The `img/not-uploaded.png` decoy stays in `write_repo`

## Next Step
- Re-run preflight after the `PublishTests` tag fix
