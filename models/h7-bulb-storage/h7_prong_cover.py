"""H7 (PX26d) prong cover: a cap that presses onto the bulb's two tabs.

It keeps the tabs clean and straight while the bulb is stored. It fits any
bulb or LED plug with the standard H7 tabs: two flat 6.3 x 0.8 tabs, faces
parallel, 11.5 apart centre to centre.

The cover is a small rounded block, no bigger than its springs need, so it
reads as an extension of the plug that happens to cover the tabs. Grip its
sides and pull. Its flat end has a slot for each tab. Each tab is pinched between two springs, one on each face.
The springs are thin walls joined to the cover at one end only, with a gap
all round, so they bend sideways like leaf springs. A rounded ridge on each
spring presses the tab; the grip comes from how far the tab pushes the
springs back (SQUEEZE), not from how exactly the slot prints. One spring's
ridge is low and the other's high, so they never face each other across the
slot: facing ridges would leave a gap too thin to print.

The cover prints standing on its slotted end. The springs stand on the bed
and bend within the layers, which is where printed plastic is strongest.
Each slot mouth has a 45 degree lead-in, and the ridges ramp in and out at
45 degrees, so the tabs find their way in and slide back out.

Sources for the default dimensions:
  - IEC 60061-1 sheet 7004-5 (cap PX26d), read from its identical Russian
    adoption GOST IEC 60061-1-2014, PDF page 15: two contact tabs, D 11.5
    nominal apart; tab length X at least 8 behind the base, tab tips Y 15-16
    and the base V at least 6 behind the reference plane; note 9 sends the
    other tab sizes to ISO 8092-1 (6.3 x 0.8).
  - Test print 1 (2026-10-18), a 25 mm spool with 9 mm springs: gripped
    the operator's LED plug well but was too big. These shorter, thinner
    springs keep about the same force.
  - Test print 2 (2026-10-18), these defaults: works.
  - The operator's LED H7 plug, measured 2026-10-18: tabs 0.8 thick, 6.2
    wide, 10.3 long, 10.75 apart face to face (so 11.55 centre to centre),
    narrowing to 4.5 wide over the last 2.3 mm, with a hole about 2.5 across
    near the tip.

Coordinates: z = 0 is the cover's slotted face, which rests on the bulb's
base; +z runs away from the bulb. The tabs lie parallel to x, at y = +-
TAB_PITCH / 2. The cover is built in print orientation.

Run:  python h7_prong_cover.py   (needs cadquery)
Writes STEP (opens in Solid Edge) and STL (for the slicer), standing on the
slotted end.
"""

from pathlib import Path

import cadquery as cq

# ---- Tabs (PX26d, ISO 8092-1 6.3 x 0.8) -------------------------------------
TAB_T = 0.8          # tab thickness
TAB_W = 6.4          # tab width: 6.3 nominal plus tolerance (operator's LED: 6.2)
TAB_PITCH = 11.5     # tab centre to centre, PX26d D (operator's LED: 11.55)
TAB_LEN = 10.3       # longest tab behind the base: PX26d allows 10 (Y 16 - V 6); operator's LED 10.3

# ---- Springs ------------------------------------------------------------------
SQUEEZE = 0.25       # how far the tab pushes each spring back; sets the grip
SLOT_CLEAR = 0.25    # gap between each spring and the tab, away from the ridge
SPRING_T = 0.9       # spring thickness
SPRING_H = 9.0       # spring height from the face; tabs are at least 8 long
SPRING_L = 7.0       # spring length from its root to the ridge; longer is softer
RIDGE_W = 2.4        # ridge width along the spring
RIDGE_X = 1.6        # ridge centre, from the tab centre toward the spring's free end
RIDGE_SPLIT = 4.75   # the inner spring's ridge ends below this height, the outer one's starts above it
RIDGE_GAP_Z = 0.5    # height between the end of one ridge and the start of the other
GAP = 0.6            # printed gap round the springs
TOP_GAP = 1.2        # gap above the springs: their roof is a bridge and may sag
END_CLEAR = 0.3      # slot ends past the tab's edges
DEPTH_CLEAR = 0.7    # slot deeper than the longest tab, so the face rests on the base
LEAD = 0.3           # 45 degree lead-in on the springs at the slot mouth
E_PLA = 3000.0       # MPa, printed PLA, for the grip estimate printed on each run

# ---- Body: a rounded block -------------------------------------------------------------
WALL = 1.0           # outside the gaps round the springs
END_WALL = 1.2       # above the tab tips
CORNER_R = 1.0       # rounds the block's long edges; more would thin the wall at the springs' corners
EDGE = 0.4           # chamfer round the slotted face (also takes the first layer's squash)
TOP_EDGE = 0.8       # chamfer round the far end

# ---- Derived ----------------------------------------------------------------
Y_C = TAB_PITCH / 2                          # tab centre plane, +y tab
S = TAB_T / 2 + SLOT_CLEAR                   # spring face, from the tab centre plane
RIDGE = SLOT_CLEAR + SQUEEZE                 # ridge height above the spring face
X_FREE = TAB_W / 2 + END_CLEAR               # springs' free ends and the slot end
X_ROOT = RIDGE_X - SPRING_L                  # where the springs join the body
Y_IN = Y_C - S - SPRING_T - GAP              # inner edge of the gaps round the springs
Y_OUT = Y_C + S + SPRING_T + GAP             # outer edge
Z_ROOF = SPRING_H + TOP_GAP                  # roof over the springs
Z_TIP = TAB_LEN + DEPTH_CLEAR                # top of the slot
HALF_X = max(-X_ROOT, X_FREE + GAP) + WALL    # block half-width along the tabs
HALF_Y = Y_OUT + WALL                        # block half-width across them
Z_TOP = Z_TIP + END_WALL

