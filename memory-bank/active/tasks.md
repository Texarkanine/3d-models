# Current Task: cults-manufacturing-field

**Complexity:** Level 1

The manufacturing text was appended to the Cults description under a Manufacturing heading. `_manufacturing_argument` only matched a schema name containing "manufactur". Cults keeps those instructions in `details`, so the match failed.

`details` is now that argument when no name contains "manufactur". The description no longer gets the Manufacturing section. The gallery refresh still changes `details` and then restores the manufacturing text.

Files: `tools/cults_publish.py`, `tests/test_cults_publish.py`

## QA Result (2026-10-15): PASS

* Reviewed `tools/cults_publish.py` (`_manufacturing_argument` fallback to `details`, `assemble_description` omission, `publish` payload, gallery refresh) against this task and the project brief rework note.
* Full suite: 80 tests passed (`python -m unittest discover -s tests`).
* Advisories only, none blocking:
    - Empty manufacturing on update leaves pre-existing `details` in place (payload omits the key; refresh restores gallery state). Pre-existing semantics, out of scope.
    - `systemPatterns.md` does not name the `details` fallback; plan scoped files to the publisher and its tests, so no doc change required.
