# -*- coding: utf-8 -*-
"""
================================================================
RUEDA DE ENFOQUE DOBLE
Bresser Reflektor 130/650  ---  Art. No. 46-14600
================================================================

Pieza unica con dos coronas concentricas sobre el mismo eje:
  - Corona GRANDE (54 mm) atras -> par y tacto fino
  - Corona PEQUENA (34 mm) delante -> enfoque grueso rapido

Sustituye a la ruleta original de plastico.
Fijacion mediante tuerca M4 embebida en la cara trasera,
sobre el esparrago M4 del extremo del eje del pinon.

----------------------------------------------------------------
DATOS MEDIDOS DEL ENFOCADOR
----------------------------------------------------------------
  Diametro del pinon .................. 8,50 mm
  Diametro del eje liso ............... 4,90 mm
  Rosca del extremo ................... M4 (fondo 3,35 mm)
  Profundidad de rosca original ....... 6,95 mm
  Ruleta original: Dext 34,3 / ancho 10 mm
  Holgura al obstaculo mas proximo .... 14,40 mm
  -> Radio maximo teorico 31,55 mm (63 mm de diametro)
  -> Se disena a 54 mm dejando 4 mm de margen

----------------------------------------------------------------
COMO EJECUTARLO
----------------------------------------------------------------
  Rhino > Tools > PythonScript > Edit
  Pegar este archivo y pulsar Run (F5)
  O bien: comando _RunPythonScript y seleccionar el .py

Probado con rhinoscriptsyntax (Rhino 7 y 8).
================================================================
"""

import rhinoscriptsyntax as rs
import math


# ================================================================
# PARAMETROS  --  toca solo esta seccion
# ================================================================

# ---- Corona grande (trasera, la que va hacia el tubo) ----------
D_GRANDE        = 54.0    # diametro exterior sobre puntas
H_GRANDE        =  8.0    # espesor
N_DIENTES_G     =   28    # numero de dientes

# ---- Corona pequena (delantera) --------------------------------
D_PEQUENA       = 34.0
H_PEQUENA       = 10.0
N_DIENTES_P     =   18

# ---- Perfil del dentado ----------------------------------------
PROF_DIENTE     =  2.0    # profundidad radial del diente
FRAC_SUBIDA     = 0.30    # fraccion del paso en la rampa
                          #   0.30 -> V simetrica (recomendado)
                          #   0.05 -> sierra asimetrica
FRAC_PUNTA      = 0.15    # fraccion del paso en el plano de punta
                          #   0 -> punta viva (se clava con frio)

# ---- Fijacion al eje -------------------------------------------
# Inserto termofusible de laton RECUPERADO de la ruleta original
#   moleteado exterior .. 5,83 mm
#   cuello central ...... 5,15 mm
#   longitud ............ 5,00 mm
#   rosca ............... M4
#
# No se modela el moleteado: el taladro es liso y el inserto se
# introduce en caliente con un soldador. El plastico funde, el
# moleteado se hunde en el y el cuello central impide que salga.

D_EJE_PASO      =  4.3    # taladro pasante para el esparrago M4

INS_LARGO       =  5.0    # longitud del inserto
INS_D_ALOJ      =  5.5    # DIAMETRO DEL TALADRO  <-- calibrar
                          #   5,4 si queda flojo / gira
                          #   5,6 si cuesta entrar o abomba
INS_D_BOCA      =  6.1    # avellanado de entrada
INS_H_BOCA      =  0.8    #   recoge el rebose de plastico
INS_D_ALIVIO    =  6.4    # alivio al fondo
INS_H_ALIVIO    =  0.6    #   hueco para el material desplazado

# ---- Aligeramiento ---------------------------------------------
N_RADIOS        =    8
ANCHO_RADIO     =  3.0
R_CUBO          = 18.5    # radio interior de la ventana
R_INT_CORONA    = 24.0    # radio exterior de la ventana

# ---- Rebaje frontal (para marca de referencia) -----------------
D_REBAJE        = 24.0
PROF_REBAJE     =  1.5

# ---- Calidad de malla del perfil -------------------------------
SEG_VALLE       =    6    # segmentos por valle (suavidad)


