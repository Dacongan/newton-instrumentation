# -*- coding: utf-8 -*-
"""
================================================================
TAPA SOLAR CON CIERRE DE BAYONETA
Bresser Reflektor 130/650  ---  Art. No. 46-14600
================================================================

UNA sola tapa que hace dos funciones:

  Tapon puesto   ->  tapa normal del telescopio
  Tapon quitado  ->  filtro solar de 38 mm

Genera TRES piezas:

  1. TAPA    cuerpo con faldon, apertura y asiento de bayoneta
  2. ARO     retencion de la lamina Baader (4 x M3)
  3. TAPON   cierre de bayoneta, 3 pestanas, 60 grados de giro

----------------------------------------------------------------
POR QUE 38 mm ES EL TAMANO OPTIMO
----------------------------------------------------------------
  LIMITE GEOMETRICO
    Secundario 47 mm ..... radio libre desde  23,5 mm
    Primario  130 mm ..... radio util hasta   65,0 mm
    Corona disponible ....               41,5 mm de ancho
    Un agujero fuera de eje debe caber entero ahi.
    38 mm deja 5,5 mm de margen para las patas de la arana.

  LIMITE ATMOSFERICO
    38 mm  ->  limite de Dawes 3,0 segundos de arco
    Seeing diurno tipico   3 a 5 segundos de arco
    La atmosfera ya limita antes que la apertura, asi que
    ampliar el agujero no daria mas detalle real.

  38 mm sobre 650 de focal = f/17
  Muestreo excelente para solar con la SVBony SV105.

----------------------------------------------------------------
MONTAJE DE LA LAMINA  --  NO SE PEGA
----------------------------------------------------------------
  La lamina va APRISIONADA entre el fondo de la cajera y el
  aro, apretada por los 4 tornillos M3 del borde exterior.

  Debe quedar LIGERAMENTE FLOJA. Las arrugas suaves son
  normales y no degradan la imagen. Una lamina tensada se
  deforma opticamente y acaba rasgandose con los ciclos
  termicos.

  Nada de adhesivo en la zona optica: arruina el filtro e
  impide cambiar la lamina cuando se desgaste.

----------------------------------------------------------------
SEGURIDAD
----------------------------------------------------------------
  Lamina: Baader AstroSolar Safety Film ND5, comprada en
  proveedor de astronomia. Nunca improvisada.

  Revisar a contraluz ANTES DE CADA USO: si aparece un solo
  punto de luz, arana o despegue, no se usa.

  Tapar o desmontar la mira reflex antes de apuntar al Sol.

  Material: PETG, ASA o ABS. NUNCA PLA: la pieza apunta al
  Sol y el PLA reblandece hacia los 55 C.

----------------------------------------------------------------
DATOS DE PARTIDA (medidos)
----------------------------------------------------------------
  D exterior de la tapa del ventilador .... 167,60 mm
  D interior de la tapa del ventilador .... 163,60 mm
  D interior del tubo ..................... 155,30 mm
  -> pared 2,0 mm, ajuste ya validado en el telescopio

================================================================
"""

import rhinoscriptsyntax as rs
import math


# ================================================================
# PARAMETROS
# ================================================================

# ---- Cuerpo de la tapa -----------------------------------------
D_EXT           = 167.6   # diametro exterior
D_INT           = 163.6   # diametro interior del faldon
H_CARA          =  12.0   # espesor del frontal
H_FALDON        =  12.0   # cuanto se mete en el tubo

# ---- Apertura optica -------------------------------------------
D_APERTURA      =  38.0   # ver justificacion en la cabecera
RC_APERTURA     =  44.0   # radio de posicion del centro
ANG_APERTURA    =  90.0   # grados, ajustar segun la arana

# ---- Cierre de bayoneta ----------------------------------------
D_BAYONETA      =  46.0   # diametro del asiento
D_PESTANA       =  52.0   # diametro sobre las pestanas
H_BAYONETA      =   5.0   # profundidad total del asiento
H_RETEN         =   3.0   # espesor del reten (z = 0 a H_RETEN)
N_PESTANAS      =     3
ANG_PESTANA     =  40.0   # grados de arco de cada pestana
ANG_CANAL       =  46.0   # grados del canal de entrada
JUEGO_BAY       =   0.4   # holgura diametral del tapon

