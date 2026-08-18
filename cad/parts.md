# Part index

Part numbers are grouped by subsystem, not by date. `NI-04` is fixed:
that number is already stamped on the title block of the motor pulley
drawing. Everything else was numbered around it.

| No. | Part | Subsystem | Script | Model | Drawing | Status |
|---|---|---|---|---|---|---|
| NI-01 | Ventilation cover | Thermal | — | `models/NI-01_ventilation_cover.3dm` | `drawings/NI-01_ventilation_cover.pdf` | Printed, in service |
| NI-02 | Secondary heater mount | Thermal | — | — | — | Not designed |
| NI-03 | Focus wheel (dual crown) | Focuser | `scripts/focus_wheel.py` | `models/NI-03_focus_wheel.3dm` | `drawings/NI-03_focus_wheel.pdf` | **Printed and fitted** |
| NI-04 | Motor pulley | Focuser | `scripts/motor_pulley.py` | `models/NI-04_motor_pulley.3dm` | `drawings/NI-04_motor_pulley.pdf` | Designed v3, not printed |
| NI-05 | Motor mount | Focuser | — | — | — | **Blocked** — see below |
| NI-06 | Solar cap, bayonet | Optics | `scripts/solar_cap.py` | `models/NI-06_solar_cap.3dm` | — | Designed, awaiting PETG |
| NI-06.1 | Film retaining ring | Optics | `scripts/solar_cap.py` | — | — | Designed |
| NI-06.2 | Bayonet plug | Optics | `scripts/solar_cap.py` | — | — | Designed |
| NI-07 | Bahtinov mask | Optics | `scripts/bahtinov_mask.py` | `models/NI-07_bahtinov_mask.3dm` | — | **Printed**, not star-tested |
| NI-08 | Focuser dust cap | Optics | — | `models/NI-08_focuser_dust_cap.3dm` | `drawings/NI-08_focuser_dust_cap.pdf` | Printed, in service |

## Naming convention

**Geometry carries the part number; scripts do not.**

```
cad/scripts/motor_pulley.py         ← generator, clean module name
cad/models/NI-04_motor_pulley.3dm   ← model
cad/step/NI-04_motor_pulley.step    ← exchange geometry
cad/stl/NI-04_motor_pulley.stl      ← mesh
cad/drawings/NI-04_motor_pulley.pdf ← dimensioned drawing
```

A `.3dm`, a `.step`, an `.stl` and a `.pdf` are all *the part* — the
number is how a reader ties a downloaded file back to a drawing, exactly
as it is stamped in the title block. A `.py` is not the part, it is the
thing that generates it, and a Python filename starting with a digit and
containing a hyphen cannot be imported as a module. Keeping scripts clean
costs nothing and avoids that trap later.

`scripts/title_block.py` is not a part either: it draws the A4 frame and
title block on the active layout page. Edit its `PIEZA` dictionary per
drawing.

`models/NI-04_motor_pulley_sheet.3dm` is the drawing sheet for NI-04, kept
separate from the model file.

## Materials and print settings

| No. | Material | Orientation | Perimeters | Infill | Layer |
|---|---|---|---|---|---|
| NI-01 | PLA — **do not reprint** | — | — | — | — |
| NI-03 | PLA | Large crown on the bed | 5 | 30 % | 0.20 |
| NI-04 | PLA | **Upright, axis vertical** | 5 | 40 % | 0.20 |
| NI-06 | **PETG** | Outer face on the bed | 4 | 25 % | 0.20 |
| NI-06.1 | **PETG** | Nut face up | 4 | 25 % | 0.20 |
| NI-06.2 | **PETG** | Flange on the bed, tabs up | 4 | 25 % | 0.20 |
| NI-07 | PLA, matte black | Plate on the bed, skirt up | **3 — no more** | 15 % | 0.28 (first 0.20) |

Three of these are not preferences:

- **NI-04 prints upright.** Laid flat, the groove comes out oval and the
  O-ring jumps off.
- **NI-06 is PETG, ASA or ABS — never PLA.** The part points at the Sun
  and PLA softens around 55 °C. If the frame deforms with the film
  fitted, it slackens or opens a gap *while you are observing*.
- **NI-07 stops at 3 perimeters.** The 4.33 mm bar is 10.8 lines of
  0.4 mm; more perimeters and the bar prints hollow.

PETG on the CR-10 V2 has its own document: the full Cura profile, the
release layer, and the per-piece overrides live in
[`../docs/printing-petg.md`](../docs/printing-petg.md). Short version:
nozzle 240 °C, bed 80 °C first layer and 70 °C after, part fan **40 %**
(not 100 %, or layer adhesion suffers), retraction **slower** rather than
longer, and a glue-stick or hairspray release layer — PETG welds to glass
and takes a chip out of the plate on removal.

Note that NI-06.1 overrides the 25 % in the table above and prints at
**100 %**. It is a bolted clamp: four M3 screws pulling a 3.5 mm plate
against the film. The reason is stiffness, not light — the ring sits
behind 8.5 mm of cap and the film spans its full bore.

## Mass in the title block

The `MASA` field of a drawing is the mass of the part **as modelled**:

```
mass = solid volume from Rhino  x  material density
       PLA  1.24 g/cm3
       PETG 1.27 g/cm3
```

Not the figure the slicer reports. A drawing describes the part, and
infill is a manufacturing parameter — it is recorded in the table above,
which is where it belongs. Reprinting the same part at a different infill
must not invalidate its drawing, and any reader must be able to reproduce
the number from the drawing alone.

Worked example, NI-03: 18 977.17 mm3 solid → 18.98 cm3 × 1.24 =
**23.5 g**. Sliced at 30 % it weighs about 17–20 g; that number does not
go on the drawing.

**NI-01 is unverified.** Its title block says 46.0 g and there is no
record of how that was obtained. Recompute it under this rule before the
drawing is cited anywhere.

## What blocks NI-05

The motor mount cannot be dimensioned until one measurement exists:

> **The gap between the focuser body and the face of the metal pulley.**

It places the motor pulley in the same plane as the metal one so the
O-ring runs straight instead of skewed. The mount also needs tensioning
slots and a 41.2 mm centre distance for the OD52 × CS4 O-ring, and it
anchors to the four Phillips screws on the focuser base. The motor goes
**below** the focuser: more room, clear of the eyepiece, weight close to
the tube.

Second open dimension, needed before printing NI-04: the **flat-to-flat
distance on the 28BYJ-48 shaft**. 3.00 mm is assumed; it varies between
manufacturers. Measure it when the motor arrives and adjust `PLANO_EJE`.

## Regenerating a part

```
Rhino 8 → _RunPythonScript → cad/scripts/<part>.py
_SelBadObjects                    must select nothing
_Export → STEP (AP214 or AP242)   →  cad/step/NI-xx_<part>.step
_Export → STL, binary             →  cad/stl/NI-xx_<part>.stl   (release only)
```

STEP and the source go in every commit. STL is a derived artefact: it is
git-ignored and shipped as a ZIP attached to a release, because that is
what people download from Printables and the forums. Nobody clones a
repository to print a part.
