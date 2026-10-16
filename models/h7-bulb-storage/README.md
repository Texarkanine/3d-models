# H7 bulb storage

A printed cover for a spare H7 headlamp bulb. It holds the bulb by its flange, the way a headlamp does. The head sits in a closed tube; the back of the bulb (heatsink, fan, cable) stays free, whatever its size. A clip slides through the collar and latches with a click.

To print one, get it from the [Cults listing](https://cults3d.com/en/3d-model/gadget/h7-bulb-storage). This directory is the source: how the files are made, and why they are shaped this way.

![The cover with a bulb in it](img/00-h7-bulb-storage.jpg)

## Files

| File | What it is |
| --- | --- |
| `h7_led_cover.py` | CadQuery source. Every dimension is a named parameter at the top. |
| `h7_cover.stl` / `.step` | The cover, turned to print orientation. |
| `h7_fit_test.stl` / `.step` | The collar and seat only: a quick print to check the flange, key and clip. |
| `clips/h7_clip_flange_A-Bmm.stl` / `.step` | The clip, one per flange-plate thickness band, A to B mm. |
| `measure_flange.svg` | To-scale drawing of the flange at the standard's largest sizes, the key blocks around it, and where the clip presses. Compare a bulb to it before you change the flange parameters. |
| `tools/` | The fit-check suite (`check_fit.py`) and scripts that inspect the parts. |
| `memory-bank/` | Design notes: what the cover must do, how the parts work together, how to build and test. |

## How it works

- Line the tab on the bulb's flange up with the notch on the back of the collar, and push the bulb in. Two key blocks fill the steps beside the tab, so the bulb sits one way and cannot turn.
- Slide the clip's arms through the tunnels in the collar, from either side. The arms are printed angled out a little, so pinch the tips to start them. A barb on each arm snaps out past the far face: that click is the latch. A bump on each arm presses the flange onto the seat.
- To release, squeeze the two tips together, push them back about 2 mm, and pull the clip out by its loop.

## Which clip

Measure the flange plate at its outer rim, where the clip arms cross it, and print the clip whose band contains it. The H7 standard makes the plate 0.6 to 0.8 mm thick, so start with **0.5-1.0**.

The bulb does not sit on its plate. It stands on three small lugs on the front of the plate, so the back of the plate, where the clip's bumps press, sits deeper than the plate is thick. The clips assume 1 mm deeper (`PLATE_SETBACK`), measured by fit on the operator's LED bulb with a 0.85 mm plate. The standard allows less. If a bulb rattles in the 0.5-1.0 clip, its plate sits closer to the seat: print **0.0-0.5**, which has a taller bump.

Before 2026-10-16, clip names gave that depth, which is 1 mm more: the old 1.5-2.0 clip is today's 0.5-1.0.

## What fits

The defaults are the H7 standard (cap PX26d) at its largest, plus clearance:

- Flange up to 34 mm across, plate up to 1.0 mm thick.
- Head up to 21 mm across and 54 mm long: the longest the standard allows (44 mm), plus 10 mm.
- Behind the seat, the bulb must be narrower than 29 mm for the first 4.5 mm beside the tab (key blocks), 26 mm for the first 5.4 mm where the clip arms cross, and 35 mm for the first 5.95 mm (collar).

Outside, the collar is 43 mm square and the cover is 62 mm long.

## Printing

- Cover: closed end down, no supports. The tunnel roofs are short bridges; if the slicer adds supports, turn on "don't support bridges".
- Clip: flat, as exported, at 100% infill, because the arms are springs. PETG keeps its spring longer than PLA.
- Print the cover and clips from the same build. They are one mechanism.

## Changing it

To fit an odd bulb, change the parameters at the top of `h7_led_cover.py` and rebuild:

```sh
uv run --no-project --with cadquery python h7_led_cover.py
```

That rewrites the cover, the fit test and every clip. `memory-bank/techContext.md` covers the checks to run, and `memory-bank/systemPatterns.md` covers what to keep in mind before you change anything.

## Sources

- IEC 60061-1 sheet 7004-5 (cap PX26d), read from its identical Russian adoption, GOST IEC 60061-1-2014. The [meganorm.ru copy](https://meganorm.ru/mega_doc/norm/gost_gosudarstvennyj-standart/18/gost_IEC_60061-1-2014_mezhgosudarstvennyy_standart_tsokoli_i.html) has the drawing. Flange O 33.8–34.0, tab K 7.9–8.0, centre to flat Q 13.2–13.7, front ring M 25.9–26.0, plate T 0.6–0.8, back of the plate Z at most 1.4 behind the reference plane (mm).
- UNECE R37 sheet H7/1, maximum lamp outline: Ø25 for 4.1 mm, then Ø19, at most 44 mm long.
- The MakerWorld screw-together H7 case cup (`h7-bulbholderv2.stl`), which uses Ø26.4 × 4 mm and Ø36.
- Test prints on the operator's bulbs.
