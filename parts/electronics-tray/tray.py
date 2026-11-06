"""esp-rc electronics tray v1 (build123d 0.13).

Bolts to the four 5 mm through-holes in the top plate of the Tarmo5 centre
chassis (B03): a 45 mm (along the car) x 20 mm (across) pattern, measured from
the community STEP assembly. B03's top plate is 6 mm thick with the battery bay
under it, so each bolt is an M4x16 button head from the top with a washer and
M4 nyloc nut inside the bay (reach it with the battery out).

Frame: origin = centre of that hole pattern on B03's top face (z=0),
+X = towards the front of the car. In car coordinates the origin is at
(64.4, 8.15, 16.44).

v1 changes from v0: 5 mm floor (bolt heads sink into counterbores, so the
H-bridge heatsink sits flat over them), M4 instead of M3, and a cable notch on
the open (-Y) side for the battery lead coming up from the bay.
"""
from build123d import *
import sys

W = 58.0                 # B03 top width
X0, X1 = -108.0, 45.0    # tray length on B03 top
T = 5.0                  # floor
WALL = 2.0
HOLE = 4.5               # M4 clearance
CB_D, CB_H = 8.4, 2.6    # counterbore for an M4 button head (7.6 x 2.2)

# pockets: (name, x_centre, y_centre, length_x, width_y, wall_h)
POCKETS = [
    ("hbridge", 17.0, 0.0, 52.0, 52.0, 6.0),
    ("esp32",   -43.0, -10.0, 19.0, 23.5, 11.0),   # ESP32-C3 SuperMini (22.5 x 18 published) across the car, USB-C to the -Y edge; sits on 9 mm end rails
    ("mp1584",  -43.0, 17.5, 20.0, 13.5, 4.0),    # MH-MINI-360: boards vary 17.4-18.6 x 11.1-12.2 (published footprints); 18.5 was too short on the real board. Key kept for the assembly script
    ("xl4015",  -89.0, 0.0, 28.0, 53.0, 4.0),      # turned across the car
]
BOLTS = [(sx * 22.5, sy * 10.0) for sx in (-1, 1) for sy in (-1, 1)]

# XL4015: its four corner holes are also its IN+/IN-/OUT+/OUT- pads, so the board
# screws down with M2x8 screws (thread-forming into the plastic) that double as
# terminals: ring terminal + spring washer under each head. Holes 47.9 x 22.5 mm
# (MaybeCube model, VRAC KiCad footprint). Bosses lift it 1.5 mm to clear the
# solder bulges and the R050 shunt on the underside.
XL_HOLES = (22.5, 47.9)          # (x, y) centre-to-centre; board turned across the car
BOSS_D, BOSS_H, M2_PILOT = 5.0, 1.5, 1.7
# MINI-360: corner holes are only 0.6-1.0 mm, too small to screw. It sits on a
# 1.5 mm pad in the middle (clear of the corner solder joints), held with
# double-sided foam tape; the pocket walls stop it sliding.
MINI_PAD = (11.0, 6.0)
# MINI-360 corner standoffs: same 1.5 mm height as the pad, under the four corner
# pads (published hole spacing 15.2-16.4 x 9.0-10.0 mm, so the centres split the
# range). The 2.2 mm holes swallow the solder tails of the wires soldered on top.
MINI_SO = (15.8, 9.5)            # (x, y) centre-to-centre
MINI_SO_D, MINI_SO_HOLE = 3.6, 2.2

# H-bridge: DubstepOwl's BTS7960 standoff (vendor/bts7960-standoff, CC BY) bolts
# to the floor through the two 4 mm holes in its base frame (40.1 mm apart, middle
# of two opposite sides) with M3x8 screws into M3 nuts captured in hex pockets
# under the frame. The IBT_2 then screws onto the four post tops (40 x 40 mm).
HB_SO_HOLES = 40.1
NUT_AF, NUT_H, M3_CLR = 5.7, 2.6, 3.3

