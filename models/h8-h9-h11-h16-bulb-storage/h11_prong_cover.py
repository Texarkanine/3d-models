"""H11 (PGJ19) connector cap: a plug for the bulb's connector that clips on.

Fits H8, H9, H11 and H16: their connectors are the same. The connector on
the bulb is an oval socket with two pins recessed inside it and a small hook
on each end of the oval, which the car's plug clips onto. The cap stands in
for the car's plug while the bulb is stored.

An insert fills the socket the way the car's plug does: it fills the mouth
recess and carries on into the inner cavity, around the pins, so the cap
cannot rock. The insert has a slot for each pin and a slot across it for the
keys between the pins, wide enough for every type's keys (H9's differ), so it
splits into two towers deep inside.

Two springy arms clip onto the hooks. Each arm runs along one long side of
the oval and curves round one end, fixed at one end only, with a gap all
round. A tooth on its free end rides over the hook and drops behind it. The
tooth's catch face slopes at 45 degrees, so it pulls the cap onto the socket
whatever the hook's exact size, and a firm pull lifts it out again: grip the
cap and pull. A fingernail under an arm's free end helps.

The cap prints standing on its back face, insert up. The arms stand on the
bed and bend within the layers, where printed plastic is strongest; their
teeth's catch faces are 45 degree overhangs. No supports.

Sources for the default dimensions:
  - IEC 60061-1 sheet 7004-110-2 (cap PGJ19), read from GOST IEC 60061-1-2014,
    PDF pages 230-232, connector end: socket outside Y 14.85-15.15 by
    V 24.0-24.6, ends round (r3 = Y/2); mouth recess M 11.75-12.05 by
    N 21.15-21.45, ends round, R 5.85-6.15 deep; inner cavity P 8.2-8.5 by
    Q 17.65-17.95, at least S 15.85 deep; pins (ISO 8092-1 2.8 x 0.8) D 6.1
    apart, tips L 5.25-6.75 in; keys U 1.55-1.85 wide between the pins, up
    to T 5.6 long (H9: T1 and T2 from either side), ending at the recess.
    Hooks ("view a", note 4: they hold the connector) on both ends of the
    oval, about 2.4 wide, to W 28.15-28.45 across, catch face J 2.5-2.9 in
    from the mouth face, leaning back about 10 degrees, with a 45 degree
    ramp toward the mouth.
  - Test print 1 (2026-10-18): a 4.5 mm plug in the mouth recess and one
    latch on the side bump landed but let the cap flop; its plug's 45 degree
    underside left a visible diagonal.
  - Test print 2 (2026-10-18), these defaults: works.

Coordinates (use position): z = 0 is the socket's mouth face, -z runs into
the socket, +z away from the bulb. y runs along the oval, x across it.
to_print stands the cap on its back face.

Run:  python h11_prong_cover.py   (needs cadquery)
Writes STEP (opens in Solid Edge) and STL (for the slicer), standing on its
back face.
"""

import math
from pathlib import Path

import cadquery as cq

# ---- Connector (PGJ19), the sizes that matter ----------------------------------
SOCKET_W = 15.15     # outside width, Y max
SOCKET_L = 24.6      # outside length, V max
MOUTH_W = 11.75      # recess width, M min
MOUTH_L = 21.15      # recess length, N min
RECESS = 5.85        # recess depth, R min
CAVITY_W = 8.2       # inner cavity width, P min
CAVITY_L = 17.65     # inner cavity length, Q min
CAVITY_DEPTH = 15.85 # mouth face to the cavity floor, S min
PIN_PITCH = 6.1      # pins centre to centre, D
PIN_W = 2.8          # pin width (across the oval)
PIN_T = 0.8          # pin thickness
PIN_DEPTH = 5.25     # pin tips are at least this far in from the mouth face, L min
KEY_W = 1.85         # keys between the pins, U max
HOOK_TIP_MIN = 28.15 / 2   # hook tips from the centre, W min
HOOK_TIP_MAX = 28.45 / 2   # W max
HOOK_W = 2.4         # hook width across the oval (read off the drawing)

