"""Slide-on TPU grips for the Commercial Electric wire stripper's bare steel handles.

A grip is a closed tube that slides onto the bare steel from its tip A to B,
where the old grip's open end sat. The inside follows the steel's measured
centre line and taper (`steel.py`). The outside is a new design shared by both
grips: the steel's own outline grown by a set wall on each side, with rounded
corners, flared a little at the open end with its edge rounded, and domed at the
closed end.

Inside: the bore is the steel plus BORE_CLEAR on every side, with tight
corners so even a sharp steel corner clears it. Eight lengthwise ribs, two
on each face near the corners, reach RIB_BITE past the steel's face. They
locate the grip on the steel. The valleys between them, BORE_CLEAR deep, give
glue something to fill and key into, and they stay there if the outside is
vapor-smoothed. Glue and air escape along the valleys when you push the grip
on. The ribs are glue keys, not crush ribs: test prints decide whether the grip
also holds dry.

The bore's closed end is a gable roof. Its ridge is placed so that both slopes
are ROOF_ANGLE above horizontal when the grip stands on its open end, whichever
way the tip leans. The outside's dome starts at the ridge's height, so the wall
over the roof is never thinner than the body's.

Print: standing on the open end, closed end up. Its lean follows the steel's
curve (about 15 degrees at the tip). The flare is widest a little above the
bed. Below that, a bevel at BEVEL_ANGLE brings its edge in toward the bed, and a
round blends the bevel into the flare, so the edge is neither sharp nor
overhanging. The dome and roof face up, so no supports are needed.

Coordinates are those of `steel.py` (use position: the handle flat in XY, T
along Z, s along the centre line from A). Each cross-section is in the plane
square to the centre line: u along the W direction, v along T.

Run:  python grips.py   (needs cadquery)
Writes STEP (opens in CAD) and STL (for the slicer) for the curved grip and its
fit test, already standing on the open end, and prints the main sizes.
"""

import math
from pathlib import Path

import cadquery as cq

import steel

# ---- Bore (creative-bore-fit-and-glue-key; ribs as glue keys) --------------
BORE_CLEAR = 0.3     # steel face to bore wall, each side
BORE_CORNER_R = 0.5  # bore corner radius; a sharp steel corner clears it by >= 0.15
RIB_BITE = 0.1       # how far a rib tip reaches past the steel face
RIB_BASE = 1.2       # rib width at the wall
RIB_TIP = 0.5        # rib width at its tip
RIB_INSET = 1.5      # rib centre line from the steel's corner
RIB_EMBED = 0.05     # rib roots sink this far into the wall, so they fuse
END_CLEAR = 1.0      # the bore runs this far past A
ROOF_ANGLE = 50.0    # both roof slopes, degrees above horizontal in print
RIDGE_W = 0.2        # the roof's ridge is a strip this wide

# ---- Outside (creative-outside-shape) --------------------------------------
WALL_SIDE = 3.8      # steel face to outside, in the plane of the handles
WALL_FACE = 2.5      # steel face to outside, across that plane
CORNER_R = 4.8       # outside corner radius (>= 2 mm over each bore corner)
FLARE = 2.3          # extra wall each side at the open end ...
FLARE_LEN = 8.0      # ... fading out over this length
BEVEL = 1.8          # the open end's edge on the bed comes in this far from the flare's full width
BEVEL_ANGLE = 50.0   # the bevel up from the bed, degrees above horizontal in print
RIM_R = 0.8          # radius of the round between the bevel and the flare
DOME_LEN = 5.0       # the dome's length, and how far it shrinks each side
END = 3.0            # thinnest cap over the roof's ridge

# ---- Build -----------------------------------------------------------------
SECTION_STEP = 4.0   # longest gap between lofted cross-sections
RIM_STEP = 3.0       # degrees the outline turns between the open end's lofted sections
FIT_LEN = 15.0       # the fit test is the grip's first FIT_LEN mm from the open end

