---
task_id: wire-stripper-grips-closed-end
date: 2026-11-02
complexity_level: 2
---

# Reflection: wire-stripper-grips-closed-end

## Summary

Both grips' bores now end on the steel's rounded tip, with the same 0.3 clearance as the sides and a 50-degree roof above it. Hollow past the tip fell from 5.3 to 2.3 (straight) and from 4.7 to 2.9 (curved), and the grips are 3.03 and 1.77 shorter. QA passed on its second run; the operator's print is still to come.

## Requirements vs Outcome

- All eight requirements are met, and the open ends moved at most 0.013 in CAD.
- The one change in figures came before the build. In chat I quoted 2.9 and 1.7 off, which was the apex of the slopes. Preflight run 1 showed the planned roof stops at the ridge strip, 0.1 lower, so the grips come out 3.03 and 1.77 shorter. The operator was told in the next update.
- The tip readings (`tip_r`, the old grip's depth) were not in the opening request. They came from the operator's answers during the "how much empty space" discussion.

## Plan Accuracy

- **Order and files:** right. Readings first (no printed change), then the iteration, then docs.
- **Two checks were wrong, not the design:**
    - B2's figures were the apex (preflight run 1).
    - B5 compared STL slices, whose export error (0.094) is bigger than its 0.02 limit (preflight run 2).
- **What the build hit that the plan didn't foresee:** a rib-bite check at a fixed station went 15 µm over. Moving the loft's sections moved where the ruled ribs' mid-span error lands. The old build had the same error, between sections.
- **The challenges the plan did predict** (loft failure, fuse, row duplicates) did not happen. Preflight's advisories had already handled the duplicates.

## Build & QA Observations

- **Build:** went straight through. The roof built first time as a ruled loft of `rrect` rows sharing the body's last section, and step 1 left the printed files byte-identical.
- **QA run 1:** caught a stale line in the build's own size report. Its "at A" row still described a full-width bore with ribs. The geometry was right; the printed report, which the operator reads, was not.

## Insights

### Technical
- **The STL export misses its tolerance on lofted faces.** It strays up to 0.094 from the CAD at a 0.01 tolerance. For changes of hundredths, compare CAD sections (STEP), not STL slices. This is now in `techContext.md`.
- **Ruled ribs bend between sections.** With sections up to 4 apart on the curved grip's bend (radius about 175), a rib bites about ± 0.015 more or less midway between them. A check at a fixed s changes whenever the sections move. Size such tolerances to the section spacing, or put sections at the stations.
- **Model the tip's shape from the start.** The square-tip assumption alone accounted for more than half of the hollow. The tracings had shown rounded tips since the first readings.

### Process
- **Pausing to measure paid off.** The operator's request changed twice in one conversation: shorten the open end, then keep the stagger, then cut the hollow at the closed end. Pausing to put a number on "how much empty space" before planning meant the wrong change was never built.
- **Quote the modelled quantity, not a proxy.** I gave the operator the apex figures from a sweep script before the plan had defined the roof. Define the quantity first.
- **Check the printed report too.** When geometry changes near a station that `sizes()` reports, check the report against the new shape. QA caught what the plan's checks did not cover.
- **Preflight's trial build was worth it.** It took three runs, but each was far cheaper than a failed build, and run 2's trial build found the one check that could never pass.

### Million-Dollar Question

If the steel's full outline, tip included, had been part of `steel.Handle` from the start, the bore would be one general operation: the steel grown by `BORE_CLEAR`, then filled up to the printer's overhang limit above it in print orientation. Preflight run 3 sketched it as a running maximum of `edge(z') + cot(ROOF_ANGLE)·(z − z')`. `END_CLEAR`, the special roof and the tip-radius arithmetic would fold into it, and it would take a traced or uneven tip as easily as a round one. What was built is that operation solved in closed form for two arcs. That is enough while the tips are modelled as arcs; the general form earns its place when a tip is traced point by point.

---

# Reflection: Rework (2026-11-02): the pair that fits, ready to publish

## Summary

The operator printed both closed ends on both grips and kept curved iteration 5 and straight iteration 2, the pair that fits as the original grips did. One source now builds exactly that pair, byte for byte. The model is ready to publish: the listing record is filled out, and the docs describe only the two grips that ship. QA passed first time.

## Requirements vs Outcome

- **The pair from one source:** met, byte for byte, both from a fresh build and in the commit. The curved grip's code is the old code line for line, reading `END_CLEAR` per grip.
- **The publish record:** met, apart from the photos, which are the operator's. Two judgement calls go to the operator:
    - the fit tests ship, unlike the bulb models';
    - the tool-closing line is worded as design intent, not as a tested fact (QA Q-A1).
- **The clean-up:** met. The iteration histories and hashes are gone, the reasons stay, and the alternatives are recorded in SumMem.

## Plan Accuracy

- Right as planned.
- The one hazard the plan named, byte identity, was real. It needed one thing the plan had not spelled out: each closed end keeps its own rib rule. The straight grip's last loft position is 4.299999999999997, so one shared `>=` rule would have changed its STL. A quick probe of the float caught this before any code was written.

## Build & QA Observations

- **Build:** went straight through.
- **Preflight's advisories improved the result.** A fresh build in a temporary folder proves the source, not only the committed files. The pinned CadQuery versions make the byte check repeatable.
- **QA:** passed. Its notes were wording, and they were fixed before reflect.

## Insights

### Technical
- **To keep printed files exact across a refactor, keep each variant's code path whole,** down to comparisons and section positions. Unify only what is provably bit-identical, such as `−(a + b)` and `−a − b`. A fresh build compared byte for byte is the proof.
- **A rebuild matches byte for byte only on the same CadQuery and OCP versions,** so the build command pins them.

### Process
- **Test prints chose between alternatives that were each committed on their own** (the operator's one-commit-per-iteration rule). That made "keep this one from that one, and that one from this" a precise, cheap request.

### Million-Dollar Question

Nothing notable. With two printed closed ends to keep exactly, a per-grip setting and two code paths is the simplest honest source. A general closed-end operation (see the first reflection above) would serve a new design, not these two printed ones.
