import numpy as np


''' TIPO DE PERTURBACIÓN '''

# cubica : encoje el centro y aumenta el valle bastante
# parabola : encoje simplemente
# cubica_disipada : como la cúbica pero de 0.5 a 0 es lineal; parece un huevo frito
# arcoseno : utilizando la función arcoseno normalizada; muy picuda/concentrada

TIPO_PERTURBACION = "ninguna"


def gauss_disipacion(t, scale, kdeviation):

    valor = scale*np.exp(-(pow(t, 2)/(2*pow(kdeviation*1000, 2))))

    return valor


def gauss(t, scale, desviacion_tipica):

    valor = scale*np.exp(- t * t / (2 * desviacion_tipica * desviacion_tipica))

    return valor


def perturbacion_factor(factor):
    if TIPO_PERTURBACION == "cubica":
        valor = ((2*factor-1)**3 + 1)/2
    elif TIPO_PERTURBACION == "parabola":
        valor = factor**2
    elif TIPO_PERTURBACION == "cubica_disipada":
        if factor >= 1/2:
            valor = ((2 * factor - 1) ** 3 + 1) / 2
        else:
            valor = factor
    elif TIPO_PERTURBACION == "arcoseno":
        valor = (np.arcsin(2*factor-1)+np.pi/2)/np.pi
    else:
        valor = factor

    return valor
