"""esp-rc electronics tray v0 (build123d 0.13).

Bolts to the four 5 mm holes on top of the Tarmo5 centre chassis (B03):
a 45 mm (along the car) x 20 mm (across) pattern, measured from the
community STEP assembly. Frame: origin = centre of that hole pattern on
B03's top face (z=0), +X = towards the front of the car.

Holds, from rear to front (all zip-tied, so exact board hole spacings
don't matter): XL4015 (servo 5.5 V), ESP32 DevKit + MP1584 side by side,
IBT_2 / BTS7960 H-bridge (heatsink down, vented side walls).
"""
from build123d import *
import sys

W = 58.0          # B03 top width
X0, X1 = -108.0, 45.0   # on B03 top (B03 rear lip at -125.9, front end at +45.5)
T = 3.0           # floor
WALL = 2.0
HOLE = 3.4        # M3 clearance; B03's holes are 5 mm (insert/what goes there: unverified)

# pockets: (name, x_centre, y_centre, length_x, width_y, wall_h)
POCKETS = [
    ("hbridge", 17.0, 0.0, 52.0, 52.0, 6.0),
    ("esp32",   -43.0, -10.0, 56.0, 30.0, 11.0),   # board sits on 9 mm end rails: header pins hang below
    ("mp1584",  -43.0, 17.5, 24.0, 19.0, 4.0),
    ("xl4015",  -89.0, 0.0, 28.0, 53.0, 4.0),     # turned across the car
]
BOLTS = [(sx * 22.5, sy * 10.0) for sx in (-1, 1) for sy in (-1, 1)]

with BuildPart() as tray:
    with BuildSketch():
        with Locations(((X0 + X1) / 2, 0)):
            RectangleRounded(X1 - X0, W, 6)
    extrude(amount=T)
    # pocket rims
    for name, cx, cy, lx, ly, h in POCKETS:
        with BuildSketch(Plane.XY.offset(T)):
            with Locations((cx, cy)):
                RectangleRounded(lx + 2 * WALL, ly + 2 * WALL, 3)
                RectangleRounded(lx, ly, 1.5, mode=Mode.SUBTRACT)
        extrude(amount=h)
    # bolt holes + counterbores
    with Locations(*[(x, y, 0) for x, y in BOLTS]):
        Hole(HOLE / 2, depth=T + 10)
    with Locations(*[(x, y, T) for x, y in BOLTS]):
        CounterBoreHole(HOLE / 2, 3.1, 2.0, depth=T)  # M3 button head
    # zip-tie slots: 4 x 2.2 mm pairs across each pocket
    for name, cx, cy, lx, ly, h in POCKETS:
        for dx in (-lx / 4, lx / 4):
            with BuildSketch():
                with Locations((cx + dx, cy - ly / 2 - WALL - 0.5), (cx + dx, cy + ly / 2 + WALL + 0.5)):
                    Rectangle(4.2, 2.4)
            extrude(amount=T + 10, mode=Mode.SUBTRACT)
    # vents in the H-bridge floor (heatsink sits on them)
    name, cx, cy, lx, ly, h = POCKETS[0]
    with BuildSketch():
        with Locations((cx, cy), (cx, cy - 18), (cx, cy + 18)):
            SlotCenterToCenter(32, 4)
    extrude(amount=T + 10, mode=Mode.SUBTRACT)
    # lightening under the ESP32 area (between bolts)
    with BuildSketch():
        with Locations((-89, 0)):
            SlotCenterToCenter(30, 10, rotation=90)
    extrude(amount=T + 10, mode=Mode.SUBTRACT)
    # ESP32 end rails (no pins at the antenna and USB ends)
    _, cx, cy, lx, ly, h = POCKETS[1]
    with BuildSketch(Plane.XY.offset(T)):
        with Locations((cx - lx / 2 + 1.5, cy), (cx + lx / 2 - 1.5, cy)):
            Rectangle(3, ly)
    extrude(amount=9)

p = tray.part
print("valid", p.is_valid, "vol cm3", round(p.volume / 1000, 2), "bbox", p.bounding_box())
out = sys.argv[1] if len(sys.argv) > 1 else "tray_v0.stl"
export_stl(p, out)
