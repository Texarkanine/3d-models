# H11 bulb storage

A printed holder that stores a spare H11 headlamp bulb, halogen or LED, with the same push-and-twist lock as a car's socket. H8, H9 and H16 bulbs fit too. To print one, use the [Cults listing](https://cults3d.com/en/3d-model/gadget/h8-h9-h11-h16-bulb-storage). This directory is the source.

## Where things are

| Path | What it is |
| --- | --- |
| `h11_holder.py` | CadQuery source. Every dimension is set here. The docstring explains how the holder works and cites the source behind each default. |
| `h11_holder.*`, `h11_fit_test.*` | Files the script makes. They are committed so people can print without Python. The fit test is the open end alone, a quick print to check your bulbs. |
| `h11_connector_cap.py`, `h11_connector_cap.*` | A cap that latches onto the bulb's connector while it is stored, and the files it makes. Separate from the holder. |
| `measure_cap.svg` | To-scale drawing of the cap at its largest, with a letter for each size, to compare a bulb against before you change the cap parameters. |
| `tools/` | `check_fit.py`, the pass/fail test suite, and scripts that draw the diagram and inspect the parts. |
| `publish.yaml` | The Cults listing: its text, print settings, and the files it ships. |
| `img/` | The listing photos. |
| `memory-bank/` | Design notes: what the holder must do, how the parts depend on each other, how to build and test. |

## Build

```sh
uv run --no-project --with cadquery --with shapely python h11_holder.py
```

That rewrites the holder and the fit test, and prints the main sizes. `h11_connector_cap.py` needs only `cadquery` and rewrites the connector cap. Read `memory-bank/systemPatterns.md` before you change a parameter, and `memory-bank/techContext.md` for the checks to run after.

Releases and the Cults publish work the same for every model in this repository; see the [repository README](../../README.md).
