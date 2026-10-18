"""H11 (PGJ19) connector cap: a plug for the bulb's connector, with a latch.

Fits H8, H9, H11 and H16: their connectors are the same. The connector on
the bulb is an oval socket with two pins recessed inside it, and a small
bump on one long side for the car's plug to latch onto. The cap stands in
for the car's plug while the bulb is stored: a short plug fills the mouth of
the socket, short of the pins, and a lever reaches over the bump and hooks
behind it, so the cap clicks on and stays put.

To take it off, squeeze the lever's tail toward the body of the cap, thumb
on the lever, finger on the far side of the body, and pull. The lever is a
see-saw: it hangs on two thin crossed leaves just behind the mouth, so
pressing its tail lifts the hook. The leaves only bend; pulling on the cap
stretches one and pushes the other end-on, so the hook holds firmly even
though it lifts easily.

The cap prints standing on one end of the oval, so the lever, its hook and
the leaves are all drawn in the bed's plane: they bend within the layers,
where printed plastic is strongest, and the hook comes out sharp. The leaves
start part way up and print as bridges. The plug's lower end is a 45 degree
point inside the oval's round end, and its underside rises from the body at
45 degrees. No supports.

Sources for the default dimensions:
  - IEC 60061-1 sheet 7004-110-2 (cap PGJ19), read from GOST IEC 60061-1-2014,
    PDF pages 230-232, connector end: socket outside Y 14.85-15.15 by
    V 24.0-24.6, ends round (r3 = Y/2); mouth recess M 11.75-12.05 by
    N 21.15-21.45, ends round, R 5.85-6.15 deep; pin tips L 5.25-6.75 in
    from the mouth face; the keys between the pins stop at the recess, so the
    cap fits every variant. Latch bump ("view b") on the middle of a long
    side: XA 2.4-2.6 wide, catch face XE 7.4-7.6 from the mouth face and
    XC 1.1-1.3 tall there, rising to XD 1.6-1.8, then a 58-62 degree slope
    toward the mouth.

Coordinates (use position): z = 0 is the socket's mouth face, -z runs into
the socket, +z away from the bulb. The bump is on the +x side; y runs along
the oval. to_print stands the cap on its -y end.

Run:  python h11_connector_cap.py   (needs cadquery)
Writes STEP (opens in Solid Edge) and STL (for the slicer), standing on end.
"""

import math
from pathlib import Path

import cadquery as cq

# ---- Connector (PGJ19), the sizes that matter ----------------------------------
MOUTH_W = 11.75      # recess width, M min
MOUTH_L = 21.15      # recess length, N min
PIN_DEPTH = 5.25     # pin tips are at least this far in from the mouth face, L min
SOCKET_W = 15.15     # outside width, Y max
SOCKET_W_MIN = 14.85 # outside width, Y min: the bump side sits lowest
SOCKET_L = 24.6      # outside length, V max
CATCH_Z = 7.6        # bump's catch face from the mouth face, XE max (7.4-7.6)
CATCH_H = 1.1        # bump height at its catch face, XC min (1.1-1.3)
BUMP_H = 1.8         # bump's highest point, XD max (1.6-1.8)

# ---- Fit ------------------------------------------------------------------------
PLUG_CLEAR = 0.25    # plug to recess, each side
PLUG_LEN = 4.5       # plug length into the recess; stays clear of the pins
PLUG_TIP = 0.3       # half-width of the flat at the bottom point of the plug, as printed
HOOK_CLEAR = 0.15    # hook behind the catch face when the cap is fully on
HOOK_GAP = 0.3       # hook tip above the socket's side
HOOK_FLAT = 0.8      # flat on the hook tip
HOOK_LEAD = 40.0     # slope the hook rides up the bump on, degrees from the socket's side
HOOK_UNDERCUT = 5.0  # catch face leans back this much, so a pull draws the hook in
LEVER_CLEAR = 0.3    # lever above the bump's highest point
LEVER_T = 2.0        # lever thickness
LIFT = 1.9           # hook lift when the tail is squeezed fully

