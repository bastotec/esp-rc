"""Write a light, single-file copy of the assembled car for a web/phone 3D viewer,
from the per-part STLs in viewer/parts (listed in viewer/manifest.json).
Usage: python -I tools/viewer_lod.py OUT.stl FACE_BUDGET [group,group,...]"""
import sys, json, os, trimesh
man = json.load(open("viewer/manifest.json"))["parts"]
want = set(sys.argv[3].split(",")) if len(sys.argv) > 3 else None
ms = [(p, trimesh.load(os.path.join("viewer", p["file"]))) for p in man if want is None or p["group"] in want]
tot = sum(len(m.faces) for _, m in ms); n = int(sys.argv[2]); out = []
for p, m in ms:
    k = max(80, int(len(m.faces) * n / tot))
    out.append(m.simplify_quadric_decimation(face_count=k) if len(m.faces) > k else m)
r = trimesh.util.concatenate(out); r.export(sys.argv[1])
print(len(ms), "parts,", tot, "->", len(r.faces), "faces")
