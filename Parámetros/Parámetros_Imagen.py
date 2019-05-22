#### Parámetros de la imagen ####

from Espiral.LogSpiral import posicion_espiral_logaritmica
from Parámetros.Parámetros_Vídeos import SIZE
import numpy as np


DESVIACION = 0.75

''' Tipo de alcance '''
# "E" para exacto con parámetro EPSILON
# "P" para parametrizado asignánsole un valor

TIPO_ALCANCE = "E"
EPSILON = 0.01

if TIPO_ALCANCE == "E":
    ALCANCE = np.sqrt(-2 * DESVIACION * DESVIACION * np.log(EPSILON))
elif TIPO_ALCANCE == "P":
    ALCANCE = 2
else:
    raise ValueError("Hay que decidir un tipo de alcance válido.")


[X_CERO, Y_CERO] = posicion_espiral_logaritmica(60)
[X_CENTRO, Y_CENTRO] = [int(SIZE[0] / 2), int(SIZE[1] / 2)]
