import logging
from PIL import Image
from Espiral.LogSpiral import posicion_espiral_logaritmica, B_LOG_SPIRAL
from Color.RGB_HSL import *
from Espiral.Distancias import *
from Utilidades.Gaussian import *
from Utilidades.Conversor import *
from Utilidades.Diccionarios import diccionario_posicion_cilindro
from Parámetros.Parámetros_Vídeos import SIZE, NORMA
from Parámetros.Parámetros_Imagen import ALCANCE, DESVIACION
from Parámetros.Parámetros_Creación import ACORDES_CRE_RE, NOTAS_CRE_RE
import os


''' Carpetas '''
PATH_NOTAS = os.path.join('..', 'Outputs', 'Imágenes', 'Notas', str(NORMA))
PATH_ACORDES = os.path.join('..', 'Outputs', 'Imágenes', 'Acordes', str(NORMA))

if NOTAS_CRE_RE == "C":
    ''' Diccionario de posición en el cilindro '''
    DICCIONARIO_POSICION = diccionario_posicion_cilindro(SIZE)


# Función que sirve para pintar las notas
def pinta_nota_guarda(nota, path_carpeta):

    altura = nota.altura
    nombre = str(altura)
    print("Creando NOTA " + nombre + " con norma " + str(NORMA))

    img = Image.new('RGB', SIZE, "black")  # create a new black image
    pixels = img.load()  # create the pixel map
    centro_nota = posicion_espiral_logaritmica(altura)
    if centro_nota[0] > SIZE[0] or centro_nota[1] > SIZE[1] or centro_nota[0] < 0 or centro_nota[1] < 0:
        print("El centro de esta NOTA está fuera del marco. La NOTA será negra.")
        return img

    centro_nota_cilindro = DICCIONARIO_POSICION[centro_nota[0], centro_nota[1]]

    for i in range(img.size[0]):
        for j in range(img.size[1]):
            pos_cilindro = DICCIONARIO_POSICION[i, j]
            distancia = distancia_cilindro(pos_cilindro[0], pos_cilindro[1],
                                           centro_nota_cilindro[0], centro_nota_cilindro[1], NORMA)

            if distancia <= ALCANCE:
                factor = gauss(distancia, 1, DESVIACION)
                factor = perturbacion_factor(factor)
                color_hsl = hsl_espiral(altura)
                pixels[i, j] = hsl2rgb(color_hsl[0], color_hsl[1] * factor, color_hsl[2] * factor)

    file_name = str(nombre) + '.jpg'
    guarda_imagen(img, path_carpeta, file_name)

    return img


# Función que sirve para crear los acordes a partir de las notas
def mergea_acorde_fijo_guarda(acorde, size, path_carpeta):

    notas = acorde.alturas
    inicio = acorde.inicio
    duracion = acorde.duracion

    imagen = Image.new('RGB', size, "black")  # create a new black image

    inicio_style = numero_punto2coma(inicio)
    duracion_style = numero_punto2coma(duracion)

    nombre_acorde = ""
    for n in range(len(notas)):
        if n+1 == len(notas):
            nombre_acorde += str(notas[n])
        else:
            nombre_acorde += str(notas[n]) + '_'
    archivo_acorde = nombre_acorde + ".jpg"
    path_acorde = os.path.join(PATH_ACORDES, archivo_acorde)

    if not os.path.exists(path_acorde) or ACORDES_CRE_RE == "C":
        if len(notas) == 1:
            path_nota = os.path.join(PATH_NOTAS, str(notas[0]) + '.jpg')
            imagen = recupera_imagen(path_nota)
            guarda_imagen(imagen, PATH_ACORDES, nombre_acorde + ".jpg")
        else:
            carpeta_acorde = os.path.join(PATH_ACORDES, nombre_acorde)
            if len(notas) != 2:
                if not os.path.exists(carpeta_acorde):
                    os.mkdir(carpeta_acorde)

            nombre_anterior = ""
            for n in range(1, len(notas)):
                if n == 1:
                    nombre_anterior = str(notas[n-1])
                else:
                    nombre_anterior = nombre_anterior + '_' + str(notas[n-1])
                nombre_actual = str(notas[n])
                nombre_anteriores = nombre_anterior + '.jpg'
                nombre_nota_actual = nombre_actual + '.jpg'

                if n == 1:
                    path_img_1 = os.path.join(PATH_NOTAS, str(notas[0]) + '.jpg')
                else:
                    path_img_1 = os.path.join(carpeta_acorde, nombre_anteriores)

                path_img_2 = os.path.join(PATH_NOTAS, nombre_nota_actual)

                if n + 1 == len(notas):
                    imagen = merge_dos_imagenes(path_img_1, path_img_2, PATH_ACORDES)
                else:
                    nombre_1 = os.path.splitext(os.path.basename(path_img_1))[0]
                    nombre_2 = os.path.splitext(os.path.basename(path_img_2))[0]
                    nombre_file = nombre_1 + '_' + nombre_2 + '.jpg'
                    file_path = os.path.join(carpeta_acorde, nombre_file)
                    if os.path.exists(file_path):
                        imagen = recupera_imagen(file_path)
                    else:
                        imagen = merge_dos_imagenes(path_img_1, path_img_2, carpeta_acorde)

        print("Acorde " + str(notas) + " creado.")
    else:
        imagen = recupera_imagen(path_acorde)
        print("Acorde " + str(notas) + " ya existe")

    file_name = str(inicio_style) + '_' + str(duracion_style) + '.jpg'
    guarda_imagen(imagen, path_carpeta, file_name)

    return imagen


