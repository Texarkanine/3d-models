# Progress

Caps for the electrical ends of stored bulbs: a friction cap for H7 tabs and a latching cap for the PGJ19 connector (H8/H9/H11/H16), each in its storage model's directory.

**Complexity:** Level 2

## 2026-10-18 - BUILD (test print 1) - COMPLETE

* Work completed
    - H7: spool-shaped cap (25 mm across, 31 long); each tab pinched by two in-plane leaf springs (commit 3532019)
    - H11: oval plug in the mouth recess plus a see-saw lever on crossed leaves hooking the side bump (commit 6944c72)
* Decisions made
    - Build to the cap standard (GOST IEC 60061-1-2014, sheets 7004-5 and 7004-110-2). H7 has two tabs, not three; the operator's LED plug matches it
    - Springs and latch beams stand on the bed and bend within the layers
* Insights
    - Test print 1, H7: works and grips; too big
    - Test print 1, H11: the hook lands but the cap flops: one catch, and a 4.5 mm plug with 0.25 clearance does not hold it square. The plug's 45 degree underside reads as a flaw

## 2026-10-18 - BUILD (rework 1, test print 2) - COMPLETE

* Work completed
    - H7: spool replaced by a rounded block sized only by the springs (12.8 x 17.8 x 12.2, was 25 x 31). Springs 7 mm long and 0.9 thick, ridges at 1.6 mm: about 3.6 N each at 0.25 mm squeeze (21 MPa)
    - H11: new cap. The insert fills the mouth recess (0.15 clearance) and runs 13 mm into the inner cavity, with pin slots and a full-width key slot (two towers). Two arms stand on the bed, each running up a long side and round one end of the oval to a 45 degree tooth behind that end's hook. About 2.8 N per arm at full deflection (16 MPa); cap 21.7 x 31.2 x 17. Prints on its back face
    - Mock-socket check at both ends of the PGJ19 tolerances, H11 and H9 keys: only the teeth touch the hooks, 0.47-0.99 mm in (preload); each tooth still reaches 1.2-1.35 under the hook tip
* Decisions made
    - H11: clip the two end hooks (the standard's connector catches, note 4), not the side bump. The side bump is 1.8 tall and catching it in-plane needs an arm too long to fit beside the socket
    - H11: 45 degree catch faces, so the cap takes up the hooks' tolerance with preload and pulls off without prising the arms
* Insights
    - Facing ridges and thin gaps that print shut, and spring roots poking through face chamfers, only show up in sections; render sections of every new face

## 2026-10-18 - QA (test print 2) - PASS

* Operator: "Those both work!" Both caps are accepted for the listings; the operator prints a set and adds the listing photos.
* No `/niko-qa` subagent ran: the test prints were the QA.

## 2026-10-18 - REFLECT - COMPLETE

* The mock-tab and mock-socket checks became `check_fit.py` sections M (H7) and G (H11); both suites and the 83 repository tests pass; rebuilt STLs match the committed ones byte for byte
* Both caps added to their models' `publish.yaml` (files, description, printing)
* Reflection: `reflection/reflection-prong-covers.md`
