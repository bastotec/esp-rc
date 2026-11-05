# 540/550 motor mod

Replaces the stock D3542 brushless motor with a standard **540 or 550 brushed motor** (36 mm can), driven by our ESP32 + BTS7960 electronics. It replaces the 775 attempt in [`../motor775`](../motor775), because a 42 mm 775 hits the upper rear arm (A02).

**Status: design draft, fit-checked in the CAD assembly only. Not printed or test-fitted.**

## Motor dimensions used (Mabuchi RS-540RH/SH datasheet)
- Can Ø35.8 × 50 mm (550: × 57 mm)
- Front boss Ø13.0 × 4.5 mm
- Shaft Ø3.17 mm, 13.0 mm out from the motor face (a long-shaft variant has 17.0 mm)
- 2 × M3×0.5 tapped face holes, 25 mm apart; screws must not go more than 5 mm into the motor

## Parts (all PLA)
| File | Part | Notes |
|---|---|---|
| `m540_standoff_local.stl` | Standoff | Bolts to the gearbox lid (B01) with the two stock M4 screws (M4×20). Two M3 nuts in pockets underneath. |
| `m540_motorplate_local.stl` | Motor plate | Motor screws to it with 2 × **M3×8** (4 mm plate + 4 mm into the motor). Joins the standoff with 2 × M3×16. |
| `m540_pinion.stl` | Long pinion | Stock C08 (10 T, module 1.3) with a hub reaching the shaft: Ø3.30 bore (picked from the bore test strip), M3 grub screw + square nut. Grips 7.7 mm of a 13 mm shaft (11.7 mm on a 17 mm shaft). |

Scripts: `mount540.py` (build123d, generated from `../motor775/mount775_v2.py`), `pinion540.py`, `fit540.py`. Run from the repo root with `~/.venvs/tarmo5/bin/python` on workload.

## Fit check (`fit540.py`, motor face at car y = 57.0)
- No printed part or motor overlaps any car part. The pinion/C07 overlap (2.65 mm³) is the gear mesh and is identical in the stock assembly.
- Same result for a 540 and a 550 body.
- **Tight spot: the motor can is 1.6 mm from the upper rear arm (A02)** at rest, at the side of the can (car y ≈ 101). The stock motor has 8 mm there. The arm moves with the suspension and this check is static, so the arm's full travel is not yet verified.
- Other gaps: rear plate B13-T 2.6 mm, hub A03 5.9 mm, lower arm 7.5 mm.

## Open
1. Sweep the upper arm through its suspension travel against the motor can.
2. 7.7 mm of grip on a 3.17 mm shaft with one grub screw is untested under load; file a flat on the shaft for the grub screw, or buy a 17 mm-shaft 540.
3. Print the three parts and test-fit on the real lid before printing the rest of the car.

## Gear mesh test (`mesh_test.py`)

Checks that our long pinion meshes with the real Tarmo5 main gear (C07) on your 540, without printing the gearbox.

- `mesh_test_gear.stl`: a 90° sector of the real C07 teeth, 3 mm thick, on a hub with a 6.4 mm hole.
- `mesh_test_link.stl`: a ring that slides over the pinion's smooth hub (15.5 mm hole, above the 25 mm flange) and holds a 6 mm pin 38.98 mm away, the C07–C08 centre distance in the car model. The gear turns on that pin, held by an M3 screw and washer in the pin's end.
- `mesh_test_plate.stl`: both parts on one plate.
- Fit check in the car frame: link–pinion 0 mm³, link–gear 0 mm³. Gear–pinion overlap 0.44 mm³ is the 3 mm share of the stock car's own C07–pinion tooth overlap (2.65 mm³ over 18 mm).
- Print: PETG, Ender 0.2 mm nozzle, 0.16 mm layers, 2 walls, 15% infill, **no brim**: 2.95 g, 55 min 51 s (slicer estimate). File on the Ender: `mesh_test_petg_02_016_ender.gcode`.
- Assembly: take the pinion off the motor shaft, slide the link's ring on from the motor end, refit the pinion, put the gear sector on the pin, then the M3 screw and washer (leave it loose enough that the gear turns).
- Test: turn the motor shaft by hand through the sector. It should roll smoothly with a little play, no binding and no skipping.

## Motor plate fit test (`plate_fit_test.py`)

A 3 mm slice of the motor plate with the same motor-face layout: 13.5 mm boss hole and 2x 3.4 mm M3 holes 25 mm apart. Use 2x M3x6 (the motor takes 5 mm of screw at most). PETG, Ender 0.2 nozzle, 0.16 mm layers, 2 walls, no brim: 1.03 g, 15 min 14 s (slicer estimate).
