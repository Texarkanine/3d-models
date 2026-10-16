# Current Task: cults-manufacturing-field

**Complexity:** Level 1

The manufacturing text was appended to the Cults description under a Manufacturing heading. `_manufacturing_argument` only matched a schema name containing "manufactur". Cults keeps those instructions in `details`, so the match failed.

`details` is now that argument when no name contains "manufactur". The description no longer gets the Manufacturing section. The gallery refresh still changes `details` and then restores the manufacturing text.

Files: `tools/cults_publish.py`, `tests/test_cults_publish.py`
