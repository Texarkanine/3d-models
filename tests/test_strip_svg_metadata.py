"""SVG metadata stripping: what is removed, what stays, and what is refused."""
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.strip_svg_metadata import main, strip

INKSCAPE = """<?xml version="1.0" encoding="UTF-8"?>
<!-- keep this note -->
<svg xmlns="http://www.w3.org/2000/svg"
   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
   xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:dc="http://purl.org/dc/elements/1.1/"
   width="10" height="10"
   inkscape:version="1.3"
   inkscape:export-filename="/home/someone/drawing.png"
   sodipodi:docname="drawing.svg">
  <title>Part</title>
  <sodipodi:namedview id="nv" pagecolor="#ffffff" inkscape:window-width="1920">
    <inkscape:page x="0" y="0" width="10" height="10" />
  </sodipodi:namedview>
  <metadata id="m">
    <rdf:RDF><dc:creator>Someone</dc:creator></rdf:RDF>
  </metadata>
  <rect id="r" width="5" height="5" inkscape:label="box" />
</svg>
"""

COMMENT_AND_ELEMENTS = """<?xml version="1.0" encoding="UTF-8"?>
<!-- see <metadata> and <sodipodi:namedview> below -->
<svg xmlns="http://www.w3.org/2000/svg"
   xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd">
  <metadata>hello</metadata>
  <sodipodi:namedview id="nv"></sodipodi:namedview>
  <rect width="1" height="1"/>
</svg>
"""

COMMENT_ONLY = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg">
  <!-- see <metadata> below -->
  <rect width="1" height="1"/>
</svg>
"""

CDATA_COMMENT_START = """<svg xmlns="http://www.w3.org/2000/svg" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" inkscape:export-filename="/home/someone/a.png">
<text><![CDATA[<!--]]></text>
<metadata>Someone</metadata>
<!-- note -->
</svg>
"""

PI_COMMENT_START = """<svg xmlns="http://www.w3.org/2000/svg">
<?note <!-- ?>
<metadata>Someone</metadata>
<!-- note -->
</svg>
"""

UNPARSED = COMMENT_AND_ELEMENTS.replace(
    "<rect", "<text>a&nbsp;b</text>\n  <rect", 1)


class StripTests(unittest.TestCase):
    def test_editor_and_rdf_metadata_are_removed(self):
        result = strip(INKSCAPE)
        for gone in ("<metadata", "dc:creator", "namedview", "inkscape:page",
                     "inkscape:version", "export-filename", "docname", "inkscape:label",
                     "window-width", "/home/someone"):
            self.assertNotIn(gone, result)

    def test_drawing_title_and_comments_stay(self):
        result = strip(INKSCAPE)
        for kept in ("<title>Part</title>", "<!-- keep this note -->",
                     '<rect id="r" width="5" height="5"', 'width="10" height="10"'):
            self.assertIn(kept, result)

    def test_self_closing_metadata_is_removed(self):
        text = '<svg xmlns="http://www.w3.org/2000/svg"><metadata/><rect/></svg>'
        self.assertEqual(strip(text), '<svg xmlns="http://www.w3.org/2000/svg"><rect/></svg>')

    def test_svg_without_metadata_is_unchanged(self):
        text = '<svg xmlns="http://www.w3.org/2000/svg">\n  <rect width="1"/>\n</svg>\n'
        self.assertEqual(strip(text), text)

    def test_stripping_twice_changes_nothing_more(self):
        once = strip(INKSCAPE)
        self.assertEqual(strip(once), once)

    def test_result_that_would_not_parse_is_refused(self):
        text = ('<svg xmlns="http://www.w3.org/2000/svg">'
                "<metadata><![CDATA[</metadata>]]></metadata></svg>")
        with self.assertRaises(ValueError):
            strip(text)

    def test_metadata_mentioned_in_a_comment_stays_in_the_comment(self):
        ET.fromstring(COMMENT_AND_ELEMENTS.encode("utf-8"))
        result = strip(COMMENT_AND_ELEMENTS)
        self.assertIn("<!-- see <metadata> and <sodipodi:namedview> below -->", result)
        self.assertNotIn(">hello</metadata>", result)
        self.assertNotIn('id="nv"', result)
        self.assertIn("<svg", result)
        self.assertIn("<rect", result)
        ET.fromstring(result.encode("utf-8"))

    def test_comment_only_mention_is_unchanged(self):
        self.assertEqual(strip(COMMENT_ONLY), COMMENT_ONLY)

    def test_comment_start_inside_cdata_does_not_hide_metadata(self):
        result = strip(CDATA_COMMENT_START)
        self.assertNotIn("export-filename", result)
        self.assertNotIn("<metadata>", result)
        self.assertIn("<![CDATA[<!--]]>", result)
        self.assertIn("<!-- note -->", result)
        ET.fromstring(result.encode("utf-8"))

    def test_comment_start_inside_a_processing_instruction_does_not_hide_metadata(self):
        result = strip(PI_COMMENT_START)
        self.assertNotIn("<metadata>", result)
        self.assertIn("<?note <!-- ?>", result)
        self.assertIn("<!-- note -->", result)
        ET.fromstring(result.encode("utf-8"))


class MainTests(unittest.TestCase):
    def test_files_are_rewritten_in_place(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "a.svg"
            path.write_text(INKSCAPE, encoding="utf-8")
            self.assertEqual(main([str(path)]), 0)
            self.assertEqual(path.read_text(encoding="utf-8"), strip(INKSCAPE))

    def test_refused_file_is_left_alone_and_fails(self):
        text = ('<svg xmlns="http://www.w3.org/2000/svg">'
                "<metadata><![CDATA[</metadata>]]></metadata></svg>")
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "bad.svg"
            good = Path(tmp) / "good.svg"
            bad.write_text(text, encoding="utf-8")
            good.write_text(INKSCAPE, encoding="utf-8")
            self.assertEqual(main([str(bad), str(good)]), 1)
            self.assertEqual(bad.read_text(encoding="utf-8"), text)
            self.assertEqual(good.read_text(encoding="utf-8"), strip(INKSCAPE))

    def test_unparsed_file_is_not_written(self):
        with self.assertRaises(ValueError):
            strip(UNPARSED)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "a.svg"
            path.write_text(UNPARSED, encoding="utf-8")
            self.assertEqual(main([str(path)]), 1)
            self.assertEqual(path.read_text(encoding="utf-8"), UNPARSED)

    def test_empty_file_is_not_written(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "a.svg"
            path.write_text("", encoding="utf-8")
            self.assertEqual(main([str(path)]), 1)
            self.assertEqual(path.read_text(encoding="utf-8"), "")


if __name__ == "__main__":
    unittest.main()
