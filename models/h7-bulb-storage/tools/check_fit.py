"""Fit checks for the cover and clip: the pass/fail test suite.

Builds the cover, the clips and mock bulbs from h7_led_cover.py and checks how
they meet. Each check prints PASS or FAIL with its numbers; the script exits 1
if any check fails. Sections are lettered; name some to run only those.

usage: check_fit.py [SECTION ...]   e.g. check_fit.py H J   (default: all)
"""
import importlib.util, math, sys
sys.dont_write_bytecode = True
import cadquery as cq

SRC = str(__import__("pathlib").Path(__file__).resolve().parent.parent / "h7_led_cover.py")
spec = importlib.util.spec_from_file_location("h7", SRC)
h7 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h7)

EPS = 1e-3          # mm³; overlaps below this are touching faces, not collisions
lo, hi = 0.5, 1.0   # the clip band the operator's bulb takes (v2; its plate is 0.85 mm)
FAILED = []
SECTIONS = {}


def check(label, ok, detail=""):
    print(f"  {'PASS' if ok else 'FAIL'}  {label}: {detail}")
    if not ok:
        FAILED.append(label)


def section(letter, title):
    def register(fn):
        SECTIONS[letter] = (title, fn)
        return fn
    return register


def vol(w):
    return sum(s.Volume() for s in w.solids().vals()) if w.solids().size() else 0.0


def bb(w):
    b = w.val().BoundingBox()
    return b


def fmt(b):
    return f"x[{b.xmin:.2f},{b.xmax:.2f}] y[{b.ymin:.2f},{b.ymax:.2f}] z[{b.zmin:.2f},{b.zmax:.2f}]"


def cyl(r, z0, z1):
    return cq.Workplane("XY").circle(r).extrude(z1 - z0).translate((0, 0, z0))


def flange(t=1.0, d=h7.FLANGE_D, tab=h7.TAB_W, q=h7.FLAT_Q):
    """Circle with a tab at +x; one flat square to the tab, q from the centre."""
    r = d / 2
    f = cyl(r, -t, 0)
    for side in (-1, 1):
        ys = sorted((side * tab / 2, side * (r + 1)))
        f = f.cut(h7.box(q, r + 1, ys[0], ys[1], -t - 1, 1))
    return f


def bulb(ang=0.0, dx=0.0, dy=0.0, **kw):
    b = flange(**kw).union(cyl(12.5, -3.5, -1.0)).union(cyl(19, -40, -6.0))
    b = b.union(cyl(12.0, 0, 3)).union(cyl(8, 3, 40))
    return b.rotate((0, 0, 0), (0, 0, 1), ang).translate((dx, dy, 0))


FLANGES = {"PX26d max (34.0, 8.0, 13.7)": dict(d=34.0, tab=8.0, q=13.7),
           "PX26d min (33.8, 7.9, 13.2)": dict(d=33.8, tab=7.9, q=13.2),
           "operator (33.3, 7.7, 12.84)": dict(d=33.3, tab=7.7, q=12.84)}

# Longest lamp the H7 standard allows: UNECE R37 sheet H7/1, at most 44.0 mm in
# front of the reference plane. The tube promises SPARE beyond that.
R37_LEN = 44.0
SPARE = 10.0


def max_lamp(length):
    """The H7/1 maximum lamp outline in front of the seat, cut off at length."""
    return cyl(12.5, 0, 4.1).union(cyl(9.5, 4.1, length))


body = None  # the cover, built once in main()


@section("A", "latched clip vs cover")
def latched():
    for v in h7.CLIP_VARIANTS:
        o = vol(h7.clip(*v).intersect(body))
        check(f"clip {v[0]}-{v[1]} latched", o < EPS, f"overlap {o:.4f}")


