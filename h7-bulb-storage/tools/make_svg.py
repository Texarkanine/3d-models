"""Draw measure_flange.svg: the PX26d flange (max sizes), and the key around it.

Everything is seen from the back (heatsink side), tab pointing right. In model
coordinates that view has +y pointing down, so drawing y = -model y.
"""
import importlib.util
import math
import sys

sys.dont_write_bytecode = True
OUT = sys.argv[1]
SRC = str(__import__("pathlib").Path(__file__).resolve().parent.parent / "h7_led_cover.py")
spec = importlib.util.spec_from_file_location("h7", SRC)
h7 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h7)

S = 8.0
R = h7.FLANGE_D / 2
T2 = h7.TAB_W / 2
XF = h7.X_FLAT
YF = math.sqrt(R ** 2 - XF ** 2)  # where the flat meets the circle
MINE = dict(r=33.3 / 2, t2=7.7 / 2, xf=12.84)   # operator's bulb, measured
STEP = math.sqrt(R ** 2 - T2 ** 2) - XF

out = []
w = out.append


def P(cx, cy, x, y):
    return f"{cx + x * S:.1f},{cy - y * S:.1f}"


def arc(r, a0, a1, n=90):
    return [(r * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
             r * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]


def flange_pts(r=R, t2=T2, xf=XF):
    """Circle with a tab at +x and a flat on each side of it."""
    yf = math.sqrt(r ** 2 - xf ** 2)
    a_flat = math.degrees(math.atan2(yf, xf))
    xt = math.sqrt(r ** 2 - t2 ** 2)
    return ([(xt, -t2), (xt, t2), (xf, t2), (xf, yf)] + arc(r, a_flat, 360 - a_flat)
            + [(xf, -yf), (xf, -t2)])


def poly(cx, cy, pts, attrs):
    w(f'<polygon points="{" ".join(P(cx, cy, x, y) for x, y in pts)}" {attrs}/>')


def dim(cx, cy, x0, y0, x1, y1, label, lx, ly, anchor="middle", ext=()):
    for (ax, ay), (bx, by) in ext:
        w(f'<line x1="{cx + ax * S:.1f}" y1="{cy - ay * S:.1f}" x2="{cx + bx * S:.1f}" y2="{cy - by * S:.1f}" class="ext"/>')
    w(f'<line x1="{cx + x0 * S:.1f}" y1="{cy - y0 * S:.1f}" x2="{cx + x1 * S:.1f}" y2="{cy - y1 * S:.1f}" '
      f'class="dim" marker-start="url(#arr)" marker-end="url(#arr)"/>')
    w(f'<text x="{cx + lx * S:.1f}" y="{cy - ly * S:.1f}" class="lab" text-anchor="{anchor}">{label}</text>')


W, H = 1300, 800
w(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
  'font-family="Segoe UI, Helvetica, Arial, sans-serif">')
w("""<defs>
  <marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
    <path d="M0,0 L10,5 L0,10 z" fill="#111"/></marker>
  <style>
    .dim { stroke:#111; stroke-width:1.4; }
    .ext { stroke:#777; stroke-width:1; stroke-dasharray:3 3; }
    .lab { font-size:16px; font-weight:600; fill:#111; }
    .note { font-size:15px; fill:#222; }
    .title { font-size:20px; font-weight:700; fill:#111; }
    .small { font-size:13px; fill:#555; }
    .flange { fill:#d4d7db; stroke:#333; stroke-width:1.5; }
  </style>
</defs>
<rect width="100%" height="100%" fill="#ffffff"/>""")

# ---------- Panel 1: the flange as modelled ----------
cx, cy = 300, 330
w('<text x="40" y="44" class="title">1. The H7 flange (cap PX26d), largest allowed</text>')
w('<text x="40" y="68" class="small">IEC 60061-1 sheet 7004-5 maximum sizes, your bulb in brackets. Seen from the heatsink side, to scale.</text>')
poly(cx, cy, flange_pts(), 'class="flange"')
w(f'<circle cx="{cx}" cy="{cy}" r="3" fill="#333"/>')
xt = math.sqrt(R ** 2 - T2 ** 2)
dim(cx, cy, R + 2.5, -T2, R + 2.5, T2, f"K  tab {h7.TAB_W:g}  (7.7)", R + 3.3, -0.6, "start",
    ext=[((xt, T2), (R + 3.3, T2)), ((xt, -T2), (R + 3.3, -T2))])
dim(cx, cy, -R, -R - 3.0, R, -R - 3.0, f"O  Ø{h7.FLANGE_D:g}  (33.3), tab tip is on this circle", 0, -R - 5.4, "middle",
    ext=[((-R, 0), (-R, -R - 4.0)), ((R, 0), (R, -R - 4.0))])
yq = -(T2 + YF) / 2
dim(cx, cy, 0, yq, XF, yq, f"Q  {h7.FLAT_Q:g} to the flat  (12.8)", XF / 2 - 4, yq - 2.1, "middle")
w(f'<text x="{cx + (XF + 0.3) * S:.0f}" y="{cy - (T2 + 1.4) * S:.0f}" class="small">step {STEP:.1f} deep</text>')
w(f'<text x="{cx + (XF + 0.3) * S:.0f}" y="{cy + (T2 + 2.2) * S:.0f}" class="small">same both sides</text>')

ty = 650
for i, t in enumerate([
    "One straight cut across the circle, square to the tab, with the tab left standing",
    f"in the middle. The standard allows O 33.8-34.0, K 7.9-8.0 and Q 13.2-13.7 mm.",
    "The cover is built for the largest of each plus clearance, so smaller flanges like",
    f"yours fit too. Even the largest flange leaves a step {STEP:.1f} mm deep beside the tab.",
]):
    w(f'<text x="40" y="{ty + i * 21}" class="note">{t}</text>')

# ---------- Panel 2: the cover around it ----------
cx, cy = 980, 330
HB = h7.HALF
w('<text x="700" y="44" class="title">2. The cover around it</text>')
w(f'<text x="700" y="68" class="small">Same view and scale. Bore Ø{2 * h7.R_BORE:.1f}, collar {2 * HB:.1f} mm square.</text>')
w(f'<clipPath id="bore"><circle cx="{cx}" cy="{cy}" r="{h7.R_BORE * S}"/></clipPath>')
w(f'<rect x="{cx - HB * S}" y="{cy - HB * S}" width="{2 * HB * S}" height="{2 * HB * S}" rx="{h7.CORNER_R * S}" '
  'fill="#c9d8ee" stroke="#4a7ab5" stroke-width="1.5"/>')
w(f'<circle cx="{cx}" cy="{cy}" r="{h7.R_BORE * S}" fill="#ffffff" stroke="#4a7ab5" stroke-width="1.5"/>')
poly(cx, cy, flange_pts(), 'class="flange"')
poly(cx, cy, flange_pts(**MINE), 'fill="none" stroke="#7a3db8" stroke-width="1.3" stroke-dasharray="5 4"')
# key block
kx, ky0 = XF + h7.KEY_FLAT_CLEAR, T2 + h7.KEY_CLEAR
ky1 = min(h7.Y_SQ - 0.3, math.sqrt(h7.R_BORE ** 2 - kx ** 2))
a0 = math.degrees(math.asin(ky0 / h7.R_BORE))
a1 = math.degrees(math.asin(ky1 / h7.R_BORE))
key = [(kx, ky0)] + arc(h7.R_BORE, a0, a1, 30) + [(kx, ky1)]
for sy in (1, -1):
    poly(cx, cy, [(x, sy * y) for x, y in key], 'fill="#4a7ab5" stroke="#23466f" stroke-width="1"')
# clip arms
w('<g clip-path="url(#bore)">')
for top in (h7.Y1, -h7.Y0):
    w(f'<rect x="{cx - h7.R_BORE * S}" y="{cy - top * S}" width="{2 * h7.R_BORE * S}" height="{(h7.Y1 - h7.Y0) * S}" '
      'fill="#d0452f" fill-opacity="0.35"/>')
    w(f'<rect x="{cx - 2.5 * S}" y="{cy - top * S}" width="{5 * S}" height="{(h7.Y1 - h7.Y0) * S}" '
      'fill="#d0452f" fill-opacity="0.75"/>')
w('</g>')
# back-face mark at the tab
w(f'<polygon points="{P(cx, cy, h7.R_BORE + 0.2, 0)} {P(cx, cy, HB, 1.0)} {P(cx, cy, HB, -1.0)}" fill="#23466f"/>')
w(f'<text x="{cx + (HB + 0.8) * S:.0f}" y="{cy + 5}" class="small">mark</text>')

ty = 650
for i, (t, col) in enumerate([
    (f"Blue blocks: the keys, {h7.KEY_DEPTH:g} mm tall on the seat, one in each step beside", "#23466f"),
    ("the tab. The bulb only goes in one way and turns 1 to 2 degrees at most;", "#23466f"),
    ("the mark on the back face shows where the tab goes.", "#23466f"),
    ("Purple dashed: your bulb (33.3 / 7.7 / 12.8). It sits inside the largest flange.", "#7a3db8"),
    ("Red bands: where the clip arms cross the flange; the dark middle is the bump", "#a02b18"),
    ("that presses it. They now always land on full flange, well away from the step.", "#a02b18"),
]):
    w(f'<text x="{716 if t[0].islower() else 700}" y="{ty + i * 21}" class="note" fill="{col}">{t}</text>')

w('</svg>')
open(OUT, "w").write("\n".join(out))
print("wrote", OUT)
