"""H11 (PGJ19) bulb holder with a twist lock, like a headlamp socket.

Fits H8, H9, H11 and H16: they share the PGJ19 cap and differ only in the wide
fin. The open end of the holder is a wall with a keyhole: a round hole for
the nose and an opening for each fin. Push the bulb in, glass first, until
the fins are through the wall, then twist. The fins' back faces then rest on
the wall's inner face, and the bulb's seal is squeezed between the wall's
outer face and the bulb's plate, which pushes the fins onto the wall, as in a
car. The head sits in a closed tube.

The bulb turns one way only: a stop block beside one narrow-fin opening stops
the turn in the right place, and also blocks the turn in the wrong direction.
The holder carries its own lock, so bulbs without the halogen spring (LED
retrofits) lock too: two springy catches stand in the ring the fin tips turn
in. Each is a curved beam fixed at one end with a bump on its free end. A
narrow fin's tip pushes the bump outward, passes it, and the bump springs
back behind the fin. The narrow fins are the same on every bulb type, so the
catches and the stop act on them only.

The holder prints standing on its open end, so the wall the fins rest on is
the first layers on the bed. The catches stand on the bed too and are free on
every other side. The ring the fins turn in has a 45 degree ceiling, and so do
the gaps around the catches and the inside of the closed end. The outside of
the closed end is a round dome: it faces up, so it needs no support. No supports.

Sources for the default dimensions:
  - IEC 60061-1 sheet 7004-110-2 (cap PGJ19), read from GOST IEC 60061-1-2014:
    fin tip radius r8 12.15-12.25, fins F at most 4.0 thick, narrow fin edges
    B 7.8-8.0 and B1 3.3-3.5, wide fin B5 6.0 + B6 4.0 or B4 10.0, nose A1
    at most 19.0, plate face E at least 3.0 behind the fins.
  - IEC 60061-2 sheet 7005-110-3 (holder PGJ19), read from GOST IEC 60061-2-2017:
    hole Z 19.5-20.0, openings r8 12.4-12.5, B 8.1-8.3, B1 3.7-3.9,
    B5 6.1-6.2; wall at least 2.2 (2.4 for H16).
  - UNECE R37 sheet H8/1 head outline (GOST R 41.37-99): at most 44.0 long.
  - The operator's LED H11 (2026-10-15): fins 1.0 thick, plate 3.33 behind
    the fins, seal face 1.38 behind them, 32 long.

Coordinates: z = 0 is the wall's inner face, where the fins' back faces rest;
+z points into the holder, toward the bulb's tip; the wall is z = -WALL..0.
Seen from the glass end, the wide-fin opening is at -x (180 degrees) and the
narrow-fin openings are near +-63 degrees. The twist is +TWIST_DEG about +z
(counterclockwise seen from the glass end, clockwise seen from the plug).

Run:  python h11_holder.py   (needs cadquery and shapely)
Writes STEP (opens in Solid Edge) and STL (for the slicer), already standing
on the open end.
"""

import math
from pathlib import Path

import cadquery as cq
from shapely import affinity
from shapely.geometry import Point, Polygon
from shapely.ops import unary_union

# ---- Bulb cap PGJ19: the largest sizes the standard allows -----------------
FIN_R = 12.25        # fin tip radius, r8 max
FIN_R_MIN = 12.15    # r8 min: the catches must still grip this
CAR_FIN_R = 12.5     # a car socket's openings reach 12.5 (r8 max), so no bulb that fits a car reaches further
FIN_F = 4.0          # fin thickness in front of their back faces, F max (operator's LED: 1.0)
FIN_B = 8.0          # narrow fin: straight edge this far from the centre line, B max
FIN_B1 = 3.5         # narrow fin: other edge this far from the 60 degree line, B1 max
# Wide fin, (below, above) the centre line: H8 PGJ19-1, H11 -2, H16 -3, H9 -5.
WIDE = {"H8": (4.05, 4.05), "H11": (4.05, 6.05), "H16": (5.05, 5.05), "H9": (6.05, 4.05)}
NOSE_D = 19.0        # nose, A1 max
HEAD_D = 21.0        # bore for the head (R37: Ø19, glass Ø15; a car's hole is at most Ø20)
HEAD_LEN = 48.0      # wall's inner face to the start of the closed end: longest head (R37: 44) + 4