def sweep(make, label):
    """Insert a rigid clip; overlaps are legal only where a barb drags on a tunnel's outer wall.
    The arms are pressed straight (spread 0): the tunnels hold them so while they slide,
    and the tips are pinched slightly to start them in."""
    worst, bad = 0.0, []
    for s in [-62 + 0.5 * k for k in range(125)]:
        i = make(s).intersect(body)
        for sol in i.solids().vals():
            b = sol.BoundingBox()
            barb_only = (b.ymin >= h7.Y_GATE - 0.02 or b.ymax <= -h7.Y_GATE + 0.02) and b.zmax <= -h7.L + h7.ARM_T + 0.01
            depth = max(abs(b.ymin), abs(b.ymax)) - h7.Y_GATE
            if barb_only:
                worst = max(worst, depth)
            else:
                bad.append((s, round(sol.Volume(), 4), fmt(b)))
    room = h7.Y0 - h7.Y_SQ
    check(f"{label}: only the barbs drag", not bad, f"other overlaps {len(bad)}")
    for x in bad[:12]:
        print("      ", x)
    check(f"{label}: arms have room to squeeze the barbs through", worst <= room - 0.1,
          f"barb drag depth {worst:.2f} mm, room {room:.2f} mm")


@section("B", "insertion from -x (rigid clip)")
def insert_minus_x():
    sweep(lambda s: h7.clip(lo, hi, s, spread=0.0), "from -x")


@section("C", "insertion from +x (rigid clip)")
def insert_plus_x():
    sweep(lambda s: h7.clip(lo, hi, spread=0.0).rotate((0, 0, 0), (0, 0, 1), 180).translate((-s, 0, 0)),
          "from +x")


@section("D", "release: tips squeezed, clip pushed back")
def release():
    """Squeeze the tips until the barbs clear the collar, then push the clip back: the
    squeezed arms must fit the tunnels. Measured on arms pressed straight (spread 0),
    as the tunnels hold them once the barbs are inside."""
    d = h7.BARB - h7.CLEAR + 0.15  # just past what clears the barbs
    room = h7.Y0 - h7.Y_SQ
    check("squeeze fits the tunnels", d <= room, f"squeeze {d:.2f} mm per tip, room {room:.2f} mm")

    def squeezed(shift, x_cut=5.0):
        cl = h7.clip(lo, hi, shift, spread=0.0)
        outer = cl.intersect(h7.box(x_cut + shift, 80, -40, 40, -20, 20))
        inner = cl.cut(h7.box(x_cut + shift, 80, -40, 40, -20, 20))
        up = outer.intersect(h7.box(-80, 80, 0, 40, -20, 20)).translate((0, -d, 0))
        dn = outer.intersect(h7.box(-80, 80, -40, 0, -20, 20)).translate((0, d, 0))
        return inner.union(up).union(dn)
    for s in (0, -1, -2, -4, -6, -8):
        o = vol(squeezed(s).intersect(body))
        check(f"squeezed, pushed back {-s} mm", o < EPS, f"overlap {o:.4f}")


@section("E", "tab key against PX26d limits and the operator's bulb")
def key_seat():
    for name, kw in FLANGES.items():
        seated = vol(bulb(**kw).intersect(body))
        free = 0.0
        for a_ in [0.25 * k for k in range(1, 17)]:
            if vol(bulb(ang=a_, **kw).intersect(body)) > EPS or vol(bulb(ang=-a_, **kw).intersect(body)) > EPS:
                break
            free = a_
        check(f"{name} seats", seated < EPS, f"overlap {seated:.4f}")
        check(f"{name} turns 2 deg at most", free <= 2.0, f"turns freely to ±{free:.2f} deg")
        # Information only: the bore leaves 0.5 mm round the largest flange.
        shift = max(vol(bulb(dx=dx, **kw).intersect(body)) for dx in (-0.45, 0.45))
        print(f"        (x-shift ±0.45 overlap {shift:.4f})")
    o = vol(bulb(ang=180).intersect(body))
    check("PX26d max turned 180 deg collides", o > 1.0, f"overlap {o:.4f}")