# ---- Tool shut -------------------------------------------------------------
# The operator's reading of 2026-11-01: with the tool squeezed shut and an
# iteration-4 curved grip (87e777c) on each handle, the two open ends were
# SHUT_GAP apart. Those grips' wall at the widest point, on the side facing the
# other handle, was SHUT_WALL from the steel face. Both describe the grips that
# were measured, so they stay as they are when WALL_SIDE or the open end changes.
SHUT_GAP = 3.3
SHUT_WALL = 4.274    # iteration 4: WALL_SIDE 3.8 + its widest point's 0.474
MIN_SHUT_GAP = 0.8   # least gap to leave; the operator called 0.3 "pushing it"


def V(p):
    return cq.Vector(*p)


def section_plane(h, s):
    """Plane square to the centre line at s; x along W, normal toward B."""
    return cq.Plane(origin=h.point(s), xDir=h.normal(s), normal=h.tangent(s))


def rrect(plane, w, t, r, du=0.0):
    """Rounded rectangle w (along x) by t, centred du along x from the plane's origin."""
    r = min(r, 0.45 * min(w, t))
    wire = cq.Workplane(plane).center(du, 0).rect(w, t).val()
    return wire.fillet2D(r, wire.Vertices())


def loft_positions(start, stop, step=SECTION_STEP):
    """Evenly spaced s values from start to stop, inclusive, no gap over step."""
    n = max(1, math.ceil(abs(stop - start) / step))
    return [start + (stop - start) * k / n for k in range(n + 1)]


def steel_solid(h):
    """Mock bare steel from A to B: sharp W x T rectangles along the centre line."""
    secs = [cq.Workplane(section_plane(h, s)).rect(h.width(s), h.thickness(s)).val()
            for s in loft_positions(h.length, 0.0)]
    return cq.Solid.makeLoft(secs)


def roof(h):
    """The bore's roof: its ridge centre R and its axial height past the bore's end.

    Worked in the plane of the handles, in print orientation (up is away from B
    along B's tangent): the two roof slopes rise at ROOF_ANGLE from the ends of
    the bore's end section and meet at R.
    """
    p = V(h.point(-END_CLEAR))
    n, ta = V(h.normal(0)), V(h.tangent(0))
    up = -V(h.tangent(h.length))
    ex = (n - up * n.dot(up)).normalized()
    hw = h.width(0) / 2 + BORE_CLEAR
    ends = sorted(((p + n * k * hw - p).dot(ex), (p + n * k * hw - p).dot(up)) for k in (-1, 1))
    (x0, z0), (x1, z1) = ends
    k = math.tan(math.radians(ROOF_ANGLE))
    xr = (x0 + x1) / 2 + (z1 - z0) / (2 * k)
    r = p + ex * xr + up * (z0 + (xr - x0) * k)
    return r, (r - p).dot(-ta)


def bore(h):
    """The cavity: steel plus BORE_CLEAR from B to END_CLEAR past A, then the roof."""
    secs = [rrect(section_plane(h, s), h.width(s) + 2 * BORE_CLEAR,
                  h.thickness(s) + 2 * BORE_CLEAR, BORE_CORNER_R)
            for s in loft_positions(h.length, -END_CLEAR)]
    body = cq.Solid.makeLoft(secs)
    r, _ = roof(h)
    end = section_plane(h, -END_CLEAR)
    du = (r - end.origin).dot(end.xDir)
    ridge_plane = cq.Plane(origin=end.origin + end.zDir * (r - end.origin).dot(end.zDir),
                           xDir=end.xDir, normal=end.zDir)
    ridge = rrect(ridge_plane, RIDGE_W, h.thickness(0) + 2 * BORE_CLEAR, BORE_CORNER_R, du)
    cap = cq.Solid.makeLoft([secs[-1], ridge], ruled=True)
    return body.fuse(cap).clean()


