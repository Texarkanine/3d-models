# Current Task: svg-comment-mask

**Complexity:** Level 1

## Fix

`<!--` inside CDATA or a processing instruction was masked as a comment through the next `-->`, so a real `<metadata>` element in between survived while other edits were written.

`_LITERAL_OR_COMMENT` matches CDATA and processing instructions first and copies them through. Only a real comment is replaced with a token.

Files: `tools/strip_svg_metadata.py`, `tests/test_strip_svg_metadata.py`.

## QA Results

- **Status:** PASS
- **Findings:** None. `_LITERAL_OR_COMMENT` cleanly consumes CDATA and processing instructions before comments, preserving literal spans while masking only real `<!--...-->` comments. Both use cases and all acceptance criteria in `projectbrief.md` are covered by unit tests.