@section("F", "flange squeeze per clip band (bump contact only)")
def squeeze():
    for lo_, hi_ in h7.CLIP_VARIANTS:
        for t in (lo_, hi_):
            z = t + h7.PLATE_SETBACK  # the back of the plate, behind the seat
            fl = flange(z).union(cyl(12, -z - 4.2, -z))
            i = h7.clip(lo_, hi_).intersect(fl)
            if vol(i) > 1e-6:
                b = bb(i)
                sq = b.zmax - b.zmin
                check(f"{lo_}-{hi_} on a {t} mm plate", 0.05 <= sq <= 0.65,
                      f"squeeze {sq:.2f} at x[{b.xmin:.1f},{b.xmax:.1f}]")
            else:
                check(f"{lo_}-{hi_} on a {t} mm plate", False, "no contact")


@section("G", "heatsink and LED body")
def bodies():
    t = 2.0
    led = flange(t).union(cyl(12, -t - 4, -t)).union(cyl(19, -t - 34, -t - 4)).union(cyl(8, 0, 40))
    o = vol(body.intersect(led))
    check("Ø38 heatsink 4 mm behind a 2 mm flange clears the cover", o < EPS, f"overlap {o:.4f}")
    o = vol(h7.clip(lo, hi).translate((0, 0, -0.6)).intersect(led.cut(flange(t))))
    check("clip flexed 0.6 mm back clears the LED body", o < EPS, f"overlap {o:.4f}")
    # What README promises may sit right behind the flange beside the tab.
    t = 1.0
    o = vol(body.intersect(flange(t).union(cyl(14.5, -6.0, -t))))
    check("a Ø29 body right behind a 1 mm flange clears the keys", o < EPS, f"overlap {o:.4f}")



@section("H", "latch: how deep the barbs catch on the collar face")
def latch_catch():
    """Pull the latched clip back past the barbs' lean; the barbs then overlap the
    collar face by their full catch. 0.3 caught 1.2 mm and pulled out too easily;
    0.4 caught 1.7; v1 1.9. In v2 the far tunnel holds each spread arm with its edge
    on the tunnel wall, so the barb catches its full 2.2 mm. The 0.01 tolerance
    absorbs rounding in the intersection."""
    i = h7.clip(lo, hi).translate((-1.5, 0, 0)).intersect(body)
    catches, other = [], 0
    for sol in i.solids().vals():
        b = sol.BoundingBox()
        if min(abs(b.ymin), abs(b.ymax)) >= h7.Y_GATE - 0.02:
            catches.append(b.ymax - b.ymin)
        else:
            other += 1
    check("only the barbs meet the collar face", len(catches) == 2 and not other,
          f"barbs {len(catches)}, other overlaps {other}")
    check("each barb catches at least 2.2 mm", catches and min(catches) >= 2.2 - 0.01,
          "catch " + ", ".join(f"{c:.2f}" for c in catches) + " mm")


@section("I", "tab held when the bulb lifts; the bulb goes in through the back")
def tab_held():
    """Rocking the bulb while the clip goes in lifts the flange off the seat. With
    a 1 mm flange lifted 3 mm, the tab must still sit between the key blocks: free
    at 0 degrees, colliding at ±3. And the flange must pass the back of the collar
    on its way to the seat (nothing may sit inside the bore)."""
    for name, kw in FLANGES.items():
        lifted = flange(1.0, **kw).translate((0, 0, -3.0))
        free = vol(lifted.intersect(body))
        turned = min(vol(lifted.rotate((0, 0, 0), (0, 0, 1), a).intersect(body)) for a in (-3, 3))
        check(f"{name} lifted 3 mm sits free", free < EPS, f"overlap {free:.4f}")
        check(f"{name} lifted 3 mm cannot turn 3 deg", turned > EPS, f"overlap at ±3 deg {turned:.4f}")
    path = max(vol(flange(1.0).translate((0, 0, -0.5 * k)).intersect(body)) for k in range(16))
    check("PX26d max passes the back of the collar to the seat", path < EPS, f"worst overlap {path:.4f}")