def rib_wire(plane, u, v, du, dv, height):
    """Rib trapezoid rooted on the wall at (u, v); (du, dv) points into the bore."""
    pu, pv = -dv, du
    a, b = -RIB_EMBED, height
    pts = [(u + pu * RIB_BASE / 2 + du * a, v + pv * RIB_BASE / 2 + dv * a),
           (u - pu * RIB_BASE / 2 + du * a, v - pv * RIB_BASE / 2 + dv * a),
           (u - pu * RIB_TIP / 2 + du * b, v - pv * RIB_TIP / 2 + dv * b),
           (u + pu * RIB_TIP / 2 + du * b, v + pv * RIB_TIP / 2 + dv * b)]
    return cq.Wire.makePolygon([plane.toWorldCoords(q) for q in pts], close=True)


def ribs(h):
    """Eight lengthwise ribs from B to A, fading into the wall over END_CLEAR past A."""
    ss = loft_positions(h.length, 0.0) + [-END_CLEAR]
    out = []
    for side in (1, -1):
        for off in (1, -1):
            for on_face in (False, True):
                secs = []
                for s in ss:
                    w, t = h.width(s), h.thickness(s)
                    height = BORE_CLEAR + RIB_BITE if s >= 0 else 0.0
                    if on_face:   # on a T face (the faces with the holes)
                        args = (off * (w / 2 - RIB_INSET), side * (t / 2 + BORE_CLEAR), 0, -side)
                    else:         # on a W face
                        args = (side * (w / 2 + BORE_CLEAR), off * (t / 2 - RIB_INSET), -side, 0)
                    secs.append(rib_wire(section_plane(h, s), *args, height))
                # ruled: a smooth loft overshoots where the rib fades out
                out.append(cq.Solid.makeLoft(secs, ruled=True))
    return out


def flare(d):
    """Extra wall d from the open end, and its slope along d: FLARE at B, fading
    quadratically to 0 at FLARE_LEN. Kept together so the two cannot drift apart."""
    if d >= FLARE_LEN:
        return 0.0, 0.0
    k = 1 - d / FLARE_LEN
    return FLARE * k ** 2, -2 * FLARE / FLARE_LEN * k


def rim_profile():
    """The open end's outline: (d, grow) points from B (d = 0) to FLARE_LEN, d along
    the centre line toward A, grow past the body wall.

    The flare widens toward B. On the bed its edge sits BEVEL in from the
    flare's full width, and a straight bevel rises from there at BEVEL_ANGLE
    above horizontal (in print). A round of radius RIM_R, touching both the
    bevel and the flare, blends one into the other. Past the round, the flare
    runs on unchanged into the body.
    """
    r = RIM_R
    c = 1 / math.tan(math.radians(BEVEL_ANGLE))         # the bevel's grow per unit d
    foot = FLARE - BEVEL                                # the bevel's foot on the bed

    def centre(t):
        """Centre of the circle of radius r that touches the flare at d = t, inside it."""
        g, m = flare(t)
        q = math.hypot(1.0, m)
        return t + r * m / q, g - r / q

    def gap(t):
        """centre(t)'s depth inside the bevel's line, less r: 0 where its circle touches it."""
        cd, cg = centre(t)
        return (foot + c * cd - cg) / math.hypot(1.0, c) - r

    lo, hi = 0.0, FLARE_LEN        # the touch point whose circle also touches the bevel
    for _ in range(60):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if gap(mid) < 0 else (lo, mid)
    t = (lo + hi) / 2
    cd, cg = centre(t)
    m = flare(t)[1]
    start = 180.0 - BEVEL_ANGLE                         # the round leaves the bevel here
    stop = math.degrees(math.atan2(1.0, -m))            # and touches the flare here
    pts = [(0.0, foot)]
    n = max(1, math.ceil((start - stop) / RIM_STEP))
    for k in range(n + 1):
        phi = math.radians(start + (stop - start) * k / n)
        pts.append((cd + r * math.cos(phi), cg + r * math.sin(phi)))
    n = max(1, math.ceil(math.degrees(math.atan(-m)) / RIM_STEP))
    for k in range(1, n + 1):                           # the rest of the flare
        d = t + (FLARE_LEN - t) * k / n
        pts.append((d, flare(d)[0]))
    return pts


