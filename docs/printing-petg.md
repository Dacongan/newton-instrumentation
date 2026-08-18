# Impresión en PETG · Creality CR-10 V2

> **Única fuente de verdad de los ajustes de impresión en PETG.** Las
> temperaturas y el ventilador estaban resumidos en
> [`design-notes.md`](design-notes.md) §6; a partir de aquí manda este
> documento y aquello queda como el porqué de haber elegido PETG.
>
> | | |
> |---|---|
> | [`design-notes.md`](design-notes.md) §6 | por qué PETG y no ABS/ASA |
> | [`design-notes.md`](design-notes.md) §7 | seguridad del filtro solar |
> | [`../cad/parts.md`](../cad/parts.md) | orientación, perímetros y relleno por pieza |
>
> Perfil escrito para **Ultimaker Cura**, boquilla 0,4 mm, cama de
> cristal. Primer material distinto del PLA en esta impresora.

---

## 1. Piezas que van en PETG

| Pieza | Motivo |
|---|---|
| NI-06 tapa solar | apunta al Sol; el PLA reblandece a 55 °C |
| NI-06.1 aro de retención de la lámina | mismo conjunto |
| NI-06.2 tapón de bayoneta | mismo conjunto |
| NI-05 soporte del motor | par y vibración continuados |
| Chasis de gafas de eclipse | mismo rollo |

**Filamento: PETG negro opaco.** El color no es estética. Un PETG natural
o translúcido deja pasar luz difusa por el propio material y arruina el
contraste solar, y en una pieza cuyo trabajo es tapar el Sol eso no vale.
El negro además absorbe mejor la luz parásita dentro del tubo.

## 2. Orden de impresión

No se empieza por la tapa: son horas y filamento para calibrar un
material nuevo.

1. **NI-06.1 aro de retención** — pequeño, sin voladizos, y lleva los
   hexágonos de las tuercas. Valida el perfil entero.
2. **NI-06.2 tapón de bayoneta** — valida el ajuste de la bayoneta.
3. **NI-06 tapa** — solo cuando las dos anteriores salgan bien.

## 3. Preparación de Cura

1. `Preferences → Configure setting visibility → All`. Sin esto, la mitad
   de los ajustes de abajo no aparecen en la interfaz.
2. Impresora **Creality CR-10 V2**, 300 × 300 × 400, boquilla 0,4.
3. Material **Generic PETG**. Cargarlo **antes** de tocar los valores: si
   se carga después, pisa los cambios.
4. Perfil de partida: **Standard Quality - 0.2mm**, el genérico. **No
   partir de un perfil propio de PLA**: los perfiles guardados llevan
   dentro overrides de velocidad, ventilador y temperatura que se
   arrastran sin verse. Al terminar, guardar el resultado como
   `PETG CR10 0.2` y reutilizarlo para NI-06 y NI-06.2.
5. `Print settings → Custom`.

## 4. Perfil base PETG

### Quality

| Setting | Valor |
|---|---|
| Layer Height | 0,20 |
| Initial Layer Height | 0,30 |
| Line Width | 0,40 |
| Wall Line Width | 0,38 |
| Initial Layer Line Width | 110 % |

### Walls

| Setting | Valor |
|---|---|
| Wall Line Count | 4 |
| Minimum Wall Line Width | 0,34 (por defecto) |
| Minimum Feature Size | 0,1 (por defecto) |
| Outer Before Inner Walls | Off |
| Z Seam Alignment | User Specified |
| Z Seam X / Y | 150 / 400 |
| Seam Corner Preference | Smart Hiding |
| Horizontal Expansion | 0 |
| Initial Layer Horizontal Expansion | −0,10 |
| Hole Horizontal Expansion | 0 |

### Top/Bottom

| Setting | Valor |
|---|---|
| Top Layers | 5 |
| Bottom Layers | 5 |
| Top/Bottom Pattern | Lines |
| Monotonic Top/Bottom Order | On |
| Enable Ironing | **Off** — el PETG planchado hace pelusa |

### Infill

| Setting | Valor |
|---|---|
| Infill Pattern | Lines |
| Infill Line Directions | `[45,135]` |
| Infill Overlap | 15 % |
| Infill Before Walls | Off |

Densidad **por pieza**, ver §5 y [`../cad/parts.md`](../cad/parts.md).

### Material

| Setting | Valor |
|---|---|
| Printing Temperature | 240 (rango útil 235-245) |
| Printing Temperature Initial Layer | 245 |
| Build Plate Temperature | 80 |
| Build Plate Temperature Initial Layer | 85 |
| Flow | 95 % |
| Infill Flow | 100 % |
| Initial Layer Flow | 100 % |
| Retraction Distance | 5,0 |
| Retraction Speed | 30 |
| Retraction Minimum Travel | 1,5 |
| Maximum Retraction Count | 10 |
| Minimum Extrusion Distance Window | 10 |

