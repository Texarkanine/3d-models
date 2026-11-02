---
task_id: wire-stripper-grips-closed-end
complexity_level: 2
date: 2026-11-02
status: completed
---

# TASK ARCHIVE: Wire-stripper grips: the closed end, and the pair that ships

## SUMMARY

The operator found hollow space past the steel tip in the printed grips: it flexes and carries no load. The task modelled the steel tips' shape and built a closed end that sits on the rounded tip: curved grip iteration 6 and straight grip iteration 2 (`a61aa6d`), 1.77 and 3.03 shorter.

The operator printed both. In a rework they kept the pair that fits as the original grips did: straight iteration 2, and the earlier, longer curved iteration 5 (`e1b3528`). One source now builds exactly that pair, byte for byte. The rework also filled out the publish record and cleaned the model directory for publishing. The photos are the operator's to add.

## REQUIREMENTS

- **Closed end:** the bore follows the steel's rounded tip with `BORE_CLEAR` all round. The roof slopes stay at `ROOF_ANGLE` (no supports). The solid end stays `DOME_LEN`, so the grip gets shorter. The open ends and their stagger do not change.
- **Readings:** the tips' shape and the old straight grip's depth go into `steel.py` and the dated log. Each radius is read small.
- **Rework:**
    - one source builds curved iteration 5 and straight iteration 2, byte for byte;
    - `publish.yaml` is filled out as far as the facts allow;
    - the model's docs describe only the two grips that ship;
    - the alternatives (full-length straight `3046d4e`, shorter curved `a61aa6d`) stay findable in SumMem.
- **Commits:** each printable iteration is committed on its own.

## IMPLEMENTATION

