#### PARÁMETROS DEL TIPO DE VÍDEO ####

import numpy as np

''' TAMAÑO '''

HEIGHT = 480
WIDTH = 852
SIZE = [WIDTH, HEIGHT]


''' TIPO DE VÍDEO '''

TIPO_VIDEO = 2

VIDEO_1 = False
VIDEO_2 = False
VIDEO_3 = False
VIDEO_4 = False
VIDEO_5 = False
VIDEO_6 = False
VIDEO_7 = False

if TIPO_VIDEO == 1:
    VIDEO_1 = True
    NOMBRE_VIDEO = "Vídeo_1"
elif TIPO_VIDEO == 2:
    VIDEO_2 = True
    NOMBRE_VIDEO = "Vídeo_2"
elif TIPO_VIDEO == 3:
    VIDEO_3 = True
    NOMBRE_VIDEO = "Vídeo_3"
elif TIPO_VIDEO == 4:
    VIDEO_4 = True
    NOMBRE_VIDEO = "Vídeo_4"
elif TIPO_VIDEO == 5:
    VIDEO_5 = True
    NOMBRE_VIDEO = "Vídeo_5"
elif TIPO_VIDEO == 6:
    VIDEO_6 = True
    NOMBRE_VIDEO = "Vídeo_6"
elif TIPO_VIDEO == 7:
    VIDEO_7 = True
    NOMBRE_VIDEO = "Vídeo_7"
else:
    raise ValueError("Hay que elegir algún vídeo.")

### Vídeos 1, 2, 3:

# Estos vídeos mergean las notas base sin saturación

# Vídeo 1 : norma 1
if VIDEO_1:
    NORMA = 1
# Vídeo 2 : norma 2
elif VIDEO_2:
    NORMA = 2
# Vídeo 3 : norma inf
elif VIDEO_3:
    NORMA = np.inf
else:
    raise ValueError("Hay que decidir qué norma se elige.")
