# Current Task: cults-creation-lookup

**Complexity:** Level 1

## Fix

- What broke: an update deploy raised "Cults has no creation with this id" for a design that exists. `creationsBatch(ids:)` filters on `creation.identifier` (`Creation/<number>`). The publisher sent the slug of `creation.id`. A slug does not filter, and `limit: 1` then returns the newest design.
- Why the earlier fixes held: they were checked when the target was the only design, or the newest one.
- What changed: the asset read and the gallery read page this account's designs and keep the row whose `id` equals the stored `cults_creation_id`. They do not send `ids`. `updateCreation` still receives that stored id.
- Files: `tools/cults_publish.py`, `tests/test_cults_publish.py`
