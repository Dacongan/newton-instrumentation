# Wiring and pinout

> **Status: skeleton.** Pin numbers are unassigned until the hardware
> arrives and each one is verified on the real expansion board. The
> electrical reasoning below is settled; the pin table is not.
> Mirror every decision here into `firmware/include/config.h`.

## The architecture in one line

Everything in the tube runs on **5 V over USB**. One cable type, one
connector, one battery, and it can be bench-tested plugged into the
laptop.

```
power bank 10 000 mAh, 5 V
        │
        ├── ESP32 DevKit V1 ──┬── I2C ──── AHT20 + BMP280   (ambient air)
        │      │              ├── 1-Wire ─ 4 x DS18B20
        │      │              └── 4 x GPIO ─ ULN2003 ─ 28BYJ-48  (focuser)
        │      │
        │      ├── GPIO ─ IRLZ44N ─ secondary heater   1.5 W
        │      └── GPIO ─ IRLZ44N ─ rear fan           1.0 W
        │
        └── 1000 uF + 100 nF across the ESP32 supply
```

Peak draw ≈ **4 W** (heater 1.5 + fan 1.0 + ESP32 0.5 + motor 1.0). With
roughly 35 Wh usable from the power bank, that is about **8.8 h** — a
full night with margin.

**What does not run on 5 V:** the NEMA 17s of a future OnStep GoTo. A
TMC2209 starts from 4.75 V, but a NEMA 17 at 5 V delivers a fraction of
its torque. The mount gets its own 12 V supply when it arrives.

## Three things that bite at 5 V and would not at 12 V

1. **Voltage drop.** 0.5 V is 4 % at 12 V but **10 % at 5 V**. Short
   runs, 22 AWG minimum, silicone insulation. Measure at the board, not
   at the battery — that is what the USB meter in the BOM is for.
2. **ESP32 brown-out.** WiFi transmit peaks reach 500 mA. Without local
   decoupling the board resets itself mid-session. **1000 µF + 100 nF
   right at the board**, not somewhere along the rail.
3. **Separate returns.** The heater's 0.300 A flowing down a shared
   ground shifts the reference under the DS18B20 readings — 1-Wire is
   sensitive to exactly this. Power and signal each return on their own
   conductor to a single common point.

## Pin assignment

| Signal | GPIO | Direction | Notes |
|---|---|---|---|
| 1-Wire bus (4× DS18B20) | TODO | bidir | 4k7 pull-up already on the probe module |
| I2C SDA | 21 | bidir | AHT20 + BMP280 share the bus |
| I2C SCL | 22 | bidir | |
| Heater gate | TODO | out | IRLZ44N, PWM |
| Fan gate | TODO | out | IRLZ44N, PWM |
| Focuser IN1–IN4 | TODO | out | ULN2003 |

Constraints when assigning: avoid GPIO 6–11 (SPI flash), be careful with
the strapping pins (0, 2, 12, 15), and never put a MOSFET gate on
GPIO 34–39 — those are input-only.

## DS18B20 placement

1. **Edge of the primary mirror** — aluminium tape or a printed clip,
   **never on the optical face**
2. **Secondary holder, beside the heater** — this one closes the control
   loop
3. **Air inside the tube** — gives the internal gradient
4. **Spare**

Plus the AHT20+BMP280 reading ambient air. That set is the whole thermal
story — mirror, secondary, internal air, ambient — and it is what makes
the acclimation curve publishable rather than anecdotal.

## Mounting the secondary heater

- On the **metal holder**, never on the glass, and **never with rigid
  epoxy** — thermal stress, and irreversible. Thermal pad or neutral
  silicone.
- Everything added there must end up **black, matte, and hidden inside
  the shadow the secondary already casts**.
- Cables: two, thin and flat, bonded to the **edge of a single spider
  vane**, not to its wide face. The vanes are about 1 mm; adding 1 mm
  doubles that vane's diffraction. Invisible on planets — Jupiter is a
  disc, not a point — but detectable on bright stars.
- If it becomes intrusive: a heater ring **outside** the tube at the
  height of the secondary. Less efficient, more current, but nothing in
  the light path.

## Validation before it goes on the telescope

Put the heater assembly in the fridge for half an hour with current
flowing. The resistor array should come out **only lukewarm**. Target is
ambient +1 to +2 °C, just above the dew point — nothing more.
