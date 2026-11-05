"""Export every leaf of the Tarmo5 STEP assembly to build/world/ as STL in car
coordinates (sub-assembly placements composed). Coarse tessellation for viewing."""
import sys, json, os
from build123d import *
a = import_step(sys.argv[1])
out = sys.argv[2] if len(sys.argv) > 2 else "build/world"
rows = []; seen = {}
def walk(n, acc):
    ch = list(getattr(n, "children", []) or [])
    if ch:
        nxt = acc * n.location if n.label not in ("tarmo5",) else acc
        # compound children carry parent-local placement: compose
        for c in ch:
            walk(c, nxt if isinstance(n, Compound) and n.label not in ("tarmo5", "Chassis") else acc)
        return
    s = n.moved(acc) if acc is not None else n
    lab = n.label.replace("/", "_")
    i = seen.get(lab, 0); seen[lab] = i + 1
    fn = f"{out}/{lab}__{i}.stl"
    export_stl(s, fn, tolerance=0.15, angular_tolerance=0.4)
    b = s.bounding_box()
    rows.append(dict(label=n.label, file=fn, min=list(b.min), max=list(b.max)))
walk(a, Location())
json.dump(rows, open(f"{out}/index.json", "w"), indent=1)
print(len(rows), "parts")
