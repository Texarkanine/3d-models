"""H7 (PX26d) bulb cover with a snap-latch clip.

The cover seats on the bulb's flange the way a headlamp does: the flange's
front face rests on a flat seat, and the bulb head sits in a closed tube.
Everything behind the flange stays open, so heatsinks, fans and cables of any
size hang out the back.

The flange is a circle with a tab: on each side of the tab a straight flat
is cut across the circle, square to the tab, so the tab stands proud of the
flats. Two key blocks inside the collar fill those steps, one each side of
the tab, so the bulb sits at one rotation and the clip arms always press on
solid flange. The keys stand well behind the flange, so a bulb that rocks
while the clip goes in keeps its tab in the pocket. A notch on the back face
of the collar marks where the tab goes.

A short U-clip holds the bulb in. Its two arms slide through tunnels in the
collar, between the flange and the heatsink (the gap the headlamp's wire
spring clip uses). The clip goes in from either side. A barb on each arm
drags through the tunnel and snaps out past the far face of the collar,
where it catches. Across the bore the barb rides on a narrow roof over its
groove, so the arm cannot drop out of its path on the way. To release,
squeeze the two arm tips together and push them back, then pull the clip
out by its loop (a small screwdriver fits the loop).
A bump on each arm presses the flange onto the seat; the arms rest on the
collar only inside the tunnels, so they flex like springs.

The collar is square so that every tunnel roof is a short bridge held on both
sides: the cover prints upright (closed end down) with no supports. The roofs
over the barb grooves are flat only for a 1 mm ledge against the wall, then
rise at 45 degrees. No other downward face overhangs more than 45 degrees.

The bulb rests on three small lugs on the front of its flange plate, so the
back of the plate, where the bumps press, sits deeper than the plate is thick
(PLATE_SETBACK). Clips are named for the plate's thickness at its rim, in
0.5 mm bands (CLIP_VARIANTS). Measure the plate, or try them.
The arms are printed spread ARM_SPREAD outward; the far tunnel pushes them
back, so they press the barbs out. clip() is the clip as held in use;
printed_clip() is what is exported.

Sources for the default dimensions:
  - UNECE R37 sheet H7/1, maximum lamp outline: Ø25.0 for 4.1 mm in front of
    the reference plane, then Ø19.0, glass at most Ø15.0, at most 44.0 mm
    long from the reference plane.
  - The MakerWorld screw-together H7 case cup (h7-bulbholderv2.stl):
    Ø26.4 x 4 mm in front of the flange, Ø36 around the flange.
  - IEC 60061-1 sheet 7004-5 (cap PX26d), read from its identical Russian
    adoption GOST IEC 60061-1-2014: flange O 33.8-34.0, tab K 7.9-8.0,
    centre to flat Q 13.2-13.7, front ring M 25.9-26.0. The letters are
    mapped by fit to a measured LED bulb (Ø33.3, tab 7.7, flat at 12.8) and
    a retailer's "34 mm plate, 21 mm flat, 8 mm tab". Plate thickness
    T 0.6-0.8 and the back of the plate at most Z 1.4 behind the reference
    plane are read off the sheet's drawing (meganorm.ru copy).
  - Test prints of 0.2 to 0.4 on the operator's LED bulbs (2026-10-12/13).

Coordinates (use position): z = 0 is the seat (the bulb's reference plane),
+z points to the bulb tip, the clip slides in along +x, the tab sits at +x.
Seen from the back (heatsink side), +x is right and +y is down.

Run:  python h7_led_cover.py   (needs cadquery)
Writes STEP (opens in Solid Edge) and STL (for the slicer), already turned
to their print orientation.
"""

import math
from pathlib import Path

import cadquery as cq

# ---- Bulb (measure yours and change these if needed) ----------------------
FLANGE_D = 34.0      # flange plate diameter, PX26d O max; the tab's outer edge is on this circle
FLANGE_T_MAX = 3.0   # deepest the back of the flange plate may sit behind the seat; sizes the tunnels
PLATE_SETBACK = 1.0  # the bulb rests on lugs in front of its plate, so the back of the plate sits this
                     # much deeper than the plate is thick (PX26d: plate T 0.6-0.8, back Z at most 1.4).
                     # From test prints: the operator's LED bulb, plate 0.85, takes the clip built for 1.75.
NECK_MAX_W = 26.0    # widest part of the bulb in the first 4.5 mm behind the flange
FRONT_D = 26.4       # clearance for the ring just in front of the flange (PX26d M max 26.0)
FRONT_LEN = 4.6      # length of that ring zone (std 4.1)
HEAD_D = 21.0        # bore for the bulb head (std envelope Ø19, glass ≤ Ø15)
HEAD_LEN = 54.0      # seat to inside of the closed end: the longest standard head (R37 H7/1: 44) + 10 mm spare

