"""Build viewer/web/car.glb: every part as a named mesh in car coordinates (mm, Z up)."""
import json, os, sys, trimesh, numpy as np
man = json.load(open("viewer/manifest.json"))["parts"]
ms = [(p, trimesh.load(os.path.join("viewer", p["file"]))) for p in man]
tot = sum(len(m.faces) for _, m in ms); N = int(sys.argv[1]) if len(sys.argv) > 1 else 240000
sc = trimesh.Scene(); info = []; worst = 0
for p, m in ms:
    k = max(80, int(len(m.faces) * N / tot))
    d = m.simplify_quadric_decimation(face_count=k) if len(m.faces) > k else m.copy()
    dv = float(np.abs(d.bounds - m.bounds).max()); worst = max(worst, dv)
    d.visual = trimesh.visual.ColorVisuals(d)
    sc.add_geometry(d, node_name=p["name"], geom_name=p["name"])
    b = m.bounds
    info.append({"name": p["name"], "group": p["group"], "faces": len(d.faces), "bmin": [round(float(v), 2) for v in b[0]], "bmax": [round(float(v), 2) for v in b[1]], "bbox_change_mm": round(dv, 2)})
os.makedirs("viewer/web", exist_ok=True)
open("viewer/web/car.glb", "wb").write(sc.export(file_type="glb"))
json.dump(info, open("viewer/web/parts.json", "w"), indent=0)
print(len(ms), "parts", tot, "->", sum(i["faces"] for i in info), "faces; worst bbox change", round(worst, 2), "mm; glb", os.path.getsize("viewer/web/car.glb") // 1024, "KB")
print(sorted(((i["bbox_change_mm"], i["name"]) for i in info), reverse=True)[:6])