# ---- Wall and openings --------------------------------------------------------
WALL = 2.4           # a car's wall is at least 2.2 (H16: 2.4); the plate is at least 3.0 behind the fins
HOLE_D = 20.2        # nose hole; a car's is 19.5-20.0, and printed holes come out a little small
KEY_CLEAR = 0.4      # fin openings: this much bigger than the largest fin, each side
KEY_R = 12.75        # fin openings reach this far from the centre

# ---- The ring the fins turn in -------------------------------------------------
SLOT_R = 12.9        # outer radius of the ring (fins reach at most CAR_FIN_R)
SLOT_H = 4.5         # flat height of the ring above the wall; the ceiling then slopes in at 45 degrees
TWIST_DEG = 65.0     # how far the bulb turns
TWIST = "cw"         # "cw": clockwise seen from the plug end; "ccw" mirrors the stop and catches
STOP_CLEAR = 0.3     # gap between the stop block and the narrow fin it stops
STOP_IN = 10.6       # stop block's inner radius: clear of the head (Ø21 bore)

# ---- Catches ----------------------------------------------------------------------
CATCH_R = 11.8       # the bump reaches in to this radius: fin tips pass it with 0.35-0.7 to spare
CATCH_CLEAR = 0.3    # gap between the bump and the locked fin behind it
BEAM_T = 1.0         # beam thickness; sets the click force
BEAM_ARC = 40.0      # beam length, degrees, from the free end to where it is fixed; shorter clicks harder
BEAM_GAP = 0.9       # room behind the beam to bend outward (it moves at most CAR_FIN_R - CATCH_R)
GAP = 0.6            # printed gap around the beams and bumps
BUMP_ENTRY = 30.0    # slope the fin rides up when locking, degrees from the ring wall
BUMP_RETAIN = 50.0   # slope it rides up when unlocking: steeper, so unlocking takes more force
BUMP_FLAT = 0.4      # flat top of the bump

# ---- Body -------------------------------------------------------------------------
SIDE_WALL = 1.6      # outside the catches
TUBE_WALL = 1.8      # around the head and over the closed end
BASE_CHAMFER = 0.6   # outer edge on the bed

# ---- Derived ------------------------------------------------------------------------
R_HOLE = HOLE_D / 2
R_HEAD = HEAD_D / 2
R_LAND = SLOT_R - GAP              # where the wall is cut to free the beams
R_P = SLOT_R + BEAM_T + BEAM_GAP   # outer face of the gap behind the beams
R_OUT = R_P + SIDE_WALL
R_TUBE = R_HEAD + TUBE_WALL
C0 = SLOT_R + SLOT_H               # the ring's 45 degree ceiling is the cone r + z = C0
SQ2 = math.sqrt(2)
Z_TOP = HEAD_LEN + R_TUBE           # top of the dome: a half sphere on the tube
Q = 128                            # circle segments for 2D shapes

assert R_LAND >= FIN_R + 0.05, "fin tips must rest on the wall beside the catches"
assert SLOT_R >= CAR_FIN_R + 0.3, "ring must clear the fin tips"
assert FIN_R_MIN - CATCH_R >= 0.3, "catch must grip the shortest fins"
assert CAR_FIN_R - CATCH_R < BEAM_GAP - 0.1, "beam needs room to bend out of the way"
assert STOP_IN >= R_HEAD + 0.05, "stop block must clear the head bore"
assert KEY_R >= CAR_FIN_R + 0.2, "openings must pass any fin that fits a car"
assert Z_TOP - (HEAD_LEN + R_HEAD - 0.5) >= TUBE_WALL, "dome must cover the inner cone's tip"