# ---- Tab key ----------------------------------------------------------------
# On each side of the tab, a straight flat is cut across the flange at right
# angles to the tab, leaving a step. A key block fills each step.
KEY = True           # False: no key, the bulb can sit at any rotation
TAB_W = 8.0          # tab width, PX26d K max
FLAT_Q = 13.7        # centre to each flat, PX26d Q max (the step is shallowest here)
KEY_DEPTH = 4.5      # key height above the seat: deeper than the flange, so a rocking bulb keeps its
                     # tab in the pocket. Beside the tab the bulb must be clear this far behind the seat.
KEY_LEAD = 1.0       # 45 degree slope on the key tops facing the tab and the flat, to guide the tab in
KEY_CLEAR = 0.35     # gap between each key and the side of the tab
KEY_FLAT_CLEAR = 0.3 # gap between each key and the flat at FLAT_Q

# ---- Printer / fit ----------------------------------------------------------
CLEAR = 0.3          # sliding clearance per side
Z_CLEAR = 0.2        # extra height under the tunnel roofs, which print as bridges and may sag
WALL = 2.0           # tube wall
COLLAR_WALL = 4.0    # collar wall at its thinnest, across the flats
CORNER_R = 2.0       # collar corner radius
SHOULDER = 55.0      # shoulder faces, degrees from flat; 55 puts the corner ridges at 45
END_WALL = 2.0       # closed end of the tube
SEAT_PLATE = 2.5     # flat collar plate in front of the seat
LIP = 1.0            # tunnel roof (printed as a bridge)

# ---- Clip -------------------------------------------------------------------
ARM_W = 3.8          # width of each arm
ARM_T = 1.6          # thickness of each arm; sets the spring rate
BARB = 2.2           # how far the barb sticks out sideways; 2.2 is the most SQUEEZE allows
BARB_LEN = 4.4       # barb ramp length; 2 x BARB keeps the ramp at about 27 degrees
BARB_LEAN = 20.0     # catch face leans this many degrees off square, so it drags smoothly
TIP_OUT = 7.0        # arm tips stick out this far past the collar, to pinch
SQUEEZE = 2.2        # room for the arms to move inward in the tunnels
ARM_SPREAD = 1.5     # degrees each arm turns outward as printed; the far tunnel holds it pressed out
X_SUPPORT = 15.0     # arms rest on the tunnel roofs only beyond ±X_SUPPORT
GROOVE_LEDGE = 1.0   # roof over the barb groove across the bore: flat this far from its wall, then 45 degrees
MOUTH = 0.5          # 45 degree slope at the bore end of each tunnel roof, so a low tip rides up into it
BUMP_PRELOAD = 0.35  # nominal squeeze on the flange, mid-band
BUMP_FLAT = 3.0      # flat top of the bump, along the arm
PAD_MAX = 1.2        # grip pad on each tip: at most this tall, never taller than the bump
PAD_FLAT = 2.5
BRIDGE_T = 3.0       # thickness of the bridge and loop
BRIDGE_W = 2.4       # width of the bridge bar
LOOP_HOLE = 4.0      # screwdriver hole
LOOP_RIM = 1.8
CLIP_VARIANTS = [(0.0, 0.5), (0.5, 1.0)]  # flange plate thickness at its rim, mm

# ---- Derived ----------------------------------------------------------------
R_BORE = FLANGE_D / 2 + 0.5
HALF = R_BORE + COLLAR_WALL                   # collar half-width (square)
R_FRONT = FRONT_D / 2
R_HEAD = HEAD_D / 2
R_TUBE = R_HEAD + WALL
L = FLANGE_T_MAX + ARM_T + 0.15 + Z_CLEAR    # seat to the tunnel roofs, where the arms rest
Z_BACK = -(L + LIP)                          # back face of the collar
Z_END = HEAD_LEN + END_WALL                  # outside of the closed end
Y0 = NECK_MAX_W / 2                          # arm inner edge
Y1 = Y0 + ARM_W                              # arm outer edge
Y_GATE = Y1 + CLEAR                          # tunnel outer wall: the barb drags along it
Y_FREE = Y1 + BARB + CLEAR                   # in the bore the barbs spring out to here
Y_SQ = Y0 - SQUEEZE                          # tunnel inner wall
X_FREE = X_SUPPORT - (Y_FREE - Y_GATE)       # 45 degree ramp from the bore back into the tunnel
X_BARB = HALF + 0.2                          # barb catch face when latched (collar face + gap)
X_FLAT = FLAT_Q                              # centre to the flats
X_BAR = -(HALF + CLEAR)                      # inner face of the clip's bridge bar
HELD_SPREAD = math.degrees(math.atan(CLEAR / (HALF - X_BAR)))  # in use: arm edge on the far tunnel wall
Z_ARM = -L + ARM_T + 0.4                     # top of the clip path across the bore (the groove top)

