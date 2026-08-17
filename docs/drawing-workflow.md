# Guía: plano acotado en Rhino 8

> **Método de secciones dinámicas.** Sustituye al de `_Make2D` + rayado
> manual, que era el flujo de Rhino 7 y anteriores.
>
> Ventaja decisiva para este proyecto: la sección se **actualiza sola**
> cuando cambia el modelo. Como las piezas salen de scripts
> paramétricos, cada vez que toques un parámetro y regeneres, el plano
> se recalcula sin rehacer nada.

**Objetivo:** una página A4 horizontal con el 3D sombreado arriba y,
debajo, la sección longitudinal rayada y la vista superior, acotadas.

---

## FASE 1 — Estilo de sección (define el rayado)

En Rhino 8 el rayado de las zonas cortadas **no se dibuja a mano**: es
una propiedad del objeto o de la capa que se aplica sola al cortar.

1. Panel **Capas** → localiza la capa de la pieza
2. Busca la columna **Section Style** (Estilo de sección)
3. Clic en `None` → se abre el diálogo
4. Configura:

```
Hatch Pattern ..... ANSI31     (rayado a 45°, el normalizado)
Rotation .......... 0
Scale ............. 0,5        (ajustar al ver el resultado)
Background ........ None
```

5. OK

> El estilo se puede poner **por capa** o **por objeto**. Por capa es lo
> práctico: todas las piezas de esa capa se rayan igual.

Si `ANSI31` no aparece, hay que importarlo:
`_Options` → página **Hatch** → botón **Import** → elegir el patrón.

---

## FASE 2 — Plano de corte

1. Comando `_ClippingPlane`
2. Dibuja el plano **pasando por el eje de la pieza**, en la vista
   Frontal, de lado a lado
3. Selecciona el plano recién creado y abre **Propiedades**

Ahí verás, y conviene revisarlo:

```
Nombre .............. A-A          (aparecerá en la etiqueta)
Section Style ....... By Layer     (usa el de la Fase 1)
Objects Clipped ..... All
Views Clipped ....... marca solo la vista que quieras cortar
Depth ............... por defecto
```

> **Ponle nombre al plano.** Rhino lo usa para etiquetar el dibujo y
> para nombrar las capas que va a generar.

4. Mueve y gira el plano con los puntos de control hasta que el corte
   pase exactamente por el eje. El punto central lo mueve, los de los
   extremos lo escalan.

En la vista ya deberías ver la pieza cortada **y rayada**.

---

## FASE 3 — Generar el dibujo vectorial

1. Comando `_ClippingDrawings`
2. Selecciona el plano de corte `A-A`
3. En las opciones de la línea de comandos:

```
AddBackground .... Yes      dibuja también lo que hay detrás del corte
Projection ....... Parallel  proyección paralela, NO perspectiva
ShowLabel ........ No        (o Yes si quieres la etiqueta A-A)
Hatches .......... Yes       genera el rayado del estilo de sección
HiddenCurves ..... Yes       líneas ocultas del fondo
```

4. Haz clic donde quieras colocar el dibujo

Rhino genera el dibujo **organizado en capas automáticamente**:

| Capa | Contenido |
|---|---|
| `A-A_Drawing` | curvas de la sección |
| `A-A_DrawingHatch` | el rayado |
| `A-A_DrawingHidden` | líneas ocultas del fondo |
| `A-A_DrawingBackground` | siluetas de lo que hay detrás |

> Aquí está la ganancia: **visibles, ocultas y rayado ya vienen
> separadas.** No hay que tocar el diálogo de "Capas por resultado" ni
> asignar estilos a mano.

Si no quieres ver las líneas ocultas, oculta `A-A_DrawingHidden`.

### Asignar grosores

| Capa | Anchura de impresión |
|---|---|
| `A-A_Drawing` | 0,50 |
| `A-A_DrawingHidden` | 0,25 + tipo **Discontinua** |
| `A-A_DrawingBackground` | 0,35 |
| `A-A_DrawingHatch` | 0,13 |

> **Las capas del dibujo nacen bloqueadas.** Si las desbloqueas y mueves
> el dibujo, volverá a su sitio al actualizarse. Para reposicionarlo,
> usa la opción **Move** del propio `_ClippingDrawings`.

---

## FASE 4 — La vista superior

De la planta solo interesa el perfil de doble D del agujero. No lleva
corte, así que hay dos vías:

**A. Detalle con modo técnico** (más simple)
En la página, un detalle en vista **Superior** con el modo de
visualización **Technical** o **Pen**. Esos modos imprimen como
vectores desde la página, así que no hace falta generar curvas.

**B. `_Make2D`** (si prefieres curvas editables)
Vista Superior, y en el diálogo:
```
Propiedades de objeto .. Capas por resultado
Líneas ocultas ......... marcado
Proyección ............. Primer ángulo
```

---

## FASE 5 — La página

1. Pestaña **Diseños** abajo → clic derecho → **Nueva página**
2. **A4, horizontal** (297 × 210)
   > Para la Bahtinov y la tapa solar, que miden 167,6 mm, usa **A3
   > horizontal**: a 1:1 no caben en A4 con márgenes y cajetín, y a
   > 1:2 se pierde el detalle de las ranuras.
