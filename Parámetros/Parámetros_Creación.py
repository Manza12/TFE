#### PARÁMETROS DE CÓMO SE CREA EL VÍDEO ####


# Est4e parámetro sirve para decidir si en frame_merge se reescriben las imágenes ya existentes o no
REESCRIBIR_FRAME_MER = False
REESCRIBIR_FRAME_LIST = False


''' Parámetros que deciden si se crean o recuperan los elementos básicos: las notas y acordes '''

# Crea (C) o recupera (R) las Notas
NOTAS_CRE_RE = "R"
# Crea (C) o recupera (R) los Acordes
ACORDES_CRE_RE = "R"

''' Parámetros que deciden si se crean o recuperan las diversas listas de frames '''

# Cambiar aquí
CREA_TODO = False
# Éste no hace nada
RECUPERA_TODO = False

if not CREA_TODO:
    # Cambiar aquí
    RECUPERA_TODO = True


if CREA_TODO:
    # Crea (C) o recupera (R) el FrameSkeleton
    FR_SK_CRE_RE = "C"
    # Crea (C) o recupera (R) la FrameList
    FR_LIST_CRE_RE = "C"
    # Crea (C) o recupera (R) los FramesMerged
    FR_MER_CRE_RE = "C"

elif RECUPERA_TODO:
    # Crea (C) o recupera (R) el FrameSkeleton
    FR_SK_CRE_RE = "R"
    # Crea (C) o recupera (R) la FrameList
    FR_LIST_CRE_RE = "R"
    # Crea (C) o recupera (R) los FramesMerged
    FR_MER_CRE_RE = "R"

else:
    # Aquí es donde hay que parametrizar cuando no es CREA_TODO o RECUPERA_TODO
    # Crea (C) o recupera (R) el FrameSkeleton
    FR_SK_CRE_RE = "R"
    # Crea (C) o recupera (R) la FrameList
    FR_LIST_CRE_RE = "R"
    # Crea (C) o recupera (R) los FramesMerged
    FR_MER_CRE_RE = "C"
