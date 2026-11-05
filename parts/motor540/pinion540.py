"""Long pinion for a 540/550: stock C08 (10T, module 1.3) + a hub extension that reaches the 3.17 mm shaft.
Car coords: axis along +Y at x=-129.0, z=-13.56. Motor face at y=57.0 (same as the 775 v2 mount):
  boss 13.0 x 4.5 -> boss bottom y=52.5; shaft 3.17 x 13.0 from face -> shaft tip y=44.0.
Hub r7.5 from y=10.0 (fills the C08 socket) to y=51.7 (0.8 under the boss). Bore 3.30 from y=43.5 (matches the 3.3 mm hole of the PETG 0.2 nozzle bore test, snug on the 3.17 mm shaft).
Shaft grip = 51.7-44.0 = 7.7 mm. M3 grub along -x at y=48.0, square-nut slot open at the top.
A 540 with the long (17 mm) shaft variant gets 11.7 mm of grip with the same part."""
import numpy as np, trimesh
from trimesh.creation import cylinder, box
CX,CZ=-129.0,-13.56
R=trimesh.transformations.rotation_matrix(-np.pi/2,[1,0,0])
def ycyl(r,y0,y1,x=CX,z=CZ,sec=128):
    c=cylinder(radius=r,height=y1-y0,sections=sec); c.apply_transform(R); c.apply_translation([x,(y0+y1)/2,z]); return c
def xcyl(r,x0,x1,y,z=CZ,sec=48):
    c=cylinder(radius=r,height=x1-x0,sections=sec)
    c.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2,[0,1,0])); c.apply_translation([(x0+x1)/2,y,z]); return c
HUB_TOP=51.7; GRUB_Y=48.0
c08=trimesh.load("build/asm_C08_0.stl"); c08.merge_vertices()
p=trimesh.boolean.union([c08,ycyl(7.5,10.0,HUB_TOP)],engine="manifold")
nut=box(extents=[2.1,HUB_TOP+1.0-(GRUB_Y-3.0),5.8]); nut.apply_translation([CX-4.4,(GRUB_Y-3.0+HUB_TOP+1.0)/2,CZ])
for c in [ycyl(1.65,43.5,HUB_TOP+1,sec=64), xcyl(1.6,CX-9.0,CX,GRUB_Y), nut]:
    p=trimesh.boolean.difference([p,c],engine="manifold")
print("pinion540 watertight",p.is_watertight,"vol_cm3",round(p.volume/1000,2),"y",round(p.bounds[0][1],2),round(p.bounds[1][1],2))
p.export("build/car_pinion540.stl")
M=trimesh.transformations.rotation_matrix(np.pi/2,[1,0,0])
q=p.copy(); q.apply_translation([-CX,0,-CZ]); q.apply_transform(M); q.apply_translation([0,0,-q.bounds[0][2]])
q.export("mods/motor540/m540_pinion.stl"); print("print-frame height",round(q.bounds[1][2],2))