# ---- Insert ------------------------------------------------------------------------
INSERT_CLEAR = 0.15  # insert to recess and cavity, each side
INSERT_LEN = 13.0    # insert length into the socket; the cavity floor is at least 15.85 in
PIN_CLEAR = 0.5      # pin slots, each side: the cap does not touch the pins
KEY_CLEAR = 0.3      # key slot, each side
TIP_EDGE = 0.6       # chamfer on the insert's tip

# ---- Arms -----------------------------------------------------------------------------
BACK = 4.0           # back plate thickness: what you grip to pull the cap off
PLATE_MARGIN = 1.0   # back plate past the socket's outline
ARM_T = 1.1          # arm thickness; sets the grip
ARM_GAP = 0.6        # printed gap between the arms and the back plate, at least
HOOK_CLEAR = 0.25    # arms outside the hook tips
ENGAGE = 1.2         # tooth reaches this far below the smallest hook's tip
CATCH_Z = 3.6        # tooth's catch face meets its tip this far in from the mouth face
TOOTH_LEN = 1.4      # tooth along the socket, past its catch face
TOOTH_SPAN = 44.0    # degrees of arc the tooth covers, centred on the hook
ROOT_Y = -2.0        # arm root, along the long side (the +x arm; the other is turned half a turn)
FREE_DEG = 125.0     # arm's free end, degrees round the end of the oval from the long side
E_PLA = 3000.0       # MPa, printed PLA, for the arm estimates printed on each run

# ---- Derived ---------------------------------------------------------------------
C_END = SOCKET_L / 2 - SOCKET_W / 2          # centres of the oval's round ends
R_PLATE = SOCKET_W / 2 + PLATE_MARGIN        # back plate: an oval this much bigger
R_IN = HOOK_TIP_MAX - C_END + HOOK_CLEAR     # arm inner face, from the end's centre
R_OUT = R_IN + ARM_T
R_TOOTH = HOOK_TIP_MIN - C_END - ENGAGE      # tooth tip
Z_ARM = -(CATCH_Z + TOOTH_LEN)               # far end of the arms
RECESS_Z = -(RECESS - 0.25)                  # where the insert steps down to the cavity
PIN_TOP = -(PIN_DEPTH - 0.5)                 # pin slots reach this close to the mouth
LIFT = HOOK_TIP_MAX + 0.1 - (C_END + R_TOOTH)  # arm deflection to pass the largest hook

assert C_END + R_TOOTH >= SOCKET_L / 2 + 0.3, "tooth must clear the socket's end"
assert R_IN - R_PLATE >= ARM_GAP, "arms need a printed gap round the back plate"
assert INSERT_LEN <= CAVITY_DEPTH - 1.5, "insert must stop short of the cavity floor"
assert PIN_TOP > RECESS_Z, "pin slots must reach up past the step"
assert R_TOOTH * math.sin(math.radians(TOOTH_SPAN / 2)) >= HOOK_W / 2 + 1.5, \
    "tooth must cover the hook with room to spare across the oval"


def box(x0, x1, y0, y1, z0, z1):
    return (cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False)
            .translate((x0, y0, z0)))


def oval(w, l, z0, z1):
    """Stadium w across (x) by l long (y), round ends, from z0 to z1."""
    return cq.Workplane("XY").workplane(offset=z0).slot2D(l, w, angle=90).extrude(z1 - z0)


def insert():
    w, l = MOUTH_W - 2 * INSERT_CLEAR, MOUTH_L - 2 * INSERT_CLEAR
    cw, cl = CAVITY_W - 2 * INSERT_CLEAR, CAVITY_L - 2 * INSERT_CLEAR
    body = oval(w, l, RECESS_Z, 0).union(
        oval(cw, cl, -INSERT_LEN, RECESS_Z + 0.01).faces("<Z").chamfer(TIP_EDGE))
    pins = cq.Workplane("XY")
    for y in (PIN_PITCH / 2, -PIN_PITCH / 2):
        pins = pins.union(box(-PIN_W / 2 - PIN_CLEAR, PIN_W / 2 + PIN_CLEAR,
                              y - PIN_T / 2 - PIN_CLEAR, y + PIN_T / 2 + PIN_CLEAR,
                              -INSERT_LEN - 1, PIN_TOP))
    keys = box(-SOCKET_W, SOCKET_W, -KEY_W / 2 - KEY_CLEAR, KEY_W / 2 + KEY_CLEAR, -INSERT_LEN - 1, RECESS_Z)
    return body.cut(pins).cut(keys)


