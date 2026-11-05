"""Motor plate fit test: a 3 mm slice of the 540 motor plate (mount540.py) with the same motor-face layout.
Checks the 540's 2x M3 face screws (25 mm apart) and its front boss (13.0 -> 13.5 mm hole) line up.
Use 2x M3x6 (3 mm plate + 3 mm into the motor; the motor allows 5 mm max)."""
from build123d import *
FACE_SCR = 12.5
T = 3.0
with BuildPart() as p:
    with BuildSketch() as s:
        Circle(11.0)
        for sg in (1, -1):
            with Locations((0, sg*FACE_SCR)):
                Circle(5.0)
        make_hull()
    extrude(amount=T)
    Cylinder(6.75, 2*T, mode=Mode.SUBTRACT)            # boss hole, same 13.5 mm as the real plate
    for sg in (1, -1):
        with Locations((0, sg*FACE_SCR, 0)):
            Cylinder(1.7, 2*T, mode=Mode.SUBTRACT)     # M3 clearance, same 3.4 mm as the real plate
part = p.part
print("valid", part.is_valid, "vol_cm3", round(part.volume/1000, 2), "bbox", part.bounding_box().size)
export_stl(part, "parts/motor540/plate_fit_test.stl")
