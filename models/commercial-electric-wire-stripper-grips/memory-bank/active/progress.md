# Progress

Take the hollow space out of both grips' closed ends. The bore's roof comes down onto the steel's rounded tip, with `BORE_CLEAR` all round. The solid end keeps its thickness, so the straight grip gets about 2.9 shorter and the curved one about 1.7. The tip shapes and the operator's new depth readings are recorded as steel readings. The open ends do not change.

**Complexity:** Level 2

## 2026-11-01 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Print feedback recorded as SumMem and OptMem notes: straight grip iteration 1 (`3046d4e`) went on, and its open end sits about 2.5 above the curved grip's.
    - Measured in the model: the straight grip reaches 10.33 past the tip (5.33 of it hollow) and the curved one 9.66 (4.66 hollow).
    - Swept the tip corner radius: a roof seated on a half-circle straight tip saves 2.92; on 1.5 mm curved corners, 1.66 (`.scratch/wirestripper-grip/tip_roof_sweep.py`).
    - Baselines saved in `.scratch/wirestripper-grip/baseline/`: curved iteration 5's and straight iteration 1's STLs, and the steel report at `5d73490`.
* Decisions made
    - The operator dropped the 2.5 mm shortening of the straight grip's open end: they like the stagger.
    - A new task, not a rework of the root memory bank's curved-grip task. It lives in the model's own memory bank (operator).
    - Level 2: the design was settled in chat. Straight tip: a full half circle. Curved tip: corners of 1.5, read small. `BORE_CLEAR` at the tip. The solid end stays `DOME_LEN`.
* Insights
    - The old straight grip's floor is 1.2 deeper at the centre than near the edge. On a half circle of the straight W at A, the steel ends 1.23 short of A at 0.75 in from the side. Both point to a half-circle tip.
    - The printed grip's 87.7 depth fits the model: a rod about 1.3 in from a side wall lands on the roof slope there.

## 2026-11-01 - PLAN - COMPLETE

* Work completed
    - Wrote the Level 2 plan in `tasks.md`: behaviours B1 to B9, and four steps (tip readings, the closed end in `grips.py`, model docs, final verification).
* Decisions made
    - The tip radius is a steel reading, `Handle.tip_r`, in `steel.py`. `END_CLEAR` goes. The ribs fade over a new `RIB_FADE` and end where the round starts.
    - The roof is worked in a frame at the start of the tip's round. Each slope is the lowest line at `ROOF_ANGLE` in print that clears the tip grown by `BORE_CLEAR`. The ridge strip sits where the slopes are `RIDGE_W` apart.
    - The commits are the readings first, then curved iteration 6 and straight iteration 2 together, as one printable iteration.
* Insights
    - Moving the body lofts' end moves their sections, so the open end can shift by hundredths. B5 bounds it rather than requiring identical files.

## 2026-11-01 - PREFLIGHT - COMPLETE

* Work completed
    - Checked the plan against the code: TDD order, conventions, dependencies, conflicts and completeness. The first line of `.preflight-status` is `FAIL (fixable)`.
    - Probes, run in the session scratchpad:
        - Worked the Geometry independently. The `RIDGE_W` row sits 2.300 (straight) and 2.887 (curved) past A. The apex sits 2.419 and 2.992 past A.
        - Moving the bore loft's end moves the bore at most 0.0075 (curved) and 0.0013 (straight).
        - Today the cap over the ridge is 5.000 on both grips.
        - The straight's half-circle tip ends 1.205 short of A at 0.75 in from the side.
        - The current files pass `overhang.py`, `corner_bevel.py` and `lip.py`. The catalog suite gives 88 OK.
* Decisions made
    - F1, a required fix: B2's `past` figures (2.42 and 3.00 ± 0.1) are the apex. The Geometry ends the bore at the `RIDGE_W` row, 0.12 and 0.10 lower, so B2 fails on a correct build. The re-plan should define `past` as that row's height past A and restate the figures. With that definition, the grips shorten by 3.03 and 1.77 and end 7.30 and 7.89 past A.
    - Advisories A1 to A7 and a tip-test print idea are in `.preflight-status`. A1 and A2 are the ones the build would hit:
        - A1: B7's `ROOF_ANGLE` 10 case is also caught by the ≥ 45 guard; use 80 on the curved grip instead.
        - A2: both sides' arc samples give duplicate row heights, so the rows must be deduplicated.
* Insights
    - B5's 0.02 bore tolerance has real margin. Unlike the outside in the last task (0.075), the bore's loft barely moves when its sections shift.

