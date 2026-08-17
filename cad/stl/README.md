# cad/stl — meshes, not versioned

The `.stl` files in this folder exist on disk but are **git-ignored**.
That is deliberate.

A mesh is a derived artefact. The source of truth is the parametric
generator in `cad/scripts/`, and the published geometry is the STEP in
`cad/step/`. Committing a 600 kB mesh on every parameter tweak inflates
the history permanently and adds nothing that cannot be regenerated in
thirty seconds.

## Where to get the printable files

Attached as a ZIP to each **release**. That is the link to hand to
Printables and to the forum thread — nobody clones a repository to print
a part.

## Regenerating

```
Rhino 8 → _RunPythonScript → cad/scripts/<part>.py
_SelBadObjects            must select nothing
_Export → STL, binary, millimetres → cad/stl/NI-xx_<part>.stl
```

Mesh density: fine enough that the facets do not show on curved
surfaces. On the motor pulley groove — a 2.30 mm radius channel — a
coarse mesh flattens exactly the surface the O-ring seats on.

## To publish the meshes anyway

Delete the `cad/stl/*.stl` line from `.gitignore`. One line, reversible.
