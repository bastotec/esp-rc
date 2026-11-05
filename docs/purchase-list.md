# Purchase list (2 cars, 2 drivers)

Brazil-only alternatives (motors, ESCs, wheels, shocks): see [local-sourcing.md](local-sourcing.md).

**Sources:**
- **Quantities:** the designer's official BOM ([`official-bom.csv`](official-bom.csv), exported from the sheet linked in the [instructions post](https://www.reddit.com/r/EngineeringNS/comments/zvellk/tarmo5/)). Where the BOM gives none, the counts come from [Carl Paton's build](https://carlpaton.github.io/2024/06/tarmo5-3d-printed-rc-car/).
- **Prices:** Mercado Livre search results, read in Bruno's Chrome on **2026-11-05**. Each is the lowest relevant non-sponsored result. I didn't open the listings to check stock, shipping or the seller.

## Drivetrain decision (2026-11-05)

We replaced the stock brushless motor with a **540 or 550 brushed motor** (36 mm can, 3.17 mm shaft; chosen 2026-11-05 after the 42 mm 775 turned out to hit the upper rear arm). The ESC and radio are replaced by **our own ESP32 electronics** (decided 2026-11-05, see below and [electronics.md](electronics.md)).

- **Speed depends on which 540 you buy.** A 12 V drill-type RS-540SH (17,500 rpm at 12 V) gives about 10,800 rpm on 2S, against about 16,000 rpm for the stock motor on 3S: roughly **40 km/h** with the stock gears. RC 540s (21T–27T) are rated for 7.2 V and usually spin faster, so check the listing's rpm. The ESP32 firmware's throttle cap (kid mode) limits it either way. Calculated, not measured.
- **Gears (measured from the official STLs):** the main gear C07 has **50 teeth** and the pinion C08 has **10 teeth**, both **module 1.3** (OD 67.6 mm = 1.3 × 52, and 15.6 mm = 1.3 × 12; tooth depth 2.9 mm = 2.25 × 1.3). That makes the first stage 5:1. Module 1.3 isn't a standard size, so **no bought metal pinion meshes** with the main gear (32P = mod 0.8, plus mod 1 and mod 1.5). Keep the **printed C08 pinion**.
- **Shaft:** 3.17 mm, about 13 mm long. Our printed long pinion (C08 + hub, 3.25 mm bore, M3 grub screw) replaces the 5 mm drive adaptor, so that Amazon-only part is no longer needed.
- **Our mod:** [`mods/motor540`](../mods/motor540): a standoff, a motor plate and the long pinion, fit-checked in the CAD assembly (540 and 550 both fit; 1.6 mm from the upper rear arm at rest, suspension travel not yet checked).
- **Electronics:** ESP32 + BTS7960 43A H-bridge in the car, a second ESP32 with joysticks as the controller, talking over ESP-NOW. No ESC, no radio.

## The power plan

The official BOM says **"ANY 2 OR 3S BATTERY WILL WORK"**, so 2×18650 in series (2S, 7.2 V) is within spec.

- **Speed:** see the drivetrain decision above. (For reference, the stock D3542 1450KV on 2S would spin about 10,700 rpm.)
- **Current:** a brushless 1:10 car can pull 40 A or more when it accelerates hard. Real high-drain 18650s are rated 20–35 A.
  - Start with **2S1P** (two cells) and a gentle throttle ramp in our firmware.
  - If the voltage sags or the cells get hot, go **2S2P** (four cells). The battery tray should allow both.

## Phase 1: rolling car

| Item | Per car | ×2 | Price seen | Listing |
|---|---:|---:|---:|---|
| **Motor 540 or 550 brushed, 36 mm can, 3.17 mm shaft, M3 holes 25 mm apart** (chosen 2026-11-05; prefer a 17 mm shaft if offered) — **already have 1** (36 × 52 mm, 3.2 mm shaft by micrometer) | 1 | 2 | ~R$95–190 | pick a Brazil-shipped listing; earlier finds R$155–190, cheaper ones seen near R$95 |
| M3×8 screws (motor to plate; max 5 mm into the motor), M3×16 + 2 M3 nuts (plate to standoff), M3 grub screw + square nut (pinion) | 1 set | 2 | — | |
| Servo DS3218MG 20 kg digital — **already have servos; model and size still to identify** (needs standard size, metal gears, ≥15 kg·cm; check horn spline vs the steering parts) | 1 | 2 | R$138 | [listing](https://www.mercadolivre.com.br/servo-digital-ds-3218mg-20kg-48v-a-68v-metal-gear/p/MLB2081493377) |
| Wheels + tires 1:10, **12 mm hex, 100–120 mm OD** | 4 | 8 | R$40–247 per set | [R$40 set](https://www.mercadolivre.com.br/jogo-de-rodas-para-automodelo-110-hexa-12mm/up/MLBU3356327457) (check the OD) · [Aimrock R$225](https://www.mercadolivre.com.br/rc-buggy-wheels-and-tires-aimrock-12mm-hex-22-for-110/p/MLB2092655437) |
| Shocks, ~80 mm | 4 | 8 | R$46 per 4 | [listing](https://www.mercadolivre.com.br/4pcs-metal-110-rc-car-front-rear-shock-80mm-style-2/p/MLB2028814778) |
| Bearings 6802-2RS 15×24×5 ("do not substitute") | 12 | 24 | R$34 per 10 | [listing](https://www.mercadolivre.com.br/kit-10-pecas-rolamento-6802-2rs-marca-gbr-15x24x5/up/MLBU4082722049) (buy 3 kits) |
| Steel balls 6 mm (CV joints) | 20 | 40 | R$30 per 300 | [listing](https://www.mercadolivre.com.br/esfera-aco-carbono-6-mm-alta-qualidade-300-pecas/up/MLBU595121627) |
| M3 threaded rod, 350 mm ("do not substitute") | 3 | 6 | R$39 per 500 mm | [listing](https://www.mercadolivre.com.br/barra-roscada-m3-inox-laminada-500mm-1-peca/p/MLB46479343) (buy 6) |
| Main drive gear adaptor (5 mm ID, 11 mm OD shank) | 1 | 2 | not found | Designer's part: [Amazon B07W669S33](https://www.amazon.com/dp/B07W669S33). A plain 5 mm retaining ring is **not** the same part |
| Metal servo horn | 1 | 2 | — | Only if the servo doesn't come with one |
| Super Lube 92003 (PTFE silicone grease, "do not substitute") — **already have grease; confirm it's silicone/PTFE, plastic-safe** | — | 1 shared | R$192 | [listing](https://www.mercadolivre.com.br/tubo-automotivo-de-graxa-de-silicone-super-lube-92003-de-3-oncas/p/MLB2091272713) |

### Battery

| Item | Per car | ×2 | Price seen | Notes |
|---|---:|---:|---:|---|
| 18650 high-drain cells | 4 | 8 | about R$25–40 each | 2 packs of 2S per car. **Fakes warning:** the cheapest "Molicel 2800mAh" listings say **10 A**, but a real P28A is rated 35 A. "Compatível com 25R" means a clone. Buy from a seller who shows genuine stock |
| BMS 2S **40 A** with balancing | 2 | 4 | R$46 | [listing](https://www.mercadolivre.com.br/placa-bms-2s-74v-40a-balanceada-ideal-para-baterias-21700/up/MLBU3944058650). Most 2S boards are 13–20 A, which is too low for this motor |
| XT60 pairs + 14 AWG silicone wire | 3 | 6 | not checked | |
| 18650 charger (4-slot) | — | 1 shared | not checked | Charge outside the car |

### Screws (official BOM quantities, per car)

M3: 10 nylon nuts, 10 × M3×8, 20 × M3×16.
M4: 10 nylon nuts, 10 × M4×12, 20 × M4×20, 15 × M4×35 socket, 4 × M4×35 **hex head**, 20 × M4×40.

Double these for two cars. Prices not checked.

### Filament (official BOM, per car)

| Item | Per car | ×2 | Price seen |
|---|---:|---:|---:|
| PLA (or nylon; **no ABS, no PETG on the drivetrain**) | 1 kg | 2 kg (+ spares) | not checked |
| Hard TPU 95A | 0.5 kg | 1 kg | R$128–169 per kg ([Polimus R$128](https://www.mercadolivre.com.br/filamento-de-impressao-3d-tpu-95a-cor-branco-1kg-brilho-premium-flexivel-by-polimus-3d/p/MLB79477240), [Elegoo R$152](https://www.mercadolivre.com.br/filamento-elegoo-tpu-branco-1kg-175mm-95a-premium-branco/p/MLB65171542)) |

**Already on hand (2026-11-05):** motor, H-bridge, servos, step-downs, grease. Still to buy for the proof of concept: ESP32 DevKit V1, 6802-2RS bearings, fuse holders + 30 A *medium* blade fuses (ATO/ATC; the holder listing has no fuses), and screws/grub screw/TPU if missing. The servo and the electronics bay must be designed around the parts actually on hand, not the listed ones.

**Rough Phase 1 total:** about **R$1,100–1,400 per car** with a 540 and our ESP32 electronics. That's my sum of the prices above plus guesses for screws, PLA and wiring. It's an estimate, not a quote.

## Phase 2: FPV

| Item | Qty | Price seen | Notes |
|---|---:|---:|---|
| AIO camera + 5.8 GHz transmitter (25 mW, 40 ch) | 1 per car | R$215–272 | [listing](https://www.mercadolivre.com.br/camera-fpv-aio-58ghz-25mw-40-canais-800tvl-transmissor/up/MLBU4261338151). Put each car on its own channel |
| 5 V buck regulator, ≥ 1 A | 1 per car | not checked | Gives the camera a clean 5 V |
| Analog goggles with DVR | 1 per driver | R$890–1,304 | [EV800D-style R$890](https://www.mercadolivre.com.br/oculos-fpv-xvpy-ev800d-com-dvr-res-de-40-canais-5-polegadas/p/MLB2028053115). Goggles are expensive in Brazil; the BETAFPV VR03 (US$74.99 abroad) may cost less imported, even after tax. Not calculated |

## Phase 3: steering wheel + ExpressLRS

| Item | Qty | Notes |
|---|---:|---|
| ExpressLRS 2.4 GHz receiver with PWM outputs | 1 per car | **Superseded:** the ESP32 controller doubles as the wheel bridge (see Electronics) |
| ExpressLRS TX module | 1 per driver | Driven by [elrs-joystick-control](https://github.com/kaack/elrs-joystick-control) |
| Raspberry Pi 4 or a laptop | 1–2 | Runs the bridge |
| USB wheel + pedals | 1–2 | |

Phase 3 prices not checked yet.

## Electronics (chosen): ESP32 + H-bridge, no ESC, no radio

Wiring, pins and firmware rules: [electronics.md](electronics.md). Prices are Brazil-shipped Mercado Livre search results, 2026-11-05.

### In the car (per car)

| Item | Per car | Price seen | Listing |
|---|---:|---:|---|
| BTS7960 43A H-bridge (IBT-2), 1000+ sold — **already have 1** (HW-039 board, used: clean and bench-test first) | 1 | R$42 | [listing](https://www.mercadolivre.com.br/modulo-driver-ponte-h-43a-bts7960-controle-motor-dc-robotica/p/MLB37899442) |
| ESP32 WROOM DevKit V1, 500+ sold | 1 | R$49.90 | [listing](https://www.mercadolivre.com.br/esp32-wroom-devkit-v1-wifi-bluetooth-dual-core-esp32-desenvolvimento-iot-autom) |
| XL4015 5A buck (servo rail, set to 5.5 V) — **already have step-downs; chip to identify** (servo rail needs ≥3 A) | 1 | R$22.41 | [listing](https://www.mercadolivre.com.br/regulador-de-tensao-xl4015-conversor-dc-dc-step-down-arduino/p/MLB2048275336) |
| MP1584 3A mini buck (ESP32 rail, set to 5.0 V) — **already have step-downs; chip to identify** | 1 | R$19 | [listing](https://www.mercadolivre.com.br/modulo-conversor-tensao-mp1584-step-down-dc-dc-mp1584en/p/MLB35506732) |
| Blade fuse holder (2.5 mm wire) + 30 A blade fuse | 1 | R$31.99 per 10 holders | [listing](https://www.mercadolivre.com.br/kit-10-porta-fusivel-lamina-medio-automotivo-fio-25mm/up/MLBU3136674600); fuses not priced |
| Resistors 100 kΩ + 33 kΩ (battery voltage divider) | 1 each | a few reais | |
| **Car electronics** | | **~R$137** | vs R$99 ESC + R$253 radio = R$352 |

### Controller (per driver)

| Item | Per driver | Price seen | Listing |
|---|---:|---:|---|
| ESP32 WROOM DevKit V1 | 1 | R$49.90 | same as above |
| Analog joystick modules (KY-023), pack of 2 | 1 pack | R$24.30 | [listing](https://www.mercadolivre.com.br/02-modulo-joystick-analogico-5v-ideal-p-arduino-pic/p/MLB75105243) |
| Power | — | R$0 | any USB power bank or phone charger |
| **Controller** | | **~R$74** | |

The same controller board, plugged into a laptop by USB, becomes the steering-wheel bridge later: the laptop reads the wheel and sends it to the ESP32 over serial. That replaces Phase 3's ExpressLRS parts.

**Total electronics, car + controller: ~R$211 per car, against ~R$352 for ESC + FlySky radio. Saves ~R$140 per car (~R$280 for both).**

Choices and their reasons:
- **Classic ESP32 DevKit, not ESP32-C3 SuperMini** (R$39.90). The SuperMini saves R$10, but many batches are reported to have weak antennas, and we want ~100 m. Not tested by us.
- **Two regulators.** The servo's current spikes can brown out the ESP32 if they share a rail, and an ESP32 reset is a car with no control. The MP1584 is R$19 of insurance.
- **XL4015 at 5.5 V, not 6 V:** two 18650s sag to about 6.4 V near empty, and the buck needs headroom.
- **Don't use an L298N:** it's only about 2 A and wastes about 2 V.
- **Alternative if the DIY route stalls:** 320A brushed ESC R$98.99 + FlySky FS-GT3B R$253 ([listing](https://www.mercadolivre.com.br/transmissor-flysky-fs-gt3b-3ch-24ghz-receptor-fs-gr3e/up/MLBU5779157194)).
