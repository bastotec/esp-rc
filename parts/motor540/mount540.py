"""Tarmo5 540/550 motor mount (build123d 0.13). Two printed parts + a long pinion.
Derived from mods/motor775/mount775_v2.py; same lid interface and standoff.

Local frame: motor axis = +Z, origin on the gearbox-lid outer face (car y=37.14) at the axis.
Car coords: x = -129.0 + u, y = 37.14 + h, z = -13.56 - v   (u=X, v=Y, h=Z here).

Fixed by the car (measured from the assembly, tools/ + fitcheck.py):
  lid bolts M4 at (u,v)=(3.98, +-24), threaded into 3.6 mm holes ~14 mm deep in the lid (B01)
  rear B plate (B13-T) blocks anything with u>14.5 below h=18.46 (car y<55.6)
  -> 540 can (r17.9 > 14.5) also needs the face at h>=18.5; we use h=19.86 (car y=57.0)
540 (Mabuchi RS-540RH/SH drawing): can 35.8 x 50 (550: 57), boss 13.0 x 4.5, shaft 3.17 x 13.0 from face,
  2 x M3x0.5 face holes 25 mm apart, usable screw depth 5.0 max.
Assembly: standoff -> lid (2x M4x20). Motor -> motor plate on the bench (2x M3x8: 4 mm plate + 4 mm into the motor).
  Pinion shaft-coupler grub (M3) onto the 540 shaft through the open side of the standoff.
  Motor plate -> standoff (2x M3x16 into captive nuts), heads clear of the motor.
"""
from build123d import *
import sys

FACE_H   = 19.86          # motor face height above lid face
STAND_H  = 11.86          # standoff top
PLATE_T  = FACE_H - STAND_H   # 8 mm motor plate
BOLT     = (3.98, 24.0)   # lid bolts (u, +-v)
JOIN     = (3.98, 32.0)   # M3 joining screws (u, +-v)
FACE_SCR = 12.5           # 540 face screws at (0, +-12.5)
U_MAX    = 13.5           # stay clear of B13-T (u>14.5)

def hull_sketch(circles, plane=Plane.XY):
    with BuildSketch(plane) as s:
        for (x, y, r) in circles:
            with Locations((x, y)):
                Circle(r)
        make_hull()
    return s.sketch

# ---------------- standoff ----------------
with BuildPart() as standoff:
    for sgn in (1, -1):
        prof = hull_sketch([(BOLT[0], sgn*BOLT[1], 7.0), (JOIN[0], sgn*JOIN[1], 5.0)])
        extrude(prof, STAND_H)
    # spine on the +u side joins the two lobes, leaves the -u side open for the grub key
    with BuildSketch() as spine:
        with Locations((11.75, 0)):
            RectangleRounded(3.5, 2*BOLT[1], 1.5)
    extrude(spine.sketch, STAND_H)
    # round the outer vertical edges and the top
    try:
        fillet(standoff.edges().filter_by(Axis.Z), 1.2)
    except Exception as e:
        print("vertical fillet skipped:", e)
    try:
        fillet(standoff.faces().sort_by(Axis.Z)[-1].outer_wire().edges(), 1.0)
    except Exception as e:
        print("top fillet skipped:", e)
    for sgn in (1, -1):
        # lid bolt: clearance + counterbore 6 deep (head 4 + 2 mm for the plate spigot)
        with Locations((BOLT[0], sgn*BOLT[1], 0)):
            Cylinder(2.25, 2*STAND_H, mode=Mode.SUBTRACT)
        with Locations((BOLT[0], sgn*BOLT[1], STAND_H - 3)):
            Cylinder(4.25, 6, mode=Mode.SUBTRACT)
        # M3 join: clearance + hex nut pocket from the bottom (nut is held by the lid face)
        with Locations((JOIN[0], sgn*JOIN[1], 0)):
            Cylinder(1.7, 2*STAND_H, mode=Mode.SUBTRACT)
        with BuildSketch(Plane.XY) as nut:
            with Locations((JOIN[0], sgn*JOIN[1])):
                RegularPolygon(3.25, 6)
        extrude(nut.sketch, 2.8, mode=Mode.SUBTRACT)

# ---------------- motor plate ----------------
with BuildPart() as plate:
    prof = hull_sketch([(0, 0, 11.0), (0, FACE_SCR, 5.0), (0, -FACE_SCR, 5.0),
                        (JOIN[0], JOIN[1], 5.0), (JOIN[0], -JOIN[1], 5.0),
                        (BOLT[0], BOLT[1], 6.0), (BOLT[0], -BOLT[1], 6.0)],
                       plane=Plane.XY.offset(STAND_H))
    extrude(prof, PLATE_T)
    try:
        fillet(plate.faces().sort_by(Axis.Z)[-1].outer_wire().edges(), 2.0)
    except Exception as e:
        print("plate top fillet skipped:", e)
    try:
        fillet(plate.faces().sort_by(Axis.Z)[0].outer_wire().edges(), 0.8)
    except Exception as e:
        print("plate bottom fillet skipped:", e)
    # spigots into the standoff counterbores: concentric location of the motor
    for sgn in (1, -1):
        with Locations((BOLT[0], sgn*BOLT[1], STAND_H - 0.9)):
            Cylinder(4.1, 1.8)
    # boss pilot (13.0 boss -> 13.5 hole, 5 deep) + coupler clearance (bottom)
    with Locations((0, 0, FACE_H - 2.5)):
        Cylinder(6.75, 5.0, mode=Mode.SUBTRACT)
    with Locations((0, 0, STAND_H - 2)):
        Cylinder(10.0, 2*(FACE_H - 5 - STAND_H) + 4, mode=Mode.SUBTRACT)
    for sgn in (1, -1):
        # 540 face screws (M3): clearance + head counterbore from below, 4 mm of plate left
        with Locations((0, sgn*FACE_SCR, STAND_H)):
            Cylinder(1.7, 4*PLATE_T, mode=Mode.SUBTRACT)
        with Locations((0, sgn*FACE_SCR, STAND_H - 2 + 2.0)):
            Cylinder(3.1, 4.0 + 4, mode=Mode.SUBTRACT)
        # M3 join: clearance + head counterbore from the top
        with Locations((JOIN[0], sgn*JOIN[1], STAND_H)):
            Cylinder(1.7, 4*PLATE_T, mode=Mode.SUBTRACT)
        with Locations((JOIN[0], sgn*JOIN[1], FACE_H)):
            Cylinder(3.1, 6.0, mode=Mode.SUBTRACT)
    # lightening pockets between boss and join screws (cosmetic + mass)
    for sgn in (1, -1):
        with BuildSketch(Plane.XY.offset(FACE_H)) as pk:
            with Locations((-5.5, sgn*24.0)):
                SlotOverall(10, 4.5, rotation=90)
        extrude(pk.sketch, -4.0, mode=Mode.SUBTRACT)

for name, p in (("standoff", standoff.part), ("motorplate", plate.part)):
    bb = p.bounding_box()
    print(name, "valid", p.is_valid, "vol_cm3", round(p.volume/1000, 2),
          "u", round(bb.min.X,2), round(bb.max.X,2), "v", round(bb.min.Y,2), round(bb.max.Y,2),
          "h", round(bb.min.Z,2), round(bb.max.Z,2))
    export_stl(p, f"mods/motor540/m540_{name}_local.stl", tolerance=0.02, angular_tolerance=0.15)
