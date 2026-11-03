# Commercial Electric wire stripper grips

Replacement grips for the Commercial Electric Double Jaw Wire Stripper, Cutter and Crimper, model CE190205, when its rubber grips have gone sticky. Print a grip in TPU 95A, pull the old one off, and slide the new one onto the bare steel handle. There is a grip for each handle: `curved_grip` for the curved one and `straight_grip` for the straight one. Both share one outside design, and each one's inside is shaped to its own steel. This directory is the source.

## Where things are

| Path | What it is |
| --- | --- |
| `steel.py` | The measured bare steel: the operator's readings, and the centre line, width, thickness and tip shape that the grips are built around. |
| `grips.py` | CadQuery source. Every design dimension is set here. The docstring explains how a grip works and prints. |
| `curved_grip.*`, `straight_grip.*` | The grips, as the script makes them, standing on the open end. They are committed so people can print without Python. |
| `curved_grip_fit_test.*`, `straight_grip_fit_test.*` | Each grip's open end alone, a quick print to check the bore on the steel after a change. They are for development and are not published. |
| `reference/` | How and when each reading was taken, and the photos that hold information not yet in numbers. |
| `tools/` | `overhang.py` lists faces that need support. |
| `publish.yaml` | The Cults listing. |
| `memory-bank/` | Design notes: what the grips must do, how the parts depend on each other, how to build and test. |

## Build

```sh
uv run --no-project --with cadquery==2.8.0 --with cadquery-ocp==7.9.3.1.1 python grips.py
```

That rewrites both grips and their fit tests, and prints each grip's main sizes. The CadQuery versions are pinned because the committed files are the ones that were printed and fit; `memory-bank/techContext.md` says why. `python steel.py` prints both handles' cross-checks without CadQuery. Read `memory-bank/systemPatterns.md` before you change a parameter, and `memory-bank/techContext.md` for the checks to run after.

Releases and the Cults publish work the same for every model in this repository; see the [repository README](../../README.md).
