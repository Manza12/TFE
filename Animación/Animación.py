import matplotlib.pyplot as plt
import shutil
from Beans.Música import *
from Imagen.Frame import *
import matplotlib.animation as animation
from Parámetros.Parámetros_Vídeos import NOMBRE_VIDEO, VIDEO_1, VIDEO_2, VIDEO_3, VIDEO_4, VIDEO_5, VIDEO_6, VIDEO_7
from Parámetros.Parámetros_Creación import FR_LIST_CRE_RE, FR_MER_CRE_RE, FR_SK_CRE_RE


DPI = 100
W_INCH = 8.52
H_INCH = 4.80


def anima_obra(obra, size):

    ''' Creación del plot '''

    # Figure object
    fig = plt.figure()
    fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=None, hspace=None)
    fig.set_size_inches(W_INCH, H_INCH, True)

    plt.axis('off')

    # Parametraje
    delay_frames = 29  # En milisegundos
    logging.debug("delay_frames = " + str(delay_frames))

    ''' Preparación de los acordes '''

    # Agrupamiento por t_d
    acordes = agrupa_por_t_d(obra)
    print("Acordes agrupados; hay " + str(len(acordes)) + " acordes por pintar.")

    ''' Creación de las carpetas '''
    lista_carpetas = list()

    # Carpetas Principales
    path_obra = os.path.join('..', 'Outputs', 'Vídeos', NOMBRE_VIDEO, obra.nombre)
    path_imagenes = os.path.join('..', 'Outputs', 'Vídeos', NOMBRE_VIDEO, obra.nombre, 'Imágenes')
    path_animacion = os.path.join('..', 'Outputs', 'Vídeos', NOMBRE_VIDEO, obra.nombre, 'Animación')
    lista_carpetas.append(path_obra)
    lista_carpetas.append(path_imagenes)
    lista_carpetas.append(path_animacion)

    # FrameSkeleton
    path_fr_sk = os.path.join('..', 'Outputs', 'Vídeos', NOMBRE_VIDEO, obra.nombre, 'Imágenes', 'FrameSkeleton')
    lista_carpetas.append(path_fr_sk)

    # FrameList
    path_fr_list = os.path.join('..', 'Outputs', 'Vídeos', NOMBRE_VIDEO, obra.nombre, 'Imágenes', 'FrameList')
    lista_carpetas.append(path_fr_list)

    # FrameMerge
    path_fr_mer = os.path.join('..', 'Outputs', 'Vídeos', NOMBRE_VIDEO, obra.nombre, 'Imágenes', 'FrameMerge')
    lista_carpetas.append(path_fr_mer)

    # Eliminación de imágenes que perturban el buen desarrollo
    if os.path.exists(path_fr_list) and FR_LIST_CRE_RE == "C":
        shutil.rmtree(path_fr_list)

    # Creación de carpetas
    for carpeta in lista_carpetas:
        if not os.path.exists(carpeta):
            os.mkdir(carpeta)
            print("Carpeta ", carpeta, " creada ")
        else:
            print("Carpeta ", carpeta, " ya existe")

    ''' Creación del FrameSkeleton'''

    if VIDEO_1 or VIDEO_2 or VIDEO_3:
        if FR_SK_CRE_RE == "C":
            print("Creación de FrameSkeleton;", len(acordes), "acordes por crear.")
            frame_skeleton = mergea_frame_skeleton(acordes, path_fr_sk, size)
        elif FR_SK_CRE_RE == "R":
            frame_skeleton = recupera_frame_skeleton(path_fr_sk)
        else:
            print("La opción del FrameSkeleton no es correcta")
            frame_skeleton = list()
    else:
        raise ValueError("Necesitas crear un frame skeleton")

    ''' Creación del FrameList'''

    if FR_LIST_CRE_RE == "C":
        print("Creación de FrameList;", len(frame_skeleton), "frames por difuminar.")
        crea_frame_list(frame_skeleton, path_fr_list)
        frame_list = recupera_frame_list(path_fr_list)
    elif FR_LIST_CRE_RE == "R":
        frame_list = recupera_frame_list(path_fr_list)
    else:
        print("La opción del FrameList no es correcta")
        frame_list = list()
    print("Difuminación de frames realizada.")

    del frame_skeleton

    ''' Creación de FrameMerge '''

    if FR_MER_CRE_RE == "C":
        print("Creación de FrameMerge")
        crea_frames_merged(frame_list, path_fr_mer)
        frame_mer = recupera_frames_merged(path_fr_mer)
    elif FR_MER_CRE_RE == "R":
        frame_mer = recupera_frames_merged(path_fr_mer)
    else:
        print("La opción del FrameMerge no es correcta")
        frame_mer = list()

    del frame_list

    ''' Ordenado de los frames '''

    frames_sort = ordena_frames(frame_mer)
    del frame_mer

    frames_plot = convierte_imagenes_plot(frames_sort)
    del frames_sort

    print("Frames ordenados.")

    ''' Creación de la animación '''

    ani = animation.ArtistAnimation(fig, frames_plot, interval=delay_frames, blit=True,
                                    repeat=True)  # repeat_delay=1000)
    print("Animación creada.")

    return ani