def widest():
    """The open end's widest point: (d from B, grow past the body wall)."""
    return max(rim_profile(), key=lambda p: p[1])


def shut_gap():
    """Gap left between the two grips' open ends with the tool shut, for the pair
    built here: the curved grip on the curved handle, the straight grip on the
    straight handle.

    From the measured SHUT_GAP, each grip's wall at the widest point moves out by
    its change from SHUT_WALL. One more term: the measured grip on the straight
    handle was a curved grip, whose bore was built for the curved steel, which is
    narrower at B. Stretched over the wider straight steel, its wall moved out by
    at most half the difference. The straight grip, built for its own steel, sits
    a full half-difference out. Counting that half-difference in full is the worst
    case.
    """
    _, most = widest()
    c, st = steel.CURVED, steel.STRAIGHT
    extra = max(0.0, (st.width(st.length) - c.width(c.length)) / 2)
    return SHUT_GAP - 2 * (WALL_SIDE + most - SHUT_WALL) - extra


def outside(h):
    """Outside: steel + walls, flared at B, straight past A to the ridge, then a dome."""
    _, rise = roof(h)
    s_dome = -END_CLEAR - rise

    def sec(s, grow, corner_r):
        w = h.width(s) + 2 * (WALL_SIDE + grow)
        t = h.thickness(s) + 2 * (WALL_FACE + grow)
        return rrect(section_plane(h, s), w, t, corner_r)

    # The open end is a true offset of the body: its corners grow and shrink
    # with it, so the bevel keeps BEVEL_ANGLE at the corners as on the flats.
    # Ruled: a smooth loft would ring through the round.
    rim = cq.Solid.makeLoft([sec(h.length - d, g, CORNER_R + g) for d, g in rim_profile()],
                            ruled=True)
    secs = [sec(s, 0.0, CORNER_R) for s in loft_positions(h.length - FLARE_LEN, s_dome)]
    for deg in (20, 38, 54, 67, 78, 90):       # dome: quarter circle of radius DOME_LEN;
        phi = math.radians(deg)                 # rrect caps CORNER_R as it shrinks
        secs.append(sec(s_dome - DOME_LEN * math.sin(phi), -DOME_LEN * (1 - math.cos(phi)),
                        CORNER_R))
    return rim.fuse(cq.Solid.makeLoft(secs)).clean()


def grip(h):
    """The grip in use position: outside minus bore, plus ribs."""
    g = outside(h).cut(bore(h))
    for rb in ribs(h):
        g = g.fuse(rb)
    g = g.clean()
    assert g.isValid() and len(g.Solids()) == 1, "grip did not build as one valid solid"
    return g


def print_location(h):
    """Location that stands a use-position part on its open end: B at the origin,
    B's tangent pointing down, W along x, T along y."""
    plane = cq.Plane(origin=h.point(h.length), xDir=h.normal(h.length),
                     normal=-V(h.tangent(h.length)))
    return cq.Location(plane).inverse


def to_print(shape, h):
    return shape.moved(print_location(h))


def fit_test(printed):
    """The printed grip's first FIT_LEN mm: the open end alone, for a quick check."""
    bb = printed.BoundingBox()
    box = cq.Solid.makeBox(bb.xlen + 20, bb.ylen + 20, FIT_LEN,
                           cq.Vector(bb.xmin - 10, bb.ymin - 10, 0))
    return printed.intersect(box)


def export(shape, stem, out):
    cq.exporters.export(shape, str(out / f"{stem}.step"))
    cq.exporters.export(shape, str(out / f"{stem}.stl"), tolerance=0.01, angularTolerance=0.1)


def corner_wall(grow=0.0):
    """Material over each bore corner where the outside is offset grow past the body
    wall, its corner radius with it (as at the open end)."""
    c, r = BORE_CLEAR, BORE_CORNER_R
    rc = CORNER_R + grow
    gap_u = WALL_SIDE + grow - rc - (c - r)
    gap_v = WALL_FACE + grow - rc - (c - r)
    return rc - math.hypot(gap_u, gap_v) - r


