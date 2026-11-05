# Electronics: ESP32 + BTS7960 (our design)

Decided 2026-11-05: no commercial ESC or radio. A car ESP32 drives the motor through a BTS7960 H-bridge and the servo directly. A second ESP32 with joysticks sends commands over ESP-NOW. Parts and prices: [purchase-list.md](purchase-list.md#electronics-chosen-esp32--h-bridge-no-esc-no-radio).

**Status: plan only.** Nothing here has been built or tested yet.

## Power

```
2×18650 (2S) ─ BMS 40A ─ XT60 ─ switch ─ 30 A fuse ─┬─ BTS7960 B+/B-  ─ M+/M- ─ 775 motor
                                                   ├─ XL4015 (5.5 V) ─ servo +/-
                                                   ├─ MP1584 (5.0 V) ─ ESP32 VIN
                                                   └─ 100k/33k divider ─ ESP32 GPIO34
```

- All grounds common. Motor and battery path in 14 AWG.
- Set both bucks with a multimeter **before** connecting anything.
- Put a 0.1 µF ceramic capacitor across the 775's terminals to cut brush noise.
- Divider: 8.4 V full → 2.08 V at the pin; 6.0 V → 1.49 V. Calibrate against a multimeter.

## Car pin map (ESP32 DevKit V1)

| ESP32 pin | Goes to | Notes |
|---|---|---|
| GPIO25 | BTS7960 RPWM | forward PWM, ~20 kHz (above hearing) |
| GPIO26 | BTS7960 LPWM | reverse PWM |
| GPIO27 | BTS7960 R_EN + L_EN | low = motor off (coast); used by failsafe |
| 3V3 | BTS7960 VCC | runs the module's logic at 3.3 V to match the ESP32. **Check on the bench** that it switches reliably |
| GND | BTS7960 GND | |
| GPIO13 | servo signal | 50 Hz, 1000–2000 µs |
| GPIO34 | battery divider | ADC1 (ADC2 can't be used while Wi-Fi/ESP-NOW is on) |
| GPIO2 | onboard LED | link status |

Optional later: the BTS7960's R_IS/L_IS current-sense pins to an ADC1 pin for stall protection.

## Controller pin map (ESP32 DevKit V1)

| ESP32 pin | Goes to |
|---|---|
| GPIO32 | left joystick Y (throttle) |
| GPIO33 | right joystick X (steering) |
| GPIO14 | joystick button (input pullup): toggles kid mode |
| 3V3 / GND | both joysticks' +5V / GND pins: **power them from 3.3 V**, since the ESP32 ADC tops out at 3.3 V |

Powered from any USB power bank. Plugged into a laptop, the same board takes commands over USB serial instead of the joysticks: that's the steering-wheel bridge.

## Firmware rules (must hold before a kid drives it)

1. **Failsafe:** the controller sends a packet every 20 ms. If the car gets no valid packet for **250 ms**, it brakes (both PWM low), centres the steering, then disables the bridge.
2. **Arming:** after power-up or a failsafe, the car ignores throttle until it sees throttle at neutral. It never jumps forward when switched on.
3. **Pairing:** the car only accepts packets from its own controller's MAC address, with a sequence number and checksum. Two cars must not take each other's commands.
4. **Kid mode:** caps throttle (start at 40%) and slows the acceleration ramp. Default **on** at boot.
5. **Battery:** below 6.4 V under load, halve throttle and blink the LED; below 6.0 V, stop the motor. The BMS is the last line, not the first.
6. **Throttle ramp:** limit how fast PWM can rise, so a full-stick jab doesn't spike current through the 18650s.

Test 1–3 with the car on a stand, wheels off the ground: power off the controller, walk out of range, unplug it mid-throttle.

## Range

~100 m is a typical open-field figure for ESP-NOW on DevKit boards. ESP32 has a long-range Wi-Fi mode (`WIFI_PROTOCOL_LR`) that can help. **Not measured on this car** — measure it with the failsafe working, before trusting it.
