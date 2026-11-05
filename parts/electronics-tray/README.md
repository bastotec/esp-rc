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
