# 3d-models

Publishable models. People download a single model from Cults, or from that model's GitHub release. This repository is the workshop: source, printable files, and one release stream per directory.

| Directory | What it is |
| --- | --- |
| `h7-bulb-storage` | Parametric H7 bulb cover and clip. Source is `h7_led_cover.py`. |
| `fire-extinguisher-rattlinator` | Solid Edge part. A TPU sleeve that stops an extinguisher handle from rattling in a car. |

Each directory has a `publish.yaml`. That file lists what a publish ships. Release-please cuts a version when commits land in that directory; the package list is `release-please-config.json`. Adding a model is both steps. Deploy is a separate workflow you run by hand against a tag. The Cults upload inside it is not wired yet. `author.yaml` holds the shared Cults nickname.

The license for this repository is AGPL-3.0. The license on a Cults listing is the `license_code` in that model's `publish.yaml`, chosen at publish time.
