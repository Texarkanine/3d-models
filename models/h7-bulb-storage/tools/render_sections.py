import sys, importlib.util
sys.dont_write_bytecode = True
import cadquery as cq, trimesh, numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
SP = sys.argv[1] + "/"
SRC = str(__import__("pathlib").Path(__file__).resolve().parent.parent / "h7_led_cover.py")
spec = importlib.util.spec_from_file_location("h7", SRC); h7 = importlib.util.module_from_spec(spec); spec.loader.exec_module(h7)
def cyl(r, z0, z1): return cq.Workplane("XY").circle(r).extrude(z1 - z0).translate((0, 0, z0))
def tm(w, name):
    p = SP + name + ".stl"; cq.exporters.export(w, p, tolerance=0.02, angularTolerance=0.1); return trimesh.load(p)
t = 2.0
bulb = cyl(16, -t, 0).union(h7.box(0, 18.6, -3.5, 3.5, -t, 0).intersect(cyl(17.6, -t, 0)))
bulb = bulb.union(cyl(12, -6, -t)).union(cyl(19, -36, -6)).union(cyl(12.0, 0, 3)).union(cyl(8, 3, 22)).union(cyl(6, 22, 40))
cover_m, clip_m, bulb_m = tm(h7.cover(), "cover"), tm(h7.clip(0.5, 1.0), "clip"), tm(bulb, "bulb")

fig, axes = plt.subplots(1, 3, figsize=(20, 7))
y_arm = (h7.Y0 + h7.Y1) / 2
for ax, (kind, val, title, lim) in zip(axes, [
        ("y", 0.0, "Section y = 0 (through the tab slot at +x)", ((-34, 32), (-10, 58))),
        ("y", y_arm, f"Section y = {y_arm:.1f} (along a clip arm)", ((-34, 32), (-9, 6))),
        ("z", -h7.L + 0.8, f"Section z = {-h7.L + 0.8:.2f} (arm level, from the back)", ((-34, 32), (-24, 24)))]):
    for m, col in ((bulb_m, "#c9a227"), (cover_m, "#4a7ab5"), (clip_m, "#d0452f")):
        n = [0, 1, 0] if kind == "y" else [0, 0, 1]
        o = [0, val, 0] if kind == "y" else [0, 0, val]
        sec = m.section(plane_origin=o, plane_normal=n)
        if sec is None: continue
        for ent in sec.discrete:
            ax.fill(ent[:, 0], ent[:, 2] if kind == "y" else ent[:, 1], color=col, alpha=0.7, lw=0.5, ec="k")
    ax.set_aspect("equal"); ax.set_title(title); ax.grid(alpha=0.3)
    ax.set_xlim(*lim[0]); ax.set_ylim(*lim[1])
fig.suptitle("cover (blue), clip 0.5-1.0 (red), mock LED (gold: Ø32x2 flange with 7 mm tab at +x, Ø38 heatsink)")
fig.tight_layout(); fig.savefig(SP + "sections.png", dpi=80)

def view(meshes, fname, elev, azim, title):
    fig = plt.figure(figsize=(8, 8)); ax = fig.add_subplot(111, projection="3d")
    light = np.array([0.4, -0.5, 0.8]); light /= np.linalg.norm(light)
    allv = []
    for m, col in meshes:
        tri = m.vertices[m.faces]; nn = m.face_normals
        shade = 0.35 + 0.65 * np.clip(nn @ light, 0, 1)
        base = np.array(matplotlib.colors.to_rgb(col))
        ax.add_collection3d(Poly3DCollection(tri, facecolors=np.outer(shade, base), edgecolors="none")); allv.append(m.vertices)
    v = np.vstack(allv); c = (v.max(0) + v.min(0)) / 2; r = (v.max(0) - v.min(0)).max() / 2
    ax.set_xlim(c[0]-r, c[0]+r); ax.set_ylim(c[1]-r, c[1]+r); ax.set_zlim(c[2]-r, c[2]+r)
    ax.view_init(elev=elev, azim=azim); ax.set_box_aspect((1, 1, 1)); ax.set_axis_off(); ax.set_title(title)
    fig.tight_layout(); fig.savefig(SP + fname, dpi=80); plt.close(fig)
D = "/mnt/v/Users/Austin/Documents/3D Printer/models/Trinkets/H7 bulb case/"
view([(cover_m, "#4a7ab5"), (clip_m, "#d0452f")], "assembly_back.png", -50, -60, "Assembled, from the back")
view([(cover_m, "#4a7ab5")], "cover_back.png", -70, -100, "Cover from the back: key ribs, tunnels, mark")
view([(trimesh.load(D + "h7_cover.stl"), "#4a7ab5")], "print_cover.png", 20, -60, "h7_cover.stl as printed")
view([(trimesh.load(D + "clips/h7_clip_flange_2.0-2.5mm.stl"), "#d0452f")], "print_clip.png", 50, -70, "clip as printed")
print("ok")
