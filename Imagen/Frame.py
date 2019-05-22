from Imagen.Imagen import *
from Parámetros.Parámetros_Creación import REESCRIBIR_FRAME_MER


FPS = 24
BPM = 60
FRAME_RATE = int(FPS * 60 / BPM)


class FrameSec:

    def __init__(self, img, inicio_sec, duracion_sec):
        self.img = img
        self.inicio_sec = inicio_sec
        self.duracion_sec = duracion_sec
        self.inicio_fr = int(FRAME_RATE * inicio_sec)
        self.duracion_fr = int(FRAME_RATE * duracion_sec)

    def __str__(self):
        frase = "Frame; inicio_sec = " + str(self.inicio_sec) + ", duracion_sec = " + str(self.duracion_sec) \
                + "inicio_fr = " + str(self.inicio_fr) + ", duracion_fr = " + str(self.duracion_fr)

        return frase

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class FramePos:

    def __init__(self, img, posicion):
        self.img = img
        self.posicion = posicion

    def __str__(self):
        frase = "Frame; posición = " + str(self.posicion)
        return frase

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


def mergea_frame_skeleton(acordes, path_fr_sk, size):
    frame_skeleton = list()
    for i in range(len(acordes)):
        frame = FrameSec(mergea_acorde_fijo_guarda(acordes[i], size, path_fr_sk), acordes[i].inicio, acordes[i].duracion)
        frame_skeleton.append(frame)
        print("Acorde " + str(i + 1) + " creado.")

    return frame_skeleton


def recupera_frame_skeleton(path_fr_sk):
    frame_skeleton = list()
    lista_imagenes = os.listdir(path_fr_sk)

    for i in range(0, len(lista_imagenes), 1):
        file_name = lista_imagenes[i]
        file_path = os.path.join(path_fr_sk, file_name)
        img = recupera_imagen(file_path)
        [inicio, duracion] = devuelve_inicio_duracion(file_name)
        frame = FrameSec(img, inicio, duracion)
        frame_skeleton.append(frame)
        logging.info("Frame " + str(i + 1) + " recuperado.")
        print("Acorde " + str(i + 1) + " recuperado.")

    return frame_skeleton


def crea_frame_list(frame_skeleton, path_fr_list):

    # Reberberación del sonido
    # Si optima = True : se calculará el valor para que el decaimiento sea exacto con un fin establecido
    # Si optima = False : se asignará un valor de reberberación para establecer la dispersión del sonido

    optima = False

    if optima:
        fin = 0.01
        desviacion = np.sqrt(-(np.power(FRAME_RATE, 2)) / (2*np.log(fin))) / 1000
    else:
        reberberacion = 5  # Valores de 1 a 10 es una buena orquilla
        dispersion = 40*np.power(1.2, reberberacion)
        desviacion = 1 / dispersion

    k = 1
    for frame in frame_skeleton:
        print("Difuminamos acorde " + str(k))

        duracion_sec = frame.duracion_sec
        duracion_fr = frame.duracion_fr

        for fr in range(0, duracion_fr, 1):
            factor = gauss_disipacion(fr / duracion_sec, 1, desviacion)
            rep_frame = 1
            posicion = frame.inicio_fr + fr
            path_candidato = os.path.join(path_fr_list, str(posicion) + '_' + str(rep_frame) + '.jpg')
            while os.path.isfile(path_candidato):
                rep_frame += 1
                path_candidato = os.path.join(path_fr_list, str(posicion) + '_' + str(rep_frame))
            nombre_img = str(posicion) + '_' + str(rep_frame)

            difumina_guarda(frame, factor, path_fr_list, nombre_img)

        k += 1


def recupera_frame_list(path_fr_list):
    frame_list = list()

    lista_imagenes = os.listdir(path_fr_list)

    for i in range(0, len(lista_imagenes), 1):
        file_name = lista_imagenes[i]
        file_path = os.path.join(path_fr_list, file_name)
        img = recupera_imagen(file_path)
        posicion = devuelve_posicion_frame(file_name)
        frame = FramePos(img, posicion)
        frame_list.append(frame)

        print("Frame " + str(posicion) + " recuperado.")

    return frame_list


def crea_frames_merged(frame_list, path_fr_mer):
    # frame_mer = list()
    position_list = list()

    for frame in frame_list:
        if frame.posicion not in position_list:
            position_list.append(frame.posicion)
    position_list.sort()

    print("Hay que mergear", len(position_list), "frames.")

    for posicion in position_list:
        if REESCRIBIR_FRAME_MER:
            frames_pos = frames_con_tempo(frame_list, posicion)
            frame = merge_frames(frames_pos, posicion)

            # Borra las imágenes antiguas
            for fr in frame_list:
                if fr.posicion == posicion:
                    frame_list.remove(fr)

            file_name = str(posicion) + '.jpg'
            guarda_imagen(frame.img, path_fr_mer, file_name)
            # frame_mer.append(frame)
            porcentaje = round(int(posicion) * 100 / len(position_list), 2)
            print("Frame " + str(posicion) + " mergeado.", "(" + str(porcentaje) + "%)")
        else:
            file_name = str(posicion) + '.jpg'
            file_path = os.path.join(path_fr_mer, file_name)
            if os.path.exists(file_path):
                print("El Frame " + str(posicion) + " ya existe.")
            else:
                frames_pos = frames_con_tempo(frame_list, posicion)
                frame = merge_frames(frames_pos, posicion)

                # Borra las imágenes antiguas
                for fr in frame_list:
                    if fr.posicion == posicion:
                        frame_list.remove(fr)

                guarda_imagen(frame.img, path_fr_mer, file_name)

                porcentaje = round(int(posicion) * 100 / len(position_list), 2)
                print("Frame " + str(posicion) + " mergeado.", "(" + str(porcentaje) + "%)")

    # return frame_mer


def recupera_frames_merged(path_fr_mer):
    frame_mer = list()

    lista_imagenes = os.listdir(path_fr_mer)

    for i in range(0, len(lista_imagenes), 1):
        file_name = lista_imagenes[i]
        file_path = os.path.join(path_fr_mer, file_name)
        img = recupera_imagen(file_path)
        posicion = recupera_posicion(file_name)
        frame = FramePos(img, posicion)
        frame_mer.append(frame)

        print("Frame mergeado " + str(posicion) + " recuperado.")

    return frame_mer


def merge_frames(frames_pos, posicion):
    lista_imagenes = list()

    for frame in frames_pos:
        lista_imagenes.append(frame.img)

    img_merged = merge_lista(lista_imagenes)

    frame_merged = FramePos(img_merged, posicion)

    return frame_merged


def frames_con_tempo(frame_list, tempo):
    frames = list()
    for frame in frame_list:
        if frame.posicion == tempo:
            frames.append(frame)

    return frames


def ordena_frames(frame_mer):
    frame_sort = list()
    position_list = list()

    for frame in frame_mer:
        if frame.posicion not in position_list:
            position_list.append(frame.posicion)
    position_list.sort()

    for posicion in position_list:
        for frame in frame_mer:
            if frame.posicion == posicion:
                frame_sort.append(frame)

    return frame_sort