# ---- Shapes ------------------------------------------------------------------------
# Each flat shape is a region: a list of terms that all hold at once.
#   ("hp", nx, ny, d)  points p with p . (nx, ny) >= d
#   ("in", r) / ("out", r)  inside / outside the circle of radius r
#   ("poly", points)  inside a polygon
# region_2d() makes it a shapely polygon (for the checks), region_3d() a CadQuery
# prism with true circles and straight edges (for the model). Both come from
# the same terms, so the checks test the shapes the model is made of.
# Seen from the glass end: x right, y up.

def _half_plane(nx, ny, d, big=60):
    """Points p with p . (nx, ny) >= d, clipped to a large square."""
    tx, ty = -ny, nx
    p0 = (nx * d, ny * d)
    return Polygon([(p0[0] - tx * big, p0[1] - ty * big), (p0[0] + tx * big, p0[1] + ty * big),
                    (p0[0] + tx * big + nx * big, p0[1] + ty * big + ny * big),
                    (p0[0] - tx * big + nx * big, p0[1] - ty * big + ny * big)])


def disc(r):
    return Point(0, 0).buffer(r, quad_segs=Q // 4)


C30, S30 = math.cos(math.radians(30)), math.sin(math.radians(30))


def narrow_terms(lower, r8=FIN_R, b=FIN_B, b1=FIN_B1, c=0.0):
    """A narrow fin with the nose under it, grown by c: lower is the one near -63 degrees.

    One edge is the straight line x = b; the other is b1 from the line through
    the centre at 60 degrees to the y axis."""
    s = 1 if lower else -1
    return [("hp", -1, 0, -(b + c)), ("hp", 0, -s, -c), ("hp", C30, s * S30, -(b1 + c)), ("in", r8 + c)]


def wide_terms(below, above, r8=FIN_R, c=0.0):
    return [("hp", -1, 0, -c), ("hp", 0, 1, -(below + c)), ("hp", 0, -1, -(above + c)), ("in", r8 + c)]


def region_2d(terms):
    shape = disc(40)
    for t in terms:
        if t[0] == "hp":
            shape = shape.intersection(_half_plane(*t[1:]))
        elif t[0] == "in":
            shape = shape.intersection(disc(t[1]))
        elif t[0] == "out":
            shape = shape.difference(disc(t[1]))
        else:
            shape = shape.intersection(Polygon(t[1]))
    return shape


def regions_2d(regions):
    return unary_union([region_2d(r) for r in regions])


def narrow_fin(lower, r8=FIN_R, b=FIN_B, b1=FIN_B1):
    return region_2d(narrow_terms(lower, r8, b, b1))


def wide_fin(below, above, r8=FIN_R):
    return region_2d(wide_terms(below, above, r8))


def cap(below, above, r8=FIN_R, b=FIN_B, b1=FIN_B1):
    """Nose and three fins of one bulb type, at the twist-in position."""
    return unary_union([disc(NOSE_D / 2), wide_fin(below, above, r8),
                        narrow_fin(True, r8, b, b1), narrow_fin(False, r8, b, b1)])


def keyhole_regions():
    """Nose hole plus openings that pass every bulb type's fins, KEY_CLEAR all round."""
    widest = max(max(lo, hi) for lo, hi in WIDE.values())
    clip = ("in", KEY_R)
    return [[("in", R_HOLE)],
            wide_terms(widest, widest, c=KEY_CLEAR)[:-1] + [clip],
            narrow_terms(True, c=KEY_CLEAR)[:-1] + [clip],
            narrow_terms(False, c=KEY_CLEAR)[:-1] + [clip]]


def keyhole():
    return regions_2d(keyhole_regions())


def rot(shape, deg):
    return affinity.rotate(shape, deg, origin=(0, 0))


def stop_terms():
    """Between the upper narrow-fin opening and where the lower narrow fin ends up.

    The lower narrow fin's leading edge is its straight edge x = FIN_B; after
    the twist it lies on p . u = FIN_B. The upper narrow fin's straight edge
    faces the other side of the block before the twist, so the bulb cannot
    turn the wrong way."""
    t = math.radians(TWIST_DEG)
    return [("hp", math.cos(t), math.sin(t), FIN_B + STOP_CLEAR), ("hp", 1, 0, FIN_B + KEY_CLEAR),
            ("in", R_LAND - 0.05), ("out", STOP_IN)]


def stop_block():
    return region_2d(stop_terms())


def polar(r, deg):
    a = math.radians(deg)
    return (r * math.cos(a), r * math.sin(a))


def bump_points(at):
    """The catch bump, its catching edge's top at angle `at` (degrees)."""
    h = SLOT_R - CATCH_R
    deg = 180 / (math.pi * SLOT_R)                      # degrees per mm along the ring wall
    entry, retain = h / math.tan(math.radians(BUMP_ENTRY)), h / math.tan(math.radians(BUMP_RETAIN))
    s0, s1 = -(BUMP_FLAT + entry), retain              # mm along the wall, from `at`
    return [polar(SLOT_R + 0.3, at + s0 * deg), polar(SLOT_R, at + s0 * deg),
            polar(CATCH_R, at - BUMP_FLAT * deg), polar(CATCH_R, at),
            polar(SLOT_R, at + s1 * deg), polar(SLOT_R + 0.3, at + s1 * deg)]


def bump(at):
    return Polygon(bump_points(at))


def locked_fins():
    """The two narrow fins, turned to where they lock (largest sizes)."""
    return rot(narrow_fin(False), TWIST_DEG), rot(narrow_fin(True), TWIST_DEG)


def place_bump(fin):
    """Angle that puts a bump CATCH_CLEAR behind a locked fin's trailing edge."""
    c = fin.centroid
    mid = math.degrees(math.atan2(c.y, c.x))
    lo, hi = mid - 90.0, mid                            # well behind the fin .. inside it
    for _ in range(60):
        at = (lo + hi) / 2
        if bump(at).distance(fin) > CATCH_CLEAR:
            lo = at
        else:
            hi = at
    return lo


def sector_terms(r0, r1, a0, a1):
    """Ring from r0 to r1, between angles a0 and a1 (less than 180 apart)."""
    t0, t1 = math.radians(a0), math.radians(a1)
    return [("out", r0), ("in", r1), ("hp", -math.sin(t0), math.cos(t0), 0), ("hp", math.sin(t1), -math.cos(t1), 0)]


def catches():
    """For each catch: (pocket regions to cut, beam regions to add back)."""
    out = []
    deg = 180 / (math.pi * SLOT_R)
    for fin in locked_fins():
        at = place_bump(fin)
        a_free = at - (BUMP_FLAT + (SLOT_R - CATCH_R) / math.tan(math.radians(BUMP_ENTRY))) * deg
        a_root = a_free + BEAM_ARC
        b = bump(at)
        notch = b.buffer(GAP, join_style="bevel")
        pocket = [sector_terms(R_LAND, R_P, a_free - GAP * deg, a_root),
                  [("poly", list(notch.exterior.coords)[:-1])]]
        beam = [sector_terms(SLOT_R, SLOT_R + BEAM_T, a_free, a_root + 1.0),
                [("poly", bump_points(at))]]
        out.append((pocket, beam))
    return out


# ---- 3D ---------------------------------------------------------------------------------

def revolve(points):
    """Revolve an (r, z) outline about the z axis."""
    return cq.Workplane("XZ").polyline(points).close().revolve(360, (0, 0, 0), (0, 1, 0))


def prism(poly, z0, z1):
    pts = [tuple(p) for p in (poly.exterior.coords[:-1] if hasattr(poly, "exterior") else poly)]
    return cq.Workplane("XY").workplane(offset=z0).polyline(pts).close().extrude(z1 - z0)


def cylinder(r, z0, z1):
    return cq.Workplane("XY").workplane(offset=z0).circle(r).extrude(z1 - z0)


def region_3d(terms, z0, z1):
    shape = cylinder(40, z0, z1)
    for t in terms:
        if t[0] == "hp":
            shape = shape.intersect(prism(_half_plane(*t[1:]), z0 - 1, z1 + 1))
        elif t[0] == "in":
            shape = shape.intersect(cylinder(t[1], z0 - 1, z1 + 1))
        elif t[0] == "out":
            shape = shape.cut(cylinder(t[1], z0 - 1, z1 + 1))
        else:
            shape = shape.intersect(prism(t[1], z0 - 1, z1 + 1))
    return shape


def union_3d(regions, z0, z1):
    shape = region_3d(regions[0], z0, z1)
    for r in regions[1:]:
        shape = shape.union(region_3d(r, z0, z1))
    return shape


def below_cone(c, r_max=R_OUT + 2):
    """Everything with r + z <= c (and above the bed)."""
    z0 = -WALL - 2
    return revolve([(0, z0), (r_max, z0), (r_max, c - r_max), (0, c)])


def outer_shell():
    """Wide base round the ring, 45 degree shoulder, tube, round dome on the end.

    Inside, the closed end is a 45 degree cone (see holder()): a dome's inside
    would be too flat near the top to print without support."""
    c_sh = C0 + SIDE_WALL * SQ2         # shoulder: SIDE_WALL from the ring's ceiling cone
    a, top = math.radians(45), math.radians(88)   # stop just short of the pole: no point at the top
    return (cq.Workplane("XZ")
            .polyline([(0, -WALL), (R_OUT - BASE_CHAMFER, -WALL), (R_OUT, -WALL + BASE_CHAMFER),
                       (R_OUT, c_sh - R_OUT), (R_TUBE, c_sh - R_TUBE), (R_TUBE, HEAD_LEN)])
            .threePointArc((R_TUBE * math.cos(a), HEAD_LEN + R_TUBE * math.sin(a)),
                           (R_TUBE * math.cos(top), HEAD_LEN + R_TUBE * math.sin(top)))
            .lineTo(0, HEAD_LEN + R_TUBE * math.sin(top))
            .close().revolve(360, (0, 0, 0), (0, 1, 0)))


def holder():
    cavity = revolve([
        (0, 0), (SLOT_R, 0), (SLOT_R, SLOT_H), (R_HEAD, C0 - R_HEAD),
        (R_HEAD, HEAD_LEN), (0.5, HEAD_LEN + R_HEAD - 0.5), (0, HEAD_LEN + R_HEAD - 0.5),  # no point at the tip
    ])
    body = outer_shell().cut(cavity).cut(union_3d(keyhole_regions(), -WALL - 1, 0.01))
    for pocket, beam in catches():
        # the pocket's ceiling sits 0.2 above the ring's, so the two cones never coincide
        body = body.cut(union_3d(pocket, -WALL - 1, C0).intersect(below_cone(C0 + 0.2)))
        body = body.union(union_3d(beam, -WALL, C0).intersect(below_cone(C0 - GAP * SQ2)))
    body = body.union(region_3d(stop_terms(), -0.5, C0).intersect(below_cone(C0 + 0.5)))
    if TWIST == "ccw":
        body = body.mirror("XZ")
    return body


def to_print(body):
    # Open end on the bed.
    return body.translate((0, 0, WALL))


def fit_test(body, keep=SLOT_H + 3.0):
    """Wall, ring, stop and catches only, to check the twist quickly."""
    cutter = cq.Workplane("XY").box(200, 200, 200, centered=(True, True, False)).translate((0, 0, keep))
    return body.cut(cutter)


def export(shape, stem, out):
    cq.exporters.export(shape, str(out / f"{stem}.step"))
    cq.exporters.export(shape, str(out / f"{stem}.stl"), tolerance=0.01, angularTolerance=0.1)


if __name__ == "__main__":
    out = Path(__file__).resolve().parent
    body = holder()
    export(to_print(body), "h11_holder", out)
    export(to_print(fit_test(body)), "h11_fit_test", out)
    print(f"base Ø{2 * R_OUT:.1f}, tube Ø{2 * R_TUBE:.1f}, height {Z_TOP + WALL:.1f} mm; "
          f"twist {TWIST_DEG:g} degrees {TWIST} seen from the plug")