@section("J", "tab finds its pocket when the bulb is 2 degrees off")
def tab_lead_in():
    """With the flange's front face 0.5 mm below the key tops and the bulb turned
    2 degrees, the slope on the key tops leaves room: no overlap."""
    for name, kw in FLANGES.items():
        f = flange(1.0, **kw).translate((0, 0, -(h7.KEY_DEPTH - 0.5)))
        o = max(vol(f.rotate((0, 0, 0), (0, 0, 1), a).intersect(body)) for a in (-2, 2))
        check(f"{name} 2 deg off enters the pocket", o < EPS, f"overlap {o:.4f}")


@section("K", "longest standard bulb fits the tube, with 10 mm to spare")
def head_length():
    """A lamp at the R37 H7/1 maximum outline (Ø25.0 for 4.1 mm, then Ø19.0 to
    44.0 mm) must fit, and so must the same outline SPARE longer: README promises
    heads up to 54 mm long. This reads only the cover's solid, so anything that
    shortens the usable tube (closed end, wall, taper) turns it red."""
    for length, label in ((R37_LEN, "standard maximum"), (R37_LEN + SPARE, f"{SPARE:.0f} mm longer")):
        o = vol(max_lamp(length).intersect(body))
        check(f"lamp {length:.0f} mm long ({label}) fits", o < EPS, f"overlap {o:.4f}")


@section("L", "as printed, the arms press the barbs out")
def preload():
    """The clip is printed with its arms spread ARM_SPREAD; latched, the far tunnel
    pushes each arm back, so it presses its barb out. Overlaps of the as-printed clip
    with the cover are classed: on each far tunnel's outer wall, exactly one, 0.7-0.9
    mm deep (the preload); the bump's top corner against the bore wall, which only
    the rigid printed pose shows (A shows the held clip clear): printed, not checked;
    anything else fails."""
    for lo_, hi_ in h7.CLIP_VARIANTS:
        bump = h7.bump_height(lo_, hi_)
        bump_half = h7.BUMP_FLAT / 2 + bump / math.tan(math.radians(30))
        far, corner, other = {1: [], -1: []}, [], []
        for sol in h7.printed_clip(lo_, hi_).intersect(body).solids().vals():
            b = sol.BoundingBox()
            side = 1 if b.ymin > 0 else -1 if b.ymax < 0 else 0
            depth = max(abs(b.ymin), abs(b.ymax)) - h7.Y_GATE
            if side and b.xmin >= 14 and min(abs(b.ymin), abs(b.ymax)) >= h7.Y_GATE - 0.02:
                far[side].append(depth)
            elif b.zmin >= h7.Z_ARM - 0.01 and max(abs(b.xmin), abs(b.xmax)) <= bump_half:
                corner.append(depth)
            else:
                other.append(fmt(b))
        ok = all(len(far[s_]) == 1 and 0.7 <= far[s_][0] <= 0.9 for s_ in (1, -1))
        got = ", ".join(f"{d:.3f}" for s_ in (1, -1) for d in far[s_]) or "none"
        check(f"clip {lo_}-{hi_}: each arm presses its far tunnel wall 0.7-0.9 mm", ok, f"preload {got} mm")
        check(f"clip {lo_}-{hi_}: nothing else overlaps", not other, f"other {other}")
        print(f"        (bump corner, rigid printed pose only: {max(corner, default=0):.2f} mm)")


def main(argv):
    global body
    wanted = [a.upper() for a in argv] or sorted(SECTIONS)
    unknown = [w for w in wanted if w not in SECTIONS]
    if unknown:
        sys.exit(f"unknown section(s) {' '.join(unknown)}; have {' '.join(sorted(SECTIONS))}")
    body = h7.cover()
    for letter in wanted:
        title, fn = SECTIONS[letter]
        print(f"== {letter}. {title}")
        fn()
    print(f"\n{len(FAILED)} check(s) failed" + (": " + "; ".join(FAILED) if FAILED else ""))
    return 1 if FAILED else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
