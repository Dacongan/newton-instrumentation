# -*- coding: utf-8 -*-
"""
================================================================
MASCARA DE BAHTINOV
Bresser Reflektor 130/650  ---  Art. No. 46-14600
================================================================

Ayuda de enfoque por difraccion. Puesta sobre la boca del tubo
y apuntando a una estrella brillante, forma una X fija y una
barra central movil. El foco es exacto cuando la barra queda
perfectamente centrada en la X.

----------------------------------------------------------------
POR QUE LA ZONA DE RANURAS ES DE 130 mm Y NO DE 155
----------------------------------------------------------------
  La luz de una estrella llega COLIMADA: rayos paralelos.
  No converge hasta despues de rebotar en el primario.

  Un rayo que entra a 70 mm del eje sigue a 70 mm cuando llega
  al fondo del tubo, y el espejo acaba en 65. Se pierde.

  Por eso la zona util es exactamente la proyeccion del
  primario, 130 mm, y el borde ancho es inevitable: es la
  parte del tubo que no ve el espejo.

----------------------------------------------------------------
ESPESOR DE LA PLACA: 2 mm, NO 3
----------------------------------------------------------------
  Un disco de 167,6 mm tiene 22.000 mm3 por cada milimetro de
  espesor, y las ranuras solo vacian la corona de 56 a 130.
  Todo el borde exterior y el cubo central son macizos.

  Con la placa a 3 mm salian 76 g y casi 8 horas de impresion.
  A 2 mm baja a unos 52 g y algo mas de 4 horas.

  La rigidez de un disco de este diametro se la da el FALDON
  perimetral, que trabaja como un aro, no el espesor de la
  placa. Con 2 mm son 7 capas a 0,28: de sobra.

----------------------------------------------------------------
PERIODO DE LA REJILLA
----------------------------------------------------------------
  Criterio estandar:  ranura = focal / factor
  El factor 150 es el punto medio recomendado.

    650 / 150 = 4,33 mm de ranura
    periodo   = 8,66 mm
    unas 15 ranuras a lo ancho de la apertura

  Sirve igual para ocular y para camara: con la SV105 a foco
  primario el campo es de 30 x 17 minutos de arco y las
  espigas caben de sobra.

  Espigas debiles  -> FACTOR = 125
  Espigas difusas  -> FACTOR = 175

----------------------------------------------------------------
CUBO Y RADIOS MACIZOS
----------------------------------------------------------------
  El margen entre sectores es ANGULAR, asi que el radio macizo
  se estrecha al acercarse al centro. Con el cubo en 50 mm y
  2,5 grados de margen quedaban puntas de barra de 1 mm.

  Corregido: cubo a 56 mm y margen a 3 grados. El radio macizo
  mide 2,93 mm junto al cubo y 6,81 mm en el borde.

  Los 56 mm siguen dentro de la sombra del secundario (47 mm)
  mas las patas de la arana, asi que no se pierde luz util.

  Ademas se descarta cualquier fragmento de ranura por debajo
  de VOL_MIN: son los slivers de las fronteras entre sectores.

----------------------------------------------------------------
AJUSTE: HOLGADO PERO SIN CAERSE
----------------------------------------------------------------
  El faldon va HOLGADO (164,4) porque esto se quita y se pone
  constantemente, no como la tapa del ventilador.

  La sujecion la dan TRES LENGUETAS FLEXIBLES con resalte
  interior y rampa de entrada en tres escalones. Al flexar, se
  tragan un error de tolerancia de varias decimas.

----------------------------------------------------------------
USO
----------------------------------------------------------------
  Rotar la mascara 180 grados invierte la direccion en que se
  mueve la barra central, asi que conviene ponerla SIEMPRE en
  la misma orientacion. Marcar un punto en el borde y
  alinearlo con el enfocador.

  Si al girarla 90 o 180 grados el foco cambia, sospechar de
  la colimacion antes que de la mascara.

  Material: PLA. Solo se usa de noche, sin sol ni calor.
  Negro mate a ser posible: menos reflejos.

================================================================
"""

import rhinoscriptsyntax as rs
import math


# ================================================================
# PARAMETROS
# ================================================================

# ---- Cuerpo ----------------------------------------------------
D_EXT           = 167.6   # diametro exterior
D_FALDON        = 164.4   # interior del faldon, HOLGADO
H_PLACA         =   2.0   # espesor de la placa  <-- era 3,0
H_FALDON        =  10.0   # altura del faldon    <-- era 14,0

