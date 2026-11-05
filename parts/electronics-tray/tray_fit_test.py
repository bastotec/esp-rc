"""Electronics tray fit test: the four pocket rims of tray.py as open frames, 3 mm tall,
plus the motor plate fit test, laid out on one bed. Same inner sizes and 2 mm walls as the real tray.
Drop each board into its frame: it should go in without forcing and not slide around much.
Pocket sizes copied from parts/electronics-tray/tray.py (POCKETS); keep them in sync."""
from build123d import *
import sys
WALL, H = 1.0, 2.0   # fit test only: inner sizes match the tray, walls thinner and lower to print fast
# (name, inner_x, inner_y, bed_x, bed_y)
FRAMES = [
    ("hbridge", 52.0, 52.0, -35.0, 25.0),
    ("xl4015", 28.0, 53.0, 12.0, 25.0),
    ("esp32", 56.0, 30.0, -30.0, -22.0),
    ("mp1584", 24.0, 19.0, 20.0, -22.0),
]
with BuildPart() as p:
    for name, lx, ly, bx, by in FRAMES:
        with BuildSketch():
            with Locations((bx, by)):
                RectangleRounded(lx + 2 * WALL, ly + 2 * WALL, 3)
                RectangleRounded(lx, ly, 1.5, mode=Mode.SUBTRACT)
        extrude(amount=H)
    # ESP32 end rails (as in the tray: pins clear of the antenna and USB ends)
    with BuildSketch():
        with Locations((-30.0 - 28 + 1.5, -22.0), (-30.0 + 28 - 1.5, -22.0)):
            Rectangle(3, 30)
    extrude(amount=H)
frames = p.part
plate = import_stl("parts/motor540/plate_fit_test.stl")
plate = Pos(45, 25, 0) * plate
print("frames valid", frames.is_valid, "vol_cm3", round(frames.volume / 1000, 2), "bbox", frames.bounding_box().size)
export_stl(frames, "parts/electronics-tray/tray_fit_test.stl")
export_stl(Compound([frames, plate]), "/tmp/fit_bed.stl")
print("bed bbox", Compound([frames, plate]).bounding_box())
