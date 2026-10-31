"""Draw the curved handle as steel.py models it, over the operator's traced edges,
on a 10 mm grid, oriented like the tracing photo (tip up), to compare with
reference/curve-tracing-offsets.jpg.

Grey: the traced edges. Orange: the fitted centre line. Blue: the caliper W at
each station, square to the centre line. Also the holes, A and B.

Run from the model directory: uv run --no-project --with pillow python tools/plot_curve.py
Writes reference/curve-rebuilt.png.
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import steel  # noqa: E402

h = steel.CURVED
K, OX, OY = 12, 80, 90          # px per mm, origin offset (row 0 at OY)
P = lambda x, y: (OX + x * K, OY + y * K)  # noqa: E731
im = Image.new("RGB", (int(OX * 2 + steel.PW * K) + 330, int(OY + 95 * K)), "white")
d = ImageDraw.Draw(im)
f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
fb = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
for gx in range(0, 41, 10):
    d.line([P(gx, -5), P(gx, 90)], fill=(225, 225, 225))
for gy in range(0, 91, 10):
    d.line([P(-2, gy), P(40, gy)], fill=(225, 225, 225))
    d.text((P(-6, gy)[0] - 30, P(0, gy)[1] - 10), f"{gy}", font=f, fill=(150, 150, 150))
d.line([P(0, -5), P(0, 90)], fill=(120, 120, 120), width=2)
d.text(P(0.5, -6), "PA", font=f, fill=(90, 90, 90))
d.line([P(steel.PW, -5), P(steel.PW, 90)], fill=(120, 120, 120), width=2)
d.text(P(steel.PW - 3, -6), "PB", font=f, fill=(90, 90, 90))
d.line([P(x, y) for x, y in zip(steel.TRACED_LEFT, steel.ROW_Y)], fill=(60, 60, 60), width=3)
d.line([P(x, y) for x, y in zip(steel.TRACED_RIGHT, steel.ROW_Y)], fill=(60, 60, 60), width=3)
d.line([P(*h.point(h.length * k / 200)[:2]) for k in range(201)], fill=(255, 140, 0), width=2)


def across(s, half):
    """Ends of a line square to the centre line at s, half long each side."""
    (x, y, _), (nx, ny, _) = h.point(s), h.normal(s)
    return (x - nx * half, y - ny * half), (x + nx * half, y + ny * half)


for name, s, w, _ in h.stations:
    a, b = across(s, w / 2)
    d.line([P(*a), P(*b)], fill=(0, 160, 200), width=4)
    d.text((P(*max(a, b))[0] + 12, P(*max(a, b))[1] - 12), f"{name} W {w}", font=fb, fill=(0, 130, 170))
for name, (s, dia) in h.holes.items():
    x, y, _ = h.point(s)
    c = P(x, y)
    d.ellipse([c[0] - dia / 2 * K, c[1] - dia / 2 * K, c[0] + dia / 2 * K, c[1] + dia / 2 * K],
              outline=(200, 150, 0), width=3)
    d.text((c[0] + 70, c[1] - 12), f"{name} {dia:g} mm @ {steel.HOLES[name][0]}", font=fb, fill=(170, 120, 0))
a, b = across(h.length, 6)
d.line([P(*a), P(*b)], fill=(220, 0, 150), width=4)
d.text((P(*max(a, b))[0] + 10, P(*max(a, b))[1] - 12), f"B @ {steel.B_CHORD}", font=fb, fill=(200, 0, 130))
tx, ty, _ = h.point(0)
d.ellipse([P(tx, ty)[0] - 5, P(tx, ty)[1] - 5, P(tx, ty)[0] + 5, P(tx, ty)[1] + 5], fill=(240, 190, 0))
d.text((P(tx, ty)[0] + 12, P(tx, ty)[1] - 26), "A (tip)", font=fb, fill=(170, 120, 0))
d.text((OX, im.height - 40), "grey = your traced edges   orange = centre line   blue = caliper W   grid 10 mm",
       font=f, fill=(90, 90, 90))
im.save(HERE.parent / "reference" / "curve-rebuilt.png")