def anima_obra_desde_fr_skeleton(path_fr_sk, nombre_obra):

    ''' Creación del plot '''

    # Figure object
    fig = plt.figure()
    fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=None, hspace=None)
    fig.set_size_inches(W_INCH, H_INCH, True)

    plt.axis('off')

    # Parametraje
    delay_frames = 29  # En milisegundos
    logging.debug("delay_frames = " + str(delay_frames))

    ''' Creación de las carpetas '''
    lista_carpetas = list()

    # Carpetas Principales
    path_obra = os.path.join('..', 'Outputs', 'Vídeos', NOMBRE_VIDEO, nombre_obra)
    path_imagenes = os.path.join('..', 'Outputs', 'Vídeos', NOMBRE_VIDEO, nombre_obra, 'Imágenes')
    path_animacion = os.path.join('..', 'Outputs', 'Vídeos', NOMBRE_VIDEO, nombre_obra, 'Animación')
    lista_carpetas.append(path_obra)
    lista_carpetas.append(path_imagenes)
    lista_carpetas.append(path_animacion)

    # FrameList
    path_fr_list = os.path.join('..', 'Outputs', 'Vídeos', NOMBRE_VIDEO, nombre_obra, 'Imágenes', 'FrameList')
    lista_carpetas.append(path_fr_list)

    # FrameMerge
    path_fr_mer = os.path.join('..', 'Outputs', 'Vídeos', NOMBRE_VIDEO, nombre_obra, 'Imágenes', 'FrameMerge')
    lista_carpetas.append(path_fr_mer)

    # Eliminación de imágenes que perturban el buen desarrollo
    if os.path.exists(path_fr_list) and FR_LIST_CRE_RE == "C":
        shutil.rmtree(path_fr_list)

    # Creación de carpetas
    for carpeta in lista_carpetas:
        if not os.path.exists(carpeta):
            os.mkdir(carpeta)
            print("Carpeta ", carpeta, " creada ")
        else:
            print("Carpeta ", carpeta, " ya existe")

    frame_skeleton = recupera_frame_skeleton(path_fr_sk)

    ''' Creación del FrameList'''

    print("Creación de FrameList")
    crea_frame_list(frame_skeleton, path_fr_list)
    frame_list = recupera_frame_list(path_fr_list)

    del frame_skeleton

    ''' Creación de FrameMerge '''

    print("Creación de FrameMerge")
    crea_frames_merged(frame_list, path_fr_mer)
    frame_mer = recupera_frames_merged(path_fr_mer)

    del frame_list

    ''' Ordenado de los frames '''

    frames_sort = ordena_frames(frame_mer)
    del frame_mer

    frames_plot = convierte_imagenes_plot(frames_sort)
    del frames_sort

    print("Frames ordenados.")

    ''' Creación de la animación '''

    ani = animation.ArtistAnimation(fig, frames_plot, interval=delay_frames, blit=True,
                                    repeat=True)  # repeat_delay=1000)
    print("Animación creada.")

    return ani