# ---- Alojamiento de la lamina ----------------------------------
D_ARO           =  68.0
H_ARO           =   3.5   # >= HEX_H + 0,9 de fondo
R_TORNILLOS     =  30.0   # fuera del diametro de pestanas
N_TORNILLOS     =     4
D_M3            =   3.3   # paso libre
D_CABEZA        =   6.5   # avellanado para la cabeza
H_CABEZA        =   2.2
HEX_M3          =   5.6   # tuerca M3 = 5,5 entre caras + 0,1
HEX_H           =   2.6   # tuerca M3 = 2,4 de alto + 0,2
                          # el hueco se abre a la cara trasera:
                          # la tuerca se coloca al montar

# ---- Tapon -----------------------------------------------------
D_BRIDA         =  56.0   # apoya sobre la cara exterior
H_BRIDA         =   3.0
TIRADOR_ANCHO   =   8.0
TIRADOR_ALTO    =   3.5

# ---- Colocacion en la cama -------------------------------------
SEP_X           = 200.0

EPS             =   0.2


# ================================================================
# DERIVADAS
# ================================================================

H_TOTAL = H_CARA + H_FALDON

_A  = math.radians(ANG_APERTURA)
CX  = RC_APERTURA * math.cos(_A)
CY  = RC_APERTURA * math.sin(_A)

Z_APER_INI = H_BAYONETA           # donde arranca la apertura
Z_REBAJE   = H_CARA - H_ARO       # fondo de la cajera


# ================================================================
# UTILIDADES
# ================================================================

def cil(x, y, z, altura, diametro):
    return rs.AddCylinder((x, y, z), altura, diametro / 2.0, True)


def sector(x, y, z, altura, r_int, r_ext, ang_ini, ang_fin):
    """Sector anular extruido. Angulos en grados."""
    a0 = math.radians(ang_ini)
    a1 = math.radians(ang_fin)
    n  = 12

    pts = []
    for k in range(n + 1):
        a = a0 + (a1 - a0) * k / float(n)
        pts.append((x + r_ext * math.cos(a),
                    y + r_ext * math.sin(a), z))
    for k in range(n + 1):
        a = a1 - (a1 - a0) * k / float(n)
        pts.append((x + r_int * math.cos(a),
                    y + r_int * math.sin(a), z))
    pts.append(pts[0])

    crv  = rs.AddPolyline(pts)
    srf  = rs.AddPlanarSrf([crv])[0]
    path = rs.AddLine((0, 0, z), (0, 0, z + altura))
    sol  = rs.ExtrudeSurface(srf, path, True)
    rs.DeleteObjects([crv, srf, path])
    return sol


def hexagono(x, y, z, altura, entrecaras):
    r = (entrecaras / 2.0) / math.cos(math.pi / 6.0)
    pts = [(x + r * math.cos(math.pi / 6.0 + i * math.pi / 3.0),
            y + r * math.sin(math.pi / 6.0 + i * math.pi / 3.0),
            z) for i in range(6)]
    pts.append(pts[0])

    crv  = rs.AddPolyline(pts)
    srf  = rs.AddPlanarSrf([crv])[0]
    path = rs.AddLine((0, 0, z), (0, 0, z + altura))
    sol  = rs.ExtrudeSurface(srf, path, True)
    rs.DeleteObjects([crv, srf, path])
    return sol


def caja(x, y, z, ancho, largo, alto):
    return rs.AddBox([
        (x - ancho / 2.0, y - largo / 2.0, z),
        (x + ancho / 2.0, y - largo / 2.0, z),
        (x + ancho / 2.0, y + largo / 2.0, z),
        (x - ancho / 2.0, y + largo / 2.0, z),
        (x - ancho / 2.0, y - largo / 2.0, z + alto),
        (x + ancho / 2.0, y - largo / 2.0, z + alto),
        (x + ancho / 2.0, y + largo / 2.0, z + alto),
        (x - ancho / 2.0, y + largo / 2.0, z + alto)])


def tornillos(cx, cy):
    return [(cx + R_TORNILLOS * math.cos(2 * math.pi * i / N_TORNILLOS),
             cy + R_TORNILLOS * math.sin(2 * math.pi * i / N_TORNILLOS))
            for i in range(N_TORNILLOS)]