- **`steel.py`:**
    - `Handle.tip_r` (the tip's corner radius in the plane of the handles), `tip_flat()` and `tip_short(u)`.
    - Curved `TIP_R` 1.5: a flat end with rounded corners, from the tracing alone.
    - Straight `STRAIGHT_TIP_R` 3.3: a half circle. The old straight grip's floor is 1.2 deeper at the centre than near the edge, and a half circle gives 1.21 at 0.75 in from the side.
    - `OLD_STRAIGHT_DEPTH` (84.8, 83.6) and `OLD_DEPTH_EDGE_IN` (inferred) for the cross-check.
- **`grips.py`:**
    - `END_CLEAR = {"curved": 1.0, "straight": None}`: the closed end per grip.
    - **A length (curved):** `gap_roof()`. The bore runs that far past A at full width, as over a square tip, then a gable rises from the end section's corners to a ridge strip at the apex. The ribs run to A and fade over `END_CLEAR`.
    - **`None` (straight):** `tip_roof()`, worked in a frame at the start of the tip's round. Each slope is the lowest line at `ROOF_ANGLE` in print that clears the tip grown by `BORE_CLEAR`, and below it the bore follows the round. The ridge strip is where the slopes are `RIDGE_W` apart. The cap is a ruled loft of `rrect` rows whose first row is the body's last section, so the two share a face. The ribs fade over `RIB_FADE` and end where the round starts.
    - `closed_end()` gives `(past, ridge)`; the dome starts at `-past`.
    - Guards in `check_design`:
        - the tip radius is between 0 and W/2;
        - `ROOF_ANGLE` is at least 45;
        - `RIB_FADE` is above 0;
        - `END_CLEAR` is a length or `None`;
        - for a tip-seated roof, each slope meets its own corner (lean less than `ROOF_ANGLE`, and the two under 90) and the slopes close only above the tip.
    - `sizes()` reports each grip's closed end. Its last row is "at A" for the curved grip and "round starts" for the straight one.
- **The pair, byte for byte:** each closed end keeps its own iteration's code, down to the rib rule. The straight grip's last rib section is at 4.299999999999997, so one shared `>=` rule would have changed its STL.
- **Shipped figures:**

  | Grip | Ridge past the tip | Grip ends past the tip |
  |---|---|---|
  | Curved | 4.66 | 9.66 |
  | Straight | 2.30 | 7.30 |
- **Publish record (`publish.yaml`):**
    - description and manufacturing (TPU 95A, open end down, no supports);
    - 13 tags and `gpl`;
    - Tool (`Q2F0ZWdvcnkvMjc`), with Hand Tools (`Q2F0ZWdvcnkvMTAz`) and Spare Parts (`Q2F0ZWdvcnkvMTA1`), read from the Cults API;
    - 8 files: both grips and both fit tests, as STL and STEP.
- **Docs:**
    - `systemPatterns.md`, `productContext.md`, `techContext.md` and the README describe the shipped pair. The iteration histories and hashes are gone, and the reasons stay.
    - The CadQuery versions are pinned: 2.8.0 and OCP 7.9.3.1.1.
    - The measurement log gained "Tips and depths (2026-11-01)".
- **Commits:**
    - `0e75770`: the tip readings;
    - `a61aa6d`: curved iteration 6 and straight iteration 2;
    - `f5fefa5`: the report fix;
    - `ceaf1d8`: the shipped pair;
    - `154d883`: the publish record and the clean-up.

## TESTING

- **Checks:** ad hoc scripts in `.scratch/wirestripper-grip/` (the model's direction), each written first and run red:
    - `tip_check` (the readings, the old-grip cross-check, the steel report unchanged);
    - `closed_end` (the ridge height, the rows, the STL height);
    - `verify` (no steel in the wall; the tip's arcs 0.2989 to 0.3000 from the bore; the caps; the rib bites and volumes; the fit tests);
    - `slice_compare` (CAD sections: the open ends moved at most 0.013);
    - `roof_angles` (the roof's faces at 50 to 90 degrees; only the 2.9 mm² ridge strip flatter);
    - `design_guards`, `report_check`, and `pair_check` (a fresh build in a temporary folder, and the committed files, byte for byte against `e1b3528` and `a61aa6d`);
    - also `lip`, `corner_bevel`, `shut_gap` and `tools/overhang.py`.
- **Catalog suite:** 88 OK.
- **Preflight:** four runs:
    - the ridge's figures had to be the strip's, not the apex's;
    - B5 had to compare CAD, not STL;
    - the build and the STEP restore had to be checked against git, with pinned versions.
- **QA:** three runs. One fail: the size report's "at A" row still described a square tip. Then two passes.
- **Prints:** the operator printed curved iteration 6 and straight iteration 2, and chose the shipped pair from them and curved iteration 5.

## LESSONS LEARNED

- **The STL export misses its tolerance on lofted faces.** It strays up to 0.094 from its CAD at a 0.01 tolerance, so changes of hundredths are compared on CAD sections.
- **Ruled ribs between sections 4 apart bite about ± 0.015 between sections** on the curved bend. Size checks at fixed stations to that.
- **Model the steel's tip from the start.** The square-tip assumption made more than half of the hollow.
- **Keep each printed variant's code path whole.** Unify only what is bit-identical, and prove it with a fresh build compared byte for byte, on pinned CadQuery versions.

## PROCESS IMPROVEMENTS

- **Quote the modelled quantity, not a proxy.** The apex figures given in chat were 0.1 above the strip the build used.
- **Check the build's own printed report** when geometry near a reported station changes.
- **Pausing to measure before planning** turned a shifting request into the right change.
- **One commit per printable iteration** made "keep this one from that one" a precise request.

## TECHNICAL IMPROVEMENTS

- A general closed end (the steel grown by the clearance, filled up to the print's overhang limit) would take any traced tip. It earns its place only for a new design, not for the two printed closed ends kept here.
- A committed byte check (`grips.py --check` against a record of the printed files' hashes) would make "what ships is what was printed" permanent.

## NEXT STEPS

- Operator: listing photos in `img/` before the release merges. The description says "as pictured", and the publisher will create the listing without photos.
- Operator: confirm shipping the fit tests, and add the tool's model number or SKU to the description if known.
- Optional: finer STL export (preflight, 2026-11-01): 0.094 down to about 0.03 of mesh error, for about 40% larger files.