def anima_obra_desde_fr_list(path_fr_list, nombre_obra):

    ''' Creación del plot '''

    # Figure object
    fig = plt.figure()
    fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=None, hspace=None)
    fig.set_size_inches(W_INCH, H_INCH, True)

    plt.axis('off')

    # Parametraje
    delay_frames = 29  # En milisegundos
    logging.debug("delay_frames = " + str(delay_frames))

    ''' Creación de las carpetas '''
    lista_carpetas = list()

    # Carpetas Principales
    path_obra = os.path.join('..', 'Outputs', 'Vídeos', NOMBRE_VIDEO, nombre_obra)
    path_imagenes = os.path.join('..', 'Outputs', 'Vídeos', NOMBRE_VIDEO, nombre_obra, 'Imágenes')
    path_animacion = os.path.join('..', 'Outputs', 'Vídeos', NOMBRE_VIDEO, nombre_obra, 'Animación')
    lista_carpetas.append(path_obra)
    lista_carpetas.append(path_imagenes)
    lista_carpetas.append(path_animacion)

    # FrameMerge
    path_fr_mer = os.path.join('..', 'Outputs', 'Vídeos', NOMBRE_VIDEO, nombre_obra, 'Imágenes', 'FrameMerge')
    lista_carpetas.append(path_fr_mer)

    # Eliminación de imágenes que perturban el buen desarrollo
    if os.path.exists(path_fr_list) and FR_LIST_CRE_RE == "C":
        shutil.rmtree(path_fr_list)

    # Creación de carpetas
    for carpeta in lista_carpetas:
        if not os.path.exists(carpeta):
            os.mkdir(carpeta)
            print("Carpeta ", carpeta, " creada ")
        else:
            print("Carpeta ", carpeta, " ya existe")

    ''' Creación del FrameList'''

    print("Creación de FrameList")
    frame_list = recupera_frame_list(path_fr_list)

    ''' Creación de FrameMerge '''

    print("Creación de FrameMerge")
    crea_frames_merged(frame_list, path_fr_mer)
    frame_mer = recupera_frames_merged(path_fr_mer)

    del frame_list

    ''' Ordenado de los frames '''

    frames_sort = ordena_frames(frame_mer)
    del frame_mer

    frames_plot = convierte_imagenes_plot(frames_sort)
    del frames_sort

    print("Frames ordenados.")

    ''' Creación de la animación '''

    ani = animation.ArtistAnimation(fig, frames_plot, interval=delay_frames, blit=True,
                                    repeat=True)  # repeat_delay=1000)
    print("Animación creada.")

    return ani


def anima_obra_desde_fr_merge(path_fr_mer, nombre_obra):

    ''' Creación del plot '''

    # Figure object
    fig = plt.figure()
    fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=None, hspace=None)
    fig.set_size_inches(W_INCH, H_INCH, True)

    plt.axis('off')

    # Parametraje
    delay_frames = 29  # En milisegundos
    logging.debug("delay_frames = " + str(delay_frames))

    ''' Creación de las carpetas '''
    lista_carpetas = list()

    # Carpetas Principales
    path_obra = os.path.join('..', 'Outputs', 'Vídeos', NOMBRE_VIDEO, nombre_obra)
    path_imagenes = os.path.join('..', 'Outputs', 'Vídeos', NOMBRE_VIDEO, nombre_obra, 'Imágenes')
    path_animacion = os.path.join('..', 'Outputs', 'Vídeos', NOMBRE_VIDEO, nombre_obra, 'Animación')
    lista_carpetas.append(path_obra)
    lista_carpetas.append(path_imagenes)
    lista_carpetas.append(path_animacion)

    # Creación de carpetas
    for carpeta in lista_carpetas:
        if not os.path.exists(carpeta):
            os.mkdir(carpeta)
            print("Carpeta ", carpeta, " creada ")
        else:
            print("Carpeta ", carpeta, " ya existe")

    ''' Creación de FrameMerge '''

    print("Creación de FrameMerge")
    frame_mer = recupera_frames_merged(path_fr_mer)

    ''' Ordenado de los frames '''

    frames_sort = ordena_frames(frame_mer)
    del frame_mer

    frames_plot = convierte_imagenes_plot(frames_sort)
    del frames_sort

    print("Frames ordenados.")

    ''' Creación de la animación '''

    ani = animation.ArtistAnimation(fig, frames_plot, interval=delay_frames, blit=True,
                                    repeat=True)  # repeat_delay=1000)
    print("Animación creada.")

    return ani


def agrupa_por_t_d(obra):
    acordes = list()
    for i in range(len(obra.notas)):
        t_d = [obra.notas[i].inicio, obra.notas[i].duracion]
        notas = list()
        for j in range(len(obra.notas)):
            if t_d == [obra.notas[j].inicio, obra.notas[j].duracion]:
                notas.append(obra.notas[j].altura)
        acorde = Acorde(notas, [], t_d[0], t_d[1])
        if not (acorde in acordes):
            acordes.append(acorde)

    return acordes


def convierte_imagenes_plot(frames_sort):

    frames_plot = list()

    while len(frames_sort) != 0:
        frame = frames_sort[0]
        im = plt.imshow(frame.img, animated=True)
        frames_plot.append([im])
        frames_sort.remove(frame)

    return frames_plot


def guarda_animacion(ani, path_carpeta, file_name):
    print("Empieza el guardado de la animación")
    Writer = animation.writers['ffmpeg']
    writer = Writer(fps=24, bitrate=1024)

    file_path = os.path.join(path_carpeta, file_name)
    ani.save(file_path, writer=writer, dpi=DPI)
    print("Animación guardada.")
