# Reuse map: Tarmo5 parts in esp-rc

Part names and numbers are the designer's, from `vendor/tarmo5/`. "Reused" means printed unchanged.

## Reused as-is

| Group | Parts |
|---|---|
| Suspension and steering | A01 shock mount, A02 control arm, A03 rear bearing hub, A04 front sus mount, A05/A06 front bearing hubs, A07/A08 steering arms, A09 steering bar, A10 steering link |
| Gearbox | B01 lid, B02 gearbox, C06 main gear hub, C07 main gear (module 1.3, 50 teeth), C05-T torque damper |
| Driveline | C01 CV wheel housing, C02 CV gear housing, C03 CV cage, C04 CV inner race, C09 front axle, C10 front wheel spacer |
| Chassis | B03 centre chassis (battery bay inside, tray bolts on top), B04/B05/B06 end chassis, B10-T/B11-T front plates, B12-T/B13-T rear plates, B07-T bumper, B08-T battery clip |
| Body | D01A (cab and hood), D01B (bed). Pickup-truck shell, about 445 × 182 × 140 mm in two halves |

## Replaced by ours

| Tarmo5 part | Ours | Why |
|---|---|---|
| B09 motor mount | `parts/motor540/m540_standoff_local.stl` + `m540_motorplate_local.stl` | 540 brushed motor instead of the D3542 brushless; a 775 hit the upper rear arm (A02) |
| C08 pinion | `parts/motor540/m540_pinion.stl` | Same 10-tooth module 1.3 gear, longer hub, 3.3 mm bore (tested snug on the 540 shaft), M3 grub screw. Also replaces the 5 mm gear adaptor |

## New parts

| Part | Status |
|---|---|
| Electronics tray (`parts/electronics-tray/`) | v0 modelled, not printed |
| 18650 holder for the B03 battery bay (48 × 38 mm tunnel) | not started |

## Not checked yet

- **Body clearance over the tray.** The H-bridge stands about 42 mm tall (about 32 with its capacitor bent flat). The body STLs aren't placed in the CAD assembly, so the height under the shell is unknown.
- **MG946R in the steering servo mount.** Same class as the DS3218 the car was designed for (about 2 mm taller, 25-tooth spline), not checked in the model.
- **What goes in B03's four 5 mm top holes** in the stock car. The tray uses them with M3 screws; if they're meant for heat-set inserts, use M3 inserts.
- **Body printing.** D01A/D01B are solid in the STL (about 1.7 and 2.2 litres), which suggests they're meant to be printed in vase mode. Not confirmed.
