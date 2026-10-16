"""Strip editor and RDF metadata from SVG files in place."""
import re
import sys
import xml.etree.ElementTree as ET

_ELEMENTS = [
    re.compile(rf"[ \t]*<{name}\b[^>]*?/>[ \t]*\n?|[ \t]*<{name}\b[^>]*>.*?</{name}\s*>[ \t]*\n?", re.DOTALL)
    for name in ("metadata", "sodipodi:namedview")
]
_ATTRIBUTE = re.compile(r"""\s+(?:inkscape|sodipodi):[\w.-]+\s*=\s*(?:"[^"]*"|'[^']*')""")


def strip(text):
    """Return text without <metadata>, <sodipodi:namedview>, and inkscape: or sodipodi: attributes.

    Everything else, including comments, <title>, and <desc>, is unchanged.
    Raise ValueError when text parses as XML and the result does not.
    """
    result = text
    for pattern in _ELEMENTS:
        result = pattern.sub("", result)
    result = _ATTRIBUTE.sub("", result)
    if result != text and _parses(text) and not _parses(result):
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
