# Commercial Electric wire stripper grips

Replacement grips for a Commercial Electric wire stripper and crimper whose rubber grips have gone sticky. Print a grip in TPU 95A, pull the old one off, and slide the new one onto the bare steel handle. Only the curved handle's grip exists so far; the straight handle's will share its outside. This directory is the source.

## Where things are

| Path | What it is |
| --- | --- |
| `steel.py` | The measured bare steel: the operator's readings, and the centre line, width and thickness that the grips are built around. |
| `grips.py` | CadQuery source. Every design dimension is set here. The docstring explains how a grip works and prints. |
| `curved_grip.*`, `curved_grip_fit_test.*` | Files the script makes, standing on the open end. They are committed so people can print without Python. The fit test is the grip's first 15 mm, a quick print to check the bore on the steel. |
| `reference/` | The dated measurement log, its photos, and the curve rebuilt from the tracing. |
| `tools/` | `plot_curve.py` redraws `reference/curve-rebuilt.png`; `overhang.py` lists faces that need support. |
| `publish.yaml` | The Cults listing. |
| `memory-bank/` | Design notes: what the grips must do, how the parts depend on each other, how to build and test. |

## Build

```sh
uv run --no-project --with cadquery python grips.py
```

That rewrites the curved grip and its fit test, and prints the main sizes. `python steel.py` prints the curve's cross-checks without CadQuery. Read `memory-bank/systemPatterns.md` before you change a parameter, and `memory-bank/techContext.md` for the checks to run after.

Releases and the Cults publish work the same for every model in this repository; see the [repository README](../../README.md).
