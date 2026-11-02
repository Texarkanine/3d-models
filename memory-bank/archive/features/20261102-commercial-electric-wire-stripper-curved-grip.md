---
task_id: commercial-electric-wire-stripper-curved-grip
complexity_level: 3
date: 2026-11-02
status: completed
---

# TASK ARCHIVE: Commercial Electric wire stripper grips: the curved grip, its reworks, and the first straight grip

## SUMMARY

This task added the `models/commercial-electric-wire-stripper-grips/` model. It is a slide-on TPU 95A grip for each steel handle of a Commercial Electric wire stripper and crimper whose rubber grips went sticky from automotive fluids.

- **Curved grip:** built first (Level 3), from the operator's caliper readings and a pencil tracing.
- **Four reworks** followed, driven by test prints:
    1. a rounded lip at the open end;
    2. the flare back, with a rounded bevel;
    3. a bigger bevel;
    4. a stronger flare, plus straight grip iteration 1 from new straight readings.
- **What carried on:** curved iteration 5 (`e1b3528`) ships. Straight iteration 1 (`3046d4e`) led to the follow-up task `wire-stripper-grips-closed-end`, archived in the model's own memory bank. That task shipped straight iteration 2.

## REQUIREMENTS

- **Fit:** the inside follows the bare curved steel from A (the tip) to B (83.15 from A, where the old grip sat), through its measured curve and taper.
- **Feel:** snug enough to stay on, loose enough to slide on by hand in TPU 95A. The inside has grooves or texture for glue.
- **Outside:** a new design shared by both grips, not a copy of the old one.
- **The tool closes fully,** with the grip on.
- **Printing:** open end down, no supports.
- **Catalog:** the model lives in this catalog, with source, STL and STEP.
- **Reworks** (each printable iteration committed on its own):
    1. Round the sharp open-end edge on the bed.
    2. Bring back print 1's flare, with a small rounded bevel on the bed edge.
    3. Make that bevel taller.
    4. Put the open end's widest point 1.0 further out on both grips (a finger stop) while the tool still closes; record the straight readings; build the straight grip with the same design.

## IMPLEMENTATION

- **`steel.py`:**
    - The measured steel as `Handle`: a quartic centre line fitted to the traced centre points, with W and T from the calipers.
    - Every "from A" reading is a chord, converted to arc length.
    - The straight handle (rework 4): a constant centre line, W as one least-squares line through the tracing, T from the calipers at A and J to M.
- **`grips.py`:** CadQuery lofts of cross-sections square to the centre line. The parameters are named at the top, and `check_design` asserts the impossible cases.
- **Bore:** the steel plus `BORE_CLEAR` 0.3, with tight corners (`BORE_CORNER_R` 0.5), so a sharp steel corner clears by at least 0.15.
    - **Ribs:** eight lengthwise ribs near the corners, as ruled lofts.
        - The creative phase chose crush ribs, for a fit that holds without glue. At build the operator made them glue keys instead: a 0.1 bite, with valleys for glue and air.
        - Print 1 showed the grip holds dry anyway.
    - **Closed end:** a gable roof at 50 degrees in print, computed from the tip's lean. The bore runs `END_CLEAR` 1.0 past A.
- **Outside:** the creative phase's option A, a steel-offset rounded rectangle. The walls are measured from the steel face (`WALL_SIDE`, `WALL_FACE`, `CORNER_R` 4.8). A dome starts at the roof ridge's height, so the T wall at the ridge stays the body's.
- **Open end:** print 1's gradual flare. On the bed, the edge sits `BEVEL` in from the flare's full width; a 50-degree bevel rises from there, and a round (`RIM_R`) blends it into the flare. The open end is a true offset of the body, so the bevel keeps its angle at the corners.
- **Tool shut:** the first limit was inferred (5 mm of wall at B). It was replaced by the operator's measured gap with two grips on (`SHUT_GAP` 3.3, `SHUT_WALL`) and a worst-case term for the straight steel; at least 0.8 must be left.
- **Iterations:**

  | Commit | What it was | Outcome |
  |---|---|---|
  | `95e5f61` | Print 1 | Fits, holds dry; the bed edge is sharp. |
  | `da750d8` | Lip | Edge good; the flare lost. |
  | `c585867` | Not printed | — |
  | `87e777c` | Flare and bevel | Fits; "more flare". |
  | `e1b3528` | Curved iteration 5 | Ships. |
  | `3046d4e` | Straight iteration 1 | Its open end sits about 2.5 above the curved grip's; the stagger was kept. |

## TESTING

- **Checks:** ad hoc scripts in `.scratch/` (the operator's direction: no committed tests for shapes still being prototyped).
    - `verify.py`: mock steel never inside the bore wall; rib bites; thinnest wall; cap over the roof; fit test equal to the grip cut at `FIT_LEN`.
    - `lip.py`: the open end's profile by height.
    - `corner_bevel.py`: the bevel at least 49.9 degrees all round.
    - `slice_compare.py` and `shut_gap.py`, plus `tools/overhang.py`: only the roof's ridge strip overhangs.
- **Byte checks:** the curved STLs stayed byte-identical across refactors (the `Handle` change, the straight grip's addition).
- **Catalog suite:** OK.
- **Preflight and QA:**
    - QA failed once on copied values in the docs and once on a bevel flattened at the corners (`efac921`), caught by scanning the face normals all the way round.
    - Rework 4's preflight caught a gap guard modelling the wrong pair of grips.
- **Prints:** the operator's test prints, described above, decided each rework.

## LESSONS LEARNED

- **Lofts:**
    - In OpenCascade a smooth loft overshoots where the sections change fast: a fading rib bit 0.18 for 0.10. Loft such features ruled.
    - `Wire.fillet2D` needs every radius under half the shorter side.
    - Moving one end of a smooth loft moves every section, so "unchanged elsewhere" checks need a geometric tolerance.
- **Domes:** on a capped tube, start the dome at the inner roof's peak, or the wall at the roof's ends thins.
- **Sizes:** CadQuery's `BoundingBox()` is loose on lofted faces; measure sizes from a tessellation.
- **Calipers measure chords.** Convert to arc length before placing anything along a curve.
- **Bevels:** holding a corner radius while an outline shrinks flattens a bevel at the corners. Offset the corners with the walls, and check the angle all the way round, not only on the flats.
- **Measurements:** a measurement taken on a stand-in must be translated to the part that ships. The shut gap was measured with a curved grip on the straight steel.

## PROCESS IMPROVEMENTS

- **Confirm any requirement a design introduces** that the operator never stated. "Holds without glue" turned glue texture into crush ribs.
- **Model docs name parameters and give reasons;** they never copy values.
- **Type hand-written readings back in chat** for the operator to check before building from them.
- **Commit every printable iteration on its own,** so prints can be compared and old versions recovered.

## TECHNICAL IMPROVEMENTS

- Set the open end in the operator's terms (the widest point's reach and height, and the flare's slope), and derive `FLARE` and `BEVEL` from them.

## NEXT STEPS

None for this task. The follow-up `wire-stripper-grips-closed-end` shipped the pair, and its archive is in the model's `memory-bank/archive/`.