# ---- Lenguetas de sujecion -------------------------------------
N_LENG          =     3
ANG_LENG        =  26.0   # grados de arco de cada lengueta
RANURA_LENG     =   2.5   # mm de ranura a cada lado
RAIZ_LENG       =   2.5   # mm de raiz sin cortar
D_TOPE          = 163.0   # interior en el resalte -> friccion
H_TOPE          =   3.0   # altura del resalte

# ---- Zona optica -----------------------------------------------
D_CLARO         = 130.0   # proyeccion exacta del primario
D_CUBO          =  56.0   # centro macizo (secundario 47 + arana)

# ---- Rejilla de Bahtinov ---------------------------------------
FOCAL           = 650.0
FACTOR          = 150.0   # focal / factor = ancho de ranura
ANG_BAHTINOV    =  20.0   # angulo estandar
ANG_BASE        =  90.0   # direccion de barras del semicirculo
MARGEN_SECTOR   =   3.0   # grados macizos a cada lado
VOL_MIN         =  50.0   # mm3, descarta fragmentos parasitos

# Sin tirador a proposito: la pieza se agarra por el canto y el
# faldon. Cualquier saliente inferior obligaria a usar soportes.

EPS             =   0.2


# ================================================================
# DERIVADAS
# ================================================================

ANCHO_RANURA = FOCAL / FACTOR
PERIODO      = ANCHO_RANURA * 2.0

H_TOTAL    = H_PLACA + H_FALDON
R_CLARO    = D_CLARO / 2.0
R_CUBO     = D_CUBO / 2.0
LARGO_TIRA = D_CLARO * 1.6

SECTORES = [
    (  0.0, 180.0, ANG_BASE),
    (180.0, 270.0, ANG_BASE + ANG_BAHTINOV),
    (270.0, 360.0, ANG_BASE - ANG_BAHTINOV),
]


# ================================================================
# UTILIDADES
# ================================================================

def cil(x, y, z, altura, diametro):
    return rs.AddCylinder((x, y, z), altura, diametro / 2.0, True)


def _extruir(pts, z, altura):
    crv  = rs.AddPolyline(pts)
    srf  = rs.AddPlanarSrf([crv])[0]
    path = rs.AddLine((0, 0, z), (0, 0, z + altura))
    sol  = rs.ExtrudeSurface(srf, path, True)
    rs.DeleteObjects([crv, srf, path])
    return sol


def sector_anular(z, altura, r_int, r_ext, ang_ini, ang_fin):
    """Sector de corona circular. Angulos en grados."""
    a0 = math.radians(ang_ini)
    a1 = math.radians(ang_fin)
    n  = max(8, int(abs(ang_fin - ang_ini) / 3.0))

    pts = []
    for k in range(n + 1):
        a = a0 + (a1 - a0) * k / float(n)
        pts.append((r_ext * math.cos(a), r_ext * math.sin(a), z))
    for k in range(n + 1):
        a = a1 - (a1 - a0) * k / float(n)
        pts.append((r_int * math.cos(a), r_int * math.sin(a), z))
    pts.append(pts[0])

    return _extruir(pts, z, altura)


def tira(ang, desplazamiento, ancho, largo, z, altura):
    """Banda recta segun 'ang', desplazada en la normal."""
    a = math.radians(ang)
    ux, uy = math.cos(a), math.sin(a)
    vx, vy = -math.sin(a), math.cos(a)

    px = desplazamiento * vx
    py = desplazamiento * vy

    pts = []
    for (s, t) in [(-largo / 2.0, -ancho / 2.0),
                   ( largo / 2.0, -ancho / 2.0),
                   ( largo / 2.0,  ancho / 2.0),
                   (-largo / 2.0,  ancho / 2.0)]:
        pts.append((px + s * ux + t * vx,
                    py + s * uy + t * vy, z))
    pts.append(pts[0])

    return _extruir(pts, z, altura)


def volumen(obj):
    try:
        v = rs.SurfaceVolume(obj)
        return abs(v[0]) if v else 0.0
    except Exception:
        return 0.0


# ================================================================
# RANURAS
# ================================================================