def restar(base, cortes, nombre):
    res = rs.BooleanDifference([base], cortes, True)
    if not res:
        print("ERROR en la diferencia de: %s" % nombre)
        return None
    rs.ObjectName(res[0], nombre)
    return res[0]


# ================================================================
# PIEZA 1  --  TAPA
# ================================================================

def construir_tapa():
    """
    Estratigrafia desde la cara EXTERIOR (z = 0):

      0 .. H_RETEN          reten de la bayoneta (anillo)
      H_RETEN .. H_BAYONETA garganta donde giran las pestanas
      H_BAYONETA .. Z_REBAJE  material, apertura pasante
      Z_REBAJE .. H_CARA    cajera de la lamina y el aro
      H_CARA .. H_TOTAL     faldon anular
    """
    cara   = cil(0, 0, 0, H_CARA, D_EXT)
    faldon = cil(0, 0, H_CARA, H_FALDON, D_EXT)
    hueco  = cil(0, 0, H_CARA - EPS, H_FALDON + 2 * EPS, D_INT)

    faldon = rs.BooleanDifference([faldon], [hueco], True)[0]
    cuerpo = rs.BooleanUnion([cara, faldon], True)[0]

    cortes = []

    # --- asiento de la bayoneta ---------------------------------
    cortes.append(cil(CX, CY, -EPS, H_BAYONETA + EPS, D_BAYONETA))

    # canales de entrada, a todo lo alto del asiento
    for i in range(N_PESTANAS):
        a = 360.0 * i / N_PESTANAS
        cortes.append(sector(CX, CY, -EPS, H_BAYONETA + EPS,
                             D_BAYONETA / 2.0 - EPS,
                             D_PESTANA / 2.0,
                             a - ANG_CANAL / 2.0,
                             a + ANG_CANAL / 2.0))

    # garganta anular donde giran las pestanas
    cortes.append(cil(CX, CY, H_RETEN,
                      H_BAYONETA - H_RETEN + EPS, D_PESTANA))

    # --- apertura optica ----------------------------------------
    cortes.append(cil(CX, CY, Z_APER_INI - EPS,
                      H_CARA - Z_APER_INI + 2 * EPS, D_APERTURA))

    # --- cajera de la lamina, en la cara interior ---------------
    cortes.append(cil(CX, CY, Z_REBAJE, H_ARO + EPS, D_ARO + 0.2))

    # --- tornillos M3 con avellanado exterior -------------------
    for (tx, ty) in tornillos(CX, CY):
        cortes.append(cil(tx, ty, -EPS, H_CARA + 2 * EPS, D_M3))
        cortes.append(cil(tx, ty, -EPS, H_CABEZA + EPS, D_CABEZA))

    return restar(cuerpo, cortes, "tapa_solar_bresser")


# ================================================================
# PIEZA 2  --  ARO DE RETENCION
# ================================================================

def construir_aro():
    x0 = SEP_X

    aro    = cil(x0, 0, 0, H_ARO, D_ARO)
    cortes = [cil(x0, 0, -EPS, H_ARO + 2 * EPS, D_APERTURA)]

    for (tx, ty) in tornillos(x0, 0):
        cortes.append(cil(tx, ty, -EPS, H_ARO + 2 * EPS, D_M3))
        cortes.append(hexagono(tx, ty, H_ARO - HEX_H,
                               HEX_H + EPS, HEX_M3))

    return restar(aro, cortes, "aro_retencion_lamina")


# ================================================================
# PIEZA 3  --  TAPON DE BAYONETA
# ================================================================

def construir_tapon():
    """
    Se imprime con las pestanas hacia arriba, de modo que la
    cara vista quede contra la cama.

      0 .. H_BRIDA                      brida y tirador
      H_BRIDA .. +H_RETEN               cuello
      .. + (H_BAYONETA - H_RETEN)       pestanas
    """
    x0 = SEP_X * 1.7

    d_cuerpo  = D_BAYONETA - JUEGO_BAY
    d_pestana = D_PESTANA  - JUEGO_BAY

    z_cuello  = H_BRIDA
    h_cuello  = H_RETEN
    z_pest    = z_cuello + h_cuello
    h_pest    = H_BAYONETA - H_RETEN - 0.3   # 0,3 de juego axial

    piezas = []
    piezas.append(cil(x0, 0, 0, H_BRIDA, D_BRIDA))
    piezas.append(cil(x0, 0, z_cuello, h_cuello + h_pest, d_cuerpo))

    for i in range(N_PESTANAS):
        a = 360.0 * i / N_PESTANAS
        piezas.append(sector(x0, 0, z_pest, h_pest,
                             d_cuerpo / 2.0 - EPS,
                             d_pestana / 2.0,
                             a - ANG_PESTANA / 2.0,
                             a + ANG_PESTANA / 2.0))

    piezas.append(caja(x0, 0, -TIRADOR_ALTO,
                       TIRADOR_ANCHO, D_BRIDA * 0.75, TIRADOR_ALTO))

    res = rs.BooleanUnion(piezas, True)
    if not res:
        print("ERROR al unir el tapon")
        return None

    rs.ObjectName(res[0], "tapon_bayoneta")
    return res[0]


