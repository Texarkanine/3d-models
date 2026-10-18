# Project Brief

**Task:** prong-covers - caps that protect a stored bulb's electrical end.

Spare bulbs sit in the printed storage covers with their contacts exposed. Add a cap for each connector type, printed in PLA, to keep the contacts clean and straight:

- **H7 (PX26d):** two bare 6.3 x 0.8 tabs. A cap that grips the tabs alone, by friction, and pulls off by hand. It fits halogen bulbs and the operator's LED plugs (their tabs match the standard).
- **H8/H9/H11/H16 (PGJ19):** an oval socket with two recessed pins and catches on its outside. A cap that plugs in like the car's connector and latches, and comes off by hand.

Each part lives in its storage model's directory (`models/h7-bulb-storage`, `models/h8-h9-h11-h16-bulb-storage`) and is built to the published standard plus clearance.

## Rework 1 (2026-10-18, operator feedback on test print 1)

1. H7 cap works but is too big ("a lot" for the job). Make it much closer to a rectangular extension of the plug that happens to cover the tabs.
2. H11 cap: the 45 degree underside of the oval plug shows as a diagonal. The oval shape itself is right.
3. H11 cap flops loose: one catch lands, but the other catches on the connector are unused, and the plug never enters the socket's inner cavity, so nothing holds it square. Take ideas from harness connectors: two pinch arms on the oval's ends, and a sleeve with an insert that fills the socket.
