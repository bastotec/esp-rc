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
    ("mp1584",  -43.0, 17.5, 24.0, 19.0, 4.0),
    ("xl4015",  -89.0, 0.0, 28.0, 53.0, 4.0),      # turned across the car
]
BOLTS = [(sx * 22.5, sy * 10.0) for sx in (-1, 1) for sy in (-1, 1)]

with BuildPart() as tray:
    with BuildSketch():
        with Locations(((X0 + X1) / 2, 0)):
            RectangleRounded(X1 - X0, W, 6)
    extrude(amount=T)
    for name, cx, cy, lx, ly, h in POCKETS:
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
    # zip-tie slots through the floor beside each pocket
    for name, cx, cy, lx, ly, h in POCKETS:
        for dx in (-lx / 4, lx / 4):
            with BuildSketch():
                with Locations((cx + dx, cy - ly / 2 - WALL - 0.5), (cx + dx, cy + ly / 2 + WALL + 0.5)):
                    Rectangle(4.2, 2.4)
            extrude(amount=T + 12, mode=Mode.SUBTRACT)
    # vents under the H-bridge heatsink (kept clear of the bolt counterbores)
    _, cx, cy, lx, ly, h = POCKETS[0]
    with BuildSketch():
        with Locations((cx - 6, cy), (cx - 6, cy - 18), (cx - 6, cy + 18)):
            SlotCenterToCenter(22, 4)
    extrude(amount=T + 12, mode=Mode.SUBTRACT)
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
    # cable notch on the -Y edge (battery lead from the bay's open side)
    with BuildSketch():
        with Locations((-66.0, -W / 2)):
            RectangleRounded(12, 12, 2)
    extrude(amount=T + 12, mode=Mode.SUBTRACT)

p = tray.part
print("valid", p.is_valid, "vol cm3", round(p.volume / 1000, 2), "bbox", p.bounding_box())
export_stl(p, sys.argv[1] if len(sys.argv) > 1 else "tray_v1.stl")
