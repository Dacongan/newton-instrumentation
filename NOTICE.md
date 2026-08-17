# Licensing notice

This repository mixes hardware designs, firmware and documentation.
Each is covered by the licence that fits it. GitHub displays the root
`LICENSE` only, so this file is the authoritative breakdown.

| Path | Licence | Full text |
|---|---|---|
| `cad/` | **CERN-OHL-W v2** (weakly reciprocal open hardware) | [`LICENSE`](LICENSE) |
| `hardware/` | **CERN-OHL-W v2** | [`LICENSE`](LICENSE) |
| `firmware/` | **MIT** | below |
| `client/` | **MIT** | below |
| `docs/` | **CC-BY-SA 4.0** | https://creativecommons.org/licenses/by-sa/4.0/legalcode |

## Why these three

**CERN-OHL-W** for the physical designs. Weakly reciprocal means someone
can bolt these parts onto a larger proprietary instrument without having
to open that instrument, but if they modify *these* parts and distribute
them, the modifications come back. That is the right trade for parts
meant to be printed and improved by other people.

**MIT** for the code, so the firmware and the terminal client can be
lifted into any other project without friction.

**CC-BY-SA 4.0** for the documentation, so the measurements, the
calculations and the reasoning stay open and attributed. The NC variants
are deliberately avoided: they are incompatible with most open licences
and block legitimate educational reuse.

## MIT Licence — applies to `firmware/` and `client/`

Copyright (c) 2026 David Conesa Pagán

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Disclaimer — solar observation

The solar cap design in `cad/` is published as a mechanical frame only.
It carries no optical filter, and no part of this repository certifies
any filter material. Solar observation is performed at the user's own
risk, with certified film from a reputable astronomy supplier, inspected
before every use. See the safety section of `docs/design-notes.md`.

## Third-party components

No third-party source is vendored in this repository. Libraries pulled
by PlatformIO are declared in `firmware/platformio.ini` and keep their
own licences; Python dependencies are declared in
`client/requirements.txt`.
