# System Patterns

## How This System Works

`h7_led_cover.py` is the single source of truth. Every dimension is a named parameter at the top; the "Derived" block computes the rest, and both parts (cover and clip) are built from those same derived values. The STL and STEP files are generated outputs, committed so people can print without running Python.

Know these before changing anything:

- **The cover and the clip are one mechanism.** Tunnel sizes, where the barbs catch, bump heights and arm positions all come from the same derived values. Any change to a bulb or fit parameter moves both parts, so a cover and a clip from different commits usually will not latch. Regenerate and print them as a matched set.
- **Print orientation is designed in, not chosen in the slicer.** The cover prints closed end down. The tunnel roofs, which the clip arms rest and slide on, print as short bridges held on both sides; that is why the collar is square. `SHOULDER` is set so the rounded corner ridges come out at 45 degrees. Changing the collar outline, shoulder or tunnels can create overhangs or unanchored roofs that look fine on screen. The one deliberate exception is the roof over each barb groove across the bore. It is held on one side only, so it is kept to a 1 mm flat ledge (`GROOVE_LEDGE`) and then rises at 45 degrees.
- **Inside the bore, nothing may sit under the clip arm.** The arms are springs that bend between the tunnel roofs at ±`X_SUPPORT`. A roof under an arm in the bore shortens that span and makes the clamp much stiffer. Any guide there must stay outside the arm, as the barb-groove roof does. Nothing may sit inside the bore circle at all, because the flange goes in from the back.
- **Defaults are anchored to the H7 cap standard (PX26d)** at its largest sizes, plus clearance. Parameter comments name the standard's letter (O, K, Q, M) behind each value. Do not tune defaults to one measured bulb.
- **The assertions are geometry limits**, not style checks: arms inside the bore, barb catching on the flat of the collar face, bump fitting the tunnel, tip long enough for the barb. They fail when the script runs. Do not delete one to make a change go through.
- **`README.md` repeats derived sizes** (collar, length, the "What fits" envelope). Update it when parameters change; the script prints the main sizes on each run. The README is the welcome for source readers; design detail belongs here.

## Coordinates: built in use position

Parts are modelled where they sit in use: z = 0 is the seat (the bulb's reference plane), +z points to the bulb tip, the tab is at +x, the clip slides along x, the arms run at ±y. `to_print_cover` and `to_print_clip` turn the parts to print orientation only at export. Seen from the back (heatsink side), +y points down. See the module docstring.

## Mirror in y, symmetric in x

Clip-path and key geometry is built for the +y side and mirrored with `both_sides`. The clip path is symmetric along x so the clip goes in from either side. New tunnel or key features must keep both symmetries.

## One clip per flange-plate band

Flange plates vary between bulbs, so the clip is exported once per 0.5 mm band (`CLIP_VARIANTS`); only the spring bump height differs. Bands and file names are the plate thickness at its rim, which users can measure. The bulb rests on three lugs in front of the plate, so the bump presses on the back of the plate, `PLATE_SETBACK` deeper than the plate is thick (PX26d: plate T 0.6-0.8, back Z at most 1.4). `bump_height` builds for band + setback. The setback (1.0) comes from the operator's bulb, not the standard. Before 2026-10-16 the bands named that depth, so old names are 1.0 mm higher.

## The clip is a preloaded spring

The arms are printed turned out `ARM_SPREAD` (1.5 degrees) about the bridge bar; the far tunnel pushes them back, so they press the barbs out. A rigid model cannot bend them, so the clip has three poses, and each check must use the right one:

- `clip()` (default `spread=HELD_SPREAD`): in use, the arm held with its edge on the far tunnel wall. Fit, catch, flange squeeze and body clearance are checked here.
- `printed_clip()` (`ARM_SPREAD`): what is exported. Only the preload check (section L) uses it; its overlap with the cover is the preload, not a collision.
- `clip(spread=0)`: pressed straight, as the tunnels hold the arm while it slides. The insertion and release sweeps (B, C, D) use it.

A new clip feature must say which pose each of its checks uses.

## Test prints are tagged

Each version sent to the printer for testing gets a git tag `h7-bulb-storage-v<N>-print<M>`. The directory name is the prefix so the tag does not collide with another model in this repo. The outcome is recorded as a SumMem note for this model (`.summem/summem note --path models/h7-bulb-storage/...`). Earlier outcomes are in `README.txt` in git history, under the old clip names (1.0 mm higher than today's).

The cover and the clip now in this directory are a matched set: v2 changed only the clip, and the cover is v1's.
