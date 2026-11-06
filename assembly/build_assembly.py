"""Assemble esp-rc v1 in car coordinates, check it, and write the web viewer files.

Inputs:
  - Tarmo5 parts placed in car coordinates (assembly/tarmo5_placed/*.stl + index.json),
    exported from the community STEP assembly by tools/export_world.py
  - our parts (parts/**), the body STLs (vendor/tarmo5/CHASSIS - D01A/B.stl)
Outputs (viewer/): one STL per part, manifest.json, report.json, and three combined STLs.
Run with the build123d venv (needs trimesh + manifold3d + rtree).
"""
import json, os, sys, shutil
import numpy as np, trimesh

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda *a: os.path.join(R, *a)
OUT = P("viewer"); PARTS = os.path.join(OUT, "parts")
shutil.rmtree(PARTS, ignore_errors=True); os.makedirs(PARTS)

def box(ext, ctr):  # ext (dx,dy,dz), ctr (x,y,zmin)
    m = trimesh.creation.box(extents=ext)
    m.apply_translation([ctr[0], ctr[1], ctr[2] + ext[2] / 2]); return m
def cyl(r, h, ctr, axis="z"):
    m = trimesh.creation.cylinder(radius=r, height=h, sections=32)
    if axis == "x": m.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [0, 1, 0]))
    if axis == "y": m.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [1, 0, 0]))
    m.apply_translation(ctr); return m
def T(m, d): m = m.copy(); m.apply_translation(d); return m
U = lambda ms: trimesh.util.concatenate(ms)

items = []   # (name, group, mesh, check)
def add(name, group, mesh, check=True): items.append((name, group, mesh, check))

# ---------------- Tarmo5 (reused) ----------------
REMOVED = {"B09": "replaced by our 540 mount", "C08": "replaced by our long pinion",
           "D3542_OUTRUNNER": "replaced by the 540 motor", "Servo": "replaced by the MG946R"}
idx = json.load(open(P("assembly", "tarmo5_placed", "index.json")))
for r in idx:
    if r["label"] in REMOVED: continue
    m = trimesh.load(P("assembly", "tarmo5_placed", os.path.basename(r["file"])))
    grp = "wheels" if r["label"].startswith("Wheel") else ("hardware" if r["label"].startswith(("M3", "M4", "Part_1")) else "tarmo5")
    add(r["label"] + "_" + os.path.basename(r["file"]).split("__")[1][:-4], grp, m, grp != "wheels")

# ---------------- ours: motor ----------------
for n, f in [("motor_standoff", "car540_standoff.stl"), ("motor_plate", "car540_motorplate.stl"), ("pinion_long", "car_pinion540.stl")]:
    add(n, "ours_printed", trimesh.load(P("assembly", "ours_placed", f)))
add("motor_540", "motor", trimesh.load(P("assembly", "ours_placed", "car_motor540.stl")))

# ---------------- ours: tray + electronics ----------------
TRAY = np.array([64.4, 8.15, 16.44]); FLOOR = TRAY[2] + 5.0
add("electronics_tray", "ours_printed", T(trimesh.load(P("parts", "electronics-tray", "tray_v1.stl")), TRAY))
hx, hy = TRAY[0] + 17.0, TRAY[1]
# H-bridge on DubstepOwl's BTS7960 standoff (vendor/, CC BY): base on the tray floor,
# bolted through the tray's two M3 holes; the IBT_2 screws onto the four post tops.
SO = trimesh.load(P("vendor", "bts7960-standoff", "standoff_upright.stl"))
so_c = (SO.bounds[0] + SO.bounds[1]) / 2
SO = T(SO, (hx - so_c[0], hy - so_c[1], FLOOR - SO.bounds[0][2]))
add("hbridge_standoff", "ours_printed", SO)
PB = SO.bounds[1][2]                       # post tops = underside of the IBT_2 PCB
HS_X, HS_Y, HS_H = 35.0, 50.0, 23.4        # heatsink: 8 fins run along X (perpendicular to the terminal block)
hb = [box((HS_X, HS_Y, HS_H), (hx, hy, PB - HS_H)), box((50, 50, 1.6), (hx, hy, PB)),
      cyl(5.0, 17.0, (hx - 17, hy + 17, PB + 1.6 + 8.5)), box((8, 22, 10), (hx + 19, hy, PB + 1.6)),
      box((16, 9, 3), (hx - 10, hy - 14, PB + 1.6)), box((5, 10, 8.5), (hx - 21, hy - 15, PB + 1.6))]
