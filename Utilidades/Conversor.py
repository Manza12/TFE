def numero_punto2coma(num):
    num_str = str(num)
    partes = num_str.split('.')

    if len(partes) == 2:
        resultado = partes[0] + ',' + partes[1]
    elif len(partes) == 1:
        return num
    else:
        print("Esto no es un número")
        return num

    return resultado


def numero_coma2punto(num):
    num_str = str(num)
    partes = num_str.split(',')

    if len(partes) == 2:
        resultado = partes[0] + '.' + partes[1]
    elif len(partes) == 1:
        return num
    else:
        print("Esto no es un número")
        return num

    return resultado


def devuelve_inicio_duracion(file_name):
    nombre_archivo = file_name.split('.')
    nombre = nombre_archivo[0]
    ini_dur = nombre.split('_')
    ini = ini_dur[0]
    dur = ini_dur[1]
    inicio = float(numero_coma2punto(ini))
    duracion = float(numero_coma2punto(dur))

    return [inicio, duracion]


def devuelve_posicion_frame(file_name):
    nombre_archivo = file_name.split('.')
    nombre = nombre_archivo[0]
    frame_num = nombre.split('_')
    pos = frame_num[0]
    posicion = int(pos)

    return posicion


def recupera_posicion(file_name):
    partes = file_name.split('.')
    pos = partes[0]
    posicion = int(pos)

    return posicion
