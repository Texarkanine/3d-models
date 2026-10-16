"""Draw the H11 measuring diagram: the PGJ19 cap at the largest sizes allowed.

Usage: python tools/make_svg.py <output.svg>

Sizes come from IEC 60061-1 sheet 7004-110-2 (cap PGJ19), read from its
identical Russian adoption GOST IEC 60061-1-2014, and from the head outline in
UNECE R37 sheet H8/1 (GOST R 41.37-99). H8, H9, H11 and H16 share the cap; only
the wide fin differs.

Front views are seen from the glass end with the plug at the bottom. In the
standard's own front view the plug is at +x; `turn` rotates that to here.
"""
import math
import sys

from shapely.geometry import Point, Polygon, box
from shapely.ops import unary_union

OUT = sys.argv[1]

# ---- Cap PGJ19 (sheet 7004-110-2), largest sizes ----
NOSE_D = 19.0              # A1 max; the V-support cylinder is radius A = 9.5
R8 = 12.25                 # fin tip radius, r8 12.15-12.25
R8_MIN = 12.15
F_MAX = 4.0                # fin block thickness in front of the fin back faces
E_MIN = 3.0                # fin back faces to the plate face the seal sits on (cap notes 5, 10)
C_RANGE = (25.1, 25.5)     # diameter of that face
G_RANGE = (31.4, 31.6)     # plate
Z_MAX = 21.4               # across nose and spring, spring relaxed
H_MAX = 24.0               # plug body, axis to its far face
B, B_MIN = 8.0, 7.8        # narrow fin: straight edge, this far from the centre line
B1, B1_MIN = 3.5, 3.3      # narrow fin: other edge, this far from the 60 degree line
# Wide fin, as (below, above) the centre line in the standard's view.
WIDE = {
    "H8": ("PGJ19-1", 4.05, 4.05),
    "H11": ("PGJ19-2", 4.05, 6.05),
    "H16": ("PGJ19-3", 5.05, 5.05),
    "H9": ("PGJ19-5", 6.05, 4.05),
}
# ---- Head, UNECE R37 sheet H8/1 maximum outline ----
HEAD_L = 44.0
HEAD_D0, HEAD_L0 = 25.0, 4.0   # first 4 mm in front of the fin back faces
HEAD_D1 = 19.0
HEAD_D2 = 15.0                 # glass

out = []
w = out.append


def turn(x, y):
    """Standard's view (plug at +x) to ours (plug at the bottom)."""
    return y, -x


def cap_outline(below, above, r8=R8, b=B, b1=B1):
    """Nose and three fins, seen from the glass end, in our view."""
    nose = Point(0, 0).buffer(NOSE_D / 2, resolution=180)
    tips = Point(0, 0).buffer(r8, resolution=180)
    wide = box(-r8 - 1, -below, 0, above).intersection(tips)
    c, s = math.cos(math.radians(30)), math.sin(math.radians(30))
    big = 40
    lower = box(-big, -big, b, 0).intersection(_half_plane(c, s, -b1)).intersection(tips)
    upper = Polygon([(x, -y) for x, y in lower.exterior.coords])
    shape = unary_union([nose, wide, lower, upper])
    return [turn(x, y) for x, y in shape.exterior.coords]


def _half_plane(nx, ny, d, big=60):
    """Points p with p . (nx, ny) >= d, clipped to a large square."""
    tx, ty = -ny, nx
    p0 = (nx * d, ny * d)
    return Polygon([(p0[0] - tx * big, p0[1] - ty * big),
                    (p0[0] + tx * big, p0[1] + ty * big),
                    (p0[0] + tx * big + nx * big, p0[1] + ty * big + ny * big),
                    (p0[0] - tx * big + nx * big, p0[1] - ty * big + ny * big)])


def narrow_tip_corners(r8, b, b1):
    """The two tip corners of the lower-right narrow fin in the standard's view."""
    a0 = -math.degrees(math.acos(b / r8))
    a1 = 30 - math.degrees(math.acos(-b1 / r8))
    return [(r8 * math.cos(math.radians(a)), r8 * math.sin(math.radians(a))) for a in (a0, a1)]


def chord(p, q):
    return math.hypot(p[0] - q[0], p[1] - q[1])


