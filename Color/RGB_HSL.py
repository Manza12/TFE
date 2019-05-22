import numpy as np
from Parámetros.Parámetros_Vídeos import SIZE


# Parámetros para el color
LUM_MINIMA = 10
LUM_MAXIMA = 100
NOTA_LUM_MIN = 15
NOTA_LUM_MAX = 96

# Tipo de aumento de luz
# Opciones: lineal, parabolico
AUMENTO_LUZ = "parabolico"
ALPHA = 0

# Dirección de giro de la espiral; 1 o -1
TWIST = -1
# Desplazamiento de color; de 0 a 11
SHIFT = 4


def hsl_espiral(nota):
    hue = 0
    sat = 0
    lum = 0

    if nota != 0:
        hue = 30*(nota % 12)
        sat = 1

        if AUMENTO_LUZ == "lineal":
            a = (LUM_MAXIMA - LUM_MINIMA) / (NOTA_LUM_MAX - NOTA_LUM_MIN)
            b = LUM_MAXIMA - a * NOTA_LUM_MAX
            lum = (a * nota + b) / 100
        elif AUMENTO_LUZ == "parabolico":
            a = (ALPHA * (NOTA_LUM_MAX**2 - NOTA_LUM_MIN**2) - (LUM_MAXIMA - LUM_MINIMA)) \
                / (2 * NOTA_LUM_MIN - (NOTA_LUM_MAX**2 - NOTA_LUM_MIN**2))
            b = (LUM_MAXIMA - LUM_MINIMA - a * (NOTA_LUM_MAX**2 - NOTA_LUM_MIN**2)) / (NOTA_LUM_MAX - NOTA_LUM_MIN)
            c = LUM_MAXIMA - a * NOTA_LUM_MAX**2 - b * NOTA_LUM_MAX
            lum = (a * nota**2 + b * nota + c) / 100

    # Twist & Shift
    hue = hue_to_0_360(TWIST * (hue + SHIFT * 30))

    return [hue, sat, lum]


def rgb2hsl(r, g, b):
    r = r/255
    g = g/255
    b = b/255

    mx = max(r, g, b)
    mn = min(r, g, b)

    if mx == mn:
        hue = 0
    elif mx == r:
        hue = 60*(g-b)/(mx-mn)+360 % 360
    elif mx == g:
        hue = 60 * (b - r) / (mx - mn) + 120
    elif mx == b:
        hue = 60 * (r - g) / (mx - mn) + 240
    else:
        raise ValueError("Algo raro pasa")

    lum = (mx+mn)/2

    if mx == mn:
        sat = 0
    elif lum <= 1/2:
        sat = (mx-mn)/(2*lum)
    elif lum > 1/2:
        sat = (mx-mn)/(2-2*lum)
    else:
        raise ValueError("Algo raro pasa")

    return [hue, sat, lum]


def hsl2rgb(hue, sat, lum):
    hue_to_0_360(hue)
    lum = np.nan_to_num(lum)

    c = np.nan_to_num((1 - abs(2 * lum - 1)) * sat)

    h2 = hue / 60
    h3 = h2 % 2

    x = c*(1-abs(h3-1))

    if 0 <= h2 <= 1:
        [r1, g1, b1] = [c, x, 0]
    elif 1 <= h2 <= 2:
        [r1, g1, b1] = [x, c, 0]
    elif 2 <= h2 <= 3:
        [r1, g1, b1] = [0, c, x]
    elif 3 <= h2 <= 4:
        [r1, g1, b1] = [0, x, c]
    elif 4 <= h2 <= 5:
        [r1, g1, b1] = [x, 0, c]
    elif 5 <= h2 <= 6:
        [r1, g1, b1] = [c, 0, x]
    else:
        raise ValueError("Hue fuera de rango")

    m = lum - c / 2

    [r, g, b] = (r1+m, g1+m, b1+m)

    return int(round(r*255)), int(round(g*255)), int(round(b*255))


