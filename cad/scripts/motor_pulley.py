# -*- coding: utf-8 -*-
"""
================================================================
POLEA DEL MOTOR — enfocador motorizado
Bresser 130/650 · motor 28BYJ-48
================================================================

Polea pequena calada en el eje del 28BYJ-48. Arrastra, mediante
junta torica, la polea metalica de 34 mm que ya viene montada en
el eje del pinon del enfocador.

----------------------------------------------------------------
COMO SE CONSTRUYE  (v3)
----------------------------------------------------------------
  v1: garganta de paredes rectas  -> contacto en LINEA, mal
  v2: revolucion de un perfil     -> no cerraba como solido
  v3: cilindro macizo MENOS UN TORO  <-- esta

  Un toro es, por definicion, un anillo de seccion circular.
  Restarlo de un cilindro genera exactamente el canal
  semicircular que necesita la torica, sin depender de que
  una revolucion de perfil cierre bien.

    Toro: radio mayor = R_fondo + R_garganta = 10,30
          radio menor = R_garganta           =  2,30
          centrado en z = H_TOTAL / 2

    El punto del toro mas cercano al eje queda a 8,00 mm,
    que es justo el radio de fondo de garganta buscado.

----------------------------------------------------------------
POR QUE LA GARGANTA ES SEMICIRCULAR
----------------------------------------------------------------
  Una torica es un cilindro de goma de seccion circular.

    Fondo plano  -> apoya en una tangente: contacto en LINEA.
                    La presion se concentra, la goma se
                    deforma y se desgasta antes.

    Fondo R2,3   -> la goma asienta en el canal: contacto en
                    ARCO. Mas superficie de friccion y mas par
                    transmisible sin patinar.

  Por eso las poleas comerciales para correa redonda llevan
  garganta semicircular.

  RADIO: 2,30 mm para torica CS4 (radio de goma 2,00).
    Igual que la goma  -> la aprisiona y se calienta
    Mucho mayor        -> se vuelve al contacto en linea
    Un 15 % mayor      -> correcto

----------------------------------------------------------------
EL EJE DEL 28BYJ-48
----------------------------------------------------------------
  Eje de 5,00 mm con DOS CARAS PLANAS enfrentadas, separadas
  3,00 mm entre si (perfil de "doble D").

  Ese perfil es lo que arrastra: NO hace falta prisionero, ni
  chaveta, ni pegamento. La polea se cala a presion y el plano
  transmite el par.

  *** VERIFICAR AL RECIBIR EL MOTOR ***
  La separacion entre planos varia algo entre fabricantes.
  Medir con calibre apoyando las bocas sobre las dos caras
  planas y ajustar PLANO_EJE si no da 3,00.

----------------------------------------------------------------
TRANSMISION
----------------------------------------------------------------
  Polea grande (efectiva, fondo garganta) .... 33,3 mm
  Polea motor  (efectiva, fondo garganta) .... 16,0 mm
  Reduccion .................................. 2,08 : 1

  Pasos del 28BYJ-48 en media marcha ......... 4.096
  Pasos por vuelta del eje del pinon ......... 8.525
  Avance por vuelta (pinon 8,50) ............. 26,7 mm
  RESOLUCION ................................. 3,13 um/paso

  CFZ a f/5  = 27,5 um  ->   9 pasos
  CFZ a f/15 = 247 um   ->  79 pasos

  NO subir la reduccion: la precision ya sobra doce veces y lo
  que escasea es velocidad (50 mm de recorrido = 32 s).

----------------------------------------------------------------
IMPRESION
----------------------------------------------------------------
  DE PIE, con el eje VERTICAL. Tumbada, la garganta sale
  ovalada y la torica salta.

  PLA vale: no ve el sol, trabaja de noche y el esfuerzo es
  bajo. Reservar el PETG para la tapa solar.

  5 perimetros · 40 % relleno · capa 0,2 · sin soportes
  Brim de 3-4 mm: la base de contacto es pequena.

================================================================
"""