## 2026-11-01 - PLAN (re-plan after preflight run 1) - COMPLETE

* Work completed
    - Resolved F1 and A1 to A7 in `tasks.md` (section "Preflight run 1"). Acceptance criterion 2 of `projectbrief.md` now gives the ridge row's figures.
* Decisions made
    - Kept the planned construction: the slopes stay exactly at `ROOF_ANGLE`, and the ridge strip sits where they are `RIDGE_W` apart. `past` and `ridge` belong to that row. The grips get 3.03 (straight) and 1.77 (curved) shorter.
    - Preflight's tip-test print is offered in the report, not built.

## 2026-11-01 - PREFLIGHT (run 2) - COMPLETE

* Work completed
    - Checked the re-planned Level 2 plan. The first line of `.preflight-status` is `FAIL (fixable)`.
    - Built the plan's step 2 in the session scratchpad, by patching `grips.py` exactly as the Geometry says. Both grips build as one valid solid, and the build confirms run 1's figures:
        - `past` is 2.887 (curved) and 2.300 (straight). The straight STL is 3.028 lower.
        - No steel is inside the bore wall. The tip's arcs lie 0.2989 to 0.3000 from the bore.
        - The rib bite is within 0.4% of B4's formula.
        - `overhang.py` flags only the ridge strip, and the guards fire at `ROOF_ANGLE` 75 and 80.
        - `lip.py` and `corner_bevel.py` pass.
* Decisions made
    - F1, a required fix: B5 slices STLs, and the STLs' own mesh error is larger than B5's 0.02 bore limit.
        - On the built files the STL comparison gives 0.129 (curved), 0.037 (straight) and 0.029 (curved fit test).
        - The CAD moved at most 0.013, 0.002 and 0.007, and passes every B5 limit.
        - The re-plan should measure B5 and B8 on CAD sections against the `5d73490` STEP files, and report the STL comparison without a limit.
    - Advisories:
        - A1: the printed STLs stray up to 0.094 (committed curved) and 0.134 (built curved) from their CAD at the bore's corners. Exporting at `tolerance` 0.002 brings that to 0.029. It is outside this brief; the operator weighs it.
        - A2: B3's cap needs a tolerance (4.9948 on the curved grip).
* Insights
    - `tolerance` 0.01 in the STL export does not hold the mesh within 0.01 on the curved bore's long lofted faces. Compare CAD with CAD whenever a lofted face changes.

## 2026-11-01 - PLAN (re-plan after preflight run 2) - COMPLETE

* Work completed
    - Resolved F1 and A2 in `tasks.md` (section "Preflight run 2"). The `5d73490` STEP files are saved in `.scratch/wirestripper-grip/baseline/` for B5 and B8.
* Decisions made
    - B5 and B8 compare CAD sections (STEP against STEP). STL slices are only reported.
    - A1 (the STL export strays up to 0.094 from the CAD model) goes to the operator. The brief keeps the export as it is.

## 2026-11-01 - PREFLIGHT (run 3) - COMPLETE

* Work completed
    - Checked the plan as re-planned after run 2. The first line of `.preflight-status` is `PASS WITH ADVISORY`.
    - Probes, read-only or in the session scratchpad:
        - The baseline STEP and STL files are byte-identical to the `5d73490` files in git.
        - `python steel.py` still equals its baseline. The catalog suite gives 88 OK.
        - On the committed STLs, the roof's flattest slope is 50.525 degrees (curved) and 50.786 (straight). The bevel's unrounded minimum is 49.8952 (curved) and 50.1573 (straight).
    - Step 2 was not rebuilt: run 2's trial build stands.
* Decisions made
    - Run 2's F1 and A2 are resolved. No finding requires a change to the plan.
    - Advisories, for the build and the operator:
        - A1: check rib bites only at s ≥ `tip_r + RIB_FADE`. `verify.py`'s 0.5 row, and the straight grip's A row, now fall inside the tip's round.
        - A2: read B8's 49.9 degrees as "unchanged from `5d73490`". The curved grip's raw figure is 49.895.
        - A3: the curved tip's 1.5 has no cross-check. A lengthwise cut through the ruined old curved grip would show its floor.
        - A4: `techContext.md` should list all four new guards.
    - The radical idea, a one-pass sweep for the roof over any tip outline, is in `.preflight-status`. It is not applied.
* Insights
    - Today's slopes are steeper than `ROOF_ANGLE`, because today's ridge strip sits at the apex's height. The plan's slopes are exactly `ROOF_ANGLE`, so `roof_angles.py`'s margin falls to its 0.5 by design.

