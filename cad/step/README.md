# cad/step — exchange format

**Empty on purpose.** The STEP files still have to be exported from
Rhino, one per part.

STEP is the published geometry of this project. Unlike an STL, it is a
BREP: exact NURBS surfaces, real faces, edges and solids. Ø16.00 stays
Ø16.00 instead of becoming a facetted approximation, and anyone who
downloads a part can measure it, dimension it, modify it or mesh it for
FEA in any CAD package. An STL can only be sliced.

## Export

```
Rhino 8 → select the solid → _Export
  Format ....... STEP (*.stp, *.step)
  Schema ....... AP214 Automotive Design   (AP242 also fine)
  Units ........ Millimetres
  Tolerance .... default
```

Save as `cad/step/NI-xx_<part>.step`, matching the model filename so the
folders line up. Geometry carries the part number; scripts do not — see
`../parts.md`.

```
cad/scripts/motor_pulley.py          ← generator, clean module name
cad/models/NI-04_motor_pulley.3dm    ← Rhino model
cad/step/NI-04_motor_pulley.step     ← exchange geometry   ← committed
cad/stl/NI-04_motor_pulley.stl       ← mesh for slicing    ← git-ignored
```

## Pending export

- [ ] `NI-03_focus_wheel.step`
- [ ] `NI-04_motor_pulley.step`
- [ ] `NI-06_solar_cap.step` (three solids: cap, ring, plug)
- [ ] `NI-07_bahtinov_mask.step`
- [ ] `NI-08_focuser_dust_cap.step`
- [ ] `NI-01_ventilation_cover.step`

Run `_SelBadObjects` before every export. It must select nothing.
