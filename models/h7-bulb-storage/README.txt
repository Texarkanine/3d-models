H7 LED bulb cover (snap-latch clip), v2
=======================================

Files
  h7_cover.stl / .step     the cover. Print upright, closed end down. No supports.
  h7_fit_test.stl / .step  the cover cut off 8 mm in front of the seat, to check the flange,
                           key and clip quickly. Print the same way.
  measure_flange.svg       the flange as modelled, and the key around it (open in a browser).
  clips/h7_clip_flange_A-Bmm.stl / .step
                           the clip, one per flange-plate thickness band (A to B mm). Print flat, as
                           exported.
  h7_led_cover.py          CadQuery source. All dimensions are parameters at the top.

How it works
  1. Find the tab on the bulb's flange. Line it up with the notch on the back face of the cover.
  2. Push the bulb head into the cover until the flange sits on the seat. Two key blocks, 4.5 mm
     tall, fill the steps on each side of the tab, and the tab sinks into the pocket between them.
     The bulb only goes in one way and cannot turn, even if it rocks while you fit the clip. If
     the bulb will not drop flat, turn it until the tab finds its pocket.
  3. Slide the clip, tips first, into the tunnels on either side of the collar. It goes in from
     either side. Push until the bar meets the collar. The barbs squeeze into the tunnels, drag
     through, and snap out past the far face of the collar: that click is the latch. Across the
     middle each barb rides under a narrow roof, so the tips line up with the far tunnels by
     themselves. A bump on each arm presses the flange onto the seat.
     The arms are printed angled out a little, so pinch the tips together slightly to start them
     into the tunnels. In the cover the far tunnels push the arms back, and they keep pressing
     the barbs out.
  To release: squeeze the two tips toward each other, about 2.5 mm each (fingers or needle-nose
  pliers), and push them back about 2 mm, until the barbs are inside the collar. Then pull the
  clip out by its loop; a small screwdriver fits the loop.
  The barbs drag through the tunnels on the way out; that is normal.

Which clip
  Measure the thickness of the flange plate at its outer rim, where the clip arms cross it, and
  print the clip whose band contains it. The H7 standard makes the plate 0.6 to 0.8 mm thick, so
  start with the 0.5-1.0 clip. The band is the plate thickness, not the bump: a clip for a
  thicker plate has a lower bump.
  The bulb rests on three small lugs on the front of the plate, so the back of the plate, where
  the bumps press, sits deeper than the plate is thick: 1 mm deeper on the operator's bulb
  (PLATE_SETBACK), which is what the clips are built for. The standard allows less. If a bulb
  rattles in the 0.5-1.0 clip, its plate sits closer to the seat: print the 0.0-0.5 clip, which
  has a taller bump.
  Each clip squeezes the plate by 0.1 mm at the thin end of its band and 0.6 mm at the thick end.
  The bumps land 90 degrees round from the tab. If the bulb has a ring or ridge on the back of
  the plate there, measure through it.
  No calipers: print both clips. The right one latches with a firm push and comes out without a
  fight. A clip that is hard to pull out is one band too thin; one that feels loose is one band
  too thick.
  Tested: the operator's LED bulb, plate 0.85 mm at the rim, takes the 0.5-1.0 clip (v2,
  2026-10-13). The v1 cover is great; the v1 clip latched but pulled out with a small tug.
  Three trial clips (square catch, spread arms, both): one band thicker, all felt a little
  loose; in 0.5-1.0 the spread arms won, and that is v2. The 0.0-0.5 v2 clip has not been
  printed yet.
  Clip names changed on 2026-10-16; the shapes did not. They used to name how deep the back of
  the plate sits, which is 1 mm more: the old 1.5-2.0 clip is now 0.5-1.0, and 1.0-1.5 is now
  0.0-0.5. The old 2.0-2.5 and 2.5-3.0 clips are gone: they fit plates thicker than the standard
  allows.

What the bulb must fit (defaults: the H7 standard, cap PX26d, at its largest, plus clearance)
  flange             circle O up to 34.0 mm (FLANGE_D); bore 35.0 mm. Plate T 0.6 to 0.8 mm
                     thick, its back Z at most 1.4 mm behind the seat. The clips fit a plate up
                     to 1.0 mm whose back sits up to 2.0 mm behind the seat; the cover has room
                     for 3.0 mm (FLANGE_T_MAX).
  tab and flats      tab K up to 8.0 mm wide (TAB_W), on the circle. One straight cut across the
                     circle, square to the tab, Q 13.2 to 13.7 mm from the centre (FLAT_Q), leaves
                     a flat on each side of the tab. A key block fills each step and stands
                     KEY_DEPTH (4.5 mm) proud of the seat, well behind the flange. So beside the
                     tab, 14.7 mm or more from the centre, nothing on the bulb may sit within
                     4.5 mm of the seat: anything there must be under 29 mm across.
                     A non-standard bulb: measure it, change these and re-export, or set
                     KEY = False. measure_flange.svg shows the shape.
  head               up to 21 mm across, up to 54 mm long from the flange face: the longest
                     the H7 standard allows (44 mm, UNECE R37) plus 10 mm
  first 4.6 mm       up to 26.4 mm across (the ring in front of the flange, PX26d M max 26.0)
  behind the flange  the arms run 13 mm to about 17.1 mm either side of centre, so anything in the
                     first 5.4 mm behind the seat must be under 26 mm across in that direction.
                     The collar reaches 5.95 mm behind the seat, at 35 mm diameter and up.
                     A heatsink wider than 35 mm must start at least 5.95 mm behind the seat:
                     on the operator's bulb, about 4.1 mm behind the plate.
  outside            collar 43 x 43 mm, cover 62 mm long. With the clip in: 59 mm from the loop
                     to the clip tips.