def ranuras_de_sector(ang_ini, ang_fin, ang_barras):
    """
    Bandas rectas recortadas contra la corona angular del
    sector. Se descartan los fragmentos por debajo de VOL_MIN:
    son los slivers puntiagudos de las fronteras entre
    sectores, que no se pueden imprimir.
    """
    cortes      = []
    descartados = 0

    cuna = sector_anular(-EPS, H_PLACA + 2 * EPS,
                         R_CUBO, R_CLARO,
                         ang_ini + MARGEN_SECTOR,
                         ang_fin - MARGEN_SECTOR)

    n = int(math.ceil(R_CLARO / PERIODO)) + 1

    for i in range(-n, n + 1):
        banda = tira(ang_barras, i * PERIODO, ANCHO_RANURA,
                     LARGO_TIRA, -EPS, H_PLACA + 2 * EPS)

        copia = rs.CopyObject(cuna)
        trozo = rs.BooleanIntersection([banda], [copia], True)

        if not trozo:
            continue

        for t in trozo:
            if volumen(t) >= VOL_MIN:
                cortes.append(t)
            else:
                rs.DeleteObject(t)
                descartados += 1

    rs.DeleteObject(cuna)
    return cortes, descartados


# ================================================================
# LENGUETAS DE SUJECION
# ================================================================

def cortes_lenguetas():
    """Dos ranuras verticales a cada lado de cada lengueta."""
    cortes  = []
    r_med   = D_FALDON / 2.0
    ang_ran = math.degrees(RANURA_LENG / r_med)

    z0 = H_PLACA + RAIZ_LENG
    h  = H_TOTAL - z0 + EPS

    for i in range(N_LENG):
        a = 360.0 * i / N_LENG
        for signo in (-1.0, 1.0):
            c = a + signo * (ANG_LENG / 2.0 + ang_ran / 2.0)
            cortes.append(
                sector_anular(z0, h,
                              D_FALDON / 2.0 - 1.0,
                              D_EXT / 2.0 + 1.0,
                              c - ang_ran / 2.0,
                              c + ang_ran / 2.0))

    return cortes


def resaltes_lenguetas():
    """
    Resalte interior con rampa de entrada en tres escalones,
    para que el tubo entre suave desde el borde libre.
    """
    piezas = []
    aw = ANG_LENG * 0.8

    escalones = [
        (H_TOTAL - 1.0, 1.0, D_TOPE + 0.8),
        (H_TOTAL - 2.0, 1.0, D_TOPE + 0.4),
        (H_TOTAL - 2.0 - H_TOPE, H_TOPE, D_TOPE),
    ]

    for i in range(N_LENG):
        a = 360.0 * i / N_LENG
        for (z, h, d_int) in escalones:
            piezas.append(
                sector_anular(z, h,
                              d_int / 2.0,
                              D_FALDON / 2.0 + EPS,
                              a - aw / 2.0,
                              a + aw / 2.0))

    return piezas


# ================================================================
# CONSTRUCCION
# ================================================================

def construir():
    rs.EnableRedraw(False)

    placa  = cil(0, 0, 0, H_PLACA, D_EXT)
    faldon = cil(0, 0, H_PLACA, H_FALDON, D_EXT)
    hueco  = cil(0, 0, H_PLACA - EPS, H_FALDON + 2 * EPS,
                 D_FALDON)

    faldon = rs.BooleanDifference([faldon], [hueco], True)
    if not faldon:
        print("ERROR al vaciar el faldon")
        rs.EnableRedraw(True)
        return None, 0

    cuerpo = rs.BooleanUnion([placa, faldon[0]], True)
    if not cuerpo:
        print("ERROR al unir placa y faldon")
        rs.EnableRedraw(True)
        return None, 0
    cuerpo = cuerpo[0]

    # --- resaltes de las lenguetas ------------------------------
    res = rs.BooleanUnion([cuerpo] + resaltes_lenguetas(), True)
    if res:
        cuerpo = res[0]
    else:
        print("AVISO: no se unieron los resaltes")

    # --- cortes -------------------------------------------------
    cortes = cortes_lenguetas()
    total_descartados = 0

    for (a0, a1, ab) in SECTORES:
        c, d = ranuras_de_sector(a0, a1, ab)
        cortes.extend(c)
        total_descartados += d

    if not cortes:
        print("ERROR: no se genero ningun corte")
        rs.EnableRedraw(True)
        return None, 0

    res = rs.BooleanDifference([cuerpo], cortes, True)

    rs.EnableRedraw(True)

    if not res:
        print("ERROR en la diferencia final")
        return None, 0

    rs.ObjectName(res[0], "mascara_bahtinov_bresser_130")
    rs.ZoomExtents()
    return res[0], total_descartados


