<div align="center">

# newton-instrumentation

### Low-cost instrumentation for a Bresser 130/650 Newtonian

**Active mirror cooling · secondary dew control · motorised focusing**

Designed from parametric scripts, 3D-printed, and **validated with measured data**

[![Licence: CERN-OHL-W v2](https://img.shields.io/badge/hardware-CERN--OHL--W_v2-1f6feb?style=flat-square)](LICENSE)
[![Firmware: MIT](https://img.shields.io/badge/firmware-MIT-1f6feb?style=flat-square)](NOTICE.md)
[![Docs: CC BY-SA 4.0](https://img.shields.io/badge/docs-CC_BY--SA_4.0-1f6feb?style=flat-square)](NOTICE.md)
<br>
[![CAD: Rhino 8 + Python](https://img.shields.io/badge/CAD-Rhino_8_%2B_Python-801fbf?style=flat-square)](cad/)
[![MCU: ESP32](https://img.shields.io/badge/MCU-ESP32-e7500a?style=flat-square)](firmware/)
[![Print: FDM](https://img.shields.io/badge/print-FDM_0.4_mm-3fb950?style=flat-square)](cad/parts.md)
[![Status](https://img.shields.io/badge/status-in_progress-d29922?style=flat-square)](#status)

</div>

<!--
  HERO IMAGE — drop the photo at docs/figures/hero.jpg and uncomment:
  ![](docs/figures/hero.jpg)
  Replace it with the acclimation curve once the first thermal run exists.
  That plot is the whole argument of this repository in one image.
-->

---

<div align="center">

[Why](#why) · [What makes this different](#what-makes-this-different) · [Status](#status) · [Subsystems](#subsystems) · [Power](#power-architecture) · [Principles](#design-principles) · [Layout](#repository-layout) · [Printing](#printing) · [Roadmap](#roadmap) · [Safety](#safety--solar-filter)

</div>

---

## Why

Three things limit this telescope before its optics do: **primary mirror
acclimation**, **dew on the secondary**, and **focus drift**.

The numbers make the case without argument:

| | | |
|---|---:|---|
| Dawes limit, 130 mm mirror | **0.89″** | what the optics can resolve |
| Typical seeing | **2–3″** | what the atmosphere allows |
| Critical focus zone at f/5 | **27.5 µm** | how little it takes to lose it |
| Sampling at prime focus, SV105 | **0.95″/px** | already coarser than the mirror |

The atmosphere resolves roughly three times worse than the mirror. **Aperture
is not the bottleneck.** A 200 mm tube would not fit the EQ-3 mount, so
replacing it means replacing the mount too — 800–1000 €, to chase a limit
the sky already imposes.

Thermal management, focus precision and collimation *are* the bottleneck,
and all three are solved here for **under 60 €** and some work.

## What makes this different

> ### Published with **measured data, not renders.**

Every subsystem is instrumented. Four DS18B20 probes record the mirror edge,
the secondary, the air inside the tube and the ambient; the optical result is
quantified with [`strehl`](https://github.com/Dacongan/strehl), the planetary
processing suite this project is validated against.

That turns *"a 3D-printed cap"* into a result:

> **Strehl ratio with the fan off versus on — same target, same night,
> thirty minutes apart.**

And it closes the loop that actually matters:

```
thermal prediction  ->  thermal measurement  ->  real optical effect
```

Mirror acclimation is a natural-convection and thermal-boundary-layer
problem. With the DS18B20 series you can fit a lumped thermal model — the
mirror's time constant with and without forced ventilation — and check it
against the measured curves. Almost nobody publishing telescope
modifications can show that.

---

## Status

| Subsystem | | State |
|---|---|---|
| **NI-07** Bahtinov mask | `██████████` | Printed · awaiting a star test |
| **NI-03** Focus wheel | `██████████` | Printed, fitted · ×1.57 torque, clears the tube |
| **NI-08** Focuser dust cap | `██████████` | Printed, in service · drawing issued |
| **NI-01** Ventilation cover | `█████████░` | In service · to be reprinted in PETG |
| **NI-04** Motor pulley | `███████░░░` | Designed v3 · drawing issued · not printed |
| **NI-06** Solar cap, bayonet | `██████░░░░` | Designed · awaiting PETG and Baader film |
| **NI-05** Motor mount | `██░░░░░░░░` | **Blocked** on one measurement |
| Thermal control | `███░░░░░░░` | Components ordered · firmware not started |
| Terminal client | `░░░░░░░░░░` | Not started |

Full index, part numbers, materials and print settings →
**[`cad/parts.md`](cad/parts.md)**

---

## Subsystems

### Motorised focuser

A 28BYJ-48 drives the existing turned-metal pulley on the focuser shaft
through an O-ring, giving **3.13 µm per step** — twelve times finer than the
critical focus zone at f/5.

```
pinion Ø8.50          ->  π × 8.50  =  26.7 mm of travel per turn
Ø33.3 : Ø16.0         ->  2.08 : 1 reduction
4096 half-steps       ->  8525 steps per pinion turn
                      ->  3.13 µm / step
```

| | CFZ | Steps |
|---|---:|---:|
| f/5 | 27.5 µm | **9** |
| f/15 (Barlow ×3) | 247 µm | **79** |

<details>
<summary><b>Why the reduction stops at 2.08 : 1</b></summary>

<br>

Precision already exceeds the requirement twelvefold. What is scarce is
**speed** — 50 mm of focuser travel takes 32 s. Raising the ratio buys
resolution nobody can use and costs time on every slew.

Torque is not the constraint either: ~300 g·cm at the motor becomes
624 g·cm at the pinion, or 14.4 N at the rack. The real limit is friction
in the O-ring, which slips first — and that is a **safety feature**. If
the focuser bottoms out, the rubber slips instead of stripping the pinion.

The pulley groove is **semicircular, radius 2.30 mm**, cut by subtracting a
torus from a solid cylinder. An O-ring is a rubber cylinder of circular
section: on a flat groove floor it touches along a *line*, concentrating
pressure and wearing early. In an R2.30 channel it seats along an *arc* —
more friction area, more transmissible torque. That is why commercial
round-belt pulleys are made this way, and it is what the first two design
attempts got wrong.

The motor shaft is a **double-D**: the flats transmit the torque, so no
grub screw is needed. That is precisely why a printed pulley is reliable
here, where a printed 54 mm pulley clamped onto the steel focuser shaft
would not be.

</details>

### Thermal control

Closed-loop heating of the secondary plus forced ventilation of the primary,
both on 5 V, both logged.

| | |
|---|---|
| Heater | 6 × 100 Ω ∥ = 16.7 Ω → 0.300 A → **1.50 W** |
| Per resistor | 0.250 W against a 0.5 W rating — **50 % derated** |
| Setpoint | **dew point + 2 °C**, not a fixed temperature |
| Sensing | 4 × DS18B20 + AHT20/BMP280 ambient |

<details>
<summary><b>Why the setpoint is a relationship, not a value</b></summary>

<br>

The dew point moves through the night. A fixed temperature tracks it for
about an hour and then stops being correct — either wasting power or
letting dew form.

And the offset stays deliberately small. **Too much heat drives convection
inside the tube and destroys planetary detail faster than the dew it was
meant to prevent.** Target is ambient +1 to +2 °C, no more.

Validation before it goes near the telescope: put the assembly in the
fridge for half an hour with current flowing. The resistor array should
come out only lukewarm.

Mounting matters as much as the electronics. The heater goes on the
**metal holder, never on the glass, never with rigid epoxy** — thermal
stress, and irreversible. Cables run along the **edge of a single spider
vane**, not its wide face: the vanes are about 1 mm, and adding 1 mm
doubles that vane's diffraction.

</details>

### Solar cap with bayonet

One cap, two functions. **Plug in** → ordinary dust cap. **Plug out** →
38 mm off-axis solar filter at f/17.

```
secondary  47 mm  ->  free radius from   23.5 mm
primary   130 mm  ->  usable radius to   65.0 mm
                      ------------------------
usable annulus                           41.5 mm wide
```

An off-axis aperture must fit **entirely** inside that annulus — which is
what rules out the 60 mm hole considered first. 38 mm leaves 5.5 mm of
clearance for the spider vanes, and costs nothing optically: at f/17.1 the
Dawes limit is 3.05″ against a typical daytime seeing of 3–5″. The
atmosphere is already the limit, so a bigger hole would buy no real detail.

The film is **clamped between the recess floor and a retaining ring, never
glued**, and left slightly slack.

### Bahtinov mask

Diffraction focusing aid. Slot width = focal / 150 = **4.33 mm**, period
8.67 mm, about 15 slots across the aperture.

<details>
<summary><b>Why the slot zone is 130 mm and not 155 mm</b></summary>

<br>

Starlight arrives **collimated** — parallel rays. It does not converge
until after it reflects off the primary.

A ray entering 70 mm off-axis is still 70 mm off-axis when it reaches the
bottom of the tube, and the mirror ends at 65 mm. It is lost. So the
useful zone is exactly the projection of the primary, and the wide outer
rim is unavoidable: it is the part of the tube that never sees the mirror.

This was reasoned wrongly at first — "the light converges a little" — and
corrected. The mistake is recorded in [`docs/design-notes.md`](docs/design-notes.md) §5,
along with every other one.

**Print constraint:** the 4.33 mm bar is 10.8 lines of 0.4 mm wide.
At more than 3 perimeters it prints hollow.

</details>

---

## Power architecture

Everything inside the tube runs on **5 V over USB**. One cable type, one
connector, one battery — and it can be bench-tested plugged into a laptop.

```
power bank 10 000 mAh, 5 V
        │
        ├── ESP32 DevKit V1 ──┬── I²C ───── AHT20 + BMP280   ambient air
        │      │              ├── 1-Wire ── 4 × DS18B20      mirror edge, secondary,
        │      │              │                              tube air, spare
        │      │              └── GPIO ×4 ─ ULN2003 ─ 28BYJ-48   focuser
        │      │
        │      ├── GPIO ─ IRLZ44N ─ secondary heater   1.5 W
        │      └── GPIO ─ IRLZ44N ─ rear fan           1.0 W
        │
        └── 1000 µF + 100 nF across the ESP32 supply
```

Peak draw ≈ **4 W** → about **8.8 h** on one power bank. A full night with
margin.

<details>
<summary><b>Three things that bite at 5 V and would not at 12 V</b></summary>

<br>

**1 · Voltage drop.** 0.5 V is 4 % at 12 V but **10 % at 5 V**. Short runs,
22 AWG minimum, silicone insulation — PVC cracks when flexed at 2 °C.
Measure at the board, not at the battery.

**2 · Brown-out.** WiFi transmit peaks reach 500 mA. Without local
decoupling the ESP32 resets itself mid-session. 1000 µF + 100 nF **right at
the board**, not somewhere along the rail.

**3 · Shared returns.** The heater's 0.300 A flowing down a common ground
shifts the reference under the DS18B20 readings, and 1-Wire is sensitive to
exactly that. Power and signal each return on their own conductor to a
single common point.

**What does not run on 5 V:** the NEMA 17s of a future OnStep GoTo. A
TMC2209 starts from 4.75 V, but a NEMA 17 at 5 V delivers a fraction of its
torque. The mount gets its own 12 V supply.

</details>

Pinout, sensor placement and mounting → [`hardware/wiring.md`](hardware/wiring.md)

---

## Design principles

These are the rules the whole project was built against. They are worth
more than any individual part.

> **Safety never depends on a mechanism.**
> A rotating shutter was designed for the solar cap and then scrapped: a
> gust of wind could turn it, exposing 60 mm of unfiltered Sun with an eye
> at the eyepiece. If a single failure can hurt someone, the design is
> wrong — not the user.

> **The control loop lives in the instrument.**
> The heater loop runs inside the ESP32. If WiFi drops mid-session it keeps
> working on its last setpoint. The laptop is a window onto the instrument,
> never the thing that decides.

> **The source is the script; everything else is derived.**
> Parts come from parametric scripts, not from meshes. Change a parameter,
> re-run, and the dimensioned drawing recalculates itself — the drawings use
> Rhino 8 dynamic sections, not `Make2D`. STEP is published; STL is a
> release artefact.

> **Measure, then claim.**
> Every dimension in `docs/measurements.md` came off a caliper. Every number
> in `docs/calculations.md` shows its working. The results section stays
> empty until there are results.

> **Record the mistakes.**
> [`docs/design-notes.md`](docs/design-notes.md) §5 lists eleven of them,
> with what was wrong and why. That is the part of a project that cannot be
> reconstructed by looking at the finished object.

---

## Repository layout

```
cad/
  scripts/      .py parametric generators        ← text, commit freely
  models/       .3dm Rhino models                ← binary, commit sparingly
  step/         exchange geometry                ← committed
  stl/          meshes                           ← release artefact
  drawings/     dimensioned PDF per part
docs/           measurements, calculations, design notes, LaTeX report
firmware/       ESP32 · PlatformIO
client/         terminal UI · Python + rich
hardware/       BOM, wiring, pinout, schematics
```

**Naming:** geometry carries the part number (`NI-04_motor_pulley.3dm`,
`.step`, `.stl`, `.pdf`); scripts do not (`motor_pulley.py`). A `.py` is
not the part — it is what generates it.

| Document | |
|---|---|
| [`docs/measurements.md`](docs/measurements.md) | Every dimension measured on the telescope, with calipers |
| [`docs/calculations.md`](docs/calculations.md) | The numbers, with the reasoning behind each one |
| [`docs/design-notes.md`](docs/design-notes.md) | Architecture, what was rejected and why, mistakes made |
| [`docs/drawing-workflow.md`](docs/drawing-workflow.md) | How the dimensioned drawings are produced in Rhino 8 |
| [`cad/parts.md`](cad/parts.md) | Part index, materials, print settings |
| [`hardware/wiring.md`](hardware/wiring.md) | Wiring, pinout, sensor placement |
| [`hardware/bom.csv`](hardware/bom.csv) | Bill of materials, with the parts that must not be substituted |

> Design documentation is written in Spanish. Code, filenames and this
> README are in English.

---

## Printing

STL files are **not versioned** — they are derived artefacts, regenerated
from the sources and attached as a ZIP to each
[release](../../releases). Nobody clones a repository to print a part.

Three settings that are **not preferences**:

| | |
|---|---|
| **NI-04 prints upright, axis vertical** | Laid flat the O-ring groove comes out oval and the belt jumps off |
| **NI-06 is PETG, ASA or ABS — never PLA** | It points at the Sun; PLA softens around 55 °C. A frame that deforms with the film fitted opens a gap *while you are observing* |
| **NI-07 stops at 3 perimeters** | The 4.33 mm bar is 10.8 lines of 0.4 mm; more and it prints hollow |

PETG on a CR-10 V2: nozzle 235–245 °C, bed 75–85 °C, part fan **30–50 %**
(not 100 %, or layer adhesion suffers), higher retraction, glue stick as a
release layer — it sticks too well to bare glass.

Printed one of these? **[Send a print report](../../issues/new?template=print-report.yml)** —
fit tolerances depend on your printer as much as on the model, and reports
that say *"it fitted"* are as useful as reports that say it did not.

---

## Roadmap

| | | |
|---|---|---|
| 1 | Thermal control | fan + heater + sensors + ESP32 |
| 2 | Motorised focuser | 28BYJ-48 + ULN2003 |
| 3 | Solar cap with bayonet | awaiting PETG and film |
| 4 | Bahtinov mask | printed, awaiting a star test |
| 5 | Interior flocking | one continuous sheet, never patches |
| 6 | Dew shield | optional, 3 mm foamed PVC, external |
| 7 | OnStep GoTo | separate project, 12 V, after 1 and 2 |
| 8 | Raspberry Pi + IMX477 | 0.49″/px at native f/5 — the end of the road |

---

## Safety — solar filter

> [!WARNING]
> **Your eyesight depends on this. There is no room for improvisation.**
>
> - Film is **Baader AstroSolar Safety Film ND5**, bought from an astronomy
>   supplier. Never welding glass, X-ray film, CDs or smoked glass.
> - **Inspect it against a bright light before every use.** A single
>   pinhole, scratch or lifted edge and it does not get used. The usual
>   failure is not the film — it is the frame adhesive letting go.
> - The film is **clamped, never glued**, and left slightly slack. Soft
>   wrinkles are correct; a tensioned sheet distorts optically and tears
>   with thermal cycling.
> - **Cover or remove the red-dot finder** before pointing at the Sun. It
>   has its own unfiltered light path.
> - **Eyepiece solar filters: never.** The full energy of the telescope
>   concentrates there and they crack with your eye behind them. They have
>   caused blindness.

This repository publishes a **mechanical frame only**. It certifies no
filter material, and pull requests proposing alternative or homemade films
will not be accepted. See [`docs/design-notes.md`](docs/design-notes.md) §7
and [`CONTRIBUTING.md`](CONTRIBUTING.md).

---

## Licence

| | | |
|---|---|---|
| `cad/` · `hardware/` | **CERN-OHL-W v2** | weakly reciprocal open hardware |
| `firmware/` · `client/` | **MIT** | lift the code into anything |
| `docs/` | **CC BY-SA 4.0** | measurements and reasoning stay open |

Reasoning behind each choice → [`NOTICE.md`](NOTICE.md)

## Citing

A [`CITATION.cff`](CITATION.cff) is included — use the **Cite this
repository** button in the sidebar.

<div align="center">

---

**David Conesa Pagán**

[![ORCID](https://img.shields.io/badge/ORCID-0009--0003--9942--884X-a6ce39?style=flat-square)](https://orcid.org/0009-0003-9942-884X)
[![GitHub](https://img.shields.io/badge/GitHub-Dacongan-181717?style=flat-square)](https://github.com/Dacongan)

Naval Architecture & Marine Systems Engineering · UPCT

</div>
