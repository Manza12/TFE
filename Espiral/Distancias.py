import numpy as np
from numpy import linalg
from Parámetros.Parámetros_Imagen import X_CERO, Y_CERO, X_CENTRO, Y_CENTRO
from Espiral.LogSpiral import B_LOG_SPIRAL


# Este parámetro influye en la noción de distancia entre octavas

TIPO_FACTOR = "exacto"

# Opciones:
# 1) exacto --> hace que las octavas sean tangentes ¡¡¡¡¡¡ NO FUNCIONA!!!!!!
# 2) trivial --> las octavas pueden intersecarse o no, en función del ámbito
# 3) unitario --> hace que la distancia entre octavas sea 1; provoca hueco entre octavas


def factor_geometrico(b):
    alpha = 1

    if TIPO_FACTOR == "exacto":
        alpha = 1 / (-12 * np.log(b))
    elif TIPO_FACTOR == "unitario":
        alpha = 1 / (np.power(b, -12) - 1)

    return alpha


def posicion_cilindro(x, y):

    radio_1 = np.sqrt(np.power((x - X_CENTRO), 2) + np.power((y - Y_CENTRO), 2))
    radio_2 = np.sqrt(np.power((X_CERO - X_CENTRO), 2) + np.power((Y_CERO - Y_CENTRO), 2))

    if radio_1 != 0:
        r = np.log(radio_1 / radio_2)
    else:
        r = 1000000

    r_b = r * factor_geometrico(B_LOG_SPIRAL)

    z1 = x - X_CENTRO + 1j * (y - Y_CENTRO)
    z2 = X_CERO - X_CENTRO + 1j * (Y_CERO - Y_CENTRO)

    if X_CERO - X_CENTRO + 1j*(Y_CERO - Y_CENTRO) != 0:
        phi = np.angle(z1/z2)
    else:
        phi = 0

    phi_12 = phi*12/(2*np.pi)

    return [r_b, phi_12]


def distancia_cilindro(r_1, phi_1, r_2, phi_2, norma):
    if phi_1 >= phi_2:
        dif = phi_1 - phi_2
        if dif > 6:
            distancia_angular = 12 - dif
        else:
            distancia_angular = dif
    elif phi_2 >= phi_1:
        dif = phi_2 - phi_1
        if dif > 6:
            distancia_angular = 12 - dif
        else:
            distancia_angular = dif
    else:
        raise ValueError("Algo falla en distancia_cilindro")

    distancia_radial = max(r_1, r_2) - min(r_1, r_2)

    distancia = linalg.norm((distancia_radial, distancia_angular), norma)

    return distancia
