# Cálculos

> Los números con su razonamiento. **Única fuente de verdad de los
> cálculos**; las cotas de partida están en `measurements.md` y las
> decisiones que salen de aquí, en `design-notes.md`.
>
> Extraído de `project-context.md` §4 y §6.

---

## 1. Muestreo y límite de resolución

| Configuración | f/D | "/px con la SV105 (3 µm) |
|---|---|---|
| Foco primario | f/5 | 0,95 |
| Con Barlow ×3 | f/15 | 0,32 |

Límite de Dawes de 130 mm: **0,89"**. El seeing típico está en 2–3", así
que **la atmósfera limita antes que el espejo**. Ese es el resultado que
gobierna todo el proyecto: no hay margen que ganar por apertura, solo por
control térmico, enfoque y colimación.

### Zona de enfoque crítico

```
CFZ = 2 · lambda · N²

  f/5   ->   27,5 um
  f/15  ->  247   um
```

### Alternativa de cámara considerada

**Raspberry Pi HQ Camera (IMX477)**, ~55 €. Píxel 1,55 µm → **0,49"/px a
f/5 nativo**, y Nyquist sobre Dawes pide 0,445". Muestreo casi óptimo sin
Barlow, Bayer crudo 10/12 bits, ROI y decenas de fps.

**Avisos:** necesita adaptador C a 1,25" y hay que comprobar el
back-focus — los Newton baratos a veces no llegan a foco con cámara.

---

## 2. Enfocador motorizado

```
Ø piñón                        8,50 mm
Avance por vuelta              pi x 8,50 = 26,7 mm
Polea grande (efectiva)       33,3 mm
Polea motor (a diseño)        16,0 mm
Reducción                      2,08 : 1
Pasos motor (media marcha)  4.096
Pasos por vuelta de eje     8.525
RESOLUCIÓN                     3,13 um / paso

CFZ f/5  =  27,5 um   ->   9 pasos
CFZ f/15 = 247   um   ->  79 pasos
```

### Par disponible

```
Par 28BYJ-48 (salida)        ~300 g·cm
Par en el eje del piñón       624 g·cm
Fuerza en la cremallera      14,4 N  (~1,5 kg)
```

Factor de seguridad de varias veces sobre lo necesario. **El límite real
no es el par sino la fricción de la goma**, que patinará antes — y eso es
una ventaja de seguridad, no un defecto: si el enfocador topa, patina en
vez de romper el piñón.

**No subir la reducción.** La precisión ya sobra doce veces (3,13 µm/paso
contra 27,5 de CFZ a f/5) y lo que escasea es velocidad: 50 mm de
recorrido son 32 s.

---

## 3. Tórica de transmisión

```
Distancia mínima entre ejes por choque:
  radio cuerpo 28BYJ-48 (14) + radio polea grande (17) + 3 = 34,0 mm

Con 6 % de estiramiento:
  OD48  ->  34,5 mm   (demasiado justo)
  OD50  ->  37,9 mm
  OD52  ->  41,2 mm   <-- ELEGIDA
  OD55  ->  46,2 mm   (aleja el motor sin necesidad)
```

**Pedida: OD52 × CS4.** El soporte NI-05 llevará ranuras de ajuste para
compensar.

### Radio de garganta

Radio de garganta 2,30 contra 2,00 de la goma = **15 % de holgura**.
Igual que la goma la aprisiona y calienta; mucho mayor vuelve al contacto
en línea. El informe de `motor_pulley.py` avisa si te sales del rango.

---

## 4. Calefactor de secundario a 5 V

```
R = V² / P

6 x 100 ohm en paralelo = 16,7 ohm
  I = 0,300 A
  P = 1,50 W total
  P por resistencia = 0,250 W   (nominal 0,5 W)
```

> Con **1/2 W** cada resistencia va al 50 % de su nominal. Con 1/4 W
> estaría al 100 %, que es exactamente lo que hay que evitar.

**Objetivo térmico:** ambiente +1 a +2 °C, lo justo por encima del punto
de rocío. **Demasiado calor genera convección dentro del tubo y destruye
el detalle planetario más rápido que el propio rocío.**

**Validación:** meter el conjunto en el frigorífico media hora con
corriente. La resistencia debe quedar solo tibia al tacto.

---

## 5. Balance energético del tubo

```
Calefactor   1,5 W
Ventilador   1,0 W
ESP32        0,5 W
Motor        1,0 W
             ------
PICO         4,0 W

Power bank 10.000 mAh a 5 V  ->  ~35 Wh útiles  ->  ~8,8 h
```

Una noche entera con margen. **Lo que no entra en este balance** son los
NEMA 17 de un futuro OnStep: el TMC2209 arranca desde 4,75 V, pero un
NEMA 17 a 5 V da una fracción de su par. La montura llevará su propia
alimentación de 12 V.

---

## 6. Apertura solar

```
Secundario  47 mm  ->  radio libre desde  23,5
Primario   130 mm  ->  radio útil hasta   65,0
Corona disponible                         41,5 mm de ancho

Un agujero fuera de eje debe caber ENTERO en esa corona.
  -> Máximo teórico 41,5 mm
  -> Con margen para la araña: 38 mm

38 mm sobre 650 = f/17,1  ·  Dawes 3,05"
Seeing diurno típico 3-5"  ->  la atmósfera ya limita.
Ampliar el agujero NO daría más detalle real.
```

El informe de `solar_cap.py` comprueba esta geometría en cada ejecución:
borde interior > 23,5 y borde exterior < 65,0.

---

## 7. Máscara de Bahtinov

```
Criterio: ranura = focal / factor,  factor 150 (punto medio)

  650 / 150 = 4,33 mm de ranura
  Periodo   = 8,67 mm
  15 ranuras a lo ancho de la apertura
  Barra de 4,33 mm = 10,8 líneas de 0,4  ->  MÁXIMO 3 PERÍMETROS
```

### Por qué la zona de ranuras es 130 mm y no 155

La luz de una estrella llega **colimada**: rayos paralelos. Un rayo que
entra a 70 mm del eje sigue a 70 mm al llegar al fondo del tubo, y el
espejo acaba en 65. Se pierde. La zona útil es exactamente la proyección
del primario, y el borde ancho es inevitable.

*(Este punto se razonó mal al principio — ver `design-notes.md`,
"errores cometidos".)*

### Volumen y radios macizos

```
Placa 2 mm + faldón 10 mm  ->  41.657 mm³  ->  52 g macizo
Radio macizo entre sectores (margen 3°, cubo 56):
   2,93 mm junto al cubo
   6,81 mm en el borde
```

Un disco de 167,6 mm tiene **22.000 mm³ por cada milímetro de espesor**, y
las ranuras solo vacían la corona de 56 a 130. Por eso la placa bajó de
3 mm a 2 mm: de 76 g y 7:39 de impresión a 52 g y 5:41. La rigidez de un
disco de este diámetro la da el faldón perimetral trabajando como aro, no
el espesor de la placa.

---

## 8. Ganancia de la rueda de enfoque

```
Original       34,3 mm
Corona grande  54,0 mm   ->  x1,57 de par
Corona pequeña 34,0 mm   ->  x0,99  (equivalente a la original)
```

Las dos coronas giran lo mismo — mismo eje. Lo que cambia es la fuerza de
dedo y el ángulo recorrido, **no el avance**.