TIP_MAX = narrow_tip_corners(R8, B, B1)
TIP_MIN = narrow_tip_corners(R8_MIN, B_MIN, B1_MIN)
W_MAX, W_MIN = chord(*TIP_MAX), chord(*TIP_MIN)


# ---- SVG helpers (as in h7-bulb-storage/tools/make_svg.py) ----
S = 9.0


def P(cx, cy, x, y, s=S):
    return f"{cx + x * s:.1f},{cy - y * s:.1f}"


def poly(cx, cy, pts, attrs, s=S):
    w(f'<polygon points="{" ".join(P(cx, cy, x, y, s) for x, y in pts)}" {attrs}/>')


def circle(cx, cy, r, attrs, s=S):
    w(f'<circle cx="{cx}" cy="{cy}" r="{r * s:.1f}" {attrs}/>')


def line(cx, cy, x0, y0, x1, y1, cls):
    w(f'<line x1="{cx + x0 * S:.1f}" y1="{cy - y0 * S:.1f}" x2="{cx + x1 * S:.1f}" y2="{cy - y1 * S:.1f}" class="{cls}"/>')


def dim(cx, cy, x0, y0, x1, y1, label, lx, ly, anchor="middle", ext=()):
    for (ax, ay), (bx, by) in ext:
        line(cx, cy, ax, ay, bx, by, "ext")
    w(f'<line x1="{cx + x0 * S:.1f}" y1="{cy - y0 * S:.1f}" x2="{cx + x1 * S:.1f}" y2="{cy - y1 * S:.1f}" '
      f'class="dim" marker-start="url(#arr)" marker-end="url(#arr)"/>')
    text(cx, cy, lx, ly, label, "lab", anchor)


def text(cx, cy, x, y, t, cls, anchor="start"):
    w(f'<text x="{cx + x * S:.1f}" y="{cy - y * S:.1f}" class="{cls}" text-anchor="{anchor}">{t}</text>')