# ================================================================
# INFORME
# ================================================================

def informe():
    r_int = RC_APERTURA - D_APERTURA / 2.0
    r_ext = RC_APERTURA + D_APERTURA / 2.0
    giro  = 360.0 / N_PESTANAS / 2.0

    print("=" * 60)
    print(" TAPA SOLAR CON BAYONETA  ---  Bresser 130/650")
    print("=" * 60)
    print(" Tapa ........... %.1f mm ext,  %.1f mm de alto"
          % (D_EXT, H_TOTAL))
    print(" Apertura ....... %.1f mm  ->  f/%.1f"
          % (D_APERTURA, 650.0 / D_APERTURA))
    print(" Bayoneta ....... %d pestanas, girar %.0f grados"
          % (N_PESTANAS, giro))
    print("-" * 60)
    print(" COMPROBACION GEOMETRICA")
    print("   borde interior a %.1f mm del eje  (> 23,5 OK)"
          % r_int)
    print("   borde exterior a %.1f mm del eje  (< 65,0 OK)"
          % r_ext)
    if r_int <= 23.5 or r_ext >= 65.0:
        print("   *** FUERA DE MARGEN: revisar D_APERTURA ***")
    print("-" * 60)
    print(" TORNILLERIA")
    print("   %d x tornillo M3 Allen cabeza cilindrica"
          % N_TORNILLOS)
    print("   %d x tuerca M3 normal (5,5 entre caras)"
          % N_TORNILLOS)
    print("   Agarre necesario: %.1f mm  ->  usar M3 x %d"
          % (H_CARA - H_CABEZA + (H_ARO - HEX_H) + 2.4,
             int(math.ceil((H_CARA - H_CABEZA
                            + (H_ARO - HEX_H) + 2.4) / 2.0) * 2)))
    print("   Fondo bajo la tuerca en el aro: %.1f mm"
          % (H_ARO - HEX_H))
    if H_ARO - HEX_H < 0.6:
        print("   *** ARO DEMASIADO FINO: subir H_ARO ***")
    print("-" * 60)
    print(" MATERIAL:  PETG, ASA o ABS.  NUNCA PLA.")
    print("-" * 60)
    print(" IMPRESION")
    print("   Tapa:  cara exterior contra la cama")
    print("   Aro:   cara de las tuercas hacia arriba")
    print("   Tapon: brida contra la cama, pestanas arriba")
    print("   4 perimetros, 25 % relleno, capa 0,2 mm")
    print("   Brim de 5 mm en la tapa")
    print("-" * 60)
    print(" MONTAJE DE LA LAMINA  --  NO SE PEGA")
    print("   1. Cortar la lamina unos 5 mm mayor que el aro")
    print("   2. Apoyarla en la cajera SIN TENSAR")
    print("   3. Aro encima, tuercas M3 en sus hexagonos")
    print("   4. Tornillos desde fuera, apretar en cruz")
    print("   5. Sin forzar: las arrugas suaves son correctas")
    print("-" * 60)
    print(" ANTES DE CADA USO")
    print("   Mirar la lamina a contraluz.")
    print("   Un solo punto de luz o despegue: NO USAR.")
    print("   Tapar o quitar la mira reflex.")
    print("=" * 60)


# ================================================================
if __name__ == "__main__":
    rs.EnableRedraw(False)

    piezas = [construir_tapa(),
              construir_aro(),
              construir_tapon()]

    rs.EnableRedraw(True)
    rs.ZoomExtents()

    if all(piezas):
        informe()
    else:
        print("Alguna pieza no se genero correctamente")
