# esp-rc

A 3D-printed 1:10 RC car for a parent-and-kid build, driven by **our own ESP32 electronics** instead of a hobby ESC and radio.
It reuses most of the printed parts of the **Tarmo5** and replaces only what our parts don't fit.

- **Motor:** a 540-size brushed motor (36 × 52 mm, 1/8" shaft) on our printed mount and long pinion
- **Electronics:** ESP32 + IBT_2 (BTS7960) H-bridge + two step-downs, on our printed tray on top of the centre chassis
- **Power:** 2× 18650 (2S) in the centre chassis's battery bay; a bench supply for first tests
- **Steering:** Tower Pro MG946R servo

Status: designing. The motor parts have had their first fit print; the tray is a v0 model, not printed.

## What we reuse and what we replace

See [docs/reuse.md](docs/reuse.md). In short: suspension, steering, gearbox, differential/CV, chassis ends and body are the stock Tarmo5 parts (in [`vendor/tarmo5/`](vendor/tarmo5/)). Ours are the motor mount, the pinion, the electronics tray, and (next) an 18650 holder.

## Layout

| Path | What |
|---|---|
| `vendor/tarmo5/` | The designer's official Tarmo5 STLs, unchanged |
| `parts/motor540/` | 540 motor standoff, motor plate, long pinion (3.3 mm bore), bore test strip; build123d scripts and fit check |
| `parts/electronics-tray/` | Tray that bolts to the four holes on top of the centre chassis (B03) |
| `docs/` | Reuse map, electronics and safety rules, purchase list, Brazil sourcing |

Parts are modelled in **build123d** (0.13). Fit-test prints are kept to 1 hour at most, aiming for 30 minutes.

## Credit and license

- **Tarmo5** by Kris / Engineering NS ([Printables 348623](https://www.printables.com/model/348623-3d-printed-rc-car-tarmo5), [Onshape source](https://cad.onshape.com/documents/866dfd956b60f623aa8e6234/w/2ed44a3da1c969b8110877f0/e/3e10e517f2654f1bfe05ac4d)), licensed **CC BY-NC-SA 4.0**. The files in `vendor/tarmo5/` are his, unchanged.
- **FreeCAD/STEP conversion** used for measurements: [Nemesis81/Tarmo5-freecad](https://github.com/Nemesis81/Tarmo5-freecad), via our fork [bastotec/tarmo5-fpv](https://github.com/bastotec/tarmo5-fpv).
- Because this car reuses and adapts Tarmo5 parts, **this project is shared under the same CC BY-NC-SA 4.0**: credit the original, share alike, no commercial use.

## v1

The v1 structure (rolling chassis, drivetrain, electronics, battery, no body) and its fit checks: [docs/v1.md](docs/v1.md).
