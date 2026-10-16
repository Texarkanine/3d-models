"""Printable paths named in publish.yaml point at files that are actually there."""
import json
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
MODELS_DIR = Path("models")
COMPONENTS = ("h7-bulb-storage", "fire-extinguisher-rattlinator", "h11-bulb-storage")


class PublishRecordTests(unittest.TestCase):
    def test_every_listed_printable_exists(self):
        for component in COMPONENTS:
            model = ROOT / MODELS_DIR / component
            record = yaml.safe_load((model / "publish.yaml").read_text())
            for path in record["files"] or []:
                self.assertTrue((model / path).is_file(), f"{component}/{path}")

    def test_release_please_manifest_uses_models_paths(self):
        manifest = json.loads((ROOT / ".release-please-manifest.json").read_text())
        for component in COMPONENTS:
            self.assertIn(f"models/{component}", manifest)

    def test_release_please_config_uses_models_paths(self):
        config = json.loads((ROOT / "release-please-config.json").read_text())
        for component in COMPONENTS:
            key = f"models/{component}"
            self.assertIn(key, config["packages"])
            self.assertEqual(config["packages"][key]["component"], component)
