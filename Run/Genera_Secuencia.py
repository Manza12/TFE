from Parser.Score_Parser import score_parser
from Utilidades.Write import escribe_notas_por_voces
from Animación.Animación import *
from Parámetros.Parámetros_Creación import NOTAS_CRE_RE
from Parámetros.Parámetros_Vídeos import NOMBRE_VIDEO
import os


ESCRIBE_LISTA_NOTAS = True


def genera_animacion(seccion):
    path_seccion = seccion + '.xml'

    ''' Crea la obra '''

    print("Creando " + NOMBRE_VIDEO + " sección " + seccion)

    # Crea el path del xml
    inputs_directory = os.path.join('..', 'Inputs')
    path_obra = os.path.join(inputs_directory, path_seccion)

    # Parsea las notas
    lista_notas = score_parser(path_obra)

    # Crea el objeto Obra
    obra = Obra(seccion, 1, lista_notas)

    ''' Escribe las notas '''
    if ESCRIBE_LISTA_NOTAS:
        path_carpeta = os.path.join('..', 'Outputs', 'Vídeos', NOMBRE_VIDEO, 'Rondo Alla Turca')
        if not os.path.exists(path_carpeta):
            os.mkdir(path_carpeta)
            print("Carpeta ", path_carpeta, " creada ")
        path_carpeta = os.path.join('..', 'Outputs', 'Vídeos', NOMBRE_VIDEO, 'Rondo Alla Turca', 'Listas')
        if not os.path.exists(path_carpeta):
            os.mkdir(path_carpeta)
            print("Carpeta ", path_carpeta, " creada ")
        else:
            print("Carpeta ", path_carpeta, " ya existe")
        escribe_notas_por_voces(obra, path_carpeta)

    ''' Verifica que existen las notas base'''
    if NOTAS_CRE_RE == "C":
        for j in range(0, 100, 1):
            nota = Nota(j, 0, 0, 0, 0)
            pinta_nota_guarda(nota, PATH_NOTAS)

    else:
        for j in range(100):
            path_nota = os.path.join('..', 'Outputs', 'Imágenes', 'Notas', str(NORMA), str(j) + '.jpg')
            if not os.path.exists(path_nota):
                nota = Nota(j, 0, 0, 0, 0)
                pinta_nota_guarda(nota, PATH_NOTAS)

    ''' Crea la animación '''
    ani = anima_obra(obra, SIZE)

    ''' Guarda la animación '''
    path_save = os.path.join('..', 'Outputs', 'Vídeos', NOMBRE_VIDEO, obra.nombre, 'Animación')

    if not os.path.exists(path_save):
        os.mkdir(path_save)
        print("Carpeta ", path_save, " creada ")
    else:
        print("Carpeta ", path_save, " ya existe")
    file_name = obra.nombre + '_ani.mp4'
    guarda_animacion(ani, path_save, file_name)

    del ani


def genera_animacion_desde_fr_skeleton(path_fr_skeleton, nombre_obra, nombre_animacion):
    print("Creando obra desde el frame_skeleton de la carpeta " + path_fr_skeleton)

    ''' Crea la animación '''
    ani = anima_obra_desde_fr_skeleton(path_fr_skeleton, nombre_obra)

    ''' Guarda la animación '''
    path_save = os.path.join('..', 'Outputs', 'Vídeos', NOMBRE_VIDEO, nombre_obra, 'Animación')

    if not os.path.exists(path_save):
        os.mkdir(path_save)
        print("Carpeta ", path_save, " creada ")
    else:
        print("Carpeta ", path_save, " ya existe")
    file_name = nombre_animacion + '.mp4'
    guarda_animacion(ani, path_save, file_name)

    del ani


def genera_animacion_desde_fr_list(path_fr_list, nombre_obra, nombre_animacion):
    print("Creando obra desde el frame_list de la carpeta " + path_fr_list)

    ''' Crea la animación '''
    ani = anima_obra_desde_fr_list(path_fr_list, nombre_obra)

    ''' Guarda la animación '''
    path_save = os.path.join('..', 'Outputs', 'Vídeos', NOMBRE_VIDEO, nombre_obra, 'Animación')

    if not os.path.exists(path_save):
        os.mkdir(path_save)
        print("Carpeta ", path_save, " creada ")
    else:
        print("Carpeta ", path_save, " ya existe")
    file_name = nombre_animacion + '.mp4'
    guarda_animacion(ani, path_save, file_name)

    del ani


def genera_animacion_desde_fr_merge(path_fr_merge, nombre_obra, nombre_animacion):
    print("Creando obra desde el frame_merge de la carpeta " + path_fr_merge)

    ''' Crea la animación '''
    ani = anima_obra_desde_fr_merge(path_fr_merge, nombre_obra)

    ''' Guarda la animación '''
    path_save = os.path.join('..', 'Outputs', 'Vídeos', NOMBRE_VIDEO, nombre_obra, 'Animación')

    if not os.path.exists(path_save):
        os.mkdir(path_save)
        print("Carpeta ", path_save, " creada ")
    else:
        print("Carpeta ", path_save, " ya existe")
    file_name = nombre_animacion + '.mp4'
    guarda_animacion(ani, path_save, file_name)

    del ani
