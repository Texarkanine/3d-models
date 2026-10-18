# System Patterns

## How This System Works

`h11_holder.py` is the single source of truth, as in `h7-bulb-storage`: every dimension is a named parameter at the top, and the STL and STEP files are generated outputs, committed so people can print without running Python.

Every flat shape (fins, openings, stop, catch pockets and beams) is a region: a list of half-planes, circles and polygons that all hold at once. `region_2d()` turns a region into a shapely polygon and `region_3d()` into a CadQuery prism with true circles. The 3D model is built from the same regions, so 2D checks on them test the real shapes. `tools/check_fit.py` tests those regions; it was committed once the 0.1 fit test proved the shape. Do not build curves from shapely polylines: that made each STEP about 4 MB instead of 320 KB.

Each fact has one home. Sizes and the sources behind them live in the script (its parameter comments and docstring); it prints the main sizes on each run. Print settings live in the Cults listing text, `publish.yaml`. Design detail lives here. `README.md` only orients a source reader and points to those homes, so it never needs updating when a parameter changes.

`measure_cap.svg` is drawn by `tools/make_svg.py`, which still holds its own copy of the standard's numbers. It could import them from `h11_holder.py`, as the H7 one does, at the cost of needing CadQuery to draw the SVG.

## The holder (v1)

- Coordinates: z = 0 is the wall's inner face, where the fins' back faces rest; +z runs into the holder. Seen from the glass end, the wide-fin opening is at 180 degrees and the narrow ones near plus and minus 63 degrees. The twist is +`TWIST_DEG` about +z: clockwise seen from the plug. `TWIST = "ccw"` mirrors the stop and catches.
- The keyhole is symmetric about the x axis, so the standard's unstated view direction does not matter. The wide opening takes the widest side of every wide fin on both sides (plus or minus 6.05 plus `KEY_CLEAR`).
- One stop block sits between the upper narrow opening and where the lower narrow fin ends up. It ends the twist and blocks the wrong direction. It acts on narrow fins only, because they are the same on every bulb type; the wide fin's edges move with the type.
- Two catches, one behind each narrow fin when locked: a curved beam in the ring wall, fixed at one end, with a bump on its free end. The beam stands on the bed and has gaps all round (through the wall too), so it prints with no overhang and bends outward when a fin tip pushes the bump. The fin tip's radius is what the catch grips, so `CATCH_R` sets the grip on the shortest fins (r8 12.15) and `BEAM_GAP` must exceed the push from the longest a car takes (12.5). A click too weak or too stiff is tuned with `CATCH_R` (smaller grips harder) or `BEAM_T` (thicker is stiffer). The catches are springs, so they want a material that bends far before it breaks; PETG bends further than PLA.
- The beams are `BEAM_T` 1.0 thick and stand on the bed with `GAP` 0.6 around them. A squashed first layer can join a beam to the wall; a knife through the gap frees it.
- The closed end is a round dome outside (a half sphere on the tube; the operator asked for it to match the other models) and a 45 degree cone inside. A dome's inside would be flatter than 45 degrees over its top 15 mm and sag. Both curves stop just short of the axis with a flat under 1 mm across, because a curve that reaches the axis left a hole in the STL.
- The ring's ceiling is the cone r + z = `C0`. The pockets' ceilings sit 0.2 above it: coincident cones made OpenCascade return invalid solids.

## How an H11 bulb is held

- The bulb's datum is the back face of its fins (the standard's reference plane), the side toward the plug. The fins stand up to 4.0 mm in front of it. The plate the seal sits on is at least 3.0 mm behind it. In a car, the socket's wall (at least 2.2 mm) fills that gap and squeezes the seal against the plate; in this holder, the holder's wall does. The squeezed seal pushes the fins onto the wall, so the bulb does not rattle.
- Twist-lock: the fins pass through openings in the wall, then turn so their back faces press on the wall's inner face. The O-ring presses on the wall's outer face.
- The openings take every wide fin in the family: PGJ19-1 (H8, 8.0 centred), -2 (H11, 10.0 off-centre), -3 (H16, 10.0 centred) and -5 (H9, 10.0 off-centre the other way). The narrow fins, nose, fin reach and gaps are the same on all four.
- In the standard, the lock is a spring strip on the bulb (the halogen "nub") that snaps past a small bump in the socket's hole. LED retrofits often leave it out, so the holder must carry its own catch. Do not rely on the bulb's spring.

## Print orientation is designed in

The holder prints standing on its open end. The wall the fins press against is the first layers on the bed, so that face comes out flat. The slot the fins turn in has a ceiling that slopes at 45 degrees. It must never be a flat ring: nothing holds a flat ring up from below in any orientation.

## The connector cap

`h11_connector_cap.py` builds a separate part that shares no values with the holder. Its coordinates are the connector's: z = 0 at the mouth face, -z into the socket, y along the oval.

- **It clips onto the hooks on the oval's ends**, the ones the standard says hold the car's connector (view a and note 4 of sheet 7004-110-2). Test print 1 hooked only the side bump (view b) with one latch, and the cap flopped. One catch at one side cannot hold a cap square.
- **The insert fills the socket**, mouth recess and inner cavity, so the cap cannot rock. Test print 1's 4.5 mm plug in the recess alone let it rock. The insert's pin slots stop short of the pins' tips and never touch them. The key slot runs right across the insert, so it takes every type's keys and splits the insert into two towers deep inside.
- **Each arm is a spring standing on the bed**, fixed at one end with a gap all round, like the holder's catches: it runs up a long side, then curves round an end of the oval to a tooth. The straight run along the side makes the arm softer, so it bends further for the same stress.
- **The tooth's catch face slopes at 45 degrees**, so it takes up the play from the hooks' tolerance by pulling the cap onto the socket, and a firm pull lifts it out. `CATCH_Z` is set so the face presses even the shallowest hook. On the deepest one it still sits short of the hook's tip. A square face would lock until both arms were prised open.
- It prints standing on its back face. The arms stand on the bed and bend within the layers. The teeth's catch faces are 45 degree overhangs, and nothing else hangs. Test print 1's plug had a 45 degree underside, printed on its side, and it showed as a diagonal on the part.

## Why not the old case

The operator's earlier H11 case (someone else's design, not in this repository) taught these limits:

- Its twist slot has a flat ring ceiling about 4.75 mm wide, so every orientation droops or strings, and the sag shrinks the slot.
- The slot is 2.75 mm tall. The standard allows fins up to 4.0 mm thick.
- Its wall is 3.25 mm thick. A car socket's wall is about 2.2 to 3.0 mm, and the bulb promises only 3.0 mm behind its fins, O-ring included. Halogens had to be forced in.
- Its hole is plain and round, so nothing locks a bulb without a spring nub.
