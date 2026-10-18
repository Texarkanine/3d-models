"""Fit checks for the H11 holder: the pass/fail test suite.

Builds the holder's keyhole, wall, ring, stop and catches from h11_holder.py
and moves each bulb type's cap (largest sizes) through them. Each check prints
PASS or FAIL with its numbers; the script exits 1 if any check fails.
Sections are lettered; name some to run only those.

usage: check_fit.py [SECTION ...]   e.g. check_fit.py B C   (default: all)
"""
import importlib.util
import math
import sys

sys.dont_write_bytecode = True
from shapely.ops import unary_union

SRC = str(__import__("pathlib").Path(__file__).resolve().parent.parent / "h11_holder.py")
spec = importlib.util.spec_from_file_location("h11", SRC)
h = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)
spec = importlib.util.spec_from_file_location("cc", SRC.replace("h11_holder.py", "h11_connector_cap.py"))
cc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cc)

EPS = 1e-3     # mm²; overlaps below this are touching edges, not collisions
FAILED = []
SECTIONS = {}

# The largest fins a car socket takes (IEC 60061-2 sheet 7005-110-3 minimums):
# a bulb that fits any car is no bigger than this.
CAR = dict(r8=12.4, b=8.1, b1=3.7)
CAR_WIDE = 6.1
# Halogen spring across the nose, relaxed (Z max), and the operator's LED.
SPRING_Z = 21.4
LED_SEAL_FACE, LED_PLATE = 1.38, 3.33
PLATE_MIN = 3.0           # cap E min: plate face behind the fins' back faces
PETG_E = 2000.0           # N/mm², a round figure for printed PETG
STRAIN_MAX = 0.025        # keep the beams' bending strain under this


def check(label, ok, detail=""):
    print(f"  {'PASS' if ok else 'FAIL'}  {label}: {detail}")
    if not ok:
        FAILED.append(label)


def section(letter, title):
    def register(fn):
        SECTIONS[letter] = (title, fn)
        return fn
    return register


KEYHOLE = h.keyhole()
CATCHES = h.catches()
POCKETS = unary_union([h.regions_2d(p) for p, _ in CATCHES])
BEAMS = unary_union([h.regions_2d(b) for _, b in CATCHES])
STOP = h.stop_block()
# The wall the fins rest on (z < 0), inside the ring.
LAND = h.disc(h.SLOT_R).difference(KEYHOLE).difference(POCKETS)
# Solid parts at fin height (0 < z < FIN_F).
RING = (h.disc(h.R_OUT).difference(h.disc(h.SLOT_R)).difference(POCKETS)).union(BEAMS).union(STOP)
BUMPS = unary_union([h.bump(h.place_bump(f)) for f in h.locked_fins()])


def fins(below, above, **kw):
    """One bulb type's three fins, without the nose."""
    return [h.wide_fin(below, above, kw.get("r8", h.FIN_R)).difference(h.disc(h.NOSE_D / 2)),
            h.narrow_fin(True, **kw).difference(h.disc(h.NOSE_D / 2)),
            h.narrow_fin(False, **kw).difference(h.disc(h.NOSE_D / 2))]


@section("A", "Every bulb type goes in")
def sec_a():
    for name, (lo, hi) in h.WIDE.items():
        cap = h.cap(lo, hi)
        miss = cap.difference(KEYHOLE).area
        snug = cap.buffer(h.KEY_CLEAR - 0.02).difference(KEYHOLE).area
        check(f"{name} through the openings", miss < EPS and snug < EPS,
              f"outside {miss:.4f} mm², within {h.KEY_CLEAR - 0.02:.2f} of an edge {snug:.4f} mm²")
    car = h.cap(CAR_WIDE, CAR_WIDE, **CAR)
    gap = 0.1
    snug = car.buffer(gap).difference(KEYHOLE).area
    check("largest fins any car takes", snug < EPS,
          f"r8 {CAR['r8']}, B {CAR['b']}, B1 {CAR['b1']}, wide ±{CAR_WIDE}: at least {gap} clear ({snug:.4f} mm² short)")
    check("nose and halogen spring", h.R_HOLE - h.NOSE_D / 2 >= 0.3,
          f"nose Ø{h.NOSE_D} in hole Ø{h.HOLE_D}; spring Ø{SPRING_Z} relaxed is pressed "
          f"{(SPRING_Z - h.HOLE_D) / 2:.2f} per side (a car presses 0.7-0.95)")


