import importlib.util, sys
sys.dont_write_bytecode = True
SRC = str(__import__("pathlib").Path(__file__).resolve().parent.parent / "h7_led_cover.py")
spec = importlib.util.spec_from_file_location("h7", SRC); h7 = importlib.util.module_from_spec(spec); spec.loader.exec_module(h7)
def info(n, w):
    b = w.val().BoundingBox(); s = w.solids().size()
    v = sum(x.Volume() for x in w.solids().vals())
    print(f"{n}: solids {s} vol {v/1000:.2f} cm3 x[{b.xmin:.2f},{b.xmax:.2f}] y[{b.ymin:.2f},{b.ymax:.2f}] z[{b.zmin:.2f},{b.zmax:.2f}] valid {w.val().isValid()}")
print("L", h7.L, "Z_BACK", h7.Z_BACK, "Y_GATE", h7.Y_GATE, "Y_FREE", h7.Y_FREE, "Y_SQ", h7.Y_SQ, "X_FREE", h7.X_FREE)
info("cover", h7.cover())
for lo, hi in h7.CLIP_VARIANTS:
    info(f"clip {lo}-{hi} as printed (bump {h7.bump_height(lo,hi):.2f})", h7.printed_clip(lo, hi))
