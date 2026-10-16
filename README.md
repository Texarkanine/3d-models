# 3d-models

Publishable models. People download a single model from Cults, or from that model's GitHub release. This repository is the workshop: source, printable files, and one release stream per directory.

| Directory | What it is |
| --- | --- |
| `models/h7-bulb-storage` | Parametric H7 bulb cover and clip. Source is `h7_led_cover.py`. |
| `models/fire-extinguisher-rattlinator` | Solid Edge part. A TPU sleeve that stops an extinguisher handle from rattling in a car. |

Each model directory has a `publish.yaml`. That file lists what a publish ships. Release-please cuts a version when commits land in that directory; the package list is `release-please-config.json`. Adding a model is both steps. Publishing a GitHub release starts deploy for that tag. Run workflow remains for an older tag: start it from the branch that contains the current publisher, and pass the tag. The tag selects the model files. The publisher is the one from that branch. It publishes that model's listing to Cults. `author.yaml` holds the shared Cults nickname.
