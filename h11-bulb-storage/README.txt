H11 bulb holder (twist lock), 0.1
=================================

Holds one spare H11 bulb, halogen or LED. H8, H9 and H16 bulbs fit too: all four use the same
cap (PGJ19) and differ only in the wide fin. H8B, H9B and H11B use a different cap (PGJY19)
and do not fit.

0.1 is untested: nothing has been printed yet. Print the fit test first.

Files
  h11_holder.stl / .step    the holder. Print standing on its open end. No supports.
  h11_fit_test.stl / .step  the holder cut off 7.5 mm above the wall the fins rest on: the
                            openings, the ring the fins turn in, the stop and the two catches.
                            Print it the same way. It shows in a few minutes whether your bulbs
                            go in, turn, click and stay.
  measure_cap.svg           the cap at its largest, with a letter for each size (open in a
                            browser).
  h11_holder.py             CadQuery source. All dimensions are parameters at the top.

How it works
  1. Look into the open end. Line the bulb's wide fin up with the wide opening, and push the
     bulb in, glass first, until all three fins are through the wall. This squeezes the bulb's
     rubber seal against the holder, as a car's socket does, so it takes a firm push.
  2. Keep pushing and turn the bulb clockwise as you look at its plug, about 65 degrees, until
     it stops. Near the end each narrow fin pushes past a springy catch: that click is the lock.
     The bulb only turns one way.
  3. Let go. The seal pushes the fins back onto the wall, so the bulb does not rattle.
  To take it out: turn it back firmly, past the catches, and pull it out.
  Before you turn it, the bulb may sit loose. That is normal.

What the bulb must fit (defaults: the PGJ19 standard at its largest, plus clearance)
  fins        the openings are 0.4 mm bigger than the largest fin of each kind, all round.
              They pass any bulb that fits a car's socket. Fins up to 4.0 mm thick.
  wide fin    any of the four: H8 8 mm centred, H16 10 mm centred, H11 and H9 10 mm
              off-centre (to either side).
  fin reach   tips 12.15 to 12.5 mm from the centre. The catches reach in to 11.8 mm, so
              they grip the shortest fin by 0.35 mm.
  nose        up to 19 mm across, in a 20.2 mm hole. A halogen's spring is pressed in by
              about 0.6 mm, as in a car.
  wall        2.4 mm, like a car's (at least 2.2). The bulb's plate must be more than 2.4 mm
              behind the fins (the standard says at least 3.0). The seal in front of the plate
              gets squeezed: the operator's LED's seal face is 1.38 mm behind its fins, so it
              is squeezed about 1 mm.
  head        up to 21 mm across and 48 mm long from the back of the fins (the standard
              allows 44 mm).
  outside     32.8 mm across at the open end, 24.6 mm along the tube, 62.7 mm long.

Print notes
  Open end down, supports off. The ring the fins turn in, the gaps round the catches and the
  closed end all have 45 degree ceilings; the only flat ceiling is a 1 mm spot at the tip.
  PETG is the better choice: the catches are springs, and PETG bends further before it breaks.
  The catches are 1.0 mm thick: print with at least 3 walls (perimeters), 0.2 mm layers.
  Turn on elephant-foot compensation. The catches stand on the bed with 0.6 mm gaps around
  them, and a squashed first layer can join them to the wall. If a catch is stuck, run a knife
  through its gap.
  Click too weak or too stiff: change CATCH_R (11.8; smaller grips harder) or BEAM_T (1.0;
  thicker is stiffer) in the script and re-export.

Sources for the defaults
  IEC 60061-1 sheet 7004-110-2 (cap PGJ19), read from GOST IEC 60061-1-2014: fin tip radius
  12.15-12.25, fins at most 4.0 thick, narrow fin edges 7.8-8.0 and 3.3-3.5, wide fin 6.0 + 4.0
  or 10.0 or 8.0, nose at most 19.0, plate at least 3.0 behind the fins.
  IEC 60061-2 sheet 7005-110-3 (holder PGJ19), read from GOST IEC 60061-2-2017: hole 19.5-20.0,
  openings reach 12.4-12.5, wall at least 2.2 (2.4 for H16).
  UNECE R37 sheet H8/1 head outline, read from GOST R 41.37-99: at most 44 mm long.
  The operator's LED H11: fins 1.0 mm thick, plate 3.33 mm and seal face 1.38 mm behind the
  fins, 32 mm long.
