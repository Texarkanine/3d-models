# Task: Curved grip for the Commercial Electric wire stripper

* Task ID: commercial-electric-wire-stripper-curved-grip
* Complexity: Level 3
* Type: feature (new model)

A slide-on TPU 95A grip for the bare curved steel handle. The inside follows the measured curve and taper from A (the tip) to B (83.15 mm from A), with texture for glue. The outside is a new design that the straight grip will share later. The grip prints open end down without supports. It ships as STL and STEP from a CadQuery source in `models/commercial-electric-wire-stripper-grips/`.

## Component Analysis

### Affected Components

- `models/commercial-electric-wire-stripper-grips/steel.py` (new): the measured bare steel. It holds the operator's readings, citing `reference/measurements.md`, and reduces the tracing offsets to a centre line, plus W(s) and T(s) along it. It is pure Python (no CadQuery), so both the tools and the CAD source can import it. The straight handle's data goes here later.
- `.../grips.py` (new): the CadQuery source. It builds the mock steel, the grip and a short fit test from a handle description (centre line and W/T profile). It turns them to print orientation and writes `curved_grip.{step,stl}` and `curved_grip_fit_test.{step,stl}`. Every design dimension is a named parameter, and the script asserts the geometry limits. The builder takes a handle description, so the straight grip later only needs new steel data.
- `.../tools/check_fit.py` (new): pass/fail suite in the h7/h11 style (lettered sections, PASS/FAIL lines, exits 1 on failure).
- `.../tools/overhang.py` (new): copied from h11, which copied it from h7.
- `.../tools/reduce_curve.py`, `tools/plot_curve.py` (existing): their data moves into `steel.py`, so they import it instead of holding their own copy.
- `.../publish.yaml`: the `files` list gets the grip, and the description and manufacturing text are filled in. License, category and tags stay blank until the operator publishes.
- `.../README.md` (new): directory map in the h7 style.
- `.../memory-bank/systemPatterns.md`, `techContext.md`: record how the source works, and how to build and check it.
- `.../reference/measurements.md`: the dated record of the readings. It points to `steel.py` for the values the model uses.

### Cross-Module Dependencies

- `steel.py` → `grips.py`: centre line and W(s), T(s). The mock steel and the bore both come from it.
- `steel.py` → `tools/reduce_curve.py`, `tools/plot_curve.py`: same data, no second copy.
- `grips.py` → `tools/check_fit.py`: the parts are built in use position, and checked against the mock steel and the raw readings.
- `grips.py` outputs → `publish.yaml` `files` → `tests/test_publish_records.py`: listed files must exist.

### Boundary Changes

- `publish.yaml` `files` becomes non-empty. That is the public listing contract from the first release on.
- No catalog tooling changes. The model was registered in the setup commit.

### Invariants & Constraints

- The bore must contain the measured steel from A to B. Grip material may enter the steel's outline only where a designed contact feature presses on it, and only by its designed amount.
- The open end must sit at B, square to the steel there. The bore's closed end must leave clearance past A.
- On the convex side of the curve, which faces the straight handle, the wall at B must be no thicker than the old grip's (5 mm). That keeps the tool closing and leaves a future straight grip the room the old one had. F = 9 mm was measured with the old straight grip on.
- Print orientation is designed in: open end flat on z = 0. No downward face is flatter than 45 degrees, except bridges held on both sides that are 2 mm or less. The bore's closed end is a roof, not a flat ceiling.
- The fit must slide on by hand in TPU 95A and still stay on.
- One home per number: `steel.py` holds the readings the model uses, and `reference/measurements.md` is the dated record they cite.
- Non-goals: the straight grip, copying the old grip's outside, changing the steel.
- Catalog tests stay green, and exported STLs are watertight.

## Open Questions

- [x] **Bore fit and glue key.** → Resolved: longitudinal crush ribs, two per face near the corners, on a clearance bore with relieved corners. The valleys are the glue and vent channels. The bite is lighter in T than in W, because T barely tapers. The fit test tunes it. (see `memory-bank/active/creative/creative-bore-fit-and-glue-key.md`) Original question: How does the inside grip the steel in TPU 95A and give glue a surface? The options: a plain bore with uniform interference plus separate glue grooves; longitudinal crush ribs whose valleys double as glue channels; or circumferential grooves. They trade off differently in slide-on force, tolerance to the ±0.35 mm spread in the W readings, printability when standing up, and how well glue keys. It must slide on by hand, stay on, keep its texture after vapor-smoothing, and print without support.
- [x] **Outside shape.** → Resolved: steel-offset rounded rectangle. Walls are measured from the steel (3.8 in the plane of the handles, 2.5 across it), with large corner radii. It follows the steel's curve and taper, flares 1.0 at the open end (convex wall at B is 4.8, at most 5.0), and has a domed closed end. No sculpting yet. (see `memory-bank/active/creative/creative-outside-shape.md`) Original question: What cross-section, size profile, end and mouth details should the outside have, so the curved and straight grips share one design? The original is a near-square 19.75 × 20.67 at a collared mouth. The design is open: wall thicknesses, a palm swell, a flared mouth, how the tip is rounded. It must respect the 5 mm convex-side wall at B, print open end down without support, be comfortable, and work on a straight handle later.

## Status

- [x] Component analysis complete
- [ ] Open questions resolved
- [ ] Test planning complete (TDD)
- [ ] Implementation plan complete
- [ ] Technology validation complete
- [ ] Pre-Mortem complete
- [ ] Preflight
- [ ] Build
- [ ] QA
