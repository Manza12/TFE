from Espiral.Distancias import posicion_cilindro

NOTA_CENTRO = 60


def diccionario_posicion_cilindro(size):
    print("Creando diccionario de tamaño " + str(size))
    diccionario = {}

    numero_pixeles = 0
    franja_porcentaje = 0
    franja = 1
    total = size[0] * size[1]
    for i in range(size[0]):
        for j in range(size[1]):
            posicion = posicion_cilindro(i, j)

            diccionario[i, j] = posicion

            numero_pixeles += 1
            porcentaje = numero_pixeles * 100 / total
            if porcentaje >= franja_porcentaje:
                print(round(porcentaje), '%')
                franja_porcentaje += franja

    return diccionario