# ---- Body and pivot -----------------------------------------------------------------
BODY_LEN = 15.0      # body and lever reach this far out from the mouth face
BODY_HALF_W = 8.35   # body half-width across x; its +x face is the tail's stop
END_SKIN = 1.5       # body wall between the mouth face and the pivot pocket
LEAF_T = 0.8         # leaf thickness (two lines of a 0.4 nozzle)
LEAF_H = 6.0         # height of each leaf along y
LEAF_SPAN = 5.5      # each leaf runs this far across x (and as far along z), at 45 degrees
LEAF_SEP = 1.0       # gap between the two leaves where they cross
POCKET_CLEAR = 1.2   # pocket round the leaves
EDGE = 1.5           # rounds the body and lever at the grip end
E_PLA = 3000.0       # MPa, printed PLA, for the lever estimates printed on each run

# ---- Derived ---------------------------------------------------------------------
X_SIDE = SOCKET_W / 2                        # the socket's bump side
X_HOOK = X_SIDE + HOOK_GAP                   # hook tip
X_IN = X_SIDE + BUMP_H + LEVER_CLEAR         # lever inner face
X_OUT = X_IN + LEVER_T
Z_CATCH = -(CATCH_Z + HOOK_CLEAR)            # hook catch face, at the tip
HALF_L = SOCKET_L / 2 + 0.1                  # half-length of the cap along y
X_POCKET = X_IN - LEAF_SPAN                  # pocket's back wall, where the leaves start
Z_PIVOT = END_SKIN + POCKET_CLEAR + LEAF_SPAN / 2   # where the leaves cross
X_PIVOT = X_IN - LEAF_SPAN / 2
Z_HOOK = Z_CATCH - HOOK_FLAT / 2             # middle of the hook tip
THETA = LIFT / (Z_PIVOT - Z_HOOK)            # lever turn for a full squeeze, radians
TAIL_GAP = X_IN - BODY_HALF_W                # room for the tail to move in
Z_FRONT = Z_CATCH - HOOK_FLAT - (X_IN - X_HOOK) / math.tan(math.radians(HOOK_LEAD))

CATCH_MIN = SOCKET_W_MIN / 2 + CATCH_H - X_HOOK  # least the hook overlaps the catch face

assert CATCH_MIN >= 0.5, "hook must catch at least 0.5 of the smallest bump on the narrowest socket"
assert THETA * (BODY_LEN - Z_PIVOT) <= TAIL_GAP + 0.01, "the tail must reach the full lift before it stops"
assert LIFT >= X_SIDE + BUMP_H - X_HOOK + 0.2, "a full squeeze must lift the hook clear of the bump"
assert PLUG_LEN <= PIN_DEPTH - 0.5, "plug must stay clear of the pins"
assert END_SKIN >= 1.0, "pocket must leave the face over the mouth solid"
assert BODY_HALF_W >= X_SIDE + 0.5, "body must cover the whole mouth face"


def box(x0, x1, y0, y1, z0, z1):
    return (cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False)
            .translate((x0, y0, z0)))


def xz_prism(points, y0, y1):
    """An (x, z) polygon extruded along y from y0 to y1."""
    # The XZ workplane's normal is -y, so draw at y = y1 and extrude toward -y.
    return (cq.Workplane("XZ", origin=(0, y1, 0)).polyline(points).close().extrude(y1 - y0))


def plug():
    """Oval plug for the mouth recess. Its -y end, the bottom as printed, is a 45 degree point."""
    hw = MOUTH_W / 2 - PLUG_CLEAR
    hl = MOUTH_L / 2 - PLUG_CLEAR
    yc = hl - hw                               # centres of the round ends
    tip = -yc - (hw - PLUG_TIP)                # flat of the point
    outline = (cq.Workplane("XY").moveTo(-hw, -yc).lineTo(-hw, yc)
               .threePointArc((0, hl), (hw, yc)).lineTo(hw, -yc)
               .lineTo(PLUG_TIP, tip).lineTo(-PLUG_TIP, tip).close())
    body = outline.extrude(-PLUG_LEN).faces("<Z").chamfer(0.5)
    # The point would hang out from the body as printed: slope its underside
    # up at 45 degrees from the mouth face instead.
    chin = (cq.Workplane("YZ", origin=(-hw - 1, 0, 0))
            .polyline([(tip - 1, 1), (tip, 0), (tip + PLUG_LEN + 1, -PLUG_LEN - 1), (tip - 1, -PLUG_LEN - 1)])
            .close().extrude(2 * hw + 2))
    return body.cut(chin)


