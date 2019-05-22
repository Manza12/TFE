from Parser.Score_Parser import score_parser
from Utilidades.Write import escribe_notas_por_voces
from Animación.Animación import *
from Parámetros.Parámetros_Creación import NOTAS_CRE_RE
from Parámetros.Parámetros_Vídeos import NOMBRE_VIDEO
import os

    
SECCION = "Bach_1"
PATH_SECCION = SECCION + '.xml'
ESCRIBE_LISTA_NOTAS = True


''' Crea la OBRA '''

print("Creando " + NOMBRE_VIDEO + " sección " + SECCION)

# Crea el path del xml
INPUTS_DIRECTORY = os.path.join('..', 'Inputs')
PATH_OBRA = os.path.join(INPUTS_DIRECTORY, PATH_SECCION)

# Parsea las notas
LISTA_NOTAS = score_parser(PATH_OBRA)

# Crea el objeto Obra
OBRA = Obra(SECCION, 1, LISTA_NOTAS)


''' Escribe las notas '''
if ESCRIBE_LISTA_NOTAS:
    PATH_CARPETA = os.path.join('..', 'Outputs', 'Vídeos', NOMBRE_VIDEO, 'Rondo Alla Turca')
    if not os.path.exists(PATH_CARPETA):
        os.mkdir(PATH_CARPETA)
        print("Carpeta ", PATH_CARPETA, " creada ")
    PATH_CARPETA = os.path.join('..', 'Outputs', 'Vídeos', NOMBRE_VIDEO, 'Rondo Alla Turca', 'Listas')
    if not os.path.exists(PATH_CARPETA):
        os.mkdir(PATH_CARPETA)
        print("Carpeta ", PATH_CARPETA, " creada ")
    else:
        print("Carpeta ", PATH_CARPETA, " ya existe")
    escribe_notas_por_voces(OBRA, PATH_CARPETA)

''' Verifica que existen las notas base'''
if NOTAS_CRE_RE == "C":
    for i in range(0, 100, 1):
        NOTA = Nota(i, 0, 0, 0, 0)
        pinta_nota_guarda(NOTA, PATH_NOTAS)

else:
    for i in range(100):
        PATH_NOTA = os.path.join('..', 'Outputs', 'Imágenes', 'Notas', str(NORMA), str(i) + '.jpg')
        if not os.path.exists(PATH_NOTA):
            NOTA = Nota(i, 0, 0, 0, 0)
            pinta_nota_guarda(NOTA, PATH_NOTAS)

''' Crea la animación '''
ANI = anima_obra(OBRA, SIZE)


''' Guarda la animación '''
PATH_SAVE = os.path.join('..', 'Outputs', 'Vídeos', NOMBRE_VIDEO, OBRA.nombre, 'Animación')

if not os.path.exists(PATH_SAVE):
    os.mkdir(PATH_SAVE)
    print("Carpeta ", PATH_SAVE, " creada ")
else:
    print("Carpeta ", PATH_SAVE, " ya existe")
FILE_NAME = OBRA.nombre + '_ani.mp4'
guarda_animacion(ANI, PATH_SAVE, FILE_NAME)


''' Muestra animación '''

plt.show()
