# Medidas

> Todas las cotas medidas sobre el telescopio real, con calibre.
> **Esta es la única fuente de verdad de estos números.** Si una cota
> cambia, se cambia aquí y se propaga a los scripts de `cad/scripts/`.
>
> Extraído de `project-context.md` §2 y §3.

---

## Tubo — Bresser Reflektor, Art. No. 46-14600

| Dato | Valor | Origen |
|---|---|---|
| Focal / apertura | 650 mm / 130 mm → **f/5** | catálogo |
| Espejo secundario | 47 mm | catálogo |
| Longitud del tubo | 610 mm | catálogo |
| Ø interior del tubo | **155,30 mm** | **medido** |
| Ø exterior del tubo | ~163,5 mm | deducido |
| Enfocador | piñón y cremallera 1,25", una sola velocidad | — |
| Aumento útil máximo | ~260× | calculado |

## Montura

**EQ-3**, con motor de AR de Celestron (se ajusta con ruleta, incómodo).
Sin GoTo y sin motor de DEC.

---

## Enfocador

| Cota | Valor |
|---|---|
| Ø del piñón (sobre dientes) | **8,50 mm** |
| Ø del eje liso | **4,90 mm** |
| Tramo libre de eje | **24,35 mm** |
| Espesor del piñón | **5,15 mm** |
| Rosca del extremo | **M4 macho** (fondo medido 3,35) |
| Profundidad de rosca original | 6,95 mm |

## Polea existente (metálica, torneada, en el eje)

| Cota | Valor |
|---|---|
| Ø exterior | **34,00 mm** |
| Profundidad de garganta | **0,70 mm** |
| Espesor | **6,00 mm** |
| Ø efectivo (fondo de garganta) | 33,3 mm |

> La garganta de solo 0,7 mm indica **transmisión por fricción**, no
> arrastre positivo: lleva goma redonda apoyada en el fondo. Ventaja
> lateral: si el enfocador topa, la goma patina en vez de romper el
> piñón.

La dejó el anterior dueño, que había motorizado el enfoque. Se reutiliza
tal cual — ver `design-notes.md`, "no cambiarla por una impresa mayor".

## Ruleta original del enfocador

| Cota | Valor |
|---|---|
| Ø exterior | 34,3 mm |
| Ancho | 10 mm |
| Ø interior | 29,65 mm |
| Inserto de latón: Ø moleteado | **5,83 mm** |
| Inserto de latón: Ø cuello | **5,15 mm** |
| Inserto de latón: longitud | **5,00 mm** |
| Holgura al obstáculo más próximo | **14,40 mm** |

El inserto de latón se recuperó de esta pieza y se reutiliza en NI-03.
La holgura de 14,40 mm es la que fija el radio máximo: 31,55 mm de radio
teórico, y la corona grande se diseñó a 54 mm dejando 4 mm de margen.

## Tapa del ventilador — referencia de ajuste al tubo

| Cota | Valor |
|---|---|
| Ø exterior | **167,60 mm** |
| Ø interior | **163,60 mm** |
| Pared | 2,00 mm |

**Ajuste validado en el telescopio.** Es la referencia dimensional de la
que parten la tapa solar (NI-06) y la máscara de Bahtinov (NI-07). La
Bahtinov abre el faldón a 164,4 a propósito, porque se pone y se quita
constantemente: la sujeción la dan tres lengüetas flexibles, no el
apriete del faldón.

## Araña del secundario

**3 patas equiespaciadas**, en triángulo equilátero (cada 120°).

Los huecos libres quedan centrados a 60°, 180° y 300° respecto a
cualquier pata. La apertura solar de 38 mm a radio 44 ocupa **51,2°**, así
que cabe holgada en un hueco con ~35° de margen a cada lado.

→ `ANG_APERTURA` = 60, 180 o 300 en `cad/scripts/solar_cap.py`. En la
práctica se ajusta girando la tapa al montarla, no tocando el parámetro.

---

## Pendiente de medir

- [ ] **Separación entre el cuerpo del enfocador y la cara de la polea
      metálica.** Sitúa la polea del motor en el mismo plano para que la
      tórica trabaje recta. **Bloquea NI-05**, el soporte del motor.
      *(Se prefiere resolverlo al diseñar la carcasa, con el motor
      delante.)*
- [ ] **Separación entre las dos caras planas del eje del 28BYJ-48**, al
      recibir el motor. Se asume 3,00 mm; varía entre fabricantes. Si no
      da, cambiar `PLANO_EJE` en `cad/scripts/motor_pulley.py` y reimprimir.
- [ ] **¿El power bank soporta USB-PD?** Decide si hará falta batería
      aparte para OnStep.

### Cerradas

- [x] ~~Espárrago M4 del eje del piñón~~ — ya no hace falta. La ruleta
      nueva está montada con el inserto de latón termofundido y ocupa ese
      extremo. El motor no lo usa: arrastra la polea metálica de 34 mm
      del lado opuesto.
- [x] ~~Nº de patas de la araña~~ — 3, equiespaciadas.
