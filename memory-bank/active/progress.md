# Progress

The comment mask must ignore a `<!--` that is not a real comment, inside CDATA or a processing instruction, so a real `<metadata>` element after it is still removed.

**Complexity:** Level 1

## 2026-10-20 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Restated the fix, the push, and the handoff, and the operator approved it.
    - Classified the fix as Level 1.
* Decisions made
    - Level 1: the bug is one matcher in `tools/strip_svg_metadata.py`.
    - Literal tag text inside CDATA stays out of this fix.
* Insights
    - The mask this branch added is what hides the metadata element. The element pattern still matches `<metadata>` when that span is not masked.