assert Y_GATE < R_BORE, "clip arms must sit inside the flange bore"
assert Y_FREE < HALF - CORNER_R, "barb must catch on the flat of the collar face"
assert X_SUPPORT ** 2 + (Y_SQ - 1.0) ** 2 >= R_BORE ** 2, "tunnel roof needs 1 mm of wall inside it"
assert SQUEEZE >= BARB - CLEAR + 0.3, "arms need room to squeeze the barbs into the tunnels"
assert 0 <= KEY_LEAD < KEY_DEPTH, "key slope must be shorter than the key"
assert GROOVE_LEDGE - CLEAR >= 0.5, "barb must reach under the flat of the groove roof"
assert ARM_SPREAD > HELD_SPREAD, "arms must press on the far tunnel wall"


def revolve(points):
    """Revolve an (r, z) outline about the z axis."""
    return cq.Workplane("XZ").polyline(points).close().revolve(360, (0, 0, 0), (0, 1, 0))


def box(x0, x1, y0, y1, z0, z1):
    return (cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False)
            .translate((x0, y0, z0)))


def both_sides(shape):
    """The shape plus its mirror across y = 0."""
    return shape.union(shape.mirror("XZ"))


def outer_shell():
    """Square collar, 45 degree shoulder, round tube with a chamfered end."""
    def rounded_square(half, z):
        face = cq.Sketch().rect(2 * half, 2 * half).vertices().fillet(CORNER_R)._faces.Faces()[0]
        return face.outerWire().translate(cq.Vector(0, 0, z))

    collar = (cq.Workplane("XY").workplane(offset=Z_BACK).rect(2 * HALF, 2 * HALF)
              .extrude(SEAT_PLATE - Z_BACK).edges("|Z").fillet(CORNER_R))
    # Shoulder: the rounded square shrinks until its corners are inside the
    # tube. Faces at SHOULDER degrees leave the corner ridges at 45, so
    # nothing on the outside overhangs more than 45 degrees.
    shrink = HALF - R_TUBE / math.sqrt(2) + 1
    rise = shrink * math.tan(math.radians(SHOULDER))
    shoulder = cq.Workplane().add(cq.Solid.makeLoft(
        [rounded_square(HALF, SEAT_PLATE), rounded_square(HALF - shrink, SEAT_PLATE + rise)], True))
    chamfer = 1.5
    tube = revolve([(0, SEAT_PLATE), (R_TUBE, SEAT_PLATE), (R_TUBE, Z_END - chamfer),
                    (R_TUBE - chamfer, Z_END), (0, Z_END)])
    return collar.union(shoulder).union(tube)