assert S - RIDGE < TAB_T / 2, "ridges must press the tab"
assert Y_IN >= 1.5, "the two tabs' springs need wall between them"
assert X_ROOT < -X_FREE, "springs must reach past the far end of the tab"
assert RIDGE_X + RIDGE_W / 2 <= TAB_W / 2, "ridge must press the flat of the tab"
assert min(RIDGE_SPLIT - LEAD - 0.2, SPRING_H - RIDGE_SPLIT) - RIDGE_GAP_Z / 2 >= 2 * RIDGE + 1.0, \
    "each ridge needs 1 mm of full height between its sloped ends"
assert 2 * S - RIDGE >= 0.6, "slot beside a ridge must be wide enough to print open"
assert Z_ROOF < Z_TIP, "the tab-tip slots must rise through the roof over the springs"


def box(x0, x1, y0, y1, z0, z1):
    return (cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False)
            .translate((x0, y0, z0)))


def block():
    return (box(-HALF_X, HALF_X, -HALF_Y, HALF_Y, 0, Z_TOP).edges("|Z").fillet(CORNER_R)
            .faces("<Z").chamfer(EDGE).faces(">Z").chamfer(TOP_EDGE))


def ridge(y_face, toward, z0, z1):
    """Rounded ridge on a spring face at y_face, bulging toward +y (toward=1) or -y (-1),
    from z0 to z1, its ends sloped at 45 degrees."""
    r = (RIDGE_W ** 2 / 4 + RIDGE ** 2) / (2 * RIDGE)
    yc = y_face + toward * (RIDGE - r)
    disc = cq.Workplane("XY").center(RIDGE_X, yc).circle(r).extrude(z1)
    back, top = y_face - toward * 0.01, y_face + toward * RIDGE
    ends = (cq.Workplane("YZ").polyline([(back, z0), (top, z0 + RIDGE), (top, z1 - RIDGE), (back, z1)])
            .close().extrude(2 * RIDGE_W).translate((RIDGE_X - RIDGE_W, 0, 0)))
    return disc.intersect(ends)


def tab_features():
    """Cuts and springs for the +y tab: (gaps, springs, lead-in, tip slot)."""
    gaps = box(X_ROOT, X_FREE + GAP, Y_IN, Y_OUT, -1, Z_ROOF)
    low = (LEAD + 0.2, RIDGE_SPLIT - RIDGE_GAP_Z / 2)
    high = (RIDGE_SPLIT + RIDGE_GAP_Z / 2, SPRING_H)
    springs = (box(X_ROOT - WALL / 2, X_FREE, Y_C - S - SPRING_T, Y_C - S, 0, SPRING_H)
               .union(box(X_ROOT - WALL / 2, X_FREE, Y_C + S, Y_C + S + SPRING_T, 0, SPRING_H))
               .union(ridge(Y_C - S, 1, *low)).union(ridge(Y_C + S, -1, *high)))
    # Lead-in: a 45 degree chamfer on the spring faces at the slot mouth.
    w0 = S + LEAD + 1
    lead_in = (cq.Workplane("YZ").polyline([(Y_C - w0, -1), (Y_C + w0, -1),
                                            (Y_C + S, LEAD), (Y_C - S, LEAD)]).close()
               .extrude(X_FREE - X_ROOT).translate((X_ROOT, 0, 0)))
    tip = box(-X_FREE, X_FREE, Y_C - TAB_T / 2 - 0.3, Y_C + TAB_T / 2 + 0.3, SPRING_H, Z_TIP)
    return gaps, springs, lead_in, tip


def cover():
    def both(shape):
        # the -y tab's features are the +y tab's turned half a turn
        return shape.union(shape.rotate((0, 0, 0), (0, 0, 1), 180))

    gaps, springs, lead_in, tip = (both(f) for f in tab_features())
    return block().cut(gaps).union(springs).cut(lead_in).cut(tip)


def grip():
    """Rough force (N) and bending stress (MPa) of one spring at SQUEEZE, for tuning."""
    i = SPRING_H * SPRING_T ** 3 / 12
    force = 3 * E_PLA * i * SQUEEZE / SPRING_L ** 3
    stress = 3 * E_PLA * (SPRING_T / 2) * SQUEEZE / SPRING_L ** 2
    return force, stress


def export(shape, stem, out):
    cq.exporters.export(shape, str(out / f"{stem}.step"))
    cq.exporters.export(shape, str(out / f"{stem}.stl"), tolerance=0.01, angularTolerance=0.1)


if __name__ == "__main__":
    out = Path(__file__).resolve().parent
    export(cover(), "h7_prong_cover", out)
    force, stress = grip()
    print(f"block {2 * HALF_X:.1f} x {2 * HALF_Y:.1f} x {Z_TOP:.1f}; slots {Z_TIP:.1f} deep; "
          f"each spring about {force:.1f} N at {SQUEEZE} mm squeeze ({stress:.0f} MPa)")