Sources for the defaults
  IEC 60061-1 sheet 7004-5 (cap PX26d), read from its identical Russian adoption
  GOST IEC 60061-1-2014 (standartgost.ru): O 33.8-34.0, K 7.9-8.0, Q 13.2-13.7, M 25.9-26.0 mm.
  The text copy has no drawing, so the letters were matched to features by fit: the operator's
  LED bulb (33.3 circle, 7.7 tab, flat 12.8 from centre) and a retailer's description
  ("34 mm round plate, 21 mm flat side, 8 mm locating tab").
  The meganorm.ru copy of the same standard has the drawing (sheet 7004-5-6). From it: plate
  thickness T 0.6-0.8 mm, and the back of the plate Z at most 1.4 mm behind the reference
  plane, which three lugs on the front of the plate stand on.
  UNECE R37 sheet H7/1 maximum lamp outline (Ø25 x 4.1 mm, then Ø19, glass max Ø15, max 44 mm long).
  The MakerWorld screw-together H7 case cup (h7-bulbholderv2.stl), which uses Ø26.4 x 4 mm and Ø36.
  Test prints of 0.2 to v2 on the operator's bulbs, and their flange measurements.

Print notes
  Cover: upright, closed end down, supports off. The flat overhangs are the four tunnel roofs,
  bridges 6.3 mm wide held on both sides, and the roofs over the two barb grooves, which are
  flat only for a 1 mm ledge against the wall and then rise at 45 degrees. A 1 mm ledge prints
  fine without support. Everything else leans 45 degrees or steeper. If your slicer adds
  supports anyway, turn on "don't support bridges".
  Clip: flat, as exported. PETG is the better choice: it flexes and creeps less, so it keeps
  the arms' spread. PLA works, but slowly relaxes under a constant load.
  Print it solid (100% infill); the arms are springs. 0.2 mm layers.
  Clearance is 0.3 mm per side, plus 0.2 mm under the tunnel roofs in case the bridges sag.
  If the latch is too stiff or too loose, change BARB (2.2 mm) or CLEAR in the script and
  re-export. 2.2 mm is the biggest barb the tunnels allow; a bigger one needs a bigger SQUEEZE.
  A square catch face (BARB_LEAN 0) was also tried, alone and with the spread arms (v1-print2,
  v1-print3); the spread arms alone won. If clips still get pushed out, a stiffer bridge bar is
  the next step.

Versions
  v1 is the first release; v2 changes only the clip. The test designs before v1 are 0.1 to 0.4.
  The notes below use the clip names from before 2026-10-16: subtract 1.0 mm for today's.
  Test prints are tagged 0.3-print1, 0.4-print1 and v1-print1; v1's trial clips v1-print2
  (2.0-2.5) and v1-print3 (1.5-2.0); v2's is v2-print1.

Changes in v2 (from the v1 trial clips)
  - Each clip arm is printed angled 1.5 degrees outward. In the cover the far tunnel pushes it
    back, so the arms keep pressing the barbs out, and each catches its full 2.2 mm (v1: 1.9).
    Pinch the tips slightly to start them into the tunnels; squeeze about 2.5 mm each to release.
  - Chosen from three trial clips (a square catch face, the spread arms, both). In the 2.0-2.5
    band all felt a little loose; in the 1.5-2.0 band the spread arms won.
  - Only the clip changed. The cover is v1's, so v2 clips fit every v1 cover. To tell v1 and v2
    clips apart, lay one on the other: v2's tips stand about 1.3 mm wider each side.

Changes in v1 (from the 0.4 fit test)
  - Barbs 2.2 mm (were 2.0), with a ramp to match, so a knock in storage can't push the clip
    out. They catch 1.9 mm deep on the collar face (0.4: 1.7). The grooves they spring out
    into across the middle are 0.2 mm deeper to match.
  - The tube is 54 mm deep inside (was 52): the longest head the H7 standard allows, 44 mm,
    plus 10 mm. The cover is 62 mm long.
  - 0.4 and v1 parts have not been tried together, either way round: print the cover and clips
    as a set.

Changes in 0.4 (from the 0.3 fit test)
  - Key blocks 4.5 mm tall (were 0.8), with a slope on top to guide the tab in. In 0.3 a slight
    rock lifted the tab out of its pocket and the bulb turned while the clip went in.
  - Barbs 2.0 mm (were 1.5) with a longer ramp, so they catch deeper without a steeper push.
    The tunnels are 0.4 mm roomier on the inside to let the arms squeeze them through.
  - A narrow roof over each barb's groove across the middle, and a slope at the inner end of each
    tunnel roof. In 0.3 the tips could tilt out the open back and miss the far tunnel, worst when
    the cover was held bulb-up.
  - 0.3 clips do not fit 0.4 covers, nor 0.4 clips 0.3 covers: print them as a set.

Changes in 0.3 (from the 0.2 test print)
  - Two key blocks that fill the steps beside the tab replace the two open slots: the bulb cannot
    turn, and the clip arms always press on solid flange. A notch on the back face marks the tab.
  - Bore, tab and flats built to the H7 standard (PX26d) at its largest, plus clearance.
  - Clip goes in from either side.
  - Square collar, so every tunnel roof is a bridge: prints upright with no supports.
  - Barbs are larger (1.5 mm) and their catch face leans 20 degrees, so they drag smoothly.
    They catch on the flat outer face of the collar.
  - Tips stick out 7 mm past the collar, with a grip pad, so fingers can pinch them.
  - Straight bridge bar in place of the arc.
