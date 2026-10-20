# Current Task: svg-comment-mask

**Complexity:** Level 1

## Fix

`<!--` inside CDATA or a processing instruction was masked as a comment through the next `-->`, so a real `<metadata>` element in between survived while other edits were written.

`_LITERAL_OR_COMMENT` matches CDATA and processing instructions first and copies them through. Only a real comment is replaced with a token.

Files: `tools/strip_svg_metadata.py`, `tests/test_strip_svg_metadata.py`.
