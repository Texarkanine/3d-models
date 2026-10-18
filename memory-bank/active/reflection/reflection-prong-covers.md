---
task_id: prong-covers
date: 2026-10-18
complexity_level: 2
---

# Reflection: Prong covers

## Summary

Two caps that protect a stored bulb's electrical end: an H7 prong cover that grips the two tabs with in-plane leaf springs, and a PGJ19 connector cap with an insert that fills the socket and two arms that clip onto its end hooks. Both worked on test print 2, after one rework.

## Requirements vs Outcome

Both caps were delivered and are on their models' Cults listings, with photos still to come from the operator. Three requirements changed on the way:

- H7 has two tabs, not three. The operator confirmed this; the three-pin plug was H4.
- The hourglass, radially symmetric H7 grip was dropped. Test print 1 used it and gripped well, but the operator found it too big and asked for a block like an extension of the plug.
- The H11 cap no longer latches over the side bump, as first asked. It clips onto the two end hooks, the ones the standard says hold the car's connector, and an insert fills the socket. The side bump is unused.

## Plan Accuracy

The H7 spring design was right the first time; only the outer shape was wrong. The H11 plan was wrong in its approach: one catch on one side, plus a short plug in the mouth recess, cannot hold a cap square. The rework followed the operator's photos of two harness plugs, which do what the car's plug does: fill the socket and catch both end hooks.

## Build & QA Observations

Mock tabs and mock sockets, built in scratch scripts at both ends of the standard's tolerances, caught several defects before printing:

- facing ridges that would leave a 0.3 mm gap, too thin to print open;
- spring roots poking through a chamfer;
- a tooth revolved to the wrong angle.

Section renders found what the solid views hid. QA was the operator's two test prints; no `/niko-qa` subagent was run. The scratch checks became `check_fit.py` sections M (H7) and G (H11) once test print 2 worked.

## Insights

### Technical
- A cap that stands in for a mating connector should copy that connector's own retention: fill the socket and use the catches the standard gives the connector. Inventing a latch on another feature (the side bump) gave a cap that flopped.
- A 45 degree catch face preloads the cap against the hook. It takes up the hooks' tolerance range and still lets the cap pull off without prising the arms open.

### Process
- Photos of real mating parts settled the H11 design in one rework. Ask for them, or look for them, before designing a clip-on part.

### Million-Dollar Question

If "the cap stands in for the car's plug" had been the founding assumption, the H11 cap would have started as v2: an insert that fills the socket, and catches on the end hooks. The H7 cover would have started as a block sized only by its springs. Both now are. Nothing in the existing models would change: each cap is a separate script in its storage model's directory and shares no values with the holder.
