"""Draw the curved-handle outline rebuilt from the operator's offsets (PA/PB),
with caliper widths, holes and B, on a 10 mm grid, oriented like the tracing photo (tip up).

Run from the model directory: uv run --no-project --with pillow python tools/plot_curve.py
Writes reference/curve-rebuilt.png."""
import math, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    import reduce_curve as r

K, OX, OY = 12, 80, 90          # px per mm, origin offset (row 0 at OY)
P = lambda x, y: (OX + x * K, OY + y * K)
im = Image.new("RGB", (int(OX * 2 + r.PW * K) + 330, int(OY + 95 * K)), "white")
d = ImageDraw.Draw(im)
f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
fb = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
for gx in range(0, 41, 10):
    d.line([P(gx, -5), P(gx, 90)], fill=(225, 225, 225))
for gy in range(0, 91, 10):
    d.line([P(-2, gy), P(40, gy)], fill=(225, 225, 225))
    d.text((P(-6, gy)[0] - 30, P(0, gy)[1] - 10), f"{gy}", font=f, fill=(150, 150, 150))
d.line([P(0, -5), P(0, 90)], fill=(120, 120, 120), width=2); d.text(P(0.5, -6), "PA", font=f, fill=(90, 90, 90))
d.line([P(r.PW, -5), P(r.PW, 90)], fill=(120, 120, 120), width=2); d.text(P(r.PW - 3, -6), "PB", font=f, fill=(90, 90, 90))
d.line([P(x, y) for x, y in zip(r.xl, r.ys)], fill=(60, 60, 60), width=3)
d.line([P(x, y) for x, y in zip(r.xr, r.ys)], fill=(60, 60, 60), width=3)
d.line([P(x, y) for x, y in zip(r.xc, r.ys)], fill=(255, 140, 0), width=2)

def point_at(sv):
    """Centreline point and unit normal at arc length sv from A."""
    y = r.at_s(sv, r.ys); x = r.at_s(sv, r.xc)
    i = min(range(len(r.ys)), key=lambda k: abs(r.ys[k] - y)); m = r.slope(i)
    n = (1 / math.hypot(1, m), -m / math.hypot(1, m))
    return x, y, n

for name, (sv, w, t) in r.CAL.items():
    x, y, n = point_at(sv)
    a, b = (x - n[0] * w / 2, y - n[1] * w / 2), (x + n[0] * w / 2, y + n[1] * w / 2)
    d.line([P(*a), P(*b)], fill=(0, 160, 200), width=4)
    d.text((P(*b)[0] + 12, P(*b)[1] - 12), f"{name} W {w}", font=fb, fill=(0, 130, 170))
for name, sv in r.HOLES.items():
    x, y, _ = point_at(sv); c = P(x, y)
    d.ellipse([c[0] - 1.5 * K, c[1] - 1.5 * K, c[0] + 1.5 * K, c[1] + 1.5 * K], outline=(200, 150, 0), width=3)
    d.text((c[0] + 70, c[1] - 12), f"{name} 3 mm @ {sv}", font=fb, fill=(170, 120, 0))
x, y, n = point_at(r.B)
d.line([P(x - n[0] * 6, y - n[1] * 6), P(x + n[0] * 6, y + n[1] * 6)], fill=(220, 0, 150), width=4)
d.text((P(x + 6, y)[0] + 10, P(x, y)[1] - 12), f"B @ {r.B}", font=fb, fill=(200, 0, 130))
tx, ty = r.xc[0] + 0.3 * r.TIP_ABOVE_ROW0, -r.TIP_ABOVE_ROW0
d.ellipse([P(tx, ty)[0] - 5, P(tx, ty)[1] - 5, P(tx, ty)[0] + 5, P(tx, ty)[1] + 5], fill=(240, 190, 0))
d.text((P(tx, ty)[0] + 12, P(tx, ty)[1] - 26), "A (tip)", font=fb, fill=(170, 120, 0))
d.text((OX, im.height - 40), "grey = your traced edges   orange = centreline   blue = caliper W   grid 10 mm", font=f, fill=(90, 90, 90))
im.save(HERE.parent / "reference" / "curve-rebuilt.png")
