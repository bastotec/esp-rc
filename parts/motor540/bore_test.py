"""Bore test strip: holes 3.1 / 3.2 / 3.3 / 3.4 / 3.5 mm, 8 mm deep, left to right.
Notches on the edge count the hole: 1 notch = 3.1 ... 5 notches = 3.5. Print in PLA, same settings as the pinion."""
import trimesh
from trimesh.creation import box, cylinder
sizes=[3.1,3.2,3.3,3.4,3.5]; pitch=10.0
b=box(extents=[pitch*len(sizes)+4,14,8]); b.apply_translation([0,0,4])
for i,d in enumerate(sizes):
    x=(i-2)*pitch
    h=cylinder(radius=d/2,height=20,sections=96); h.apply_translation([x,1,4])
    b=trimesh.boolean.difference([b,h],engine="manifold")
    for k in range(i+1):
        n=box(extents=[0.8,2.0,20]); n.apply_translation([x-(i)*0.8+k*1.6,-7,4])
        b=trimesh.boolean.difference([b,n],engine="manifold")
b.export("mods/motor540/m540_bore_test.stl"); print("bore test",b.is_watertight,[round(v,1) for v in b.extents])
