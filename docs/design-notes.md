# Notas de diseño

> Las decisiones y su porqué: lo que se eligió, lo que se descartó y lo
> que se hizo mal antes de hacerlo bien. Los números están en
> `calculations.md`; las cotas, en `measurements.md`.
>
> Extraído de `project-context.md` §4, §5, §8, §9, §10b y §11.

---

## 1. Diagnóstico: qué limita de verdad a este telescopio

Por orden:

1. **La SV105.** Es UVC por USB 2.0: entrega vídeo ya desbayerizado y
   normalmente comprimido en MJPEG, sin ROI real. Alimenta a `astrostack`
   con fotogramas que ya perdieron información. **Ninguna mejora mecánica
   arregla esto.**
2. **Aclimatación del primario.**
3. **Rocío en el secundario** — Cartagena, costa mediterránea.
4. **Colimación**, a f/5 crítica y frecuente.

### Por qué NO comprar otro tubo

- La atmósfera ya limita antes que la apertura (Dawes 0,89" contra un
  seeing de 2–3").
- Un 200 mm no cabe en la EQ-3 → habría que cambiar montura → 800-1000 €.
- Los tres cuellos de botella reales se arreglan con ~100 € y trabajo.

**Criterio:** exprimir este tubo hasta poder demostrar con `strehl` que se
ha tocado su techo óptico.

---

## 2. Arquitectura eléctrica

### Todo el tubo a 5 V por USB

Un solo tipo de cable, un solo conector, misma batería, y se puede probar
enchufado al portátil. Consumo pico ~4 W → ~8,8 h con el power bank.

**Lo que NO va a 5 V:** los NEMA 17 de OnStep. El TMC2209 arranca desde
4,75 V pero un NEMA 17 a 5 V da una fracción de su par. La montura
llevará su propia alimentación de 12 V cuando llegue.

### Tres cosas que a 5 V muerden y a 12 V no

1. **Caída de tensión:** 0,5 V es 4 % a 12 V pero **10 % a 5 V**. Cables
   cortos y de 22 AWG mínimo. Medir en la placa, no en la batería.
2. **Brownout del ESP32:** los picos de WiFi llegan a 500 mA. Sin
   desacoplo, el ESP32 se resetea solo. → **1000 µF + 100 nF** junto a la
   placa.
3. **Masas separadas:** los 0,30 A del calefactor por un cable compartido
   descuadran las lecturas del DS18B20 — 1-Wire es sensible a eso.
   Alimentación y señal vuelven cada una por su cable a un punto común.

Detalle de montaje y pinout en `../hardware/wiring.md`.

---

## 3. Arquitectura de control y software

- **El ESP32 crea su propio punto de acceso WiFi (modo AP).** No necesita
  router ni cobertura: aparece la red, se conecta el Mac y se abre
  `192.168.4.1`. **Programar con fallback:** intenta conectarse al WiFi de
  casa y, si no lo encuentra en 10 s, levanta su propio AP. En el monte no
  hay router.
- Soportar **también serie por USB**, como respaldo y para depurar.
- **El ESP32 sirve JSON, no HTML.** Cliente en terminal Python con `rich`,
  coherente con el lenguaje visual de `strehl` y scriptable — que es lo
  que hace falta para el autoenfoque y para las medidas publicables.
- **FALLO SEGURO:** el lazo de control del calefactor corre DENTRO del
  ESP32. Si se cae el WiFi, sigue funcionando con la última consigna. El
  Mac es una ventana, nunca el que decide.
- **Consigna del calefactor:** no es una temperatura fija, es **"mantén el
  secundario 2 °C por encima del punto de rocío"**. El punto de rocío
  cambia durante la noche; una temperatura fija deja de seguirlo.
- **Repositorio público** desde el principio. Nada sensible.
  `.gitignore` para las credenciales WiFi, plantilla en el repo.

---

## 4. Decisiones descartadas y por qué

| Descartado | Motivo |
|---|---|
| **Obturador giratorio** en la tapa solar | Puede girarse solo con una ráfaga → 60 mm de Sol sin filtrar con el ojo en el ocular. La seguridad no debe depender de un mecanismo. |
| **Imanes de neodimio** para sujetar tapones | El tapón se acerca solo y de golpe en el último tramo → puede saltar contra la lámina, que está a 2 mm. Además pierden fuerza con el calor. |
| **Imanes para sujetar el parasol al tubo** | El tubo es de **aluminio: no es ferromagnético.** Y desviarían la brújula al orientar la montura. |
| **Apertura solar de 60 mm** | No cabe: la corona útil fuera de eje mide 41,5 mm. |
| **Segundo agujero pasante** en la tapa solar | Descartado para no llevar 3 tapas. Además era un agujero sin filtrar en una tapa que se usa apuntando al Sol. |
| **Alargue de tubo de 24 cm impreso** | 280 g rígidos a 24 cm del extremo. En una EQ-3 al límite actúa como vela: cuesta más en fotogramas movidos de lo que ahorra en rocío. |
| **Goma EVA para el parasol por fuera** | Funcionaba por dentro *porque* era blanda y hacía muelle. Por fuera no la sostiene nada: se abomba y se vence con el rocío. |
| **Parasol por dentro** | La EVA de 9 mm por lado dejaría el paso en 132 mm y el primario mide 130. A 1 mm de recortar apertura. |
| **Roscas plástico-plástico** para los tapones | Con capas de 0,2 se desgastan y acaban con holgura. |
| **Imprimir la rosca M4 en 3D** | Paso 0,7 mm = 3,5 capas por vuelta. Se pasa de rosca a la tercera noche. |
| **Autoguiado** | No hace falta para planetaria: exposiciones de 1/60 s. La deriva la corrige el alineado multipunto de `astrostack`. |
| **Raspberry Pi ahora** | El Model B no da para captura de vídeo. Y la Pi es *consecuencia* de motorizar la montura, no alternativa al portátil. |
| **Gyroid en la Bahtinov** | Cambio de dirección constante → en una CR-10 con cama pesada, tiempo y vibración. Rejilla o líneas. |
| **Kit "Electronics Fun Kit"** (12,59 €) | Las 100 Ω son 1/4 W (no valen) y los condensadores 100 µF (necesitamos 1000). Seguiría faltando lo importante. |
| **Cambiar la polea metálica de 34 mm por una impresa mayor** | Está torneada, es concéntrica y va con prisionero sobre acero. Una impresa de 54 mm con prisionero sobre eje de acero acabaría patinando, y encima bajaría la velocidad. |
| **Subir la reducción del enfocador** | La precisión ya sobra doce veces; lo que escasea es velocidad. |
| **Cambiar Rhino por FreeCAD** | Los modelos son scripts de `rhinoscriptsyntax` y eso es lo diferencial del trabajo. Cambiar de programa sería volver al día uno. |

---

## 5. Errores cometidos durante el diseño

Se dejan escritos a propósito: son la parte del proyecto que no se puede
reconstruir mirando el resultado.

1. **Hex de tuerca M3 más profundo que el aro** (2,7 mm en 2,0 mm).
   Corregido: aro a 3,5 mm y cara frontal a 12 mm.
2. **Se razonó que la zona de ranuras de la Bahtinov debía ser 152 mm**
   porque la luz "converge poco". **Falso: llega colimada.** Son 130 mm.
3. **Placa de la Bahtinov a 3 mm** → 76 g y 7:39 de impresión. Un disco de
   167,6 mm tiene 22.000 mm³ por milímetro de espesor. Corregido a 2 mm +
   faldón 10 mm → 52 g.
4. **Cubo de 50 mm y margen 2,5°** dejaban puntas de barra de 1 mm junto
   al centro. Corregido a 56 mm y 3°.
5. **Tirador centrado** en la Bahtinov: quedaba delante del secundario y
   obligaba a soportes. Eliminado — se agarra por el canto y el faldón.
6. **Polea del motor con garganta de paredes rectas** (v1). Una tórica es
   de sección circular: sobre fondo plano el contacto es una **línea**.
   Corregido a garganta semicircular.
7. **Segundo intento por revolución de perfil** (v2): la superficie salía
   pero no cerraba como sólido. Resuelto en v3 restando un **toro** a un
   cilindro macizo — un toro *es* un anillo de sección circular, así que
   el canal sale por construcción.
8. **Se insistió en medir el espárrago M4** cuando la ruleta ya estaba
   montada con el inserto termofundido y esa cota había dejado de
   importar.
9. **Se diagnosticó el plano de corte por el tipo "superficie"** que
   mostraba Propiedades. Un plano ES una superficie; ese no era el
   indicador.
10. **Se dio el flujo antiguo de `Make2D` + rayado manual** cuando Rhino 8
    tiene secciones dinámicas que hacen lo mismo automáticamente y se
    actualizan al cambiar el modelo. Ver `drawing-workflow.md`.
11. **Se añadieron cuatro referencias a la lista de compra sin avisar**
    (4,7 kΩ, 220 Ω, 10 kΩ, 100 nF) al cambiar de tienda. No estaban en la
    lista original, y en tienda europea cada valor pasa de 1 €: el precio
    de lote chino no aplica aquí.

---

## 6. Materiales de impresión

| Pieza | Material | Motivo |
|---|---|---|
| NI-06 tapa solar + aro + tapón | **PETG** | apunta al Sol; el PLA reblandece a 55 °C |
| Chasis de gafas de eclipse | **PETG** | mismo rollo |
| NI-07 máscara de Bahtinov | PLA | solo de noche |
| NI-03 rueda de enfoque | PLA | ya impresa, funciona |
| NI-04 polea del motor | PLA | no ve el sol y el PLA es más rígido que el PETG, lo que aquí viene bien |
| NI-05 soporte del motor | **PETG** | par y vibración continuados |
| NI-01 tapa del ventilador | PLA — **no reimprimir** | zona trasera, no le da el sol |

**PETG antes que ABS/ASA, decidido.** El ABS se contrae mucho y sin
cerramiento una pieza de 167 mm levanta las esquinas. Además emite
estireno. El PETG se imprime a cielo abierto y sus 80 °C sobran.

Ajustes PETG en la CR-10 V2:

- Boquilla 235-245 °C · cama 75-85 °C
- **Ventilador al 30-50 %**, no al 100 %: con demasiada refrigeración pega
  mal entre capas y queda frágil
- Sube la retracción: hace hilos
- **Se pega demasiado al cristal.** Laca o cola de barra como separador

Orientaciones y perímetros por pieza: `../cad/parts.md`.

---

## 7. Seguridad — filtro solar

> **De esto depende la vista. No hay margen para el apaño.**

- Lámina: **Baader AstroSolar Safety Film ND5**, comprada en proveedor de
  astronomía. Nunca película de soldador, radiografías, CD ni filtros de
  ocular.
- **Revisar a contraluz ANTES DE CADA USO.** Buscar agujeros, arañazos,
  zonas despegadas del marco, rayas de luz por el borde. **Un solo punto
  de luz: no se usa.** El fallo típico no es la lámina, es el pegamento
  del marco cediendo.
- El filtro heredado del anterior dueño está desgastado → **lámina nueva**.
- **La lámina NO SE PEGA.** Va aprisionada entre el fondo de la cajera y el
  aro, **ligeramente floja**. Las arrugas suaves son correctas: una lámina
  tensada se deforma ópticamente y se rasga con los ciclos térmicos.
  Apretar en cruz y sin forzar.
- **Tapar o desmontar la mira réflex** antes de apuntar al Sol. Tiene su
  propia entrada de luz sin filtrar. Usar el buscador solar de proyección
  que ya trae el tubo.
- **Filtros de ocular: JAMÁS.** Toda la energía del telescopio se concentra
  ahí y se agrietan con el ojo detrás. Han causado ceguera.

### Chasis de gafas de eclipse — idea, no proyecto cerrado

Reutilizar la **lámina certificada de unas gafas de cartón compradas**,
recortándola sin tocarla, y montarla en un chasis impreso en PETG.

**No fabricar la lámina.** Unas gafas de eclipse son producto sanitario
bajo ISO 12312-2; la certificación cubre uniformidad, IR, UV y sobre todo
**que no haya fugas por los bordes ni por el ajuste a la cara**. En un
telescopio un poro se ve a contraluz; en unas gafas pegadas a la cara, una
rendija lateral mete Sol directo sin que lo notes.

Requisitos del chasis:

- **Opaco de verdad.** Comprobar la pieza a contraluz antes de montar la
  lámina: una pieza fina impresa puede transmitir luz.
- **Labio de solape** de varios mm a ambos lados para sellar el canto.
- **Ajuste a la cara.** El cartón cede, el plástico rígido no. Patillas y
  puente en TPU, o burlete de espuma en el borde de contacto.

---

## 8. Montaje del calefactor en el secundario

- Va en el **soporte metálico**, nunca sobre el vidrio y **nunca con epoxi
  rígido** (tensión térmica e irreversible). Pad térmico o silicona
  neutra.
- Todo lo que se añada ahí debe quedar **negro, mate y escondido en la
  sombra que ya proyecta el secundario**.
- Cables: dos, finos y planos, pegados **al canto de una sola pata de la
  araña**, no a la cara ancha. Las patas miden ~1 mm; añadir 1 mm duplica
  la difracción de esa pata. En planetaria no se nota (Júpiter es un
  disco, no un punto); en estrellas brillantes se puede apreciar.
- Alternativa si molesta: anillo calefactor **por fuera** del tubo a la
  altura del secundario. Menos eficiente, más consumo, pero no mete nada
  en el camino óptico.