@section("B", "Locked: fins rest on the wall")
def sec_b():
    for name, (lo, hi) in h.WIDE.items():
        parts = []
        worst = 1.0
        for label, fin in zip(("wide", "narrow -63", "narrow +63"), fins(lo, hi)):
            fin = fin.difference(h.disc(h.R_HOLE))
            turned = h.rot(fin, h.TWIST_DEG)
            share = turned.intersection(LAND).area / turned.area
            worst = min(worst, share)
            parts.append(f"{label} {share:.0%}")
        check(f"{name} fins on the wall", worst >= 0.7, ", ".join(parts) + " of each fin outside the hole")


@section("C", "Twist path")
def sec_c():
    steps = [i * 0.25 for i in range(int(h.TWIST_DEG / 0.25) + 1)]
    for name, (lo, hi) in h.WIDE.items():
        fs = fins(lo, hi)
        worst_other, bump_hit = 0.0, 0.0
        for a in steps:
            for f in fs:
                t = h.rot(f, a)
                hit = t.intersection(RING)
                bump_part = hit.intersection(BUMPS).area
                bump_hit = max(bump_hit, bump_part)
                worst_other = max(worst_other, hit.area - bump_part)
        check(f"{name} turns to the stop, touching only the bumps", worst_other < EPS,
              f"other contact {worst_other:.4f} mm²; deepest bump contact {bump_hit:.3f} mm²")
        check(f"{name} pushes both bumps", bump_hit > 0.05)
    end = [h.rot(f, h.TWIST_DEG) for f in fins(4.05, 6.05)]
    check("locked: clear of stop and bumps", all(t.intersection(RING).area < EPS for t in end))
    over = [h.rot(f, h.TWIST_DEG + 3.0) for f in fins(4.05, 6.05)]
    check("stop blocks 3 degrees further", any(t.intersection(STOP).area > EPS for t in over))
    back = [h.rot(f, -3.0) for f in fins(4.05, 6.05)]
    check("stop blocks 3 degrees the wrong way", any(t.intersection(STOP).area > EPS for t in back))
    up, low = h.locked_fins()
    d_stop = low.distance(STOP)
    d_bump = [f.distance(h.bump(h.place_bump(f))) for f in (up, low)]
    play = math.degrees((d_stop + min(d_bump)) / h.FIN_R)
    check("locked play", play < 4.0,
          f"stop gap {d_stop:.2f}, bump gaps {d_bump[0]:.2f}/{d_bump[1]:.2f} mm: about {play:.1f} degrees of wobble")


@section("D", "Catches")
def sec_d():
    for label, r in (("shortest standard fin", h.FIN_R_MIN), ("longest standard fin", h.FIN_R),
                     ("longest fin a car takes", h.CAR_FIN_R)):
        bend = r - h.CATCH_R
        # from where the beam is fixed to the top of the bump
        ramp = (h.SLOT_R - h.CATCH_R) / math.tan(math.radians(h.BUMP_ENTRY)) + h.BUMP_FLAT
        length = math.radians(h.BEAM_ARC) * (h.SLOT_R + h.BEAM_T / 2) - ramp
        strain = 1.5 * h.BEAM_T * bend / length ** 2
        height = h.WALL + (h.C0 - h.GAP * h.SQ2 - (h.SLOT_R + h.BEAM_T / 2))   # bed to the beam's mean top
        force = 3 * PETG_E * (height * h.BEAM_T ** 3 / 12) / length ** 3 * bend
        check(f"{label} (r {r})", 0.3 <= bend < h.BEAM_GAP and strain <= STRAIN_MAX,
              f"bump moves {bend:.2f} of {h.BEAM_GAP} room; beam {length:.1f} long, "
              f"strain {strain:.1%}, about {force:.1f} N on the fin")
    check("bump covers the fin's thickness", h.C0 - h.GAP * h.SQ2 - h.CATCH_R >= h.FIN_F,
          f"bump top at the fin tip is {h.C0 - h.GAP * h.SQ2 - h.CATCH_R:.2f} above the wall; fins up to {h.FIN_F}")