# Función que sirve para difuminar los acordes y así crear la Frame_List
def difumina_guarda(frame, factor, path_carpeta, nombre_img):

    img = frame.img
    pixels = img.load()
    (x, y) = img.size
    img_new = Image.new('RGB', (x, y), "black")
    pixels_new = img_new.load()

    for i in range(img.size[0]):  # for every col:
        for j in range(img.size[1]):  # For every row
            (R, G, B) = pixels[i, j]
            if not (R, G, B) == (0, 0, 0):
                logging.log(5, "Pixel[" + str(i) + ", " + str(j) + "]")
                rgb = (R, G, B)
                logging.log(5, "RGB antes : " + str(rgb))
                rgb_new = (int(R * factor), int(G * factor), int(B * factor))
                logging.log(5, "RGB despues: " + str(rgb_new))
                pixels_new[i, j] = rgb_new

    file_name = nombre_img + '.jpg'
    guarda_imagen(img_new, path_carpeta, file_name)

    return img_new


# Utilidad para guardar las imágenes
def guarda_imagen(img, path_carpeta, file_name):
    file_path = os.path.join(path_carpeta, file_name)
    img.save(file_path, 'jpeg')


# Función que sirve para mergear una lista de imágenes
def merge_lista(lista_imagenes):
    size = lista_imagenes[0].size
    for img in lista_imagenes:
        if img.size != size:
            logging.warning("El tamaño de las imaágenes no coincide!")
            return img

    # Inicializa imagen

    imagen = Image.new('RGB', size, "black")
    pixels = imagen.load()

    lista_pixels = list()
    for img in lista_imagenes:
        pixeles = img.load()
        lista_pixels.append(pixeles)

    for n in range(0, len(lista_imagenes), 1):
        for i in range(size[0]):
            for j in range(size[1]):
                pixels[i, j] = mezcla_pixels(pixels[i, j], lista_pixels[n][i, j])

    return imagen


def merge_dos_imagenes(path_img_1, path_img_2, path_carpeta):
    img_1 = recupera_imagen(path_img_1)
    img_2 = recupera_imagen(path_img_2)
    nombre_1 = os.path.splitext(os.path.basename(path_img_1))[0]
    nombre_2 = os.path.splitext(os.path.basename(path_img_2))[0]
    size_1 = img_1.size
    size_2 = img_2.size
    pixels_1 = img_1.load()
    pixels_2 = img_2.load()

    if size_1 != size_2:
        print("El tamaño de las imágenes no coincide!")
        return img_1
    size = size_1

    # Inicializa imagen

    imagen = Image.new('RGB', size, "black")
    pixels = imagen.load()

    for i in range(size[0]):
        for j in range(size[1]):
            if not (pixels_1[i, j] == (0, 0, 0) and pixels_2[i, j] == (0, 0, 0)):
                if pixels_1[i, j] == 0:
                    pixels[i, j] = pixels_2[i, j]
                elif pixels_2[i, j] == 0:
                    pixels[i, j] = pixels_1[i, j]
                else:
                    # Color
                    rgb_1 = pixels_1[i, j]
                    rgb_2 = pixels_2[i, j]
                    hsl_1 = rgb2hsl(rgb_1[0], rgb_1[1], rgb_1[2])
                    hsl_2 = rgb2hsl(rgb_2[0], rgb_2[1], rgb_2[2])

                    # Cálculo de los parámetros ponderados
                    sat = max(hsl_1[1], hsl_2[1])
                    lum = max(hsl_1[2], hsl_2[2])

                    hue = hue_to_0_360(media_ponderada_hue(hsl_1[0], hsl_2[0], hsl_1[2], hsl_2[2], "deg"))

                    # Asignación del valor de pixel
                    pixels[i, j] = hsl2rgb(hue, sat, lum)

    file_name = nombre_1 + '_' + nombre_2 + '.jpg'
    guarda_imagen(imagen, path_carpeta, file_name)

    return imagen


def mezcla_pixels(pixel_1, pixel_2):
    if not (pixel_1 == (0, 0, 0) and pixel_2 == (0, 0, 0)):
        if pixel_1 == (0, 0, 0):
            pixel = pixel_2
        elif pixel_2 == (0, 0, 0):
            pixel = pixel_1
        else:
            # Color
            rgb_1 = pixel_1
            rgb_2 = pixel_2
            hsl_1 = rgb2hsl(rgb_1[0], rgb_1[1], rgb_1[2])
            hsl_2 = rgb2hsl(rgb_2[0], rgb_2[1], rgb_2[2])

            # Cálculo de los parámetros ponderados
            sat = max(hsl_1[1], hsl_2[1])
            lum = max(hsl_1[2], hsl_2[2])

            hue = hue_to_0_360(media_ponderada_hue(hsl_1[0], hsl_2[0], hsl_1[2], hsl_2[2], "deg"))

            # Asignación del valor de pixel
            pixel = hsl2rgb(hue, sat, lum)

    else:
        pixel = (0, 0, 0)

    return pixel


def recupera_imagen(file_path):
    img = Image.open(file_path)
    return img