def cover():
    lead_in = 1.2  # back edge chamfer: flange lead-in and heatsink clearance
    taper_top = FRONT_LEN + (R_FRONT - R_HEAD)  # 45 degree inside, prints unsupported
    inner = revolve([
        (0, Z_BACK - 1), (R_BORE + lead_in + 1, Z_BACK - 1), (R_BORE, Z_BACK + lead_in),
        (R_BORE, 0), (R_FRONT, 0), (R_FRONT, FRONT_LEN), (R_HEAD, taper_top),
        (R_HEAD, HEAD_LEN), (0, HEAD_LEN),
    ])
    body = outer_shell().cut(inner)

    # Clip path, +y side; mirrored below. The same both ways along x, so the
    # clip goes in from either side.

    def free_band(z0, z1):
        """The groove the barbs spring out into across the bore, from z0 to z1."""
        return (cq.Workplane("XY").workplane(offset=z0)
                .polyline([(-X_SUPPORT, Y_GATE - 0.01), (-X_FREE, Y_FREE), (X_FREE, Y_FREE),
                           (X_SUPPORT, Y_GATE - 0.01)]).close()
                .extrude(z1 - z0))

    # The groove has a roof in the plane of the tunnel roofs, so the barb rides on
    # it and the arm cannot drop out of its path across the bore. Flat for
    # GROOVE_LEDGE from the groove wall, then rising at 45 degrees to the back face,
    # so it prints without support. It lies outside the arm, so the arm still flexes.
    ledge = Y_FREE - GROOVE_LEDGE
    groove_roof = (cq.Workplane("YZ").polyline([(Y_GATE - 0.01, -L), (ledge, -L),
                                                 (Y_GATE - 0.01, -L - (ledge - Y_GATE + 0.01))]).close()
                   .extrude(2 * X_SUPPORT + 2).translate((-X_SUPPORT - 1, 0, 0))
                   .intersect(free_band(Z_BACK - 1, -L)))
    path = (
        # tunnel for the arm, tall enough for the bump and grip pad to pass, with
        # room on the inside for the arm to bend inward while the barb drags through
        box(-HALF - 1, HALF + 1, Y_SQ, Y_GATE, -L, -0.5)
        # in the bore the barbs spring out into the groove, under its roof
        .union(free_band(-L, Z_ARM)).union(groove_roof)
        # no roof under the arm in the bore, so the middle of the arm can flex
        .union(box(-X_SUPPORT, X_SUPPORT, Y_SQ, Y_GATE, Z_BACK - 1, -L + 0.01))
    )
    if MOUTH > 0:
        # slope the bore end of each tunnel roof, so a tip that comes across a
        # little low rides up into the tunnel
        mouth = (cq.Workplane("XZ").polyline([(X_SUPPORT - 0.01, -L + 0.01), (X_SUPPORT + MOUTH, -L + 0.01),
                                               (X_SUPPORT - 0.01, -L - MOUTH - 0.01)]).close()
                 .extrude(-(Y_GATE - Y_SQ)).translate((0, Y_SQ, 0)))
        path = path.union(mouth).union(mouth.mirror("YZ"))
    body = body.cut(both_sides(path))

    if KEY:
        # A block each side of the tab, between the tab and the flat, out to the
        # bore wall, kept clear of the clip tunnels.
        key = box(X_FLAT + KEY_FLAT_CLEAR, R_BORE + 1, TAB_W / 2 + KEY_CLEAR, Y_SQ - 0.3, -KEY_DEPTH, 0.01)
        if KEY_LEAD > 0:
            # slope the top edges that face the tab and the flat, so the tab finds its pocket
            key = key.faces("<Z").edges("<X or <Y").chamfer(KEY_LEAD)
        key = key.intersect(revolve([(0, -KEY_DEPTH), (R_BORE + 0.5, -KEY_DEPTH), (R_BORE + 0.5, 0.01),
                                     (0, 0.01)]))
        body = body.union(both_sides(key))
        # notch on the back face that marks where the tab goes
        mark = (cq.Workplane("YZ").polyline([(-1.0, Z_BACK - 0.01), (1.0, Z_BACK - 0.01),
                                             (0, Z_BACK + 1.0)]).close()
                .extrude(HALF + 1).translate((R_BORE, 0, 0)))
        body = body.cut(mark)
    return body


def bump_height(t_lo, t_hi):
    """Bump on the arm so a plate of the band's middle thickness gets BUMP_PRELOAD."""
    z_lo, z_hi = t_lo + PLATE_SETBACK, t_hi + PLATE_SETBACK  # seat to the back of the plate
    h = (L - ARM_T) - (z_lo + z_hi) / 2 + BUMP_PRELOAD
    assert L - ARM_T >= z_hi + 0.1, f"flange band {t_lo}-{t_hi}: arm would touch the flange"
    assert ARM_T + h <= L - 0.5 - 0.3, f"flange band {t_lo}-{t_hi}: bump too tall for the tunnel"
    return h


def ridge(x_end, flat, h, zb, toward=-1):
    """A 30 degree ramp-flat-ramp bump on top of the arm, one end at x_end."""
    ramp = h / math.tan(math.radians(30))
    xs = [x_end, x_end + toward * ramp, x_end + toward * (ramp + flat), x_end + toward * (2 * ramp + flat)]
    z0 = zb + ARM_T - 0.01
    return (cq.Workplane("XZ").polyline([(xs[0], z0), (xs[1], z0 + h), (xs[2], z0 + h), (xs[3], z0)])
            .close().extrude(-ARM_W).translate((0, Y0, 0)))