@section("E", "Wall and seal")
def sec_e():
    check("wall clears the plate", h.WALL <= PLATE_MIN - 0.4,
          f"wall {h.WALL}; plate at least {PLATE_MIN} behind the fins (operator's LED {LED_PLATE})")
    check("wall squeezes the LED seal", h.WALL > LED_SEAL_FACE + 0.3,
          f"seal face {LED_SEAL_FACE} behind the fins: squeezed {h.WALL - LED_SEAL_FACE:.2f}, "
          f"{LED_PLATE - h.WALL:.2f} left between wall and plate")


@section("F", "Head and nose clear the body (3D)")
def sec_f():
    import cadquery as cq

    body = h.holder()

    def cyl(r, z0, z1):
        return cq.Workplane("XY").circle(r).extrude(z1 - z0).translate((0, 0, z0))

    def vol(w):
        return sum(s.Volume() for s in w.solids().vals()) if w.solids().size() else 0.0

    nose = cyl(h.NOSE_D / 2, -h.WALL - 1, 0)
    head = cyl(10.0, 0, 44.0)   # Ø20: anything that passes a car's hole, as long as R37 allows
    check("nose clears the hole", vol(body.intersect(nose)) < EPS)
    check("Ø20 x 44 head clears the bore, stop and catches", vol(body.intersect(head)) < EPS,
          f"bore Ø{h.HEAD_D}, stop from r {h.STOP_IN}, head length {h.HEAD_LEN}")
    fins_3d = cq.Workplane("XY")
    for lo, hi in h.WIDE.values():
        for f in fins(lo, hi):
            t = h.rot(f, h.TWIST_DEG)
            fins_3d = fins_3d.union(h.prism(t, 0.0, h.FIN_F))
    check("locked fins, full 4.0 thick, clear the body", vol(body.intersect(fins_3d)) < EPS)
    # The 2D shapes these checks use are the ones the model is made of.
    wall = h.disc(h.R_OUT).difference(KEYHOLE).difference(POCKETS).union(BEAMS)
    for z, label, shape in ((-1.2, "wall", wall), (1.0, "ring", RING)):
        got = vol(body.intersect(cyl(30, z - 0.05, z + 0.05))) / 0.1   # area of a thin slice
        check(f"model matches the checked {label} (z {z})", abs(got - shape.area) / shape.area < 0.005,
              f"model {got:.1f} mm², checked shapes {shape.area:.1f} mm²")


# Mock PGJ19 connector sockets for the connector cap (sheet 7004-110-2, letters as
# there), in the cap's coordinates: mouth face at z = 0, socket toward -z, oval
# along y, side bump on +x. Keys are (side, length) from the cavity wall: H11 has
# one (T), H9 two (T1, T2).
H11_KEYS = [(1, 5.6)]
H9_KEYS = [(1, 3.8), (-1, 2.0)]
SOCKETS = {
    "smallest socket, H11 keys, shallow hooks": dict(Y=14.85, V=24.0, M=11.75, N=21.15, R=5.85, P=8.2, Q=17.65,
                                                     L=5.25, W=28.15, J=2.5, keys=H11_KEYS),
    "largest socket, H9 keys, deep hooks": dict(Y=15.15, V=24.6, M=12.05, N=21.45, R=6.15, P=8.5, Q=17.95,
                                                L=6.75, W=28.45, J=2.9, keys=H9_KEYS),
    "largest outside, smallest recess": dict(Y=15.15, V=24.6, M=11.75, N=21.15, R=5.85, P=8.2, Q=17.65,
                                             L=5.25, W=28.45, J=2.5, keys=H11_KEYS),
}
HOOK_LEAN = 10.0   # degrees the hooks' catch faces lean back