def lever():
    """Lever and hook, drawn in x-z and standing the whole height of the cap."""
    z_root = Z_CATCH - (X_IN - X_HOOK) * math.tan(math.radians(HOOK_UNDERCUT))
    pts = [
        (X_IN, BODY_LEN), (X_OUT - EDGE, BODY_LEN), (X_OUT, BODY_LEN - EDGE),
        (X_OUT, Z_FRONT + 0.8), (X_OUT - 0.8, Z_FRONT),
        (X_IN, Z_FRONT),                          # lead-in starts at the lever's face
        (X_HOOK, Z_CATCH - HOOK_FLAT), (X_HOOK, Z_CATCH),
        (X_IN, z_root),                           # catch face, undercut
    ]
    return xz_prism(pts, -HALF_L, HALF_L)


def leaves():
    """Two thin leaves crossing at 45 degrees between the pocket wall and the lever."""
    def leaf(z_wall, z_lever, y0, y1):
        a, b = (X_POCKET, z_wall), (X_IN, z_lever)
        ln = math.dist(a, b)
        ux, uz = (b[0] - a[0]) / ln, (b[1] - a[1]) / ln
        nx, nz = -uz * LEAF_T / 2, ux * LEAF_T / 2
        ext = 0.6                                 # run into the wall and the lever
        p0 = (a[0] - ux * ext, a[1] - uz * ext)
        p1 = (b[0] + ux * ext, b[1] + uz * ext)
        pts = [(p0[0] + nx, p0[1] + nz), (p1[0] + nx, p1[1] + nz),
               (p1[0] - nx, p1[1] - nz), (p0[0] - nx, p0[1] - nz)]
        return xz_prism(pts, y0, y1)

    lo, hi = Z_PIVOT - LEAF_SPAN / 2, Z_PIVOT + LEAF_SPAN / 2
    s = LEAF_SEP / 2
    return leaf(lo, hi, -s - LEAF_H, -s).union(leaf(hi, lo, s, s + LEAF_H))


def cap():
    body = box(-BODY_HALF_W, BODY_HALF_W, -HALF_L, HALF_L, 0, BODY_LEN).edges("|Y and >Z").fillet(EDGE)
    pocket = box(X_POCKET, BODY_HALF_W + 1, -(LEAF_SEP / 2 + LEAF_H + POCKET_CLEAR / 2),
                 LEAF_SEP / 2 + LEAF_H + POCKET_CLEAR / 2,
                 Z_PIVOT - LEAF_SPAN / 2 - POCKET_CLEAR, Z_PIVOT + LEAF_SPAN / 2 + POCKET_CLEAR)
    return body.cut(pocket).union(plug()).union(leaves()).union(lever())


def to_print(part):
    # Stand on the -y end: model y becomes print z.
    return part.rotate((0, 0, 0), (1, 0, 0), 90).translate((0, 0, HALF_L))


def lever_numbers():
    """Rough squeeze force (N) at the tail and leaf bending stress (MPa) at a full squeeze."""
    leaf_len = LEAF_SPAN * math.sqrt(2)
    stiffness = 2 * E_PLA * (LEAF_H * LEAF_T ** 3 / 12) / leaf_len   # N mm per radian, both leaves
    force = stiffness * THETA / (BODY_LEN - 1.0 - Z_PIVOT)
    stress = E_PLA * (LEAF_T / 2) * THETA / leaf_len
    return force, stress


def export(shape, stem, out):
    cq.exporters.export(shape, str(out / f"{stem}.step"))
    cq.exporters.export(shape, str(out / f"{stem}.stl"), tolerance=0.01, angularTolerance=0.1)


if __name__ == "__main__":
    out = Path(__file__).resolve().parent
    export(to_print(cap()), "h11_connector_cap", out)
    force, stress = lever_numbers()
    print(f"cap {2 * BODY_HALF_W:.1f} x {2 * HALF_L:.1f} body, {BODY_LEN - Z_FRONT:.1f} long with the lever; "
          f"hook catches at least {CATCH_MIN:.2f} of the bump; "
          f"full squeeze lifts it {LIFT} with about {force:.1f} N ({stress:.0f} MPa in the leaves)")
