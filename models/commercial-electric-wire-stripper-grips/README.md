# Commercial Electric wire stripper grips

Replacement grips for a Commercial Electric wire stripper and crimper whose rubber grips have gone sticky. Print a grip in TPU 95A, pull the old one off, and slide the new one onto the bare steel handle. There is a grip for each handle, the curved one and the straight one. Both share one outside design, and each one's inside is shaped to its own steel. This directory is the source.

## Where things are

| Path | What it is |
| --- | --- |
| `steel.py` | The measured bare steel: the operator's readings, and the centre line, width, thickness and tip shape that the grips are built around. |
| `grips.py` | CadQuery source. Every design dimension is set here. The docstring explains how a grip works and prints. |
| `curved_grip.*`, `curved_grip_fit_test.*`, `straight_grip.*`, `straight_grip_fit_test.*` | Files the script makes, standing on the open end. They are committed so people can print without Python. Each fit test is its grip's open end alone, a quick print to check the bore on the steel. |
| `reference/` | The dated measurement log, its photos, and the curve rebuilt from the tracing. |
| `tools/` | `plot_curve.py` redraws `reference/curve-rebuilt.png`; `overhang.py` lists faces that need support. |
| `publish.yaml` | The Cults listing. |
| `memory-bank/` | Design notes: what the grips must do, how the parts depend on each other, how to build and test. |

## Build

```sh
uv run --no-project --with cadquery python grips.py
```

That rewrites both grips and their fit tests, and prints each grip's main sizes. `python steel.py` prints both handles' cross-checks without CadQuery. Read `memory-bank/systemPatterns.md` before you change a parameter, and `memory-bank/techContext.md` for the checks to run after.

Releases and the Cults publish work the same for every model in this repository; see the [repository README](../../README.md).