import rhinoscriptsyntax as rs
import math


# ================================================================
# PARAMETROS
# ================================================================

# ---- Eje del 28BYJ-48 ------------------------------------------
D_EJE           =  5.00   # diametro nominal
PLANO_EJE       =  3.00   # entre las dos caras planas  <-- VERIFICAR
JUEGO_EJE       =  0.15   # holgura diametral
                          #   0,10 si tu impresora es precisa
                          #   0,25 si tiende a cerrar agujeros
PROF_EJE        =  8.00   # profundidad del alojamiento
CHAFLAN_EJE     =  0.60   # entrada guiada, evita astillar el borde

# ---- Garganta semicircular -------------------------------------
D_EFECTIVO      = 16.00   # diametro en el FONDO de la garganta
R_GARGANTA      =  2.30   # radio del toro (torica CS4 -> goma R2,0)

# ---- Cuerpo ----------------------------------------------------
H_TOTAL         = 10.00   # altura total
D_PESTANA       = 20.40   # diametro exterior sobre pestanas

# ---- Alivio ----------------------------------------------------
D_ALIVIO        = 11.00   # rebaje en la cara superior
PROF_ALIVIO     =  2.00

EPS             =  0.2


# ================================================================
# DERIVADAS
# ================================================================

R_FONDO   = D_EFECTIVO / 2.0
R_PESTANA = D_PESTANA / 2.0
Z_CENTRO  = H_TOTAL / 2.0
R_TORO    = R_FONDO + R_GARGANTA     # radio mayor del toro


# ================================================================
# UTILIDADES
# ================================================================

def cil(x, y, z, altura, diametro):
    return rs.AddCylinder((x, y, z), altura, diametro / 2.0, True)


def eje_doble_d(z, altura, diametro, entre_planos):
    """Circulo con dos cuerdas planas enfrentadas."""
    r = diametro / 2.0
    h = entre_planos / 2.0

    if h >= r:
        raise ValueError("entre_planos mayor que el diametro")

    a = math.acos(h / r)
    n = 24
    pts = []

    for k in range(n + 1):
        ang = -a + 2 * a * k / float(n)
        pts.append((r * math.cos(ang), r * math.sin(ang), z))
    pts.append(( h,  r * math.sin(a), z))
    pts.append((-h,  r * math.sin(a), z))
    for k in range(n + 1):
        ang = math.pi - a + 2 * a * k / float(n)
        pts.append((r * math.cos(ang), r * math.sin(ang), z))
    pts.append((-h, -r * math.sin(a), z))
    pts.append(( h, -r * math.sin(a), z))
    pts.append(pts[0])

    crv  = rs.AddPolyline(pts)
    srf  = rs.AddPlanarSrf([crv])[0]
    path = rs.AddLine((0, 0, z), (0, 0, z + altura))
    sol  = rs.ExtrudeSurface(srf, path, True)
    rs.DeleteObjects([crv, srf, path])
    return sol


# ================================================================
# CONSTRUCCION
# ================================================================

def construir():
    rs.EnableRedraw(False)

    # --- 1. cilindro macizo del diametro exterior ---------------
    cuerpo = cil(0, 0, 0, H_TOTAL, D_PESTANA)

    # --- 2. TORO que genera la garganta -------------------------
    #     plano base en el centro de altura de la polea
    plano = rs.PlaneFromNormal((0, 0, Z_CENTRO), (0, 0, 1))
    toro  = rs.AddTorus(plano, R_TORO, R_GARGANTA)

    if not toro:
        print("ERROR: no se genero el toro")
        rs.EnableRedraw(True)
        return None

    res = rs.BooleanDifference([cuerpo], [toro], True)
    if not res:
        print("ERROR al restar el toro")
        rs.EnableRedraw(True)
        return None
    cuerpo = res[0]

    # --- 3. resto de cortes -------------------------------------
    cortes = []

    # alojamiento del eje, abierto a la cara inferior
    cortes.append(eje_doble_d(-EPS, PROF_EJE + EPS,
                              D_EJE + JUEGO_EJE, PLANO_EJE))

    # chaflan de entrada
    d_ch = D_EJE + JUEGO_EJE + 2 * CHAFLAN_EJE
    cortes.append(rs.AddCone((0, 0, CHAFLAN_EJE),
                             -CHAFLAN_EJE - EPS,
                             d_ch / 2.0, True))

    # alivio en la cara superior
    cortes.append(cil(0, 0, H_TOTAL - PROF_ALIVIO,
                      PROF_ALIVIO + EPS, D_ALIVIO))

    res = rs.BooleanDifference([cuerpo], cortes, True)

    rs.EnableRedraw(True)

    if not res:
        print("ERROR en la diferencia final")
        return None

    rs.ObjectName(res[0], "polea_motor_28byj48")
    rs.ZoomExtents()
    return res[0]