def arm():
    """The arm round the +y end: up the +x side from ROOT_Y, round the end to FREE_DEG."""
    def at(r, deg):
        a = math.radians(deg)
        return (r * math.cos(a), C_END + r * math.sin(a))

    mid = FREE_DEG / 2
    outline = (cq.Workplane("XY").workplane(offset=Z_ARM)
               .moveTo(R_IN, ROOT_Y).lineTo(R_IN, C_END)
               .threePointArc(at(R_IN, mid), at(R_IN, FREE_DEG))
               .lineTo(*at(R_OUT, FREE_DEG))
               .threePointArc(at(R_OUT, mid), (R_OUT, C_END))
               .lineTo(R_OUT, ROOT_Y).close())
    body = outline.extrude(BACK - Z_ARM)
    # Root: the arm's end joins the back plate, clear of the socket's side.
    root = box(SOCKET_W / 2 + 0.25, R_OUT, ROOT_Y - 1.5, ROOT_Y + 0.01, Z_ARM, BACK)

    # Tooth: an (r, z) profile turned through TOOTH_SPAN about the end's centre.
    # Its catch face slopes at 45 degrees from the tip out to the arm.
    lead = 0.4
    profile = [(R_TOOTH, -CATCH_Z), (R_IN + 0.2, -CATCH_Z + (R_IN + 0.2 - R_TOOTH)),
               (R_IN + 0.2, Z_ARM), (R_TOOTH + lead, Z_ARM), (R_TOOTH, Z_ARM + lead)]
    tooth = (cq.Workplane("XZ").polyline(profile).close()
             .revolve(TOOTH_SPAN, (0, 0, 0), (0, 1, 0)))
    # The revolve sweeps counterclockwise (seen from +z) from the +x axis; turn it to straddle 90 degrees.
    tooth = tooth.rotate((0, 0, 0), (0, 0, 1), 90 - TOOTH_SPAN / 2).translate((0, C_END, 0))
    return body.union(root).union(tooth)


def cap():
    plate = oval(2 * R_PLATE, SOCKET_L + 2 * PLATE_MARGIN, 0, BACK).edges(">Z").chamfer(0.8)
    one = arm()
    arms = one.union(one.rotate((0, 0, 0), (0, 0, 1), 180))
    return plate.union(insert()).union(arms)


def to_print(part):
    # Back face on the bed, insert up: half a turn about x.
    return part.rotate((0, 0, 0), (1, 0, 0), 180).translate((0, 0, BACK))


def arm_numbers():
    """Rough arm force (N) at full deflection and bending stress (MPa), for tuning.

    The arm is a straight run of length L_s up the side, then a quarter turn of
    radius R to the tooth, loaded outward at the tooth.
    """
    r = (R_IN + R_OUT) / 2
    l_s = C_END - ROOT_Y
    i = (BACK - Z_ARM) * ARM_T ** 3 / 12
    flex = r ** 2 * (math.pi / 4 * r + l_s) / (E_PLA * i)   # deflection per newton
    force = LIFT / flex
    stress = force * r * (ARM_T / 2) / i
    return force, stress


def export(shape, stem, out):
    cq.exporters.export(shape, str(out / f"{stem}.step"))
    cq.exporters.export(shape, str(out / f"{stem}.stl"), tolerance=0.01, angularTolerance=0.1)


if __name__ == "__main__":
    out = Path(__file__).resolve().parent
    part = cap()
    export(to_print(part), "h11_prong_cover", out)
    bb = part.val().BoundingBox()
    force, stress = arm_numbers()
    print(f"cap {bb.xlen:.1f} x {bb.ylen:.1f} x {bb.zlen:.1f}; insert {INSERT_LEN} deep; "
          f"teeth reach {ENGAGE}-{ENGAGE + HOOK_TIP_MAX - HOOK_TIP_MIN:.2f} under the hooks; "
          f"each arm lifts {LIFT:.2f} to pass with about {force:.1f} N ({stress:.0f} MPa)")
