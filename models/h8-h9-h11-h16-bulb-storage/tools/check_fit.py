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


if __name__ == "__main__":
    want = [a.upper() for a in sys.argv[1:]] or sorted(SECTIONS)
    for letter in want:
        title, fn = SECTIONS[letter]
        print(f"{letter}. {title}")
        fn()
    print(f"\n{len(FAILED)} failed" + (": " + ", ".join(FAILED) if FAILED else ""))
    sys.exit(1 if FAILED else 0)
