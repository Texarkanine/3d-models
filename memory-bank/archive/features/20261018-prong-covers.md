---
task_id: prong-covers
complexity_level: 2
date: 2026-10-18
status: completed
---

# TASK ARCHIVE: Prong covers

## SUMMARY

Two printed PLA caps keep a stored bulb's electrical end clean and straight. `models/h7-bulb-storage/h7_prong_cover.py` makes a block that grips the H7 bulb's two tabs with in-plane leaf springs. `models/h8-h9-h11-h16-bulb-storage/h11_connector_cap.py` makes a cap for the PGJ19 connector (H8, H9, H11, H16): an insert fills the socket, and two arms clip onto its end hooks. Test print 1 led to one rework of both. Test print 2 of both worked, and both caps are now in their models' `publish.yaml`. The operator adds the listing photos.

## REQUIREMENTS

- H7 (PX26d): a cap that grips the tabs alone, by friction, and pulls off by hand, with a grip that is easy to pull.
- H8/H9/H11/H16 (PGJ19): a cap that plugs into the bulb's connector, latches, and comes off with a finger and thumb. It does not need to seal or to grip the pins.
- PLA, no supports, built to the published standard plus clearance. Each part goes in its storage model's directory.
- Rework 1, from test print 1:
  - make the H7 cap much closer to a rectangular extension of the plug;
  - remove the diagonal on the H11 cap's plug;
  - stop the H11 cap flopping.

Two first requests changed:

- H7 has two tabs, not three. The three-pin plug was H4.
- The hourglass, radially symmetric H7 grip was dropped in rework 1. It gripped well but was too big.

## IMPLEMENTATION

Sizes come from IEC 60061-1, read from GOST IEC 60061-1-2014: sheet 7004-5 for PX26d (PDF page 15) and sheet 7004-110-2 for PGJ19 (pages 230-232). The operator's LED H7 plug matched the standard's tabs.

**H7 prong cover.** A rounded block, 12.8 x 17.8 x 12.2 mm, printed on its slotted face. Its size comes only from the springs.

- Each tab sits between two thin walls fixed at one end, with a gap all round. The walls stand on the bed and bend within the layers.
- A rounded ridge on each wall presses the tab 0.25 mm (`SQUEEZE`), about 3.6 N per spring.
- The two ridges in a slot are at different heights. Facing ridges would leave a 0.3 mm gap that prints shut.
- The roof over the springs is a bridge, `TOP_GAP` above them.
- Test print 1 was a 25 mm spool with 9 mm springs.

**H11 connector cap.** A cap 21.7 x 31.2 x 17 mm, printed on its back face.

- An insert fills the mouth recess (0.15 mm clearance) and runs 13 mm into the inner cavity. Its slots clear the pins, and one slot across it takes every type's keys, H9's included.
- Two arms each run up one long side and round one end of the oval to a tooth behind that end's hook. Those are the hooks the standard says hold the car's connector.
- Each tooth's catch face slopes at 45 degrees, so it pulls the cap onto the socket over the hooks' tolerance range, and a firm pull lifts it off.
- The side bump is not used. An arm that could reach over its 1.8 mm height does not fit beside the socket.
- Test print 1 latched one lever onto the side bump and had a 4.5 mm plug in the mouth recess alone. It flopped, and the plug's 45 degree underside printed as a visible diagonal.

Other files:

- both models' `README.md` and `memory-bank/` files;
- `tools/overhang.py` in both models, which now says so when it cannot trace an outline;
- `tools/check_fit.py` section M (H7) and section G (H11);
- the H11 README's Cults link, which now uses the renamed slug.

## TESTING

- Before each print, scratch scripts set mock tabs and mock sockets at both ends of the standard's tolerances, with H11 and H9 keys. Only the ridges touched the tabs, each 0.13 to 0.37 mm in. On the sockets, only the teeth touched the hooks, 0.47 to 0.99 mm into them, and each tooth reached 1.2 to 1.35 mm under the hook's tip. `tools/overhang.py` found only bridges on the H7 cover and no overhang past 45 degrees on the H11 cap.
- Test print 1 (operator): the H7 cover worked but was too big. The H11 cap flopped.
- Test print 2 (operator, 2026-10-18): "Those both work!"
- Once the shapes settled, the scratch checks became `check_fit.py` sections M and G. Both suites report 0 failed. A deliberately broken part (more squeeze, a misplaced catch, an oversized insert) makes them fail. The 83 repository tests pass. Rebuilt STLs match the committed ones byte for byte.
- No `/niko-qa` subagent ran. The test prints were the QA.

## LESSONS LEARNED

- A cap that stands in for a mating connector should copy that connector's own retention: fill the socket and use the catches the standard gives the connector. A latch on another feature, the side bump, gave a cap that flopped.
- A 45 degree catch face preloads a cap against its hook. It takes up the hook's tolerance range and still lets the cap pull off without prising the arms open.
- Facing ridges that print shut, and spring roots that poke through a chamfer, showed only in section renders. Render sections of every new face.
- Photos of real mating parts (two harness plugs) settled the H11 design in one rework.

If "the cap stands in for the car's plug" had been the founding assumption, both caps would have started as they are now. Nothing else in either model would change.

## PROCESS IMPROVEMENTS

Before designing a clip-on part, ask for or find photos of the real part it replaces.

## TECHNICAL IMPROVEMENTS

None. Each cap is a separate script that shares no values with its model's holder or cover, and it can change and print on its own.

## NEXT STEPS

- The operator adds listing photos of both caps to each model's `img/`.
- Merging the pull request should propose a minor release for both models.
