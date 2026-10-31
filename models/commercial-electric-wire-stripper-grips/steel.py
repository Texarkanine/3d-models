"""The bare steel handles of the Commercial Electric wire stripper, as measured.

This file is the one home of the steel readings the model uses; design values
live in `grips.py`. `reference/measurements.md` is the dated log of how and when
each reading was taken, with the photos.

Coordinates (use position): the handle lies flat in the XY plane, the plane the
handles swing in. Z is T, straight up off the table. For the curved handle, X and
Y are the tracing's: y runs from tracing row 0 (near the tip) toward B, x from
the PA reference line. A distance along a handle, s, is arc length along its
centre line from A, the tip. Calipers and rulers measure straight lines, so
every reading "from A" is a chord; `Handle.s_at_chord` turns it into s. In
particular B, where the grip's open end sits, is at s = `Handle.length`, which
is longer than the 83.15 measured straight from A.

Run:  python steel.py   (pure Python)
Prints the curved handle's centre line and the cross-checks of the tracing
against the calipers.
"""

import bisect
import math

# ---- Curved handle: readings of 2026-10-31 ----------------------------------
# Pencil tracing of the bare steel, tip up (reference/curve-tracing-offsets.jpg).
# Two straight lines PA and PB, PW apart; rows PU apart. Row 0 sits about
# TIP_ABOVE_ROW0 below the tip, and row 8 is at B.
PW, PU = 38.5, 10.0
PA = [19, 16, 12.5, 9.5, 7.5, 6, 4.75, 4, 3.5]               # PA line -> left traced edge
PB = [13, 16, 18.5, 20.75, 22.5, 24, 24.5, 24.75, 24.75]     # PB line -> right traced edge
TIP_ABOVE_ROW0 = 2.3   # read off the photo; only a cross-check, A is placed from B_CHORD

# Calipers, straight from A: (name, chord from A, W, T). The deliberate
# cross-section readings; an earlier quick pass is in the log.
STATIONS = [("S1", 16.93, 7.13, 14.04), ("S2", 47.76, 8.61, 14.24), ("S3", 68.17, 9.23, 14.28)]
HOLES = {"D2": (7.0, 3.0), "D1": (76.5, 3.0)}   # name: (chord from A, diameter); through the T faces
B_CHORD = 83.15        # A to the mark where the old grip's open end sat

CENTRE_DEGREE = 4      # least-squares polynomial x(y) through the traced centre points


def polyfit(xs, ys, deg):
    """Least-squares polynomial coefficients, lowest power first (normal equations)."""
    n = deg + 1
    a = [[sum(x ** (i + j) for x in xs) for j in range(n)] for i in range(n)]
    b = [sum(y * x ** i for x, y in zip(xs, ys)) for i in range(n)]
    for c in range(n):
        p = max(range(c, n), key=lambda k: abs(a[k][c]))
        a[c], a[p], b[c], b[p] = a[p], a[c], b[p], b[c]
        for k in range(n):
            if k != c:
                f = a[k][c] / a[c][c]
                a[k] = [u - f * v for u, v in zip(a[k], a[c])]
                b[k] -= f * b[c]
    return [b[i] / a[i][i] for i in range(n)]


def poly(co, y, d=0):
    """Value (d=0) or first derivative (d=1) of the polynomial co at y."""
    if d == 0:
        return sum(c * y ** i for i, c in enumerate(co))
    return sum(i * c * y ** (i - 1) for i, c in enumerate(co) if i)


def _lerp_stations(s, pts):
    """Piecewise-linear value through (s, v) points, extended linearly past both ends."""
    i = max(1, min(len(pts) - 1, bisect.bisect_left([p[0] for p in pts], s)))
    (s0, v0), (s1, v1) = pts[i - 1], pts[i]
    return v0 + (v1 - v0) * (s - s0) / (s1 - s0)


