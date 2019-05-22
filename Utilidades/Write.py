import os


def escribe_notas_por_voces(obra, carpeta_guardado):
    lista_notas = obra.notas
    nombre = obra.nombre

    voces = list()
    for nota in lista_notas:
        if nota.voz not in voces:
            voces.append(nota.voz)

    for voz in voces:
        path_file = os.path.join(carpeta_guardado, 'Notas_' + nombre + '_voz_' + str(voz) + '.txt')
        file = open(path_file, 'w+')
        for nota in lista_notas:
            if nota.voz == voz:
                file.write(str(nota))
                file.write('\n')
