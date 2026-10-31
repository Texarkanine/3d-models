# Tech Context

## Environment Setup

- The scripts in `tools/` need Python 3. `plot_curve.py` also needs Pillow. Run them from this directory, for example `uv run --no-project --with pillow python tools/plot_curve.py`.

## Build Tools

- `tools/reduce_curve.py` turns the curve offsets in `reference/measurements.md` into a centre line, and prints it with the cross-checks against the calipers.
- `tools/plot_curve.py` draws that centre line and outline to `reference/curve-rebuilt.png`, to compare with the tracing photo.

## Testing Process

- The final test is a TPU print slid onto the operator's tool.