3. Con la página activa, ejecuta `cajetin_rhino.py`
4. Bloquea la capa `PLANO::Cajetin`

---

## FASE 6 — El 3D sombreado arriba

> `_ClippingDrawings` y `_Make2D` dan **curvas**, nunca sombreado. El
> 3D sombreado se consigue con un **detalle**, que es una ventana viva
> al modelo dentro de la página.

1. Comando `_Detail`
2. Dibuja el rectángulo de la zona superior
3. **Doble clic dentro** para entrar (el borde se resalta)
4. Orienta a una isométrica que se entienda
5. Cambia el modo de visualización a **Sombreado**
   (clic en el nombre de la vista, arriba a la izquierda del detalle)
6. Ajusta el zoom
7. **Doble clic fuera** para salir
8. Detalle seleccionado → **Propiedades** → marcar **Bloqueado**

> Sin ese bloqueo, cualquier zoom accidental te desorienta la vista.

**Truco:** oculta en ese detalle las capas del dibujo de sección, para
que no se superpongan al 3D. Los detalles admiten visibilidad de capa
independiente.

---

## FASE 7 — Colocar las vistas 2D

Dos detalles más en la zona inferior:

- **Izquierda:** la sección `A-A`, en vista Superior
- **Derecha:** la planta

En cada detalle, **Propiedades → Escala**, fija **2:1** para la polea.
Es más fiable que escalar las curvas con `_Scale`, porque la escala
queda registrada y el plano sigue siendo trazable.

Alinea las dos vistas: los ejes deben coincidir.

---

## FASE 8 — Ejes de simetría

Obligatorio en piezas de revolución.

1. Capa activa `PLANO::Ejes`, tipo de línea **Centro**
2. Línea vertical por el centro de la sección, sobresaliendo 3-5 mm
3. Cruz de centros en la planta

---

## FASE 9 — Acotar

Antes, comando `_DimStyle`:

```
Altura de texto ......... 2,5 mm
Longitud de flecha ...... 2,5 mm
Extensión de línea ...... 1,25 mm
Precisión ............... 0,00
Fuente .................. Arial
```

> **Acota en la página, no en el modelo.** Así las cotas van a escala
> del papel y no se deforman si cambias la escala del detalle.

### Cotas de la sección A-A
```
Ø 20,40    diámetro exterior sobre pestañas
Ø 16,00    diámetro efectivo, fondo de garganta
   10,00   altura total
R  2,30    radio de la garganta
   8,00    profundidad del alojamiento
   0,60 × 45°   chaflán de entrada
   2,70    pestaña (una sola vez, no las dos)
```

### Cotas de la planta
```
Ø  5,15    alojamiento del eje
   3,00    entre caras planas
Ø 11,00    alivio de la cara superior
```

**Cada cota una sola vez**, en la vista donde mejor se entienda.

---

## FASE 10 — Comprobar y exportar

### Antes de exportar
- [ ] `_SelBadObjects` no selecciona nada
- [ ] El rayado se ve a 45° y con densidad razonable
- [ ] Las líneas ocultas salen discontinuas
- [ ] Ninguna cota se solapa
- [ ] Los ejes de simetría están puestos
- [ ] La escala del cajetín coincide con la del detalle
- [ ] Los datos del cajetín son los de esta pieza

### Exportar
```
_Print
  Destino ....... PDF
  Salida ........ VECTORIAL     <-- innegociable
  Tamaño ........ A4 horizontal
  Escala ........ 1:1  (la de las vistas ya está en los detalles)
```

Guardar en `cad/drawings/NI-04-polea.pdf`

> Vectorial siempre. Un plano rasterizado se ve pixelado al imprimir y
> al hacer zoom en el PDF de la memoria.

---

## Resumen del flujo

```
capa de la pieza
   └── Section Style: ANSI31          (define el rayado)

modelo 3D
   ├── _ClippingPlane "A-A" por el eje
   │      └── _ClippingDrawings ──> curvas + rayado + ocultas,
   │                                 ya separadas en capas
   │                                 y ACTUALIZABLES
   └── vista Superior ──> _Make2D o detalle en modo Technical

página A4 horizontal
   ├── cajetín          (script)
   ├── detalle 3D       modo Sombreado, bloqueado
   ├── detalle sección  escala 2:1
   ├── detalle planta   escala 2:1
   ├── ejes de simetría
   └── cotas
        └──> _Print vectorial ──> PDF
```

---

## Por qué este método y no `_Make2D`

| | `_Make2D` | Secciones dinámicas |
|---|---|---|
| Rayado | a mano con `_Hatch` | automático, del estilo de sección |
| Separar visibles/ocultas | hay que marcarlo en el diálogo | automático por capas |
| Si cambia el modelo | rehacer todo | se actualiza |
| Cortar la pieza | hay que partir el sólido | el plano de corte no destruye nada |

El último punto es el que más pesa en este proyecto: las piezas salen
de scripts paramétricos y se van a regenerar varias veces.
