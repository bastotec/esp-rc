# Electronics tray v0

`tray.py` (build123d 0.13) builds `tray_v0.stl`: 153 × 58 mm, 3 mm floor, 14 mm tall at the ESP32 rails, about 33 cm³.

**Mounting:** four M3 screws (button head) into the four 5 mm holes on top of the centre chassis (B03): 45 mm along the car × 20 mm across, measured from the STEP assembly. The tray's front edge lines up with B03's front end.

**What it holds** (rear to front), each zip-tied through slots in the floor, so the boards' own hole spacing doesn't matter:

| Pocket | Board | Inside size (mm) |
|---|---|---|
| Rear, across the car | XL4015 step-down (servo, set 5.5–6 V) | 28 × 53 |
| Middle | ESP32 DevKit (on 9 mm end rails, so the header pins hang free) | 56 × 30 |
| Middle, beside it | MP1584 step-down (ESP32, 5 V) | 24 × 19 |
| Front | IBT_2 / BTS7960 H-bridge, heatsink down on vent slots | 52 × 52 |

**Fit check:** placed on B03 in the car model, nothing placed overlaps it. Parts the conversion left unplaced near the model's origin (CV parts, the torque damper, a wheel, the M3 rods) are ignored.

**Assumptions to check:** ESP32 DevKit board about 52 × 28 mm (30-pin); step-down sizes are the usual module sizes, not your boards; body clearance not checked.

## Fit test (`tray_fit_test.py`)

The four pocket rims as open frames, 2 mm tall with 1 mm walls, same inner sizes as `tray.py`: H-bridge 52 x 52, ESP32-C3 SuperMini 19 x 23.5 (with end rails under its short ends), MP1584 24 x 19, XL4015 28 x 53. `fit_tests_bed.stl` lays them out with the motor plate fit test. PETG, Ender 0.2 nozzle, 0.16 mm layers, 2 walls, no brim: 3.0 g, 42 min 35 s (slicer estimate).

## ESP32 pocket: ESP32-C3 SuperMini (2026-11-05)

The ESP32 pocket was 56 x 30 mm for a DevKit V1. We now use the ESP32-C3 SuperMini already on hand (published size 22.5 x 18 mm, not measured), so the pocket is **19 x 23.5 mm** inside, long axis across the car. The board rests on two rails, 11 x 3 mm and 9 mm tall, under the middle of its short ends, so they sit between the pin rows (a first version with full-width rails hit the headers in the clash check); its pin rows run along the long sides, between the rails. A 12 mm slot in the -Y wall lets a USB-C cable reach the board for flashing from the side of the car. Fit-test bed re-sliced: PETG, Ender 0.2 nozzle, 0.16 mm layers, 2 walls, no brim: 2.5 g, 35 min 28 s (slicer estimate).

## Board mounting (v1.1)

| Board | How it's held | Hardware |
|---|---|---|
| IBT_2 H-bridge | On DubstepOwl's standoff (`vendor/bts7960-standoff/standoff_upright.stl`, CC BY). The standoff's base bolts to the floor through its two 4 mm holes (40.1 mm apart) into M3 nuts captured in hex pockets in the tray. The board screws onto the four post tops (40 x 40 mm). | 2 x M3x8 + 2 x M3 nut (base); 4 x M3x8 into the 3 mm post holes (board) |
| XL4015 | Four 1.5 mm bosses under its corner holes. The corner screws are also its IN+/IN-/OUT+/OUT- terminals: ring terminal + spring washer under each head; keep the four screws apart. | 4 x M2x8, thread-forming into 1.7 mm pilots |
| MH-MINI-360 | Four 1.5 mm corner standoffs (holes 2.2 mm, to take the solder tails of the wires) + a 1.5 mm centre pad, inside a 20 x 13.5 mm pocket. Its corner holes are 0.6-1.0 mm, too small for a screw without drilling away the pad, so it's held with double-sided foam tape on the pad. | foam tape |
| ESP32-C3 SuperMini | On its two end rails, USB-C toward the side slot. | - |

Assembly order: tray to the chassis (4 x M4), drop the two M3 nuts in their pockets, bolt the standoff down, then screw the H-bridge onto the posts.

`tray_v1_with_standoff.stl` is a preview of the tray with the standoff in place (not for printing).
