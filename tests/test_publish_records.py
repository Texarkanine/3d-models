"""Printable paths named in publish.yaml point at files that are actually there."""
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
MODELS = ("h7-bulb-storage", "fire-extinguisher-rattlinator")


class PublishRecordTests(unittest.TestCase):
    def test_every_listed_printable_exists(self):
        for model in MODELS:
            record = yaml.safe_load((ROOT / model / "publish.yaml").read_text())
            for path in record["files"] or []:
                self.assertTrue((ROOT / model / path).is_file(), f"{model}/{path}")
