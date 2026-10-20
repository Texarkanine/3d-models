# Project Brief

## User Story

As a committer whose SVG hook strips metadata, I want a `<!--` that is not a real comment — inside CDATA or a processing instruction — left as text, so a real `<metadata>` element after it is still removed and the hook does not rewrite the file and exit 0 while leaving that element in place.

## Use-Case(s)

### Use-Case 1

An SVG has `inkscape:export-filename` on the root, `<text><![CDATA[<!--]]></text>`, a real `<metadata>` element, and a later comment. The hook removes the export path and the metadata element, keeps the CDATA text and the real comment, and exits 0.

### Use-Case 2

An SVG has `<?note <!-- ?>`, a real `<metadata>` element, and a later comment. The hook removes the metadata element, keeps the processing instruction and the real comment, and exits 0.

## Requirements

1. A `<!--` that begins inside a CDATA section is not a comment start.
2. A `<!--` that begins inside a processing instruction is not a comment start.
3. A real comment still protects tag names written inside it.
4. A real `<metadata>` element that sits between such a false start and a later comment is still removed.

## Constraints

1. The change stays in the SVG metadata stripper and its tests.
2. Unparsed files are still refused and left byte-identical.
3. Literal tag text inside CDATA stays on its current path. This task only stops a false `<!--` from hiding a real element.

## Acceptance Criteria

1. The reviewer's SVG loses `inkscape:export-filename` and `<metadata>Someone</metadata>`, keeps `<![CDATA[<!--]]>` and `<!-- note -->`, still parses, and the hook exits 0.
2. `<?note <!-- ?>` before `<metadata>` and a later comment loses the metadata element and keeps the processing instruction and the comment.
3. Existing comment, refusal, and empty-file tests still pass.
