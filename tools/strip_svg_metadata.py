"""Strip editor and RDF metadata from SVG files in place."""
import re
import sys
import xml.etree.ElementTree as ET

_ELEMENTS = [
    re.compile(rf"[ \t]*<{name}\b[^>]*?/>[ \t]*\n?|[ \t]*<{name}\b[^>]*>.*?</{name}\s*>[ \t]*\n?", re.DOTALL)
    for name in ("metadata", "sodipodi:namedview")
]
_ATTRIBUTE = re.compile(r"""\s+(?:inkscape|sodipodi):[\w.-]+\s*=\s*(?:"[^"]*"|'[^']*')""")
_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
_COMMENT_TOKEN = "\x00COMMENT{}END\x00"


def _mask_comments(text):
    """Replace each complete comment with a token so tag patterns cannot see inside it."""
    comments = []

    def hold(match):
        comments.append(match.group(0))
        return _COMMENT_TOKEN.format(len(comments) - 1)

    return _COMMENT.sub(hold, text), comments


def _restore_comments(text, comments):
    """Put comments masked by _mask_comments back in their original places."""
    for index, comment in enumerate(comments):
        text = text.replace(_COMMENT_TOKEN.format(index), comment, 1)
    return text


def strip(text):
    """Return text without <metadata>, <sodipodi:namedview>, and inkscape: or sodipodi: attributes.

    Everything else, including comments, <title>, and <desc>, is unchanged.
    Tags named inside a comment stay in that comment.
    Raise ValueError when text does not parse, or when stripping would leave
    text that does not parse.
    """
    if not _parses(text):
        raise ValueError("file does not parse")
    masked, comments = _mask_comments(text)
    result = masked
    for pattern in _ELEMENTS:
        result = pattern.sub("", result)
    result = _ATTRIBUTE.sub("", result)
    result = _restore_comments(result, comments)
    if result != text and not _parses(result):
        raise ValueError("stripping would leave invalid XML")
    return result


def main(argv):
    """Strip each SVG path in argv in place. Return 1 if any file was refused."""
    status = 0
    for path in argv:
        with open(path, encoding="utf-8", newline="") as handle:
            text = handle.read()
        try:
            result = strip(text)
        except ValueError as exc:
            print(f"{path}: {exc}; strip its metadata by hand", file=sys.stderr)
            status = 1
            continue
        if result != text:
            with open(path, "w", encoding="utf-8", newline="") as handle:
                handle.write(result)
    return status


def _parses(text):
    try:
        ET.fromstring(text.encode("utf-8"))
    except ET.ParseError:
        return False
    return True


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