# ================================================================
# INFORME
# ================================================================

def informe(pieza, descartados):
    macizo_cubo  = 2.0 * math.radians(MARGEN_SECTOR) * R_CUBO
    macizo_borde = 2.0 * math.radians(MARGEN_SECTOR) * R_CLARO

    vol = volumen(pieza)
    masa = vol / 1000.0 * 1.24   # PLA

    print("=" * 60)
    print(" MASCARA DE BAHTINOV  ---  Bresser 130/650")
    print("=" * 60)
    print(" Diametro exterior ..... %.1f mm" % D_EXT)
    print(" Espesor de la placa ... %.1f mm  (%d capas a 0,28)"
          % (H_PLACA, round(H_PLACA / 0.28)))
    print(" Altura del faldon ..... %.1f mm" % H_FALDON)
    print(" Altura total .......... %.1f mm" % H_TOTAL)
    print(" Zona de ranuras ....... %.1f mm  (primario 130)"
          % D_CLARO)
    print(" Centro macizo ......... %.1f mm  (secundario 47)"
          % D_CUBO)
    print("-" * 60)
    print(" VOLUMEN Y MASA")
    print("   Volumen macizo ...... %.0f mm3" % vol)
    print("   Masa en PLA macizo .. %.0f g" % masa)
    print("   Con 15 %% de relleno . unos %.0f g" % (masa * 0.75))
    if masa > 70:
        print("   *** DEMASIADO: bajar H_PLACA o H_FALDON ***")
    print("-" * 60)
    print(" REJILLA   (factor %.0f)" % FACTOR)
    print("   Ranura y barra ...... %.2f mm" % ANCHO_RANURA)
    print("   Periodo ............. %.2f mm" % PERIODO)
    print("   Ranuras a lo ancho .. %d" % int(D_CLARO / PERIODO))
    print("   Angulo Bahtinov ..... %.0f grados" % ANG_BAHTINOV)
    print("   Espigas debiles -> FACTOR = 125")
    print("   Espigas difusas -> FACTOR = 175")
    print("-" * 60)
    print(" RADIOS MACIZOS   (margen %.1f grados)"
          % MARGEN_SECTOR)
    print("   Junto al cubo ....... %.2f mm" % macizo_cubo)
    print("   En el borde ......... %.2f mm" % macizo_borde)
    if macizo_cubo < 2.0:
        print("   *** DEMASIADO FINO: subir MARGEN_SECTOR")
        print("       o subir D_CUBO ***")
    print("   Fragmentos descartados: %d" % descartados)
    print("-" * 60)
    print(" AJUSTE AL TUBO")
    print("   Faldon holgado ...... %.1f mm" % D_FALDON)
    print("   %d lenguetas con resalte a %.1f mm"
          % (N_LENG, D_TOPE))
    print("   Interferencia radial  %.2f mm por lado"
          % ((D_FALDON - D_TOPE) / 2.0))
    print("   Si queda flojo  -> bajar D_TOPE a 162,6")
    print("   Si cuesta meter -> subir D_TOPE a 163,4")
    print("-" * 60)
    print(" IMPRESION   (PLA, boquilla 0,4)")
    print("   Placa contra la cama, faldon hacia arriba")
    print("   Altura de capa ...... 0,28  (primera 0,2)")
    print("   Perimetros .......... 3")
    print("   Relleno ............. 15 %, rejilla o lineas")
    print("   Soportes ............ NO")
    print("   Brim ................ 5 mm, Outside Only")
    print("   La barra de %.2f mm son %.0f lineas de 0,4:"
          % (ANCHO_RANURA, ANCHO_RANURA / 0.4))
    print("   no subir de 3 perimetros o quedaria hueca")
    print("-" * 60)
    print(" USO")
    print("   1. Poner la mascara en la boca del tubo")
    print("   2. Apuntar a una estrella brillante")
    print("   3. Aparecen una X y una barra central")
    print("   4. Enfocar hasta centrar la barra en la X")
    print("   5. QUITAR LA MASCARA antes de observar")
    print("   Ponerla siempre en la misma orientacion:")
    print("   girarla 180 grados invierte el sentido de giro")
    print("=" * 60)


# ================================================================
if __name__ == "__main__":
    pieza, descartados = construir()
    if pieza:
        informe(pieza, descartados)
