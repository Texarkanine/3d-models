# System Patterns

## How This System Works

The model script is not written yet. The plan follows `h7-bulb-storage`: one CadQuery script is the single source of truth, every dimension is a named parameter at the top, and the STL and STEP files are generated outputs, committed so people can print without running Python.

`measure_cap.svg` is drawn by `tools/make_svg.py`, which holds the standard's numbers for now. Once the model script exists, `make_svg.py` should import its parameters, as the H7 one does.

## How an H11 bulb is held

- The bulb's datum is the back face of its fins (the standard's reference plane), the side toward the plug. The fins stand up to 4.0 mm in front of it. The plate the seal sits on is at least 3.0 mm behind it. In a car, the socket's wall (at least 2.2 mm) fills that gap and squeezes the seal against the plate; in this holder, the holder's wall does. The squeezed seal pushes the fins onto the wall, so the bulb does not rattle.
- Twist-lock: the fins pass through openings in the wall, then turn so their back faces press on the wall's inner face. The O-ring presses on the wall's outer face.
- The openings take every wide fin in the family: PGJ19-1 (H8, 8.0 centred), -2 (H11, 10.0 off-centre), -3 (H16, 10.0 centred) and -5 (H9, 10.0 off-centre the other way). The narrow fins, nose, fin reach and gaps are the same on all four.
- In the standard, the lock is a spring strip on the bulb (the halogen "nub") that snaps past a small bump in the socket's hole. LED retrofits often leave it out, so the holder must carry its own catch. Do not rely on the bulb's spring.

## Print orientation is designed in

The holder prints standing on its open end. The wall the fins press against is the first layers on the bed, so that face comes out flat. The slot the fins turn in has a ceiling that slopes at 45 degrees. It must never be a flat ring: nothing holds a flat ring up from below in any orientation.

## Why not the old case

The operator's earlier H11 case (`Trinkets/h11 bulb case/h11_case.stl`, not ours) taught these limits:

- Its twist slot has a flat ring ceiling about 4.75 mm wide, so every orientation droops or strings, and the sag shrinks the slot.
- The slot is 2.75 mm tall. The standard allows fins up to 4.0 mm thick.
- Its wall is 3.25 mm thick. A car socket's wall is about 2.2 to 3.0 mm, and the bulb promises only 3.0 mm behind its fins, O-ring included. Halogens had to be forced in.
- Its hole is plain and round, so nothing locks a bulb without a spring nub.