### Speed

| Setting | Valor |
|---|---|
| Print Speed | 45 |
| Infill Speed | 45 |
| Inner Wall Speed | 30 |
| Outer Wall Speed | 22 |
| Top/Bottom Speed | 25 |
| Initial Layer Speed | 20 |
| Travel Speed | 150 |
| Enable Acceleration Control | Off |

### Travel

| Setting | Valor |
|---|---|
| Combing Mode | Not in Skin |
| Z Hop When Retracted | On |
| Z Hop Height | 0,2 |
| Enable Coasting | On |
| Coasting Volume | 0,064 |

### Cooling

| Setting | Valor |
|---|---|
| Fan Speed | 40 % |
| Initial Fan Speed | 0 % |
| Regular Fan Speed at Layer | 4 |
| Minimum Layer Time | 8 |
| Minimum Speed | 10 |
| Lift Head | Off |

**Ventilador al 40 %, nunca al 100 % como en PLA.** Con demasiada
refrigeración el PETG pega mal entre capas y la pieza se parte al apretar
los tornillos.

### Support / Adhesion

| Setting | Valor |
|---|---|
| Generate Support | Off |
| Build Plate Adhesion Type | **Skirt** |
| Skirt Line Count | 4 |
| Skirt Distance | 10 |

Sin brim: el PETG apenas se contrae, y sobre cristal el brim cuesta más
quitarlo que lo que aporta. Además se pega al canto inferior, que en el
aro es justo la cara que aprisiona la lámina, y al recortarlo se arriesga
un mordisco donde no puede haberlo.

**Poner Skirt a mano en `Show Custom`, no con el interruptor
`Adhesion: On` del panel Recommended:** ese interruptor selecciona brim
por defecto en Cura 5.

Skirt a **10 mm y 4 líneas**, no los 5 mm y 3 líneas de fábrica. Con
filamento negro brillante sobre cristal negro, a 5 mm no se distingue el
skirt de la pieza a simple vista y no sirve para lo que está: ver el flujo
y el aplastamiento **antes** de que la boquilla toque la pieza. La cuarta
línea alarga además la purga, que en PETG viene bien.

## 5. NI-06.1 · aro de retención de la lámina

Geometría en `../cad/scripts/solar_cap.py`, función `construir_aro()`.

```
D_ARO        68,0     H_ARO        3,5
D_APERTURA   38,0     R_TORNILLOS 30,0 · 4 x
D_M3          3,3     HEX_M3       5,6 · HEX_H 2,6
Fondo bajo la tuerca  0,9
```

| Setting | Valor |
|---|---|
| Infill Density | **100 %** |
| Orientación | cara de las tuercas **arriba** |

**Relleno 100 %, no el 25 % de la tabla general.** Cuesta unos 2 g y cinco
minutos, y a cambio no existe ningún camino interno por el que pueda
colarse luz: ni detrás de la tuerca, ni bajo el fondo de 0,9 mm. En una
pieza de un filtro solar eso no se negocia. Los perímetros no son la
palanca aquí; el relleno sí.

Medido en Cura: **11 g, 3,53 m de filamento, 1 h 17 min.**

El tiempo lo domina la **piel**, no el relleno: de las 17 capas, 10 son
piel (5 de fondo y 5 de arriba) y van a `Top/Bottom Speed`, la velocidad
más lenta del perfil después de la primera capa. Con relleno alto esa piel
de más es redundante — debajo hay macizo, no huecos que tapar. En piezas
grandes como la tapa NI-06 conviene bajar a **3 / 3 capas de piel**, subir
`Top/Bottom Speed` a **35** y `Infill Speed` a **55**. En el aro no merece
la pena: es la pieza de calibración y lento juega a favor.

### Las alturas de capa las fuerzan las cotas

3,5 mm no es múltiplo de 0,2: saldrían 17,5 capas, con la última a medias
y los hexágonos mal cerrados por arriba. Con **primera capa 0,30 y resto
0,20** el reparto es exacto:

```
0,30 + 16 x 0,20 = 3,50      17 capas justas
0,30 +  3 x 0,20 = 0,90      el hexágono empieza en la capa 5
```

Las dos cotas críticas del aro caen en frontera de capa a la vez. Es el
único par de alturas que lo consigue. **No cambiar sin rehacer la cuenta.**

### Pared fina junto a los hexágonos

Tornillos a radio 30, canto exterior a radio 34. El hexágono de 5,6 entre
caras mide 3,23 de radio a la punta, así que queda **entre 0,77 y 1,2 mm
de pared** según cómo caiga la orientación del hexágono.