# ================================================================
# DERIVADAS  --  no tocar
# ================================================================

R_PUNTA_G = D_GRANDE  / 2.0
R_VALLE_G = R_PUNTA_G - PROF_DIENTE
R_PUNTA_P = D_PEQUENA / 2.0
R_VALLE_P = R_PUNTA_P - PROF_DIENTE
H_TOTAL   = H_GRANDE + H_PEQUENA
EPS       = 0.1


# ================================================================
# UTILIDADES
# ================================================================

def polar(ang, rad, z):
    """Punto en coordenadas polares sobre el plano z."""
    return (rad * math.cos(ang), rad * math.sin(ang), z)


def perfil_dentado(r_valle, r_punta, n, z):
    """
    Devuelve la lista de puntos de un perfil dentado cerrado.

    Cada diente se recorre en cuatro tramos, expresados como
    fraccion del paso angular:

        [0 .. f_valle]              valle circular (subdividido)
        [f_valle .. +FRAC_SUBIDA]   flanco de subida
        [.. +FRAC_PUNTA]            plano de punta
        [.. 1.0]                    flanco de bajada
    """
    pts = []
    paso = 2.0 * math.pi / n
    f_valle = 1.0 - 2.0 * FRAC_SUBIDA - FRAC_PUNTA

    if f_valle <= 0:
        raise ValueError("FRAC_SUBIDA y FRAC_PUNTA suman mas de 1")

    f_sub  = f_valle + FRAC_SUBIDA
    f_pun  = f_sub   + FRAC_PUNTA

    for i in range(n):
        a0 = i * paso

        # valle, subdividido para que se mantenga circular
        for k in range(SEG_VALLE):
            f = f_valle * k / float(SEG_VALLE)
            pts.append(polar(a0 + f * paso, r_valle, z))

        pts.append(polar(a0 + f_valle * paso, r_valle, z))
        pts.append(polar(a0 + f_sub   * paso, r_punta, z))
        pts.append(polar(a0 + f_pun   * paso, r_punta, z))

    pts.append(pts[0])          # cierre
    return pts


def solido_extruido(pts, altura):
    """Cierra el perfil, lo capea y lo extruye en +Z."""
    crv = rs.AddPolyline(pts)
    srf = rs.AddPlanarSrf([crv])[0]

    z0   = pts[0][2]
    path = rs.AddLine((0, 0, z0), (0, 0, z0 + altura))
    sol  = rs.ExtrudeSurface(srf, path, True)

    rs.DeleteObjects([crv, srf, path])
    return sol


def cilindro(z_base, altura, diametro):
    return rs.AddCylinder((0, 0, z_base), altura, diametro / 2.0, True)


def alojamiento_inserto():
    """
    Taladro escalonado para el inserto termofusible, abierto a la
    cara TRASERA (z = 0). Tres tramos:

        z = 0            .. INS_H_BOCA     avellanado de entrada
        z = INS_H_BOCA   .. INS_LARGO      cuerpo (aqui muerde)
        z = INS_LARGO    .. + INS_H_ALIVIO alivio de rebose

    El inserto queda enrasado con la cara trasera. Se coloca en
    z = 0 y no mas arriba porque el esparrago M4 del eje es corto:
    si el inserto estuviera hundido, la rosca no llegaria a morder.
    """
    cortes = []

    # avellanado de entrada
    cortes.append(cilindro(-EPS, INS_H_BOCA + EPS, INS_D_BOCA))

    # cuerpo del alojamiento
    cortes.append(cilindro(INS_H_BOCA,
                           INS_LARGO - INS_H_BOCA,
                           INS_D_ALOJ))

    # alivio para el plastico desplazado
    cortes.append(cilindro(INS_LARGO, INS_H_ALIVIO, INS_D_ALIVIO))

    return cortes