def socket(Y, V, M, N, R, P, Q, L, W, J, keys):
    import cadquery as cq

    s = cc.CAVITY_DEPTH
    body = cc.oval(Y, V, -20, 0).cut(cc.oval(M, N, -R, 1)).cut(cc.oval(P, Q, -s, -R + 0.01))
    # End hooks (view a): a 45 degree ramp out to W, then the catch face J in from the mouth.
    y0, tip = V / 2, W / 2 - V / 2
    deep = J + tip * math.tan(math.radians(HOOK_LEAN))
    hook = (cq.Workplane("YZ", origin=(-cc.HOOK_W / 2, 0, 0))
            .polyline([(y0 - 0.5, 0), (y0, 0), (y0 + tip, -tip), (y0 + tip, -deep), (y0, -J), (y0 - 0.5, -J)])
            .close().extrude(cc.HOOK_W))
    body = body.union(hook).union(hook.rotate((0, 0, 0), (0, 0, 1), 180))
    # Side bump (view b), the standard's largest.
    x0 = Y / 2
    body = body.union(cq.Workplane("XZ", origin=(0, 1.3, 0))
                      .polyline([(x0 - 0.5, -7.6), (x0 + 1.3, -7.6), (x0 + 1.8, -4.8), (x0, -3.76), (x0 - 0.5, -3.76)])
                      .close().extrude(2.6))
    for y in (cc.PIN_PITCH / 2, -cc.PIN_PITCH / 2):
        body = body.union(cc.box(-1.4, 1.4, y - 0.4, y + 0.4, -s - 0.5, -L))
    for side, length in keys:
        x_wall = side * P / 2
        x_tip = x_wall - side * length
        body = body.union(cc.box(min(x_wall, x_tip), max(x_wall, x_tip), -0.925, 0.925, -s - 0.5, -R))
    return body


@section("G", "Connector cap on PGJ19 sockets (3D)")
def sec_g():
    plate = cc.oval(2 * cc.R_PLATE, cc.SOCKET_L + 2 * cc.PLATE_MARGIN, 0, cc.BACK)
    insert = cc.insert()
    one = cc.arm()
    arms = one.union(one.rotate((0, 0, 0), (0, 0, 1), 180))
    for name, s in SOCKETS.items():
        sock = socket(**s)
        clash = sum(v.Volume() for part in (plate, insert) for v in part.intersect(sock).solids().vals())
        check(f"{name}: back plate and insert clear the socket", clash < EPS, f"overlap {clash:.4f} mm³")
        hits = [v.BoundingBox() for v in arms.intersect(sock).solids().vals()]
        on_hooks = all(max(abs(b.xmin), abs(b.xmax)) <= cc.HOOK_W / 2 + 0.01
                       and min(abs(b.ymin), abs(b.ymax)) >= s["V"] / 2 for b in hits)
        check(f"{name}: the arms touch both hooks and nothing else",
              on_hooks and {b.ymin > 0 for b in hits} == {True, False},
              f"{len(hits)} contacts: " + ", ".join(f"y {b.ymin:.2f}..{b.ymax:.2f} z {b.zmin:.2f}..{b.zmax:.2f}"
                                                    for b in hits))
        # The tooth's 45 degree face sits this far into the hook's corner: the preload
        # that pulls the cap onto the socket.
        reach = s["W"] / 2 - cc.C_END - cc.R_TOOTH
        face = -cc.CATCH_Z + reach
        corner = -(s["J"] + (s["W"] - s["V"]) / 2 * math.tan(math.radians(HOOK_LEAN)))
        check(f"{name}: teeth press the hooks and reach under them",
              0.3 <= face - corner <= 1.2 and reach >= 1.0,
              f"face {face - corner:.2f} into the hook's corner; tooth {reach:.2f} under the hook's tip")


if __name__ == "__main__":
    want = [a.upper() for a in sys.argv[1:]] or sorted(SECTIONS)
    for letter in want:
        title, fn = SECTIONS[letter]
        print(f"{letter}. {title}")
        fn()
    print(f"\n{len(FAILED)} failed" + (": " + ", ".join(FAILED) if FAILED else ""))
    sys.exit(1 if FAILED else 0)