class Handle:
    """One bare steel handle: centre line x(y) in the XY plane, W and T along it.

    The centre line is a polynomial x(y) (a constant for a straight handle).
    W and T are linear between the stations and extended linearly past them;
    past the tip (s < 0) they stay at their values at A. Before A and after B
    the centre line continues straight along its end tangents.
    """

    def __init__(self, name, coeffs, y_a, y_b, stations, holes, step=0.01):
        self.name, self.co, self.y_a, self.y_b = name, coeffs, y_a, y_b
        n = int(math.ceil((y_b - y_a) / step))
        self._ys = [y_a + (y_b - y_a) * k / n for k in range(n + 1)]
        self._ss = [0.0]
        for y0, y1 in zip(self._ys, self._ys[1:]):
            m = (poly(coeffs, y0, 1) + poly(coeffs, y1, 1)) / 2
            self._ss.append(self._ss[-1] + (y1 - y0) * math.hypot(1.0, m))
        self.length = self._ss[-1]
        self.stations = [(nm, self.s_at_chord(c), w, t) for nm, c, w, t in stations]
        self.holes = {nm: (self.s_at_chord(c), d) for nm, (c, d) in holes.items()}
        self._w = [(s, w) for _, s, w, _ in self.stations]
        self._t = [(s, t) for _, s, _, t in self.stations]

    def y_at(self, s):
        """Tracing y of the centre-line point at arc length s (0 <= s <= length)."""
        i = max(1, min(len(self._ss) - 1, bisect.bisect_left(self._ss, s)))
        s0, s1 = self._ss[i - 1], self._ss[i]
        return self._ys[i - 1] + (self._ys[i] - self._ys[i - 1]) * (s - s0) / (s1 - s0)

    def tangent(self, s):
        """Unit tangent, pointing from A toward B."""
        y = self.y_at(min(max(s, 0.0), self.length))
        m = poly(self.co, y, 1)
        h = math.hypot(m, 1.0)
        return (m / h, 1.0 / h, 0.0)

    def normal(self, s):
        """Unit normal in the plane of the handles (the W direction)."""
        tx, ty, _ = self.tangent(s)
        return (ty, -tx, 0.0)

    def point(self, s):
        """Centre-line point at arc length s, straight past A and B."""
        if s < 0 or s > self.length:
            end = 0.0 if s < 0 else self.length
            p, t = self.point(end), self.tangent(end)
            return tuple(pi + (s - end) * ti for pi, ti in zip(p, t))
        y = self.y_at(s)
        return (poly(self.co, y), y, 0.0)

    def width(self, s):
        return _lerp_stations(max(s, 0.0), self._w)

    def thickness(self, s):
        return _lerp_stations(max(s, 0.0), self._t)

    def s_at_chord(self, c):
        """Arc length of the centre-line point whose straight distance from A is c."""
        a = (poly(self.co, self.y_a), self.y_a)
        lo, hi = 0.0, self.length
        for _ in range(60):
            mid = (lo + hi) / 2
            x, y, _ = self.point(mid)
            lo, hi = (mid, hi) if math.hypot(x - a[0], y - a[1]) < c else (lo, mid)
        return (lo + hi) / 2

    def bend_deg(self):
        """Angle between the tangents at A and at B."""
        (ax, ay, _), (bx, by, _) = self.tangent(0), self.tangent(self.length)
        return math.degrees(math.acos(max(-1.0, min(1.0, ax * bx + ay * by))))


# ---- Build the curved handle from the tracing --------------------------------
ROW_Y = [i * PU for i in range(len(PA))]
TRACED_LEFT = list(PA)
TRACED_RIGHT = [PW - b for b in PB]
TRACED_CENTRE = [(a + b) / 2 for a, b in zip(TRACED_LEFT, TRACED_RIGHT)]
CENTRE = polyfit(ROW_Y, TRACED_CENTRE, CENTRE_DEGREE)
Y_B = ROW_Y[-1]


def _tip_y():
    """Tracing y of A: the point on the centre line B_CHORD straight from B."""
    bx = poly(CENTRE, Y_B)
    lo, hi = -10.0, 0.0
    for _ in range(60):
        mid = (lo + hi) / 2
        d = math.hypot(poly(CENTRE, mid) - bx, Y_B - mid)
        lo, hi = (lo, mid) if d < B_CHORD else (mid, hi)
    return (lo + hi) / 2


CURVED = Handle("curved", CENTRE, _tip_y(), Y_B, STATIONS, HOLES)


def report(h=CURVED):
    """Print the centre line and the cross-checks of the tracing against the calipers."""
    print(f"{h.name} handle: A at tracing y {h.y_a:.2f} (photo: {-TIP_ABOVE_ROW0:.2f}); "
          f"A to B {B_CHORD} straight, {h.length:.2f} along the centre line; bend {h.bend_deg():.1f} deg")
    print(f"\n{'row':>3} {'y':>5} {'s':>6} {'centre fit-traced':>17} {'traced W':>8} {'mock W':>6} {'diff':>5}")
    for i, y in enumerate(ROW_Y):
        s = next(s for s in (k * 0.01 for k in range(int(h.length * 100) + 2)) if h.y_at(s) >= y - 1e-9)
        tx, ty, _ = h.tangent(s)
        wt = (TRACED_RIGHT[i] - TRACED_LEFT[i]) * ty     # traced width square to the centre line
        print(f"{i:>3} {y:5.0f} {s:6.2f} {poly(h.co, y) - TRACED_CENTRE[i]:+17.3f} {wt:8.2f} "
              f"{h.width(s):6.2f} {wt - h.width(s):+5.2f}")
    print(f"\n{'':4} {'chord':>6} {'s':>6} {'W':>5} {'T':>6}")
    for nm, s, w, t in h.stations:
        print(f"{nm:4} {next(c for n2, c, *_ in STATIONS if n2 == nm):6.2f} {s:6.2f} {w:5.2f} {t:6.2f}")
    for nm, (s, d) in h.holes.items():
        print(f"{nm:4} {HOLES[nm][0]:6.2f} {s:6.2f} {h.width(s):5.2f} {h.thickness(s):6.2f}  hole {d}")
    print(f"{'A':4} {0:6.2f} {0:6.2f} {h.width(0):5.2f} {h.thickness(0):6.2f}  (extrapolated)")
    print(f"{'B':4} {B_CHORD:6.2f} {h.length:6.2f} {h.width(h.length):5.2f} {h.thickness(h.length):6.2f}  (extrapolated)")
    (ax, ay, _), (bx, by, _) = h.point(0), h.point(h.length)
    chord = math.hypot(bx - ax, by - ay)
    bow = max(abs((bx - ax) * (ay - y) - (ax - x) * (by - ay)) / chord
              for x, y, _ in (h.point(k * h.length / 200) for k in range(201)))
    print(f"\nMost the centre line strays from the straight line A-B: {bow:.2f} over {chord:.2f}")


if __name__ == "__main__":
    report()
