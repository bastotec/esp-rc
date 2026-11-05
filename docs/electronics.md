# Electronics: ESP32 + BTS7960 (our design)

Decided 2026-11-05: no commercial ESC or radio. A car ESP32 drives the motor through a BTS7960 H-bridge and the servo directly. A second ESP32 with joysticks sends commands over ESP-NOW. Parts and prices: [purchase-list.md](purchase-list.md#electronics-chosen-esp32--h-bridge-no-esc-no-radio).

**Status: plan only.** Nothing here has been built or tested yet.

## Power

```
2×18650 (2S) ─ BMS 40A ─ XT60 ─ switch ─ 30 A fuse ─┬─ BTS7960 B+/B-  ─ M+/M- ─ 775 motor
                                                   ├─ XL4015 (5.5 V) ─ servo +/-
                                                   ├─ MP1584 (5.0 V) ─ ESP32-C3 5V pin
                                                   └─ 100k/33k divider ─ ESP32-C3 GPIO3
```

- All grounds common. Motor and battery path in 14 AWG.
- Set both bucks with a multimeter **before** connecting anything.
- Put a 0.1 µF ceramic capacitor across the 775's terminals to cut brush noise.
- Divider: 8.4 V full → 2.08 V at the pin; 6.0 V → 1.49 V. Calibrate against a multimeter.

## Car pin map (ESP32-C3 SuperMini)

Boards: **ESP32-C3 SuperMini**, already on hand (two: one for the car, one for the controller). Chosen 2026-11-05 over buying DevKit V1s. It has Wi-Fi + ESP-NOW, USB-C for flashing, and a 5V pin that feeds its own 3.3 V regulator. Published size 22.5 × 18 mm (not measured).

**C3 pins to avoid:** GPIO2, 8 and 9 set the boot mode (GPIO8 is also the onboard LED, GPIO9 the BOOT button). GPIO20/21 are the serial port. Only GPIO0–4 have a usable ADC (ADC1).

| C3 pin | Goes to | Notes |
|---|---|---|
| GPIO5 | BTS7960 RPWM | forward PWM, ~20 kHz (above hearing) |
| GPIO6 | BTS7960 LPWM | reverse PWM |
| GPIO4 | BTS7960 R_EN + L_EN | low = motor off (coast); used by failsafe. Add a **10 kΩ pull-down** to GND so the bridge stays off while the C3 boots |
| 3V3 | BTS7960 VCC | runs the module's logic at 3.3 V to match the C3. **Check on the bench** that it switches reliably |
| GND | BTS7960 GND | |
| GPIO7 | servo signal | 50 Hz, 1000–2000 µs |
| GPIO3 | battery divider | ADC1, works with Wi-Fi on. The C3's ADC reads up to ~2.5 V at 11 dB attenuation; 8.4 V → 2.08 V fits |
| GPIO8 | onboard LED | link status. Output only after boot; the LED is active-low |
| GPIO10 | spare | e.g. R_IS/L_IS current sense would need an ADC pin: use GPIO0 or GPIO1 |

**Antenna:** many SuperMini batches have a weak or detuned antenna. First lower transmit power in firmware (`WiFi.setTxPower(WIFI_POWER_8_5dBm)`; on these boards that often *improves* range). If range is still short, solder a 31 mm wire antenna to the chip antenna. Reported by others, not tested on our boards.

Optional later: the BTS7960's R_IS/L_IS current-sense pins to GPIO0/1 for stall protection.

## Controller pin map (second ESP32-C3 SuperMini)

| C3 pin | Goes to |
|---|---|
| GPIO0 | left joystick Y (throttle) |
| GPIO1 | right joystick X (steering) |
| GPIO10 | joystick button (input pullup): toggles kid mode |
| 3V3 / GND | both joysticks' +5V / GND pins: **power them from 3.3 V**, since the ADC tops out below that |

Powered from any USB power bank over its USB-C port. Plugged into a laptop, the same board takes commands over USB serial instead of the joysticks: that's the steering-wheel bridge.

## Firmware rules (must hold before a kid drives it)

1. **Failsafe:** the controller sends a packet every 20 ms. If the car gets no valid packet for **250 ms**, it brakes (both PWM low), centres the steering, then disables the bridge.
2. **Arming:** after power-up or a failsafe, the car ignores throttle until it sees throttle at neutral. It never jumps forward when switched on.
3. **Pairing:** the car only accepts packets from its own controller's MAC address, with a sequence number and checksum. Two cars must not take each other's commands.
4. **Kid mode:** caps throttle (start at 40%) and slows the acceleration ramp. Default **on** at boot.
5. **Battery:** below 6.4 V under load, halve throttle and blink the LED; below 6.0 V, stop the motor. The BMS is the last line, not the first.
6. **Throttle ramp:** limit how fast PWM can rise, so a full-stick jab doesn't spike current through the 18650s.

Test 1–3 with the car on a stand, wheels off the ground: power off the controller, walk out of range, unplug it mid-throttle.

## Range

~100 m is a typical open-field figure for ESP-NOW on full-size ESP32 boards; the SuperMini's small antenna may do worse (see the antenna note above). The C3 supports the long-range Wi-Fi mode (`WIFI_PROTOCOL_LR`), which can help. **Not measured on this car** — measure it with the failsafe working, before trusting it.