HB_TOP = PB + 1.6 + 17.0
add("h_bridge_IBT2", "electronics", U(hb))
ex, ey = TRAY[0] - 43.0, TRAY[1] - 10.0; eb = FLOOR + 9.0
add("esp32c3_supermini", "electronics", U([box((18.0, 22.5, 1.6), (ex, ey, eb)), box((13, 13, 2.4), (ex, ey + 3.5, eb + 1.6)),
                                       box((9, 7.5, 3.2), (ex, ey - 9.5, eb + 1.6)),
                                       box((2.5, 20.3, 8.4), (ex - 7.6, ey, eb - 8.4)), box((2.5, 20.3, 8.4), (ex + 7.6, ey, eb - 8.4))]))
mx, my = TRAY[0] - 43.0, TRAY[1] + 17.5
add("mp1584_5V", "electronics", U([box((18.0, 11.5, 1.6), (mx, my, FLOOR + 1.5)), box((6, 6, 3), (mx + 3, my, FLOOR + 3.1))]))   # MH-MINI-360 on its 1.5 mm pad
xx, xy = TRAY[0] - 89.0, TRAY[1]
XF = FLOOR + 1.5   # on its four 1.5 mm M2 bosses
add("xl4015_servo_6V", "electronics", U([box((26, 51, 1.6), (xx, xy, XF)), cyl(5, 13, (xx - 5, xy - 15, XF + 1.6 + 6.5)),
                                        box((12, 12, 8), (xx + 4, xy + 2, XF + 1.6)), box((10, 16, 10), (xx + 5, xy + 17, XF + 1.6))]))

# ---------------- ours: battery ----------------
BAYF = -27.6 + 0.2; MOD = trimesh.load(P("parts", "battery", "battery_module_2s.stl"))
# one 2S module at the back of the bay (the bay is 139.5 mm usable: a second 71.2 mm module does not fit)
cx = -34.8 + 35.6
add("battery_module_2S", "ours_printed", T(MOD, (cx, 8.3, BAYF)))
for dy in (-10.3, 10.3):
    add("cell_18650_" + ("2" if dy > 0 else "1"), "battery", cyl(9.2, 65.2, (cx, 8.3 + dy, BAYF + 1.6 + 9.5), "x"))
add("bms_2s_40A", "electronics", box((50, 22, 4), (70.0, 8.3, BAYF)))

# ---------------- ours: MG946R in the stock servo position ----------------
S = trimesh.load(P("assembly", "tarmo5_placed", "Servo__0.stl"))
Tm = S.bounding_box_oriented.primitive.transform
def mg_local_box(y0, y1, w, l, zc=0.0):
    m = trimesh.creation.box(extents=(w, y1 - y0, l)); m.apply_translation([0, (y0 + y1) / 2, zc]); return m
def mg946r(extra):
    m = U([mg_local_box(-14.8, 20.7 + extra, 19.7, 40.7), mg_local_box(-7.4, -5.3, 19.7, 54.0),
           (lambda c: (c.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [1, 0, 0])), c.apply_translation([0, -17.7, -10.0]), c)[2])(trimesh.creation.cylinder(radius=3.0, height=5.9, sections=24))])
    m.apply_transform(Tm); return m
add("servo_MG946R", "servo", mg946r(1.6))

# ---------------- body (optional skin) ----------------
# The body is a swappable skin: v1 is checked and shown without it.
# Run with --body to add the Tarmo5 pickup shell, cut to clear the electronics.
WITH_BODY = "--body" in sys.argv
POCKET = MOTOR_NOTCH = None
body_stock = {}
if WITH_BODY:
    # ---------------- body remix: pocket over the electronics ----------------
    BODY_D = np.array([268.0, 107.85, -40.0])
    POCKET = dict(x=(TRAY[0] - 108 - 3, TRAY[0] + 45 + 3), y=(TRAY[1] - 29 - 3, TRAY[1] + 29 + 3), z=(30.0, round(HB_TOP + 4.5, 1)))
    pk = trimesh.creation.box(bounds=[[POCKET["x"][0], POCKET["y"][0], POCKET["z"][0]], [POCKET["x"][1], POCKET["y"][1], POCKET["z"][1]]])
    # notch behind the rear wheel arch: the 540 motor (on its 20 mm standoff) pokes out through the +Y side wall
    MOTOR_NOTCH = dict(x=(-151.0, -104.0), y=(80.0, 110.0), z=(-45.0, 7.0))
    pk = trimesh.boolean.union([pk, trimesh.creation.box(bounds=[[MOTOR_NOTCH[k][0] for k in "xyz"], [MOTOR_NOTCH[k][1] for k in "xyz"]])], engine="manifold")
    body_stock = {}
    for half in ("D01A", "D01B"):
        b = T(trimesh.load(P("vendor", "tarmo5", f"CHASSIS - {half}.stl")), BODY_D)
        body_stock[half] = b
        bm = trimesh.boolean.difference([b, pk], engine="manifold")
        add(f"body_{half}_esp", "body", bm)
        # printable copy, back in the designer's frame
        os.makedirs(P("parts", "body"), exist_ok=True)
        T(bm, -BODY_D).export(P("parts", "body", f"{half}_esp.stl"))