def media_hue_pond_lum(hue_1, hue_2, w_lum_1, w_lum_2, tipo, gravedad):
    p_1 = np.power(w_lum_1, gravedad)
    p_2 = np.power(w_lum_2, gravedad)
    w_1 = p_1 / (p_1 + p_2)
    w_2 = p_2 / (p_1 + p_2)

    if tipo == "deg":
        h_1 = hue_1 * 2 * np.pi / 360
        h_2 = hue_2 * 2 * np.pi / 360

        v_1 = [w_1 * np.cos(h_1), w_1 * np.sin(h_1)]
        v_2 = [w_2 * np.cos(h_2), w_2 * np.sin(h_2)]

        v = [v_1[0] + v_2[0], v_1[1] + v_2[1]]

        h = np.arctan2(v[1], v[0])

        hue = 360 * h / (2 * np.pi)
    else:
        print("Tipo de ángulo no válido")
        return hue_1

    return hue


def media_ponderada_hue(hue_1, hue_2, w_1, w_2, tipo):
    w_1 = np.nan_to_num(w_1)
    w_2 = np.nan_to_num(w_2)
    if w_1 == 0 and w_2 == 0:
        w_1 += 0.01
        w_2 += 0.01
    suma_pesos = w_1 + w_2
    p_1 = w_1 / suma_pesos
    p_2 = w_2 / suma_pesos

    if tipo == "deg":
        h_1 = hue_1 * 2 * np.pi / 360
        h_2 = hue_2 * 2 * np.pi / 360

        v_1 = [p_1 * np.cos(h_1), p_1 * np.sin(h_1)]
        v_2 = [p_2 * np.cos(h_2), p_2 * np.sin(h_2)]

        v = [v_1[0] + v_2[0], v_1[1] + v_2[1]]

        h = np.arctan2(v[1], v[0])
        h_convert = 360 * h / (2 * np.pi)
    else:
        print("Tipo de ángulo no válido")
        return hue_1

    return h_convert


def media_ponderada_hues(lista_hues, lista_pesos, tipo):
    if len(lista_hues) != len(lista_pesos):
        raise ValueError("Las longitudes de las listas no coinciden.")
    else:
        numero_hues = len(lista_pesos)

    suma_pesos = sum(lista_pesos)
    lista_w = []
    for n in range(numero_hues):
        w = lista_pesos[n] / suma_pesos
        lista_w.append(w)

    if tipo == "deg":
        lista_h = []
        for n in range(numero_hues):
            h = lista_hues[n] * 2 * np.pi / 360
            lista_h.append(h)

        lista_vectores = []
        for n in range(numero_hues):
            v = [lista_w[n] * np.cos(lista_h[n]), lista_w[n] * np.sin(lista_h[n])]
            lista_vectores.append(v)

        vector = [0, 0]
        for n in range(numero_hues):
            vector[0] += lista_vectores[n][0]
            vector[1] += lista_vectores[n][1]

        if vector == [0, 0]:
            raise ValueError("La media no se puede realizar")
        else:
            h = np.arctan2(vector[1], vector[0])
        h_convert = 360 * h / (2 * np.pi)
    else:
        print("Tipo de ángulo no válido")
        return lista_hues[0]

    return h_convert


def media_hue(hue_1, hue_2, tipo):
    if tipo == "deg":
        h_1 = hue_1 * 2 * np.pi / 360  # - DESV_RAD
        h_2 = hue_2 * 2 * np.pi / 360  # - DESV_RAD
        h = np.arctan2((np.sin(h_1) + np.sin(h_2)) / 2, (np.cos(h_1) + np.cos(h_2)) / 2)
        h_convert = 360 * h / (2 * np.pi)
        return h_convert
    else:
        print("Tipo de ángulo no válido")
        return hue_1


def hue_to_0_360(hue):
    while hue < 0:
        hue += 360
    while hue >= 360:
        hue -= 360
    return hue
