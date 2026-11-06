"""Add typical electronics (battery, ESC, receiver) as simple blocks to the original Tarmo5 web model.

usage: orig_electronics.py viewer/original [assembly/tarmo5_placed]
Reads car.glb + parts.json in place (idempotent: re-running replaces the blocks) and, if the placed STLs are given,
runs a block-vs-every-other-part clash check (triangle/box SAT on the full-resolution STLs). Coordinates = car frame, mm.
Battery position follows the design (B03 bay, B08-T clip); ESC/receiver positions are typical, not from the designer.
"""
import json, os, sys, numpy as np, trimesh
d = sys.argv[1]; placed = sys.argv[2] if len(sys.argv) > 2 else None
GROUP = "electronics"
# bay: floor z=-27.6 (corner fillets to -26.6), ceiling 10.4, rear wall x=-38.1, front wall x=104.9, +y wall y=30.1, clip tooth y=-15.86; top deck z=16.4; centre line y=8.14
BLOCKS = {
 "zeee_3s_lipo_3200":  ((33.4, 7.1, -27.6 + 13.0 + 1.0), (138, 45.6, 26)),
 "esc_1_10_brushless": ((63.5, 8.14, 16.4 + 17.5), (50, 40, 35)),
 "receiver_2ch":       ((12.0, 8.14, 16.4 + 6.0), (35, 22, 12)),
}
def box(c, s):
    m = trimesh.creation.box(extents=s); m.apply_translation(c); return m

def tri_box_overlap(tris, c, h, eps=0.0):
    """Akenine-Moller SAT, tris (n,3,3), box centre c half-size h. returns bool (n,) of triangles that penetrate by > eps."""
    h = h - eps; v = tris - c; n = len(v); ok = np.ones(n, bool)
    e = np.stack([v[:,1]-v[:,0], v[:,2]-v[:,1], v[:,0]-v[:,2]], 1)
    for a in range(3):  # box axes
        ok &= (v[:,:,a].min(1) <= h[a]) & (v[:,:,a].max(1) >= -h[a])
    nrm = np.cross(e[:,0], e[:,1]); r = (np.abs(nrm) * h).sum(1)
    ok &= np.abs((nrm * v[:,0]).sum(1)) <= r
    for i in range(3):
        for a in range(3):
            ax = np.zeros(3); ax[a] = 1
            L = np.cross(ax, e[:,i])
            p = np.einsum('nj,nkj->nk', L, v)
            r = (np.abs(L) * h).sum(1)
            ok &= (p.min(1) <= r) & (p.max(1) >= -r)
    return ok

sc = trimesh.load(os.path.join(d, "car.glb"), force="scene")
info = json.load(open(os.path.join(d, "parts.json")))
info = [i for i in info if i["group"] != GROUP]
for n in list(sc.geometry):
    if n in BLOCKS: sc.delete_geometry(n)
for n, (c, s) in BLOCKS.items():
    m = box(c, s); m.visual = trimesh.visual.ColorVisuals(m)
    sc.add_geometry(m, node_name=n, geom_name=n)
    b = m.bounds
    info.append({"name": n, "group": GROUP, "faces": len(m.faces), "bmin": [round(float(v),2) for v in b[0]],
                 "bmax": [round(float(v),2) for v in b[1]], "bbox_change_mm": 0.0})
open(os.path.join(d, "car.glb"), "wb").write(sc.export(file_type="glb"))
json.dump(info, open(os.path.join(d, "parts.json"), "w"), indent=0)
print("parts now", len(info), "of which electronics", sum(i["group"] == GROUP for i in info))

if placed:
    bad = 0
    for n, (c, s) in BLOCKS.items():
        c = np.array(c); h = np.array(s) / 2
        for f in sorted(os.listdir(placed)):
            if not f.endswith(".stl"): continue
            m = trimesh.load(os.path.join(placed, f))
            if (m.bounds[1] < c - h).any() or (m.bounds[0] > c + h).any(): continue
            tri = m.triangles; hit = tri_box_overlap(tri, c, h, eps=0.05)
            inside = False
            if not hit.any():  # box wholly inside a solid part? ray parity from the centre
                loc, _, _ = m.ray.intersects_location([c], [[0,0,1.]], multiple_hits=True)
                inside = (len(loc) % 2 == 1)
            if hit.any() or inside:
                bad += 1; print("CLASH", n, "vs", f, int(hit.sum()), "triangles", "(inside)" if inside else "")
    print("clash check:", "FAIL %d" % bad if bad else "PASS (no overlap > 0.05 mm with any of the other parts)")
    names = list(BLOCKS)
    for i, a in enumerate(names):
        for b in names[i+1:]:
            ca, sa = map(np.array, BLOCKS[a]); cb, sb = map(np.array, BLOCKS[b])
            ov = (np.abs(ca - cb) < (sa + sb) / 2 - 0.05).all(); print("blocks", a, b, "OVERLAP" if ov else "clear")
