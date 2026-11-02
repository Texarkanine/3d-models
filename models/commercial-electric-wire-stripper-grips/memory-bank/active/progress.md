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
