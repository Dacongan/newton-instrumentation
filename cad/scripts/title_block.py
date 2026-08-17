# -*- coding: utf-8 -*-
"""
================================================================
CAJETIN PARA PLANOS  ·  140 x 40 mm
newton-instrumentation · Rhino 8 · A4 apaisado
================================================================

Dibuja marco y cajetin en la PAGINA DE DISENO activa.
Para cada pieza nueva solo se edita el diccionario PIEZA.

*** EJECUTAR CON LA PAGINA ACTIVA Y FUERA DE TODO DETALLE ***
Comprobacion: arriba a la izquierda debe poner solo "Pagina 1",
sin la palabra "Detalle". Dentro de un detalle, el cajetin se
escalaria con el.

----------------------------------------------------------------
CORREGIDO EN ESTA VERSION
----------------------------------------------------------------
  El texto se salia por debajo de las celdas.

  Causa: rs.AddText coloca el texto tomando el punto dado como
  esquina SUPERIOR izquierda por defecto, asi que el texto
  colgaba hacia abajo.

  Solucion: se fija la justificacion a ABAJO-IZQUIERDA en cada
  texto (codigo 65537 = 1 izquierda + 65536 abajo). Ahora el
  punto dado es la linea base y el texto crece hacia arriba.

----------------------------------------------------------------
GEOMETRIA
----------------------------------------------------------------
  A4 apaisado ............. 297 x 210
  Margen izquierdo ........  20   (para encuadernar)
  Margen resto ............  10
  Marco ................... (20,10) a (287,200) = 267 x 190
  Cajetin ................. (147,10) a (287,50) = 140 x 40
  4 filas de 10 mm

  Fila 4  DENOMINACION 105 | N.PLANO 35
  Fila 3  DIBUJADO 45 | FECHA 40 | ESCALA 30 | HOJA 25
  Fila 2  MATERIAL 45 | ACABADO 60 | MASA 35
  Fila 1  TOLERANCIAS 85 | PROYECCION 55

================================================================
"""

import rhinoscriptsyntax as rs


# ================================================================
# DATOS DE LA PIEZA — editar solo esto
# ================================================================

PIEZA = {
    "denominacion": "POLEA DEL MOTOR",
    "numero":       "NI-04",
    "autor":        "D. Conesa Pagan",
    "fecha":        "16-08-2026",
    "escala":       "5:1",
    "hoja":         "1 / 1",
    "material":     "PLA",
    "acabado":      "FDM 0,2 mm",
    "masa":         "2,4 g",
    "tolerancias":  "ISO 2768-m",
    "proyeccion":   "1er diedro",
}

PROYECTO = "newton-instrumentation"
REPO     = "github.com/Dacongan"
LICENCIA = "CERN-OHL-W v2"


# ================================================================
# GEOMETRIA
# ================================================================

PAG_W, PAG_H = 297.0, 210.0
MARGEN_IZQ   =  20.0
MARGEN       =  10.0

CAJ_W, CAJ_H = 140.0, 40.0
FILA         =  10.0

CX = PAG_W - MARGEN - CAJ_W      # 147
CY = MARGEN                      # 10

TXT_TIT = 3.5    # denominacion
TXT_VAL = 2.5    # valores
TXT_ETQ = 1.8    # etiquetas

SANGRIA = 1.5    # desde el borde izq de la celda
Y_ETQ   = 7.0    # linea base de la etiqueta, sobre el suelo
Y_VAL   = 1.8    # linea base del valor, sobre el suelo

# justificacion: 1 (izquierda) + 65536 (abajo)
JUST_AB_IZQ = 65537


# ================================================================
# UTILIDADES
# ================================================================

def capa(nombre, color, grosor):
    if not rs.IsLayer(nombre):
        rs.AddLayer(nombre, color)
    rs.LayerPrintWidth(nombre, grosor)
    return nombre


def linea(x1, y1, x2, y2, cap):
    o = rs.AddLine((x1, y1, 0), (x2, y2, 0))
    rs.ObjectLayer(o, cap)
    return o


def rect(x, y, w, h, cap):
    pts = [(x, y, 0), (x + w, y, 0), (x + w, y + h, 0),
           (x, y + h, 0), (x, y, 0)]
    o = rs.AddPolyline(pts)
    rs.ObjectLayer(o, cap)
    return o


def texto(t, x, y, alt, cap):
    """
    El punto (x,y) es la LINEA BASE izquierda del texto.
    Sin fijar la justificacion, Rhino lo colgaria hacia abajo
    y se saldria de la celda.
    """
    o = rs.AddText(t, (x, y, 0), alt)
    if o:
        rs.ObjectLayer(o, cap)
        try:
            rs.TextObjectJustification(o, JUST_AB_IZQ)
        except Exception:
            pass
    return o


def celda(x, fila, etiqueta, valor, cap, alt_val=None):
    """
    x    : X del borde izquierdo de la celda
    fila : 1 (abajo) a 4 (arriba)
    """
    if alt_val is None:
        alt_val = TXT_VAL

    y_base = CY + FILA * (fila - 1)

    texto(etiqueta, x + SANGRIA, y_base + Y_ETQ, TXT_ETQ, cap)
    texto(valor,    x + SANGRIA, y_base + Y_VAL, alt_val,  cap)