0,77 mm no da ni para dos perímetros de 0,4. De eso se encarga el
generador de paredes **Arachne**, que desde Cura 5.0 varía el ancho de
línea y rellena esos huecos solo: ahí meterá dos líneas de unos 0,385 en
vez de dejar el hueco. No hay nada que activar; basta con dejar
`Minimum Wall Line Width` en 0,34 y `Minimum Feature Size` en 0,1, que son
los valores por defecto. En Cura 4.x esto se hacía a mano con
`Fill Gaps Between Walls = Everywhere`, ajuste que ya no existe.

De ahí también el relleno al 100 %: si aun así un perímetro se cae, hay
material igual.

Si la pared exterior sale abierta junto a una tuerca, **la solución no es
Cura**: es subir `D_ARO` a 70,0 en el script.

### La cara que aprisiona la lámina

Las tuercas van arriba, luego la cara que toca el cristal es la que
**aprisiona la lámina Baader** contra el fondo de la cajera. Sale espejo y
plana, que es justo lo que hace falta. Si tuviera pata de elefante, el
labio impediría asentar y dejaría una rendija en todo el perímetro: de ahí
el `Initial Layer Horizontal Expansion = −0,10`.

## 6. Cama y despegue

> **El PETG se suelda al cristal.** Si se aplasta la primera capa como con
> PLA, al despegar la pieza se arranca una lasca de vidrio de la cama. Es
> el fallo más caro de este material y no tiene arreglo.

Antes de imprimir:

1. Subir el Z-offset **+0,03 mm** respecto al valor de PLA.
2. **Barra de pegamento (PVA) como separador, no como adhesivo.** Con
   PLA la laca se pone para que agarre; aquí se pone para que *suelte*.
   Es una barrera de sacrificio: al despegar cede el pegamento en vez de
   ceder el vidrio. La barra va mejor que la laca porque deja película
   más gruesa y uniforme; la laca deja capa muy fina y siempre queda
   alguna zona que agarra como el cristal desnudo.

   Aplicar con la cama a 50-60 °C, en pasadas cruzadas, **cubriendo con
   margen toda la huella de la pieza**. Un solo punto de cristal
   descubierto es por donde salta la lasca. Que quede mate, no
   transparente.

   Si se usa laca: **desmontar el cristal y rociar fuera de la
   impresora.** Aerosol inflamable sobre la resistencia de la cama, el
   cableado y una boquilla a 240 °C, no.

   Y no limpiar el cristal con acetona o alcohol y dejarlo desnudo justo
   antes de imprimir PETG: vidrio recién limpio más PETG es la
   combinación que se lleva la lasca.
3. Purgar **100 mm** de filamento a 240 °C al venir de PLA. El PLA que
   queda dentro se carboniza a esa temperatura y ensucia justo las
   primeras capas.

Al terminar: **esperar a que la cama baje de 40 °C.** La pieza se suelta
sola al contraerse. Si hay que hacer palanca, se ha ido pronto.

## 7. Filamento húmedo

El PETG absorbe humedad más rápido que el PLA. Si al extruir suena *crac*
o salen burbujas en el hilo: secar a **65 °C durante 4-6 h**. Un rollo
recién abierto no suele necesitarlo.

## 8. Comprobaciones al sacar la pieza

1. Pasar el dedo por la cara de abajo: **sin labio ni rebaba**. Si lo hay,
   bajar `Initial Layer Horizontal Expansion` a −0,15.
2. Meter una tuerca M3 en un hexágono: debe entrar a mano, con
   rozamiento, sin caerse sola.
3. Un tornillo M3 debe pasar libre por el Ø3,3.
4. **Mirar la pieza a contraluz con una bombilla potente.** En negro los
   defectos no se ven a simple vista: una capa mal pegada o un hueco entre
   perímetros solo aparece con luz detrás. Si hay puntos de luz en el
   fondo de 0,9 mm, subir `Flow` a 98 % y repetir.
5. Apoyar el aro sobre un cristal plano: no debe bailar.

## 9. Corrección · retracción

[`design-notes.md`](design-notes.md) §6 dice «sube la retracción: hace
hilos». Está mal planteado y este documento lo corrige.

En un Bowden como el de la CR-10 V2, subir la **distancia** por encima de
unos 6 mm muele el PETG contra el engranaje del extrusor y acaba en un
atasco por *heat creep*. Lo que hay que bajar es la **velocidad** de
retracción — 30 mm/s en vez de los 45 del PLA — y añadir Z-hop y coasting.
Los hilos de PETG se cortan solos al enfriar; un extrusor que muele, no se
arregla solo.

## 10. Seguridad

La lámina **no se pega**: va aprisionada y ligeramente floja entre el
fondo de la cajera y este aro, apretando los cuatro M3 en cruz y sin
forzar. Protocolo completo, revisión a contraluz antes de cada uso y el
resto de reglas: [`design-notes.md`](design-notes.md) §7. **De eso depende
la vista.**
