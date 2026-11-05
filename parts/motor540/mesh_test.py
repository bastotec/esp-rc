"""Gear mesh test (slimmed to stay under 1 h on the 0.2 mm nozzle): our long pinion (on the 540) against a 90-degree slice of the real Tarmo5 main gear C07.
A link rides on the pinion's smooth r7.5 hub (above the 25 mm flange) and carries a peg 38.98 mm away,
the C07-C08 centre distance in the car model. The gear slice turns on the peg, held by an M3 screw + washer.
Car frame: pinion axis along y at x=-129.0, z=-13.56; C07 axis at x=-90.02, z=-13.56 (from asm_C07_0.stl).
Run from ~/src/esp-rc with the tarmo5 venv. Inputs from ~/src/tarmo5-fpv/build (car-frame STLs)."""
import sys, numpy as np, trimesh
from trimesh.creation import cylinder, box
B = sys.argv[1] if len(sys.argv) > 1 else "/home/bruno/src/tarmo5-fpv/build"
PX, PZ = -129.0, -13.56
GX, GZ = -90.02, -13.56
R = trimesh.transformations.rotation_matrix(-np.pi/2, [1, 0, 0])
def ycyl(r, y0, y1, x, z=PZ, sec=128):
    c = cylinder(radius=r, height=y1-y0, sections=sec); c.apply_transform(R); c.apply_translation([x, (y0+y1)/2, z]); return c
U = lambda a: trimesh.boolean.union(a, engine="manifold")
D = lambda a, b: trimesh.boolean.difference([a, b], engine="manifold")
I = lambda a, b: trimesh.boolean.intersection([a, b], engine="manifold")

# --- gear slice: real C07 teeth, y 1.5..5.5, 90-degree sector facing the pinion, own hub on a 6 mm peg
G0, G1 = 2.5, 5.5
c07 = trimesh.load(f"{B}/asm_C07_0.stl"); c07.merge_vertices()
ang = np.radians(np.linspace(135, 225, 31))       # sector centred on -x (towards the pinion)
pts = [[GX, G0, GZ], [GX, G1, GZ]]
for a in ang:
    for y in (G0, G1): pts.append([GX + 45*np.cos(a), y, GZ + 45*np.sin(a)])
wedge = trimesh.convex.convex_hull(np.array(pts))
rim = D(I(c07, wedge), ycyl(28.0, G0-1, G1+1, GX))          # teeth ring r28..tip
spoke = box(extents=[28.5, G1-G0, 6.0]); spoke.apply_translation([GX-14.25, (G0+G1)/2, GZ])
hubr = ycyl(5.5, G0, G1, GX, sec=96)
gear = D(U([rim, spoke, hubr]), ycyl(3.2, G0-1, G1+1, GX, sec=64))   # 6.4 bore on the 6.0 peg

# --- link: ring on the pinion hub (y 24..30), arm y 27..30, shoulder down to the gear, 6 mm pin through it
ring = D(ycyl(9.75, 24.0, 30.0, PX), ycyl(7.75, 21.0, 31.0, PX))   # 15.5 bore on the r7.5 hub
arm = box(extents=[GX-PX, 3.0, 6.0]); arm.apply_translation([(PX+GX)/2, 28.5, PZ])
shoulder = ycyl(4.25, G1+0.3, 30.0, GX)
pin = ycyl(3.0, G0-0.8, G1+0.3, GX, sec=96)
link = U([ring, arm, shoulder, pin])
link = D(link, ycyl(7.75, 21.0, 31.0, PX))                 # keep the ring bore clear of the arm
link = D(link, ycyl(1.25, G0-1.0, G0+8.0, GX, sec=48))      # 2.5 pilot hole, M3 self-taps into the pin end

pin540 = trimesh.load(f"{B}/car_pinion540.stl")
rep = {}
for n, m in [("gear", gear), ("link", link)]:
    rep[n] = dict(watertight=bool(m.is_watertight), vol_cm3=round(m.volume/1000, 2))
rep["overlap_mm3"] = {
    "gear-pinion (tooth mesh, stock car shows the same)": round(I(gear, pin540).volume, 2) if I(gear, pin540).volume > 0 else 0.0,
    "link-pinion": round(I(link, pin540).volume, 2),
    "link-gear": round(I(link, gear).volume, 2)}
# stock reference: real C07 vs our pinion
rep["overlap_mm3"]["C07-pinion in car model"] = round(I(c07, pin540).volume, 2)
print(rep)
gear.export("build/car_mesh_gear.stl"); link.export("build/car_mesh_link.stl")
# print frames: gear flat (y up), link with the arm face (y=30) on the bed
M = trimesh.transformations.rotation_matrix(np.pi/2, [1, 0, 0])
g = gear.copy(); g.apply_translation([-GX, 0, -GZ]); g.apply_transform(M); g.apply_translation([0, 0, -g.bounds[0][2]])
L = link.copy(); L.apply_translation([-(PX+GX)/2, 0, -PZ]); L.apply_transform(trimesh.transformations.rotation_matrix(-np.pi/2, [1, 0, 0])); L.apply_translation([0, 0, -L.bounds[0][2]])
print("gear print extents", g.extents.round(1), "link print extents", L.extents.round(1))
g.export("parts/motor540/mesh_test_gear.stl"); L.export("parts/motor540/mesh_test_link.stl")