# ================================================================
# CONSTRUCCION
# ================================================================

def dibujar():
    c_marco = capa("PLANO::Marco",   (0, 0, 0), 0.50)
    c_caj   = capa("PLANO::Cajetin", (0, 0, 0), 0.35)
    c_fino  = capa("PLANO::Fino",    (0, 0, 0), 0.18)

    rs.EnableRedraw(False)

    # --- marco --------------------------------------------------
    rect(MARGEN_IZQ, MARGEN,
         PAG_W - MARGEN_IZQ - MARGEN,
         PAG_H - 2 * MARGEN, c_marco)

    # --- caja del cajetin ---------------------------------------
    rect(CX, CY, CAJ_W, CAJ_H, c_marco)

    for i in (1, 2, 3):
        linea(CX, CY + FILA * i, CX + CAJ_W, CY + FILA * i, c_caj)

    # --- FILA 4 (arriba) ----------------------------------------
    linea(CX + 105, CY + 3 * FILA, CX + 105, CY + 4 * FILA, c_caj)
    celda(CX,       4, "DENOMINACION", PIEZA["denominacion"],
          c_caj, TXT_TIT)
    celda(CX + 105, 4, "N. PLANO",     PIEZA["numero"], c_caj)

    # --- FILA 3 -------------------------------------------------
    for dx in (45, 85, 115):
        linea(CX + dx, CY + 2 * FILA, CX + dx, CY + 3 * FILA, c_caj)
    celda(CX,       3, "DIBUJADO", PIEZA["autor"],  c_caj)
    celda(CX + 45,  3, "FECHA",    PIEZA["fecha"],  c_caj)
    celda(CX + 85,  3, "ESCALA",   PIEZA["escala"], c_caj)
    celda(CX + 115, 3, "HOJA",     PIEZA["hoja"],   c_caj)

    # --- FILA 2 -------------------------------------------------
    for dx in (45, 105):
        linea(CX + dx, CY + FILA, CX + dx, CY + 2 * FILA, c_caj)
    celda(CX,       2, "MATERIAL", PIEZA["material"], c_caj)
    celda(CX + 45,  2, "ACABADO",  PIEZA["acabado"],  c_caj)
    celda(CX + 105, 2, "MASA",     PIEZA["masa"],     c_caj)

    # --- FILA 1 (abajo) -----------------------------------------
    linea(CX + 85, CY, CX + 85, CY + FILA, c_caj)
    celda(CX,      1, "TOLERANCIAS GENERALES",
          PIEZA["tolerancias"], c_caj)
    celda(CX + 85, 1, "PROYECCION", PIEZA["proyeccion"], c_caj)

    # --- proyecto y licencia, encima del cajetin ----------------
    texto(PROYECTO, CX, CY + CAJ_H + 5.5, TXT_VAL, c_fino)
    texto(REPO + "  ·  " + LICENCIA,
          CX, CY + CAJ_H + 2.0, 1.6, c_fino)

    rs.EnableRedraw(True)
    return True


# ================================================================
# INFORME
# ================================================================

def informe():
    print("=" * 58)
    print(" CAJETIN  ---  %s" % PIEZA["denominacion"])
    print("=" * 58)
    print(" Plano %s · escala %s · hoja %s"
          % (PIEZA["numero"], PIEZA["escala"], PIEZA["hoja"]))
    print(" %s · %s · %s"
          % (PIEZA["material"], PIEZA["acabado"], PIEZA["masa"]))
    print("-" * 58)
    print(" Marco ....... (%.0f,%.0f) a (%.0f,%.0f)"
          % (MARGEN_IZQ, MARGEN, PAG_W - MARGEN, PAG_H - MARGEN))
    print(" Cajetin ..... (%.0f,%.0f) a (%.0f,%.0f) = %.0f x %.0f"
          % (CX, CY, CX + CAJ_W, CY + CAJ_H, CAJ_W, CAJ_H))
    print("-" * 58)
    print(" Texto justificado ABAJO-IZQUIERDA en todas las")
    print(" celdas: el punto dado es la linea base, no el techo.")
    print(" Asi no se sale por debajo.")
    print("-" * 58)
    print(" AHORA")
    print("   1. Bloquear la capa PLANO::Cajetin")
    print("   2. Acotar SIEMPRE desde la pagina, nunca dentro")
    print("      de un detalle, o las cotas se repiten en todos")
    print("      los detalles que enfocan esa zona")
    print("   3. Un ESTILO DE COTA por cada escala, con su")
    print("      factor de escala lineal:")
    print("        detalle  5:1  ->  factor 0,2")
    print("        detalle 10:1  ->  factor 0,1")
    print("        detalle 20:1  ->  factor 0,05")
    print("=" * 58)


if __name__ == "__main__":
    if dibujar():
        informe()
