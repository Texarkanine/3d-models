"""Find faces that need support when an STL prints as oriented.

Flags downward faces steeper than 45 deg from vertical, groups them into
connected patches, and for each flat patch (a ceiling) checks whether the
layer just below has material on both sides of it (a bridge) or only one
side (a cantilever, which needs support).

usage: overhang.py file.stl [more.stl ...]
"""
import sys
import numpy as np
import trimesh

LIMIT = np.cos(np.radians(45)) + 0.03  # |n_z| above this = flatter than ~43 deg


def analyse(path):
    m = trimesh.load(path)
    zmin = m.bounds[0, 2]
    n = m.face_normals
    c = m.triangles_center
    bad = (n[:, 2] < -LIMIT) & (c[:, 2] > zmin + 0.2)
    print(f"\n{path.split('/')[-1]}: {len(m.faces)} faces, watertight={m.is_watertight}, "
          f"{bad.sum()} faces overhang > 45 deg")
    if not bad.any():
        return
    sub = m.submesh([np.where(bad)[0]], append=True)
    parts = sub.split(only_watertight=False)
    for p in sorted(parts, key=lambda p: -p.area):
        lo, hi = p.bounds
        flat = (hi[2] - lo[2]) < 0.05
        kind = "flat" if flat else "sloped"
        msg = (f"  {kind:6s} area {p.area:6.1f} mm2  z {lo[2]:6.2f}..{hi[2]:6.2f}  "
               f"x {lo[0]:6.1f}..{hi[0]:6.1f}  y {lo[1]:6.1f}..{hi[1]:6.1f}")
        if flat:
            msg += "  " + anchors(m, p, lo[2])
        print(msg)


def anchors(m, patch, z):
    """Sample the patch outline; report the share of it that has material
    just outside it, one layer down (where a bridge would anchor)."""
    sec = m.section(plane_origin=[0, 0, z - 0.1], plane_normal=[0, 0, 1])
    if sec is None:
        return "no layer below"
    planar, to3d = sec.to_2D()
    poly = planar.polygons_full
    outline = patch.outline()
    pts = []
    for ent in outline.entities:
        v = outline.vertices[ent.points][:, :2]
        for a, b in zip(v[:-1], v[1:]):
            k = max(2, int(np.linalg.norm(b - a) / 0.25))
            for t in np.linspace(0, 1, k, endpoint=False):
                pts.append(a + t * (b - a))
    if not pts:
        return "outline not traced; check by eye"
    pts = np.array(pts)
    centre = patch.vertices[:, :2].mean(0)
    # step 0.3 mm outward from the patch, away from its centre
    out = pts + 0.3 * (pts - centre) / np.linalg.norm(pts - centre, axis=1)[:, None]
    inv = np.linalg.inv(to3d)
    loc = (inv @ np.c_[out, np.full(len(out), z - 0.1), np.ones(len(out))].T).T[:, :2]
    from shapely.geometry import Point
    hit = np.array([any(pg.buffer(0.05).contains(Point(p)) for pg in poly) for p in loc])
    # which sides: split by direction from centre
    ang = np.degrees(np.arctan2(*(pts - centre).T[::-1]))
    sides = {"+x": (ang > -45) & (ang <= 45), "+y": (ang > 45) & (ang <= 135),
             "-x": (ang > 135) | (ang <= -135), "-y": (ang > -135) & (ang <= -45)}
    held = [s for s, sel in sides.items() if sel.any() and hit[sel].mean() > 0.6]
    span = "bridge" if ({"+x", "-x"} <= set(held) or {"+y", "-y"} <= set(held)) else "CANTILEVER"
    return f"anchored {','.join(held) or 'nowhere'} -> {span}"


if __name__ == "__main__":
    for f in sys.argv[1:]:
        analyse(f)
