# H7 bulb storage

A printed cover that stores a spare H7 headlamp bulb by its flange, with a clip that latches it in. To print one, use the [Cults listing](https://cults3d.com/en/3d-model/gadget/h7-bulb-storage). This directory is the source.

## Where things are

| Path | What it is |
| --- | --- |
| `h7_led_cover.py` | CadQuery source. Every dimension is set here. The docstring explains how the parts work and cites the source behind each default. |
| `h7_cover.*`, `h7_fit_test.*`, `clips/` | Files the script makes. They are committed so people can print without Python. |
| `measure_flange.svg` | To-scale drawing of the flange, to compare a bulb against before you change the flange parameters. |
| `tools/` | `check_fit.py`, the pass/fail test suite, and scripts that inspect the parts. |
| `publish.yaml` | The Cults listing: its text, print settings, and the files it ships. |
| `img/` | The listing photos. |
| `memory-bank/` | Design notes: what the cover must do, how the parts depend on each other, how to build and test. |

## Build

```sh
uv run --no-project --with cadquery python h7_led_cover.py
```

That rewrites the cover, the fit test and every clip, and prints the main sizes. Read `memory-bank/systemPatterns.md` before you change a parameter, and `memory-bank/techContext.md` for the checks to run after.

Releases and the Cults publish work the same for every model in this repository; see the [repository README](../../README.md).
