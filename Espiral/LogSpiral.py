import numpy as np
from Parámetros.Parámetros_Vídeos import SIZE
import os


''' Variables '''

NOTA_GRAVE = 29
NOTA_AGUDA = 79

RATIO_GRAVE = 95 / 100
RATIO_AGUDO = 10 / 100

SHIFT = 9
TWIST = -1


''' Cálculo de A y B de la espiral logarítmica '''

min_size = min(SIZE)

r_g = RATIO_GRAVE * min_size / 2
r_a = RATIO_AGUDO * min_size / 2

B_LOG_SPIRAL = np.power(r_a / r_g, 1 / (NOTA_AGUDA - NOTA_GRAVE))

A_LOG_SPIRAL = r_g / np.power(B_LOG_SPIRAL, NOTA_GRAVE)


''' Guardado Imágenes '''

PATH_CARPETA = os.path.join('..', 'Outputs', 'Imágenes', 'EspiralLog')

''' Logs '''
PINTA_FRECUENCIAS = False


def posicion_espiral_logaritmica(nota):

    centro = [int(SIZE[0] / 2), int(SIZE[1] / 2)]

    radio = A_LOG_SPIRAL*np.power(B_LOG_SPIRAL, nota)

    x = radio * np.cos(TWIST * (nota+SHIFT)*(2*np.pi)/12) + centro[0]
    y = radio * np.sin(TWIST * (nota+SHIFT)*(2*np.pi)/12) + centro[1]

    return [int(x), int(y)]