def clip(t_lo, t_hi, x_shift=0.0, spread=HELD_SPREAD):
    """The clip latched in use position, moved by x_shift along the slide axis.

    spread turns each arm outward this many degrees about the bar's inner corner.
    The default is the arm as the far tunnel holds it (HELD_SPREAD); printed_clip()
    is the clip as printed (ARM_SPREAD); 0 is the arm pressed straight, as the
    tunnels hold it while it slides."""
    zb = -L
    bump = bump_height(t_lo, t_hi)
    x_root = X_BAR - BRIDGE_W / 2
    lean_x = BARB * math.tan(math.radians(BARB_LEAN))
    x_tip = HALF + TIP_OUT
    tip_ch = 0.8
    assert X_BARB + lean_x + BARB_LEN + 1.0 <= x_tip, "tip too short for the barb"

    # One arm (+y side) seen from above, with the barb on its outer edge.
    outline = [
        (x_root, Y0), (x_tip - tip_ch, Y0), (x_tip, Y0 + tip_ch), (x_tip, Y1 - tip_ch),
        (x_tip - tip_ch, Y1), (X_BARB + lean_x + BARB_LEN, Y1), (X_BARB + lean_x, Y1 + BARB),
        (X_BARB, Y1), (x_root, Y1),
    ]

    def plan(height):
        return cq.Workplane("XY").workplane(offset=zb).polyline(outline).close().extrude(height)

    arm = plan(ARM_T)
    # Spring bump at x = 0; grip pad at the tip, no taller than the bump so it
    # passes the flange the same way.
    ramp = bump / math.tan(math.radians(30))
    arm = arm.union(ridge(BUMP_FLAT / 2 + ramp, BUMP_FLAT, bump, zb))
    pad = min(bump, PAD_MAX)
    arm = arm.union(ridge(x_tip - 0.3, PAD_FLAT, pad, zb).intersect(plan(ARM_T + pad + 1)))
    if spread:
        # turn the whole arm outward about the bar's inner corner
        arm = arm.rotate((X_BAR, Y1, 0), (X_BAR, Y1, 1), spread)
    arms = both_sides(arm)

    # Bridge: a straight bar along the collar face, plus a loop for a screwdriver.
    bar = box(X_BAR - BRIDGE_W, X_BAR, -Y1, Y1, zb, zb + BRIDGE_T)
    r_loop = LOOP_HOLE / 2 + LOOP_RIM
    cx = X_BAR - BRIDGE_W - LOOP_HOLE / 2 - 0.4
    loop = (cq.Workplane("XY").workplane(offset=zb).center(cx, 0)
            .circle(r_loop).extrude(BRIDGE_T))
    neck = box(cx, X_BAR - BRIDGE_W / 2, -r_loop, r_loop, zb, zb + BRIDGE_T)
    hole = (cq.Workplane("XY").workplane(offset=zb - 1).center(cx, 0)
            .circle(LOOP_HOLE / 2).extrude(BRIDGE_T + 2))
    bridge = bar.union(loop).union(neck).cut(hole)

    return arms.union(bridge).translate((x_shift, 0, 0))


def printed_clip(t_lo, t_hi):
    """The clip as printed: arms spread ARM_SPREAD, in use position."""
    return clip(t_lo, t_hi, spread=ARM_SPREAD)


def to_print_cover(body, top=Z_END):
    # Closed end on the bed, seat face up. Tunnel roofs print as bridges.
    return body.rotate((0, 0, 0), (1, 0, 0), 180).translate((0, 0, top))


def to_print_clip(part):
    return part.translate((0, 0, L))


def fit_test(body, keep=8.0):
    """Collar and seat only, open-ended, to check the flange, key and clip quickly."""
    cutter = cq.Workplane("XY").box(200, 200, 200, centered=(True, True, False)).translate((0, 0, keep))
    return body.cut(cutter)


def export(shape, stem, out):
    cq.exporters.export(shape, str(out / f"{stem}.step"))
    cq.exporters.export(shape, str(out / f"{stem}.stl"), tolerance=0.01, angularTolerance=0.1)


if __name__ == "__main__":
    out = Path(__file__).resolve().parent
    body = cover()
    export(to_print_cover(body), "h7_cover", out)
    export(to_print_cover(fit_test(body), top=8.0), "h7_fit_test", out)
    clips = out / "clips"
    clips.mkdir(exist_ok=True)
    for lo, hi in CLIP_VARIANTS:
        export(to_print_clip(printed_clip(lo, hi)), f"h7_clip_flange_{lo:.1f}-{hi:.1f}mm", clips)
    print(f"bore Ø{2 * R_BORE:.1f}, collar {2 * HALF:.1f} mm square, tube Ø{2 * R_TUBE:.1f}, "
          f"length {Z_END - Z_BACK:.1f} mm; clip bumps "
          + ", ".join(f"{lo}-{hi}: {bump_height(lo, hi):.2f}" for lo, hi in CLIP_VARIANTS))
