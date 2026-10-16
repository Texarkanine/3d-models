"""The deploy workflow publishes one tag and writes the creation id back to main."""
import unittest
from pathlib import Path

import yaml

WORKFLOW = Path(__file__).resolve().parents[1] / ".github" / "workflows" / "deploy.yaml"
MODEL_TAG = (
    "${{ github.event_name == 'workflow_dispatch' && inputs.tag "
    "|| github.event.release.tag_name }}"
)


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
        self.assertIn("publisher/tools/cults_publish.py", upload["run"])
        self.assertEqual(upload["env"]["TAG"], MODEL_TAG)

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

    def test_published_release_starts_deploy(self):
        release = load_workflow()[True]["release"]
        self.assertEqual(release["types"], ["published"])

    def test_manual_tag_stays_required(self):
        tag = load_workflow()[True]["workflow_dispatch"]["inputs"]["tag"]
        self.assertIs(tag["required"], True)

    def test_model_checkout_uses_the_release_tag_or_the_manual_tag(self):
        job_steps = steps(load_workflow())
        checkout = next(
            step for step in job_steps
            if str(step.get("uses", "")).startswith("actions/checkout")
            and step.get("with", {}).get("lfs") is True
        )
        self.assertEqual(checkout["with"]["ref"], MODEL_TAG)
        resolve = next(step for step in job_steps if step.get("id") == "model")
        self.assertEqual(resolve["env"]["TAG"], MODEL_TAG)

    def test_publisher_checkout_uses_the_workflow_ref(self):
        checkout = next(
            step for step in steps(load_workflow())
            if step.get("with", {}).get("path") == "publisher"
        )
        self.assertEqual(checkout["with"]["ref"], "${{ github.sha }}")
        self.assertEqual(checkout["with"]["sparse-checkout"], "tools")

    def test_resolve_step_looks_under_models(self):
        resolve = next(step for step in steps(load_workflow()) if step.get("id") == "model")
        run = resolve["run"]
        self.assertIn("models/$component/publish.yaml", run)
        later = next(
            step for step in steps(load_workflow())
            if step.get("name") == "Record the Cults creation id on main"
        )
        self.assertIn("models/$COMPONENT/publish.yaml", later["run"])

    def test_creation_id_step_removes_the_publisher_checkout(self):
        job_steps = steps(load_workflow())
        upload_at = next(
            index for index, step in enumerate(job_steps) if step.get("name") == "Upload to Cults"
        )
        later = next(
            step for step in job_steps[upload_at + 1:]
            if "run" in step and "git checkout -B main" in step["run"]
        )
        run = later["run"]
        self.assertLess(run.index("rm -rf publisher"), run.index("git checkout -B main"))
