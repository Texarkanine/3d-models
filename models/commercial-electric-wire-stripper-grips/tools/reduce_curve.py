"""Turn the operator's hand measurements of the curved handle into a
centreline and outline, and cross-check them against the caliper readings.

Run from the model directory: python3 tools/reduce_curve.py

Coordinates: y runs from tracing row 0 (near the tip) toward B, in mm.
x is measured from the PA reference line. Rows are 10 mm apart (PU).
PA = PA line -> left traced edge; PB = PB line -> right traced edge; PW = PA-to-PB.
"""
import math

PW, PU = 38.5, 10.0
PA = [19, 16, 12.5, 9.5, 7.5, 6, 4.75, 4, 3.5]
PB = [13, 16, 18.5, 20.75, 22.5, 24, 24.5, 24.75, 24.75]
TIP_ABOVE_ROW0 = 2.3          # read off photo 5: rounded tip sits ~2.3 mm above row 0
CAL = {"S1": (16.93, 7.13, 14.04), "S2": (47.76, 8.61, 14.24), "S3": (68.17, 9.23, 14.28)}  # s from A, W, T
HOLES = {"D2": 7.0, "D1": 76.5}  # s from A, both 3 mm
B = 83.15
OLD_BORE = (10.0, 14.14)       # old grip inner W x T at the mouth (rubber, maybe swollen)

ys = [i * PU for i in range(len(PA))]
xl = PA
xr = [PW - b for b in PB]
xc = [(a + b) / 2 for a, b in zip(xl, xr)]

# arc length along the centreline, measured from the tip (A)
s = [TIP_ABOVE_ROW0]
for i in range(1, len(ys)):
    s.append(s[-1] + math.hypot(xc[i] - xc[i - 1], ys[i] - ys[i - 1]))

def slope(i):
    j0, j1 = max(i - 1, 0), min(i + 1, len(ys) - 1)
    return (xc[j1] - xc[j0]) / (ys[j1] - ys[j0])

print(f"{'row':>3} {'y':>5} {'s_from_A':>8} {'x_left':>6} {'x_right':>7} {'x_ctr':>6} {'angle':>6} {'W_horiz':>7} {'W_perp':>6}")
for i, y in enumerate(ys):
    th = math.atan(slope(i))
    wh = xr[i] - xl[i]
    print(f"{i:>3} {y:5.0f} {s[i]:8.2f} {xl[i]:6.2f} {xr[i]:7.2f} {xc[i]:6.2f} {math.degrees(th):6.1f} {wh:7.2f} {wh*math.cos(th):6.2f}")

def at_s(target, arr):
    """Linear interpolation of a per-row array at arc length target."""
    for i in range(1, len(s)):
        if s[i] >= target:
            t = (target - s[i - 1]) / (s[i] - s[i - 1]); return arr[i - 1] + t * (arr[i] - arr[i - 1])
    i = len(s) - 1; t = (target - s[i - 1]) / (s[i] - s[i - 1]); return arr[i - 1] + t * (arr[i] - arr[i - 1])

wperp = [(xr[i] - xl[i]) * math.cos(math.atan(slope(i))) for i in range(len(ys))]
print("\nCaliper W vs traced W at the same station:")
for k, (sv, w, t) in CAL.items():
    print(f"  {k}: s={sv:6.2f}  caliper W={w:5.2f}  traced W={at_s(sv, wperp):5.2f}  diff={at_s(sv, wperp) - w:+5.2f}   T={t}")

print(f"\nTracing arc length tip->row 8 (B row): {s[-1]:.2f} mm; measured A->B: {B} mm; diff {s[-1]-B:+.2f}")
chord = math.hypot(xc[-1] - (xc[0] + 0.3 * TIP_ABOVE_ROW0), ys[-1] + TIP_ABOVE_ROW0)
print(f"Tracing chord tip->B: {chord:.2f} mm")
bend = math.degrees(math.atan(slope(0)) - math.atan(slope(len(ys) - 1)))
print(f"Total bend tip->B: {bend:.1f} deg")
# sagitta of the centreline from the chord row0->row8
x0, y0, x1, y1 = xc[0], 0, xc[-1], ys[-1]
L = math.hypot(x1 - x0, y1 - y0)
sag = max(abs((x1 - x0) * (y0 - y) - (x0 - x) * (y1 - y0)) / L for x, y in zip(xc, ys))
print(f"Max bow off the straight line row0->B: {sag:.2f} mm over {L:.1f} mm")

# W and T trend: fit W(s) = a + b s + c s^2 through the three caliper stations
(s1, w1, t1), (s2, w2, t2), (s3, w3, t3) = CAL.values()
def quad(x1, y1, x2, y2, x3, y3):
    d = (x1 - x2) * (x1 - x3) * (x2 - x3)
    a = (x3 * (y2 - y1) + x2 * (y1 - y3) + x1 * (y3 - y2)) / d
    b = (x3**2 * (y1 - y2) + x2**2 * (y3 - y1) + x1**2 * (y2 - y3)) / d
    c = (x2 * x3 * (x2 - x3) * y1 + x3 * x1 * (x3 - x1) * y2 + x1 * x2 * (x1 - x2) * y3) / d
    return lambda x: a * x * x + b * x + c
W = quad(s1, w1, s2, w2, s3, w3)
lin = lambda x, xa, ya, xb, yb: ya + (yb - ya) * (x - xa) / (xb - xa)
print("\nSteel size estimates (W quadratic through S1-S3; T linear S2-S3 beyond S3):")
for name, sv in (("A (tip)", 0.0), ("D2", HOLES["D2"]), ("D1", HOLES["D1"]), ("B (mouth)", B)):
    t_est = lin(sv, s1, t1, s2, t2) if sv < s2 else lin(sv, s2, t2, s3, t3)
    print(f"  {name:10s} s={sv:6.2f}  W~{W(sv):5.2f}  (linear S2-S3: {lin(sv, s2, w2, s3, w3):5.2f})  T~{t_est:5.2f}")
print(f"  old grip bore at mouth: W {OLD_BORE[0]} x T {OLD_BORE[1]}")
