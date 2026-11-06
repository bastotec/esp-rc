"""Build viewer/original/car.glb from the stock Tarmo5 export (build/world of tarmo5-fpv)."""
import json, os, sys, collections, trimesh, numpy as np
src = sys.argv[1]; out = sys.argv[2]; N = int(sys.argv[3]) if len(sys.argv) > 3 else 220000
rows = json.load(open(os.path.join(src, "index.json")))
seen = collections.Counter(); parts = []
for r in rows:
    lab = r["label"]; i = seen[lab]; seen[lab] += 1
    if lab in ("M3-Nut", "Part_1") or lab.startswith("M4x"): g = "hardware"
    elif lab.startswith("Wheel"): g = "wheels"
    elif lab == "D3542_OUTRUNNER": g = "motor"
    elif lab == "Servo": g = "servo"
    else: g = "tarmo5"
    fn = os.path.join(src, os.path.basename(r["file"]))
    parts.append((f"{lab}_{i}", g, trimesh.load(fn)))
tot = sum(len(m.faces) for *_, m in parts)
sc = trimesh.Scene(); info = []; worst = 0
for n, g, m in parts:
    k = max(80, int(len(m.faces) * N / tot))
    d = m.simplify_quadric_decimation(face_count=k) if len(m.faces) > k else m.copy()
    dv = float(np.abs(d.bounds - m.bounds).max()); worst = max(worst, dv)
    d.visual = trimesh.visual.ColorVisuals(d)
    sc.add_geometry(d, node_name=n, geom_name=n)
    b = m.bounds
    info.append({"name": n, "group": g, "faces": len(d.faces), "bmin": [round(float(v), 2) for v in b[0]], "bmax": [round(float(v), 2) for v in b[1]], "bbox_change_mm": round(dv, 2)})
os.makedirs(out, exist_ok=True)
open(os.path.join(out, "car.glb"), "wb").write(sc.export(file_type="glb"))
json.dump(info, open(os.path.join(out, "parts.json"), "w"), indent=0)
print(len(parts), "parts", tot, "->", sum(i["faces"] for i in info), "faces; worst bbox change", round(worst, 2), "mm; glb", os.path.getsize(os.path.join(out, "car.glb")) // 1024, "KB")
print(collections.Counter(i["group"] for i in info))
print([i["name"] for i in info if i["group"] in ("motor", "servo")] + [i["name"] for i in info if i["name"].startswith(("C08", "B09", "Servo_Horn", "Part_1_3"))])