W, H = 1400, 1255
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
    .cap { fill:#d4d7db; stroke:#333; stroke-width:1.5; }
    .behind { fill:none; stroke:#8a8f96; stroke-width:1.2; stroke-dasharray:6 4; }
    .spring { fill:#e8b04a; fill-opacity:0.8; stroke:#9a6a10; stroke-width:1.2; }
    .ref { stroke:#c0392b; stroke-width:2.2; }
    .head { fill:#eef3f8; stroke:#4a7ab5; stroke-width:1.2; stroke-dasharray:5 3; }
    .th { font-size:14px; font-weight:700; fill:#111; }
    .td { font-size:14px; fill:#222; }
    .tl { font-size:15px; font-weight:700; fill:#111; }
    .blank { stroke:#999; stroke-width:1; }
  </style>
</defs>
<rect width="100%" height="100%" fill="#ffffff"/>""")
w('<text x="40" y="40" class="title">H11 bulb cap (PGJ19-2): what to measure</text>')
w('<text x="40" y="63" class="small">Largest sizes the standard allows, to scale, in mm. Capital letters and r8 are the standard\'s names; '
  'lowercase w, L and d are ours.</text>')

# ---------- Panel 1: front view ----------
cx, cy = 320, 345
w('<text x="40" y="100" class="title">1. Looking at the fins from the glass end</text>')
w('<text x="40" y="122" class="small">Plug at the bottom. Dashed grey parts are behind the fins.</text>')
w(f'<rect x="{cx - 7.5 * S:.1f}" y="{cy + G_RANGE[1] / 2 * S - 8:.1f}" width="{15 * S:.1f}" '
  f'height="{(H_MAX - G_RANGE[1] / 2) * S + 8:.1f}" class="behind"/>')
text(cx, cy, 8.3, -21.5, "plug (behind)", "small")
circle(cx, cy, G_RANGE[1] / 2, 'class="behind"')
circle(cx, cy, C_RANGE[1] / 2, 'class="behind"')
lo, hi = WIDE["H11"][1:]
# halogen spring: a leaf on the nose, sketched where the standard draws it
spring = [(9.5 * math.cos(math.radians(a)), 9.5 * math.sin(math.radians(a))) for a in range(118, 203, 3)]
peak = Z_MAX - NOSE_D / 2
spring += [((9.5 + (peak - 9.5) * math.sin(math.radians((a - 118) * 180 / 84))) * math.cos(math.radians(a)),
            (9.5 + (peak - 9.5) * math.sin(math.radians((a - 118) * 180 / 84))) * math.sin(math.radians(a)))
           for a in range(202, 117, -3)]
poly(cx, cy, spring, 'class="spring"')
poly(cx, cy, cap_outline(lo, hi), 'class="cap"')
circle(cx, cy, NOSE_D / 2, 'fill="none" stroke="#333" stroke-width="0.8" stroke-dasharray="2 3"')
w(f'<circle cx="{cx}" cy="{cy}" r="2.5" fill="#333"/>')

# A1: nose
dim(cx, cy, -NOSE_D / 2, 0, NOSE_D / 2, 0, "A1", 5.6, 0.6, "middle")
# r8: wide fin tip to far side of nose
x_r = -2.6
dim(cx, cy, x_r, -NOSE_D / 2, x_r, R8, "", 0, 0)
text(cx, cy, x_r - 0.6, 5.2, "r8", "lab", "end")
# B5 + B6: wide fin width
yb = R8 + 2.4
dim(cx, cy, -lo, yb, hi, yb, f"B5 + B6   wide fin {lo + hi - 0.1:.1f}", (hi - lo) / 2, yb + 1.0, "middle",
    ext=[((-lo, R8 - 0.3), (-lo, yb + 0.6)), ((hi, R8 - 0.3), (hi, yb + 0.6))])
# w: narrow fin tip width (lower-right fin in our view)
t0, t1 = turn(*TIP_MAX[0]), turn(*TIP_MAX[1])
# TIP_MAX is the lower-right fin in the standard's view, which turns to lower-left here; mirror it to the right.
t0, t1 = (-t0[0], t0[1]), (-t1[0], t1[1])
ux, uy = (t0[0] + t1[0]) / 2, (t0[1] + t1[1]) / 2
ul = math.hypot(ux, uy)
off = 1.9
dim(cx, cy, t0[0] + ux / ul * off, t0[1] + uy / ul * off, t1[0] + ux / ul * off, t1[1] + uy / ul * off,
    "w", ux / ul * (ul + off + 1.6), uy / ul * (ul + off + 1.6) - 0.5, "middle",
    ext=[(t0, (t0[0] + ux / ul * (off + 0.6), t0[1] + uy / ul * (off + 0.6))),
         (t1, (t1[0] + ux / ul * (off + 0.6), t1[1] + uy / ul * (off + 0.6)))])
# Z: across nose and spring
za = math.radians(160)
z0 = (peak * math.cos(za), peak * math.sin(za))
z1 = (-9.5 * math.cos(za), -9.5 * math.sin(za))
w(f'<line x1="{cx + z0[0] * S:.1f}" y1="{cy - z0[1] * S:.1f}" x2="{cx + z1[0] * S:.1f}" y2="{cy - z1[1] * S:.1f}" '
  'class="dim" stroke="#9a6a10" marker-start="url(#arr)" marker-end="url(#arr)" stroke-dasharray="7 3"/>')
text(cx, cy, z0[0] - 0.8, z0[1] + 0.3, "Z", "lab", "end")
text(cx, cy, -16.6, 7.2, "spring nub", "small", "end")
text(cx, cy, -16.6, 5.6, "(halogen; sketch)", "small", "end")
# C and G: leaders to the dashed circles behind
for k, name, r, ly, deg in (("C", "seal face", C_RANGE[1] / 2, -9.3, 200), ("G", "plate", G_RANGE[1] / 2, -12.6, 228)):
    a = math.radians(deg)
    text(cx, cy, -18.6, ly, f"{k}  {name}", "lab", "end")
    line(cx, cy, -18.4, ly + 0.5, r * math.cos(a), r * math.sin(a), "ext")

# ---------- Panel 2: side view ----------
sx, sy = 790, 345
w('<text x="700" y="100" class="title">2. From the side</text>')
w('<text x="700" y="122" class="small">Glass to the right, plug to the left. Blue dashed: the largest head R37 allows.</text>')
ORING_T, PLATE_T = 1.8, 2.5          # not set by the standard; drawn for the picture only
x_plate = -E_MIN
x_seal = x_plate + ORING_T           # the seal's front face, when it is not squeezed
x_body = x_plate - PLATE_T
r_tip = R8
# head envelope
cone_x0 = 25.0 - (HEAD_D1 / 2) / math.tan(math.radians(50))
cone_x1 = 25.0 - (HEAD_D2 / 2) / math.tan(math.radians(50))
env = ([(0, HEAD_D0 / 2), (HEAD_L0, HEAD_D0 / 2), (HEAD_L0, HEAD_D1 / 2), (cone_x0, HEAD_D1 / 2),
        (cone_x1, HEAD_D2 / 2)]
       + [(HEAD_L - HEAD_D2 / 2 + HEAD_D2 / 2 * math.sin(math.radians(a)), HEAD_D2 / 2 * math.cos(math.radians(a)))
          for a in range(0, 181, 10)]
       + [(cone_x1, -HEAD_D2 / 2), (cone_x0, -HEAD_D1 / 2), (HEAD_L0, -HEAD_D1 / 2), (HEAD_L0, -HEAD_D0 / 2),
          (0, -HEAD_D0 / 2)])
poly(sx, sy, env, 'class="head"')
# body and plug, behind
w(f'<rect x="{sx + (x_body - 9) * S:.1f}" y="{sy - 9 * S:.1f}" width="{9 * S:.1f}" height="{(9 + H_MAX) * S:.1f}" class="behind"/>')
text(sx, sy, x_body - 4.5, -18.5, "plug", "small", "middle")
# plate, seal, nose, fins
poly(sx, sy, [(x_body, G_RANGE[1] / 2), (x_plate, G_RANGE[1] / 2), (x_plate, -G_RANGE[1] / 2), (x_body, -G_RANGE[1] / 2)],
     'fill="#b9bdc2" stroke="#333" stroke-width="1.2"')
poly(sx, sy, [(x_plate, C_RANGE[1] / 2), (x_seal, C_RANGE[1] / 2), (x_seal, -C_RANGE[1] / 2), (x_plate, -C_RANGE[1] / 2)],
     'fill="#3a3a3a" stroke="#111" stroke-width="1"')
poly(sx, sy, [(x_plate, NOSE_D / 2), (5.5, NOSE_D / 2), (5.5, -NOSE_D / 2), (x_plate, -NOSE_D / 2)], 'class="cap"')
poly(sx, sy, [(0, NOSE_D / 2), (F_MAX, NOSE_D / 2), (F_MAX, r_tip), (0, r_tip)], 'class="cap"')
line(sx, sy, 0, -14.5, 0, 16.2, "ref")
text(sx, sy, 0.4, 18.6, "back face of the fins:", "small")
text(sx, sy, 0.4, 17.1, "measure from here", "small")
# F
dim(sx, sy, 0, r_tip + 1.0, F_MAX, r_tip + 1.0, "", 0, 0)
text(sx, sy, F_MAX + 0.6, r_tip + 0.6, f"F  fin, {F_MAX:g} max", "lab")
# E
ye = -NOSE_D / 2 - 1.6
dim(sx, sy, x_plate, ye, 0, ye, "", 0, 0, ext=[((x_plate, -C_RANGE[1] / 2), (x_plate, ye - 0.6))])
text(sx, sy, 0.6, ye - 0.6, f"E  {E_MIN:g} min", "lab")
text(sx, sy, (x_plate + x_seal) / 2, C_RANGE[1] / 2 + 1.2, "seal", "small", "middle")
text(sx, sy, (x_body + x_plate) / 2, G_RANGE[1] / 2 + 1.0, "plate", "small", "middle")
# L
yl = -HEAD_D0 / 2 - 4.0
dim(sx, sy, 0, yl, HEAD_L, yl, f"L  head, {HEAD_L:g} max from the back face of the fins", HEAD_L / 2 + 1, yl - 1.9, "middle",
    ext=[((HEAD_L, 0), (HEAD_L, yl - 0.6)), ((0, -14.5), (0, yl - 0.6))])
# d
text(sx, sy, 20.0, HEAD_D1 / 2 + 3.8, "d  widest part of the head:", "lab")
text(sx, sy, 20.0, HEAD_D1 / 2 + 2.2, f"Ø{HEAD_D0:g} for the first {HEAD_L0:g}, then Ø{HEAD_D1:g}, glass Ø{HEAD_D2:g}", "small")
text(sx, sy, 20.0, -HEAD_D2 / 2 - 1.5, "nose Ø19", "small")

# ---------- Panel 3: the family ----------
py = 710
w(f'<text x="40" y="{py - 70}" class="title">3. Same cap, different wide fin: H8, H11, H16, H9</text>')
w(f'<text x="40" y="{py - 48}" class="small">Same view as panel 1, half scale. The narrow fins, nose, fin reach and gaps are the same on all four. '
  'The holder\'s openings will take all four.</text>')
for i, (name, (cap, lo_, hi_)) in enumerate(WIDE.items()):
    qx, qy = 190 + i * 340, py + 70
    s = S / 2
    circle(qx, qy, G_RANGE[1] / 2, 'class="behind"', s)
    w(f'<polygon points="{" ".join(P(qx, qy, x, y, s) for x, y in cap_outline(lo_, hi_))}" class="cap"/>')
    w(f'<circle cx="{qx}" cy="{qy}" r="2" fill="#333"/>')
    w(f'<text x="{qx}" y="{qy + 100}" class="lab" text-anchor="middle">{name}  ({cap})</text>')
    side = "centred" if lo_ == hi_ else ("off-centre, +2 right" if hi_ > lo_ else "off-centre, +2 left")
    w(f'<text x="{qx}" y="{qy + 120}" class="small" text-anchor="middle">wide fin {lo_ + hi_ - 0.1:.1f}, {side}</text>')
w(f'<text x="40" y="{py + 222}" class="small">H8B, H9B and H11B use a different cap (PGJY19) and are not covered. '
  'If the off-centre side looks mirrored on your bulb, that is fine: only the width matters here.</text>')

# ---------- Table ----------
ty = 960
cols = [40, 100, 690, 960, 1170]
for x, h in zip(cols, ["", "What to measure (each fin, where it says so)", "Standard (H11)", "Halogen", "LED"]):
    w(f'<text x="{x}" y="{ty}" class="th">{h}</text>')
rows = [
    ("F", "Fin thickness, front to back. Each fin.", f"{F_MAX:g} max"),
    ("A1", "Nose: the round part the fins stick out from.", f"Ø{NOSE_D:g} max"),
    ("r8", "Fin tip to the far side of the nose. Each fin.", f"{R8_MIN + 9.5:.2f} to {R8 + 9.5:.2f}"),
    ("B5+B6", "Wide fin width.", "10.0 (H8: 8.0)"),
    ("w", "Narrow fin width at the tip. Each narrow fin.", f"{W_MIN:.1f} to {W_MAX:.1f}"),
    ("E", "Back face of the fins to the plate, with the seal off.", f"{E_MIN:g} min"),
    ("C", "Diameter of the face the seal sits on.", f"{C_RANGE[0]:g} to {C_RANGE[1]:g}"),
    ("G", "Plate, diameter.", f"{G_RANGE[0]:g} to {G_RANGE[1]:g}"),
    ("Z", "Halogen only: across the nose at the spring nub.", f"{Z_MAX:g} max"),
    ("L", "Head length, back face of the fins to the tip.", f"{HEAD_L:g} max"),
    ("d", "Widest part of the head, and how far from the fins.", f"glass Ø{HEAD_D2:g}"),
]
for i, (k, what, std) in enumerate(rows):
    y = ty + 24 + i * 22
    w(f'<text x="{cols[0]}" y="{y}" class="tl">{k}</text>')
    w(f'<text x="{cols[1]}" y="{y}" class="td">{what}</text>')
    w(f'<text x="{cols[2]}" y="{y}" class="td">{std}</text>')
    for x in cols[3:]:
        w(f'<line x1="{x}" y1="{y + 3}" x2="{x + 170}" y2="{y + 3}" class="blank"/>')
w(f'<text x="40" y="{H - 32}" class="small">Sources: IEC 60061-1 sheet 7004-110-2 (cap PGJ19) via GOST IEC 60061-1-2014; '
  'UNECE R37 sheet H8/1 head outline via GOST R 41.37-99.</text>')
w(f'<text x="40" y="{H - 14}" class="small">The seal sits on the plate and is squeezed between it and the holder\'s wall. '
  'Seal and plate thickness are not set by the standard; they are drawn for the picture only.</text>')

w('</svg>')
open(OUT, "w").write("\n".join(out))
print("wrote", OUT, f"(narrow fin tip {W_MIN:.2f}-{W_MAX:.2f} mm)")