def ventanas_radiales():
    """Huecos de aligeramiento entre R_CUBO y R_INT_CORONA."""
    cortes = []
    r_medio = (R_CUBO + R_INT_CORONA) / 2.0

    paso_ang   = 2.0 * math.pi / N_RADIOS
    ang_radio  = ANCHO_RADIO / r_medio      # lo que ocupa el brazo
    ang_hueco  = paso_ang - ang_radio

    if ang_hueco <= 0:
        raise ValueError("ANCHO_RADIO demasiado grande")

    for i in range(N_RADIOS):
        a_ini = i * paso_ang + ang_radio / 2.0
        a_fin = a_ini + ang_hueco

        pts = []
        n_sub = 10
        # arco exterior
        for k in range(n_sub + 1):
            a = a_ini + (a_fin - a_ini) * k / float(n_sub)
            pts.append(polar(a, R_INT_CORONA, -EPS))
        # arco interior, de vuelta
        for k in range(n_sub + 1):
            a = a_fin - (a_fin - a_ini) * k / float(n_sub)
            pts.append(polar(a, R_CUBO, -EPS))
        pts.append(pts[0])

        cortes.append(solido_extruido(pts, H_GRANDE + 2 * EPS))

    return cortes


# ================================================================
# CONSTRUCCION
# ================================================================

def construir():
    rs.EnableRedraw(False)

    # --- cuerpos principales ------------------------------------
    grande  = solido_extruido(
        perfil_dentado(R_VALLE_G, R_PUNTA_G, N_DIENTES_G, 0.0),
        H_GRANDE)

    pequena = solido_extruido(
        perfil_dentado(R_VALLE_P, R_PUNTA_P, N_DIENTES_P, H_GRANDE),
        H_PEQUENA)

    cuerpo = rs.BooleanUnion([grande, pequena], True)
    if not cuerpo:
        print("ERROR: fallo la union de las coronas")
        rs.EnableRedraw(True)
        return None
    cuerpo = cuerpo[0]

    # --- utiles de corte ----------------------------------------
    cortes = []

    # taladro pasante para el esparrago
    cortes.append(cilindro(-EPS, H_TOTAL + 2 * EPS, D_EJE_PASO))

    # alojamiento del inserto de laton, abierto a la cara trasera
    cortes.extend(alojamiento_inserto())

    # ventanas de aligeramiento
    cortes.extend(ventanas_radiales())

    # rebaje frontal
    cortes.append(cilindro(H_TOTAL - PROF_REBAJE,
                           PROF_REBAJE + EPS, D_REBAJE))

    # --- diferencia booleana ------------------------------------
    resultado = rs.BooleanDifference([cuerpo], cortes, True)

    rs.EnableRedraw(True)

    if not resultado:
        print("ERROR: fallo la diferencia booleana")
        return None

    pieza = resultado[0]
    rs.ObjectName(pieza, "rueda_enfoque_bresser_130_650")
    rs.ZoomExtents()
    return pieza


def informe():
    print("=" * 58)
    print(" RUEDA DE ENFOQUE DOBLE  ---  Bresser 130/650")
    print("=" * 58)
    print(" Corona grande ....... %.1f mm  x  %.1f mm  (%d dientes)"
          % (D_GRANDE, H_GRANDE, N_DIENTES_G))
    print(" Corona pequena ...... %.1f mm  x  %.1f mm  (%d dientes)"
          % (D_PEQUENA, H_PEQUENA, N_DIENTES_P))
    print(" Altura total ........ %.1f mm" % H_TOTAL)
    print("-" * 58)
    print(" Ganancia de par respecto a la original (34,3 mm):")
    print("   corona grande ..... x%.2f" % (D_GRANDE  / 34.3))
    print("   corona pequena .... x%.2f" % (D_PEQUENA / 34.3))
    print("-" * 58)
    print(" IMPRESION")
    print("   Corona GRANDE contra la cama")
    print("   PLA o PETG, 5 perimetros, 30 % relleno")
    print("   Capa 0,2 mm, sin soportes")
    print("-" * 58)
    print(" INSERTO DE LATON  (taladro %.2f mm)" % INS_D_ALOJ)
    print("   1. Soldador a 200-220 C con punta conica")
    print("   2. Apoyar el inserto en la boca del taladro")
    print("   3. Bajar MUY despacio y perfectamente recto")
    print("   4. Retirar el soldador antes de llegar al fondo")
    print("   5. Enrasar en frio apretando con algo plano")
    print("   Enfriar del todo antes de roscar nada")
    print("=" * 58)


if __name__ == "__main__":
    if construir():
        informe()