def check_design(h):
    """Script assertions on the parameters; geometry checks belong to the test prints."""
    c, r = BORE_CLEAR, BORE_CORNER_R
    corner_gap = c if r <= c else r - math.sqrt(2) * (r - c)
    assert corner_gap >= 0.15, f"a sharp steel corner clears the bore by only {corner_gap:.2f}"
    wall = corner_wall()
    assert wall >= 2.0, f"only {wall:.2f} over the bore's corners"
    rim = rim_profile()
    assert all(q[0] > p[0] for p, q in zip(rim, rim[1:])), \
        "the bevel and its round do not fit between the bed and FLARE_LEN"
    shut = shut_gap()
    assert shut >= MIN_SHUT_GAP, f"tool shut, the two grips' open ends would come within {shut:.2f}"
    assert corner_wall(rim[0][1]) >= 1.2, \
        "the bevel leaves under three extrusion lines over the bore's corners on the bed"
    assert BEVEL_ANGLE >= 45, "the bevel would need support"
    assert h.width(0) / 2 + WALL_SIDE - DOME_LEN > 0.4, "the dome would shrink to nothing"
    assert DOME_LEN >= END, "the dome is too short to cap the roof"
    assert RIB_INSET - RIB_BASE / 2 > r - c, "ribs would sit in the bore's corners"
    return corner_gap, wall


def sizes(h, printed):
    gap, wall = check_design(h)
    verts, _ = printed.tessellate(0.01, 0.1)   # BoundingBox() is loose on lofted faces
    span = [max(getattr(v, a) for v in verts) - min(getattr(v, a) for v in verts) for a in "xyz"]
    L = h.length
    print(f"{h.name} grip: stands {span[2]:.1f} tall on its open end; leaning, it spans "
          f"{span[0]:.1f} x {span[1]:.1f}; volume {printed.Volume() / 1000:.1f} cm3")
    rim = rim_profile()
    d_most, most = widest()
    for name, s, grow in (("open end (B)", L, rim[0][1]), ("widest", L - d_most, most),
                          ("body near B", L - FLARE_LEN, 0.0), ("at A", 0.0, 0.0)):
        w, t = h.width(s), h.thickness(s)
        print(f"  {name:13s} steel {w:5.2f} x {t:5.2f}  bore {w + 2 * BORE_CLEAR:5.2f} x "
              f"{t + 2 * BORE_CLEAR:5.2f}  ribs {w - 2 * RIB_BITE:5.2f} x {t - 2 * RIB_BITE:5.2f}  "
              f"outside {w + 2 * (WALL_SIDE + grow):5.2f} x {t + 2 * (WALL_FACE + grow):5.2f}")
    _, rise = roof(h)
    print(f"  open end: edge on the bed {rim[0][1]:+.2f} from the body wall "
          f"({corner_wall(rim[0][1]):.2f} over the bore corners); bevel up to {rim[1][0]:.2f}, "
          f"then rounding to the widest, {most:.2f} out at {d_most:.2f} from B; "
          f"the flare meets the body {FLARE_LEN} from B")
    print(f"  wall at the widest, on the side facing the other handle: {WALL_SIDE + most:.2f}; "
          f"tool shut, the two grips' open ends come within {shut_gap():.2f} (at least {MIN_SHUT_GAP})")
    print(f"  steel corner clears the bore by {gap:.2f}; {wall:.2f} over each bore corner")
    print(f"  bore ends {END_CLEAR} past A, its roof rises {rise:.2f} more; dome {DOME_LEN} beyond that")


if __name__ == "__main__":
    out = Path(__file__).resolve().parent
    h = steel.CURVED
    check_design(h)
    printed = to_print(grip(h), h)
    export(printed, "curved_grip", out)
    export(fit_test(printed), "curved_grip_fit_test", out)
    sizes(h, printed)