# ================================================================
# INFORME
# ================================================================

def informe():
    red = 33.3 / D_EFECTIVO
    res = math.pi * 8.5 / (4096 * red) * 1000
    r_goma = 2.0
    h_pest = (H_TOTAL - 2 * R_GARGANTA) / 2.0

    print("=" * 58)
    print(" POLEA DEL MOTOR  ---  28BYJ-48   (v3, toro)")
    print("=" * 58)
    print(" D exterior (pestanas) ... %.2f mm" % D_PESTANA)
    print(" D efectivo (fondo garg) . %.2f mm" % D_EFECTIVO)
    print(" Altura total ............ %.2f mm" % H_TOTAL)
    print(" Pestana a cada lado ..... %.2f mm" % h_pest)
    if h_pest < 1.2:
        print("   *** PESTANAS MUY FINAS: subir H_TOTAL ***")
    print("-" * 58)
    print(" GARGANTA — restada con un TORO")
    print("   Radio mayor del toro  %.2f mm" % R_TORO)
    print("   Radio menor del toro  %.2f mm" % R_GARGANTA)
    print("   Radio de la goma      %.2f mm  (torica CS4)"
          % r_goma)
    print("   Holgura ............. %+.0f %%"
          % ((R_GARGANTA / r_goma - 1) * 100))
    if R_GARGANTA <= r_goma:
        print("   *** APRISIONA LA GOMA: subir R_GARGANTA ***")
    elif R_GARGANTA > r_goma * 1.4:
        print("   *** DEMASIADO ABIERTA: contacto en linea ***")
    print("   Contacto en ARCO, no en linea")
    print("-" * 58)
    print(" ALOJAMIENTO DEL EJE")
    print("   Perfil doble D .... %.2f mm, planos a %.2f"
          % (D_EJE + JUEGO_EJE, PLANO_EJE))
    print("   Profundidad ....... %.2f mm" % PROF_EJE)
    print("   Chaflan entrada ... %.2f mm" % CHAFLAN_EJE)
    print("   Sin prisionero: el plano transmite el par")
    print("   *** MEDIR EL EJE REAL AL RECIBIR EL MOTOR ***")
    print("-" * 58)
    print(" TRANSMISION")
    print("   Reduccion ......... %.2f : 1" % red)
    print("   Resolucion ........ %.2f um/paso" % res)
    print("   CFZ f/5  (27,5 um)  %.0f pasos" % (27.5 / res))
    print("   CFZ f/15 (247 um)   %.0f pasos" % (247.0 / res))
    print("-" * 58)
    print(" IMPRESION")
    print("   DE PIE, eje vertical  <-- IMPORTANTE")
    print("   PLA · 5 perimetros · 40 % · capa 0,2")
    print("   Sin soportes · brim 3-4 mm")
    print("-" * 58)
    print(" COMPROBAR ANTES DE EXPORTAR")
    print("   Comando  _SelBadObjects")
    print("   No debe seleccionar nada")
    print("=" * 58)


# ================================================================
if __name__ == "__main__":
    if construir():
        informe()