## 2026-11-01 - BUILD - COMPLETE

* Work completed
    - Step 1 (`0e75770`): `Handle.tip_r` and `tip_short()`; curved 1.5, straight 3.3; the old straight grip's depth for the cross-check (1.21 modelled against 1.20); log entry "Tips and depths (2026-11-01)". A rebuild gave byte-identical STLs.
    - Steps 2 and 3 (`a61aa6d`): the roof on the rounded tip; the ribs ending `RIB_FADE` short of the round; four guards; regenerated outputs; model docs.
        - The ridge sits 2.887 and 2.300 past A.
        - The STLs stand 1.714 and 3.028 lower.
    - Step 4: catalog suite 88 OK; every check rerun green on the committed files.
* Decisions made
    - The rib-bite tolerance in `verify.py` is ± 0.02. It is an evidence-backed correction of a tolerance the plan never stated, not a change to the geometry.
* Insights
    - Ruled ribs between sections 4 apart already bite ± 0.012 to 0.015 between sections on the curved bend. A check sampled at a fixed s sees that whenever the sections move.
    - The STL files changed size with the new tessellation; the fit tests too, though their CAD moved under 0.01.

## 2026-11-01 - QA - COMPLETE (FAIL, fixable)

* Work completed
    - Semantic review of `0e75770`, `a61aa6d` and `9d9b7aa` against the brief and the plan. The results are in `tasks.md`, "QA (2026-11-01, run 1)".
    - Independent checks:
        - A scratchpad rebuild gives byte-identical STLs. The STEP files are identical past their headers.
        - `tip_check.py`, `closed_end.py` and `design_guards.py` are green, with the build's figures.
        - Catalog suite: 88 OK.
        - `roof()`'s geometry was worked through by hand.
* Decisions made
    - FAIL (fixable). Build must rerun for Q1: `sizes()`'s "at A" row still prints the square-tip bore and ribs at A. The model now has a bore 5.67 (curved) and 4.06 (straight) wide there, and no ribs.
    - Every requirement and acceptance criterion is met in the geometry and the files. Advisories A-1 to A-6 are non-blocking.
* Insights
    - A report row tied to a fixed station (A) goes stale when a change moves what is at that station. Check the build's printed sizes against the model, as well as the files.

## 2026-11-01 - BUILD (re-run after QA run 1) - COMPLETE

* Work completed
    - Q1: `sizes()` reports a "round starts" row, with no ribs, in place of "at A". `report_check.py` was red first, then green.
    - A-1 and A-3 to A-6 applied. A-2 (`ridge`) kept.
    - A rebuild gave byte-identical STLs. Every check rerun green on the final source, and the catalog suite gives 88 OK (`.scratch/wirestripper-grip/runs/final2.txt`).
* Insights
    - A printed size table can go stale when the shape near one of its stations changes. The build's own report is part of what QA reads.

## 2026-11-01 - QA (run 2) - COMPLETE (PASS)

* Work completed
    - Reviewed `f5fefa5` against QA run 1's findings, and checked again that `0e75770` and `a61aa6d` meet the brief. The results are in `tasks.md`, "QA (2026-11-01, run 2)".
    - Independent checks:
        - `report_check.py` fails on `a61aa6d`'s source and passes on the current source.
        - A scratchpad rebuild gives byte-identical STLs. The STEP files differ only in their timestamp.
        - `tip_check.py`, `report_check.py`, `design_guards.py` and `closed_end.py` all pass.
        - Catalog suite: 88 OK.
* Decisions made
    - PASS. Q1 is fixed: the size report's "round starts" row gives the bore at s = `tip_r` (W + 2 `BORE_CLEAR`) and no ribs.
    - Run 1's advisories are fixed, except A-2 (`ridge`), which is kept as the plan asked.
    - Two new advisories, N-1 and N-2, block nothing.
* Insights
    - When a fix touches only the build's printed report, a rebuild that gives byte-identical STLs shows that the printed files did not move.

## 2026-11-02 - REFLECT - COMPLETE

* Work completed
    - Reflection written. Persistent files reconciled: no further changes, since the build already updated all three.
* Insights
    - See the reflection. In short: compare CAD sections, not STL slices; ruled ribs carry ± 0.015 between sections on the bend; quote the modelled quantity, not a proxy; check the build's printed report.

## 2026-11-02 - REWORK INITIATED

