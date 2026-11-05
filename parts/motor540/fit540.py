"""Place the 540 parts and a 540 (or 550) envelope in car coordinates; report overlaps (mm^3) and closest gaps (mm).
Envelope from the Mabuchi RS-540 drawing: can r17.9; rear end-bell r12.2 x 4 + terminal tabs (taken as r17.9 x 3.5);
boss r6.5 x 4.5; shaft r1.585 x 13. 550 = same with a 57 mm can."""
import sys, numpy as np, trimesh, itertools
from trimesh.creation import cylinder
from scipy.spatial import cKDTree
CX,CZ,LID=-129.0,-13.56,37.14
L2C=np.array([[1,0,0,CX],[0,0,1,LID],[0,-1,0,CZ],[0,0,0,1]],float)
def ycyl(r,y0,y1):
    c=cylinder(radius=r,height=y1-y0,sections=64)
    c.apply_transform(trimesh.transformations.rotation_matrix(-np.pi/2,[1,0,0])); c.apply_translation([CX,(y0+y1)/2,CZ]); return c
YF=57.0
def motor(L):
    return trimesh.boolean.union([ycyl(17.9,YF,YF+L),ycyl(17.9,YF+L,YF+L+3.5),ycyl(12.2,YF+L,YF+L+4),ycyl(6.5,YF-4.5,YF),ycyl(1.585,YF-13,YF)],engine="manifold")
P={}
for n in ("standoff","motorplate"):
    m=trimesh.load(f"mods/motor540/m540_{n}_local.stl"); m.apply_transform(L2C); P[n]=m; m.export(f"build/car540_{n}.stl")
P["pinion"]=trimesh.load("build/car_pinion540.stl")
P["motor540"]=motor(50.0); P["motor550"]=motor(57.0)
P["motor540"].export("build/car_motor540.stl"); P["motor550"].export("build/car_motor550.stl")
car={k:trimesh.load(f"build/{f}") for k,f in [("B01 lid","near_B01_3.stl"),("B13-T","near_B13-T_2.stl"),("A02 upper","near_A02_5.stl"),("A02 lower","near_A02_6.stl"),("A03 hub","near_A03_7.stl"),("C07 gear","asm_C07_0.stl"),("B02","near_B02_1.stl")]}
def cloud(m,n=30000): return np.vstack([m.sample(n),m.vertices])
def gap(a,b): return cKDTree(cloud(a)).query(cloud(b),k=1)[0].min()
def ov(a,b):
    try: return trimesh.boolean.intersection([a,b],engine="manifold").volume
    except Exception: return float("nan")
print("watertight",{k:v.is_watertight for k,v in P.items()})
for pn,pm in P.items():
    for cn,cm in car.items():
        if pm.bounds[0][0]>cm.bounds[1][0]+30 or pm.bounds[1][0]<cm.bounds[0][0]-30: continue
        o=ov(pm,cm); g=gap(pm,cm) if o<0.5 else float("nan")
        print(f"{pn:10s} vs {cn:10s} overlap {o:8.2f} mm3  gap {g:6.2f}")
for a,b in itertools.combinations(["standoff","motorplate","pinion","motor540"],2):
    print(f"{a:10s} vs {b:10s} overlap {ov(P[a],P[b]):8.2f} mm3")