# ---------------- checks ----------------
report = {"removed": REMOVED, "pocket_car_coords": POCKET, "motor_notch_car_coords": MOTOR_NOTCH, "overlaps": [], "skipped_not_watertight": [], "notes": []}
ours = [i for i in items if i[1] in ("ours_printed", "motor", "electronics", "battery", "servo")]
others = [i for i in items if i[3] and i not in ours]
def ov(a, b):
    lo = np.maximum(a.bounds[0], b.bounds[0]) - 0.2; hi = np.minimum(a.bounds[1], b.bounds[1]) + 0.2
    if np.any(lo > hi): return 0.0
    if a.is_watertight and b.is_watertight:
        try: return float(trimesh.boolean.intersection([a, b], engine="manifold").volume)
        except Exception: pass
    # fallback: sample the other part's surface (4 points/mm2) and count points inside the watertight one
    w, o = (a, b) if a.is_watertight else (b, a)
    if not w.is_watertight: return None
    pts, _ = trimesh.sample.sample_surface(o, int(min(o.area * 4, 400000)), seed=1)
    m = np.all((pts > lo) & (pts < hi), axis=1); pts = pts[m]
    if not len(pts): return 0.0
    ins = w.contains(pts)
    if ins.sum() == 0: return 0.0
    SAMPLED.append([round(float(ins.sum()) / 4, 1), [round(v, 1) for v in pts[ins].min(0)], [round(v, 1) for v in pts[ins].max(0)]])
    return -float(ins.sum()) / 4   # negative = sampled estimate: mm2 of the other surface inside
SAMPLED = []
for i, (na, ga, ma, _) in enumerate(ours):
    for nb, gb, mb, _ in ours[i + 1:] + others:
        v = ov(ma, mb)
        if v is None: report["skipped_not_watertight"].append([na, nb]); continue
        if v is not None and abs(v) > 0.5:
            r = trimesh.boolean.intersection([ma, mb], engine="manifold") if v > 0 else None
            report["overlaps"].append([na, nb, round(v, 1), "mm3" if v > 0 else "mm2 of surface inside (sampled)",
                                       [[round(x, 1) for x in r.bounds[0]], [round(x, 1) for x in r.bounds[1]]] if r is not None and len(r.vertices) else (SAMPLED[-1][1:] if v < 0 else None)])
# body (stock, unmodified) vs the electronics: shows why the pocket exists
for half, b in body_stock.items():
    v = ov(b, dict((n, m) for n, g, m, _ in items)["h_bridge_IBT2"])
    report["notes"].append(f"stock {half} vs H-bridge overlap mm3: {None if v is None else round(v, 1)}")
report["electronics_top_z_car_coords"] = round(HB_TOP, 1)
report["body_included"] = WITH_BODY
# worst-case MG946R (taller body) check
for extra in (1.6, 5.7):
    m = mg946r(extra); hits = []
    for nb, gb, mb, _ in others:
        v = ov(m, mb)
        if v and abs(v) > 0.5: hits.append([nb, round(v, 1)])
    report[f"mg946r_extra_{extra}mm_overlaps"] = hits
stock_servo = [[nb, round(v, 1)] for nb, gb, mb, _ in others for v in [ov(S, mb) if S.is_watertight else None] if v and v > 0.5]
report["stock_servo_overlaps_for_reference"] = stock_servo

# ---------------- write viewer files ----------------
COL = {"tarmo5": "#9aa3ad", "hardware": "#5d6670", "wheels": "#2b2b2b", "ours_printed": "#f08a24",
       "motor": "#c9ced6", "electronics": "#2f9e5b", "battery": "#2f6fd6", "servo": "#1c1c1c", "body": "#d33f3f"}
man = []
for n, g, m, _ in items:
    fn = f"{g}__{n}.stl".replace(" ", "_"); m.export(os.path.join(PARTS, fn))
    man.append({"name": n, "group": g, "file": "parts/" + fn, "color": COL[g]})
json.dump({"groups": COL, "parts": man}, open(os.path.join(OUT, "manifest.json"), "w"), indent=1)
json.dump(report, open(os.path.join(OUT, "report.json"), "w"), indent=1)
allm = [m for n, g, m, _ in items]
U([m for n, g, m, _ in items if g != "body"]).export(os.path.join(OUT, "esp_rc_v1_chassis.stl"))
if WITH_BODY: U(allm).export(os.path.join(OUT, "esp_rc_v1_with_body.stl"))
U([m for n, g, m, _ in items if g in ("ours_printed",)]).export(os.path.join(OUT, "esp_rc_v1_our_printed_parts_in_place.stl"))
print(json.dumps(report, indent=1)[:6000]); print(len(items), "parts")