* Operator feedback (2026-11-02):
    - "we're going to keep the slightly-shortened straight one we just did, but we're going to go back on the curved one and keep the immediately-preceding curved one - the one that was slightly longer. Those two are the combination that fit the same way the originals did!"
    - Then clean up the model's directory for publishing. Fill out the publish record as well as possible; the operator will take and add the photos. Clean up stray wording and old in-progress material, so that what merges to main describes only the two grips that ship.
* Complexity: Level 2 (unchanged; re-assessed at classification).

## 2026-11-02 - COMPLEXITY-ANALYSIS (rework) - COMPLETE

* Decisions made
    - Level 2. One model. The closed end becomes a per-grip choice that reproduces the two printed iterations exactly, followed by the publish record and the documentation clean-up.
* Insights
    - The Cults categories, read from the API (read-only, 2026-11-02): Tool `Q2F0ZWdvcnkvMjc`, with Hand Tools `Q2F0ZWdvcnkvMTAz` and Spare Parts `Q2F0ZWdvcnkvMTA1`.

## 2026-11-02 - PLAN (rework) - COMPLETE

* Work completed
    - The plan is in `tasks.md`.
        - `END_CLEAR` becomes a per-grip dict. The curved grip runs `5d73490`'s closed-end code verbatim, and the straight grip keeps the roof on its tip.
        - Then the publish record and the clean-up.
    - Baselines for the straight grip's iteration 2 saved beside the curved grip's iteration 5. The curved baselines equal `e1b3528`.
* Decisions made
    - R1 asks for byte-identical STLs for both grips, so that what ships is exactly what was printed.

## 2026-11-02 - PREFLIGHT (rework) - COMPLETE

* Work completed
    - Checked the rework plan against the code. The first line of `.preflight-status` is `PASS WITH ADVISORY`. No plan edits.
    - Probes, run in the session scratchpad:
        - `5d73490`'s `grips.py` with today's `steel.py` rebuilds curved iteration 5's STLs byte for byte (cadquery 2.8.0, cadquery-ocp 7.9.3.1.1).
        - A trial `grips.py`, patched as the plan's Design says, built all four STLs byte-identical to their baselines. The STEP files differ only on the `FILE_NAME` line.
        - On that build, the unchanged checks pass, and R2's and R4's figures hold. The curved rib bite is -0.52% against 8 ribs over L, and the cap over the apex is 5.0000.
        - Catalog suite: 88 OK.
* Decisions made
    - Advisories A1 to A9 are in `.preflight-status`. The ones the build would meet first:
        - A1: restore the STEP files from git after the rebuild.
        - A2: R1 should rebuild into a temporary directory.
        - A3: pin cadquery and cadquery-ocp in the documented build command.
    - The operator's calls: A4 (shipping the fit tests is not the catalog's practice) and A5 (add photos before merging the release pull request).
* Insights
    - Byte identity depends on the toolchain uv resolves, as well as on the source. Nothing pins it today.

## 2026-11-02 - BUILD (rework) - COMPLETE

* Work completed
    - The pair from one source (`ceaf1d8`). `pair_check.py` was red first (8 curved failures), then green.
    - The publish record and the clean-up (`154d883`). The rebuild stayed byte-identical.
    - Every check is green on the committed files; catalog suite 88 OK.
* Insights
    - Keeping two printed iterations byte-identical took each closed end's own rib rule. The straight grip's last loft position is 4.299999999999997, so one shared `>=` rule would have flipped a section.

## 2026-11-02 - QA (rework) - COMPLETE (PASS)

* Work completed
    - Reviewed `ceaf1d8` and `154d883` against the rework brief and the plan. The results are in `tasks.md`, under "QA (2026-11-02, rework)".
    - Independent checks:
        - `pair_check.py` rebuilt both grips into a temporary folder. All four STLs equal `e1b3528`'s and `a61aa6d`'s byte for byte, and the STEP files are equal past `FILE_NAME`.
        - The eight committed files are the same git blobs as the printed iterations.
        - `design_guards.py` and `report_check.py` pass. Catalog suite: 88 OK.
        - The length branches were read line by line against `5d73490`'s code.
* Decisions made
    - PASS. All five rework items are met.
    - Advisories Q-A1 to Q-A5 block nothing. For the operator:
        - Q-A1: the listing says the tool still closes fully. For this pair, that is a model figure, not a recorded reading.
        - Q-A5: the photos must go in before the release pull request merges.
* Insights
    - When a refactor must reproduce printed files, comparing git blob ids of the committed outputs with the printed commits is a quick first check. A rebuild into a temporary folder then proves that the source makes them.
