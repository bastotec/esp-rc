"""esp-rc 2S battery module (build123d 0.13).

Holds two 18650 cells side by side, in series: a U-link contact plate joins
them at one end, the + and - leads come out at the other. One module = 2 cells
(the 7.4 V pack). It sits at the back of the Tarmo5 centre-chassis bay; the
2S BMS goes on the bay floor in front of it.

Bay (measured from the STEP model): usable 139.5 mm long (x -35.0 to 104.5:
a rounded corner at the back, a thicker front wall on one side), 132 mm side
opening, 51 mm wide (open on one side), 38 mm floor to ceiling. A second
71.2 mm module does NOT fit, so 4 cells (2S2P) would need a shorter holder.

Contacts: standard 18650 holder spring/plate contacts (about 12 mm wide, 0.5 mm
thick) pushed into the slots. Cells: unprotected flat or button top, 65-67 mm.
Strap: 20 mm hook-and-loop through the two floor slots, over the cells.
Frame: x along the cells, y across, z up; origin at the floor centre.
"""
from build123d import *
import sys

CELL_D = 18.4
CRADLE = 19.0            # cradle diameter
INNER_L = 68.0           # cell 65-67 + spring
WALL, DIV, FLOOR = 1.6, 1.6, 1.6
L = INNER_L + 2 * WALL   # 71.2
Wd = 2 * CRADLE + 3 * DIV   # 42.8
H_SIDE = FLOOR + 14.0
H_END = FLOOR + CELL_D + 1.0
ROWS = [-(CRADLE + DIV) / 2, (CRADLE + DIV) / 2]
ZC = FLOOR + CRADLE / 2

with BuildPart() as mod:
    Box(L, Wd, H_SIDE, align=(Align.CENTER, Align.CENTER, Align.MIN))
    # end walls, full height
    for sx in (-1, 1):
        with Locations((sx * (L - WALL - 3.0) / 2 * 1.0 + 0, 0, 0)):
            pass
    with BuildSketch():
        with Locations((-(L - 5) / 2, 0), ((L - 5) / 2, 0)):
            Rectangle(5, Wd)
    extrude(amount=H_END)
    # cradles: cylinder seats + open top
    for y in ROWS:
        with Locations((0, y, ZC)):
            Cylinder(CRADLE / 2, INNER_L, rotation=(0, 90, 0), mode=Mode.SUBTRACT)
        with BuildSketch(Plane.XY.offset(ZC)):
            with Locations((0, y)):
                Rectangle(INNER_L, CRADLE)
        extrude(amount=H_END, mode=Mode.SUBTRACT)
    # contact slots, 1.2 mm thick, 0.8 mm in from each inner end face
    xs = INNER_L / 2 - 0.8 - 0.6
    with BuildSketch(Plane.XY.offset(FLOOR + 2.0)):
        # terminal end (-X): one slot per cell
        with Locations((-xs, ROWS[0]), (-xs, ROWS[1])):
            Rectangle(1.2, 13.0)
        # link end (+X): one slot across both cells
        with Locations((xs, 0)):
            Rectangle(1.2, 2 * CRADLE + DIV - 4)
    extrude(amount=H_END, mode=Mode.SUBTRACT)
    # lead exits through the terminal end wall
    with BuildSketch(Plane.YZ.offset(-L / 2 - 1)):
        with Locations((ROWS[0], H_END - 2.5), (ROWS[1], H_END - 2.5)):
            Rectangle(4.0, 5.0)
    extrude(amount=6, mode=Mode.SUBTRACT)
    # strap slots through the floor
    with BuildSketch():
        with Locations((-20, 0), (20, 0)):
            Rectangle(3.0, 22.0)
    extrude(amount=FLOOR + 1, mode=Mode.SUBTRACT)
    # polarity marker: notch on the + corner of the terminal end
    with BuildSketch(Plane.XY.offset(H_END - 2)):
        with Locations((-L / 2 + 1.0, ROWS[1] + CRADLE / 2)):
            Rectangle(2.0, 2.0)
    extrude(amount=3, mode=Mode.SUBTRACT)

p = mod.part
print("valid", p.is_valid, "vol cm3", round(p.volume / 1000, 2), "bbox", p.bounding_box())
export_stl(p, sys.argv[1] if len(sys.argv) > 1 else "battery_module_2s.stl")
