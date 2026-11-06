# Print profiles (Ender 3 V2, Klipper, 0.2 mm nozzle, PETG)

OrcaSlicer configs exported from the Ender's 0.2 mm nozzle profile, for slicing with `orca-slicer --load-settings`.

`ender-0.2-petg-0.16-fast.process.json` is the stock profile with speeds and accelerations raised about 50% (2026-11-06):

| Setting | Before | Fast |
|---|---|---|
| Outer wall | 25 mm/s | 38 mm/s |
| Inner wall / solid infill | 40 mm/s | 60 mm/s |
| Sparse infill | 50 mm/s | 75 mm/s |
| Top surface / gap infill | 25 mm/s | 38 mm/s |
| Travel | 200 mm/s | 300 mm/s (Klipper max_velocity) |
| Default / inner wall / travel accel | 2500 | 3750 mm/s² |
| Outer wall accel | 3500 | 3000 mm/s² (kept moderate for surface quality) |
| Top surface accel | 2000 | 3000 mm/s² |
| Bridges | unchanged (15 / 70 mm/s) | PETG sags if faster |

Checks: Klipper's `max_velocity` is 300 and `max_accel` 6000, so the slicer's per-feature `SET_VELOCITY_LIMIT` values take effect. Peak commanded flow on the electronics tray went from 2.1 to 2.5 mm³/s, under the filament's 3 mm³/s cap. Tray estimate: 7 h 20 min → 5 h 29 min. **Not yet verified on a real print.**

Known mismatch: the Ender's `printer.cfg` still says `nozzle_diameter: 0.600`. It doesn't cap speed (`max_extrude_cross_section` is set to 6.1 explicitly), but should be corrected.