with BuildPart() as tray:
    with BuildSketch():
        with Locations(((X0 + X1) / 2, 0)):
            RectangleRounded(X1 - X0, W, 6)
    extrude(amount=T)
    for name, cx, cy, lx, ly, h in POCKETS:
        if name == "hbridge":
            continue   # no pocket: the H-bridge sits on its own standoff
        with BuildSketch(Plane.XY.offset(T)):
            with Locations((cx, cy)):
                RectangleRounded(lx + 2 * WALL, ly + 2 * WALL, 3)
                RectangleRounded(lx, ly, 1.5, mode=Mode.SUBTRACT)
        extrude(amount=h)
    # bolt holes + counterbores from the top
    with Locations(*[(x, y, 0) for x, y in BOLTS]):
        Hole(HOLE / 2, depth=T + 10)
    with BuildSketch(Plane.XY.offset(T - CB_H)):
        with Locations(*BOLTS):
            Circle(CB_D / 2)
    extrude(amount=CB_H + 7, mode=Mode.SUBTRACT)
    # zip-tie slots through the floor beside the H-bridge and ESP32 pockets
    for name, cx, cy, lx, ly, h in POCKETS:
        if name in ("xl4015", "mp1584", "hbridge"):
            continue
        for dx in (-lx / 4, lx / 4):
            with BuildSketch():
                with Locations((cx + dx, cy - ly / 2 - WALL - 0.5), (cx + dx, cy + ly / 2 + WALL + 0.5)):
                    Rectangle(4.2, 2.4)
            extrude(amount=T + 12, mode=Mode.SUBTRACT)
    # H-bridge standoff: M3 clearance through the floor + captured-nut hex pockets
    _, cx, cy, lx, ly, h = POCKETS[0]
    hb = [(cx - HB_SO_HOLES / 2, cy), (cx + HB_SO_HOLES / 2, cy)]
    with BuildSketch():
        with Locations(*hb):
            Circle(M3_CLR / 2)
    extrude(amount=T, mode=Mode.SUBTRACT)
    with BuildSketch(Plane.XY.offset(T - NUT_H)):
        with Locations(*hb):
            RegularPolygon(NUT_AF / 3 ** 0.5, 6, major_radius=True)
    extrude(amount=NUT_H, mode=Mode.SUBTRACT)
    # ESP32-C3 SuperMini: pins run along its long (Y) sides, so the board rests
    # on rails under its two short ends (USB-C end and antenna end).
    _, cx, cy, lx, ly, h = POCKETS[1]
    with BuildSketch(Plane.XY.offset(T)):
        with Locations((cx, cy - ly / 2 + 1.5), (cx, cy + ly / 2 - 1.5)):
            Rectangle(11.0, 3)   # 11 mm wide: fits between the two pin rows (15.2 mm apart)
    extrude(amount=9)
    # slot in the -Y wall above the rail so a USB-C plug reaches the board for flashing
    with BuildSketch(Plane.XY.offset(T + 7.0)):
        with Locations((cx, cy - ly / 2 - WALL / 2)):
            Rectangle(12.0, WALL + 1.0)
    extrude(amount=10, mode=Mode.SUBTRACT)
    # XL4015 bosses + M2 pilot holes
    _, cx, cy, lx, ly, h = POCKETS[3]
    xl = [(cx + sx * XL_HOLES[0] / 2, cy + sy * XL_HOLES[1] / 2) for sx in (-1, 1) for sy in (-1, 1)]
    with BuildSketch(Plane.XY.offset(T)):
        with Locations(*xl):
            Circle(BOSS_D / 2)
    extrude(amount=BOSS_H)
    with BuildSketch(Plane.XY.offset(T + BOSS_H)):
        with Locations(*xl):
            Circle(M2_PILOT / 2)
    extrude(amount=-(T + BOSS_H), mode=Mode.SUBTRACT)
    # MINI-360 centre pad
    _, cx, cy, lx, ly, h = POCKETS[2]
    with BuildSketch(Plane.XY.offset(T)):
        with Locations((cx, cy)):
            RectangleRounded(*MINI_PAD, 1.0)
    extrude(amount=BOSS_H)
    ms = [(cx + sx * MINI_SO[0] / 2, cy + sy * MINI_SO[1] / 2) for sx in (-1, 1) for sy in (-1, 1)]
    with BuildSketch(Plane.XY.offset(T)):
        with Locations(*ms):
            Circle(MINI_SO_D / 2)
    extrude(amount=BOSS_H)
    with BuildSketch(Plane.XY.offset(T + BOSS_H)):
        with Locations(*ms):
            Circle(MINI_SO_HOLE / 2)
    extrude(amount=-(BOSS_H + 1.0), mode=Mode.SUBTRACT)
    # cable notch on the -Y edge (battery lead from the bay's open side)
    with BuildSketch():
        with Locations((-66.0, -W / 2)):
            RectangleRounded(12, 12, 2)
    extrude(amount=T + 12, mode=Mode.SUBTRACT)

p = tray.part
print("valid", p.is_valid, "vol cm3", round(p.volume / 1000, 2), "bbox", p.bounding_box())
export_stl(p, sys.argv[1] if len(sys.argv) > 1 else "tray_v1.stl")
