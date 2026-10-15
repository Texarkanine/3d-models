"""The deploy workflow publishes one tag and writes the creation id back to main."""
import unittest
from pathlib import Path

import yaml

WORKFLOW = Path(__file__).resolve().parents[1] / ".github" / "workflows" / "deploy.yaml"


def load_workflow():
    return yaml.safe_load(WORKFLOW.read_text())


def steps(workflow):
    return workflow["jobs"]["deploy"]["steps"]


class DeployWorkflowTests(unittest.TestCase):
    def test_upload_step_runs_the_publisher_with_the_secret(self):
        upload = next(step for step in steps(load_workflow()) if step.get("name") == "Upload to Cults")
        self.assertIn("tools/cults_publish.py", upload["run"])
        self.assertIn("pyyaml", upload["run"])
        self.assertNotIn("exit 1", upload["run"])
        self.assertEqual(upload["env"]["CULTS3D_API_KEY"], "${{ secrets.CULTS3D_API_KEY }}")
        self.assertEqual(upload["env"]["TAG"], "${{ inputs.tag }}")

    def test_later_step_records_the_creation_id_on_main(self):
        workflow = load_workflow()
        self.assertEqual(workflow["permissions"]["contents"], "write")
        job_steps = steps(workflow)
        upload_at = next(
            index for index, step in enumerate(job_steps) if step.get("name") == "Upload to Cults"
        )
        later = [
            step for step in job_steps[upload_at + 1:]
            if "run" in step and "cults_creation_id" in step["run"] and "git push" in step["run"]
        ]
        self.assertEqual(len(later), 1)
        run = later[0]["run"]
        self.assertIn("main", run)
        self.assertIn("chore: record Cults creation id", run)
        self.assertIn("--set-creation-id", run)
