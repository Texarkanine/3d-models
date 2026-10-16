# Current Task: cults-gallery-refresh

**Complexity:** Level 1

## Fix

Cults kept deleted photos and STL previews on the public page after an update deploy. Asset adds and deletes do not change `updatedAt`, and the gallery rebuilds only when that timestamp changes. The text update ran before the file swap, so the page kept the in-between set.

After the old assets are removed, the publisher waits until every STL from the tag has a preview image, then sets `details` to a different value and restores it. That field change is what Cults counts. The wait is there because a gallery built before a preview exists stays without it. STEP files are not part of that wait: the page shows one preview per STL.

`updateIllustration` only takes a position, which would reorder the gallery, so it is not the bump. A read-back that fails the deploy unless the asset ids match the tag was left out; the issue marks it optional.

Files: `tools/cults_publish.py`, `tests/test_cults_publish.py`.

## QA Results

PASS (2026-10-15)

- Every plan item is implemented: the details edit-and-restore runs after the old assets are destroyed, it waits for one preview per tag STL, STEP files are not awaited, `updateIllustration` is unused, and the optional asset read-back is absent.
- New tests cover the bump order, the preview wait, the never-ready failure, the STEP exclusion, the missing-details-argument refusal, and the `details == "."` sentinel edge. Catalog suite: 66 passed.
- Advisory (non-blocking): `_gallery_state` repeats `_listing_assets`'s query-and-match-row shape; the poll loop could use for/else. Both acceptable as-is.
