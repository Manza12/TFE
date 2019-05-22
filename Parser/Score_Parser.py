from xml.dom import minidom
from Beans.Música import *
import logging


def score_parser(score_path):

    score = minidom.parse(score_path)
    logging.basicConfig(filename='TestParser.log', filemode='w',
                        format='%(asctime)s.%(msecs)03d %(levelname)s {%(module)s} [%(funcName)s] %(message)s',
                        datefmt='%Y-%m-%d,%H:%M:%S',
                        level=logging.INFO)

    notas = score.getElementsByTagName('note')
    n = len(notas)
    logging.info("Hay " + str(n) + " notas.")
    lista_notas_fake = list()

    for i in range(0, n, 1):
        nota_xml = notas[i]
        logging.info("Recuperando la Nota " + str(i + 1) + ".")
        logging.log(5, nota_xml.toxml())

        pitch = nota_xml.getElementsByTagName('pitch')
        logging.debug(str(len(pitch)))

        voice_xml = nota_xml.getElementsByTagName('voice')
        if len(voice_xml) != 0:
            voice = int(voice_xml[0].childNodes[0].toxml())

        altura = 0
        chord = False

        if not len(pitch) == 0:

            # Miramos a ver si es un acorde

            chord_xml = nota_xml.getElementsByTagName('chord')

            if len(chord_xml) != 0:
                chord = True

            # Recuperamos la altura

            pitch = pitch[0]
            logging.info("No es un silencio, buscamos su altura.")
            logging.log(5, pitch.toxml())

            step_element = pitch.getElementsByTagName('step')
            step = step_element[0].childNodes[0].toxml()

            octave_element = pitch.getElementsByTagName('octave')
            octave = octave_element[0].childNodes[0].toxml()

            logging.info("La NOTA es " + step + octave)

            alter_element = pitch.getElementsByTagName('alter')
            if len(alter_element) != 0:
                alter = alter_element[0].childNodes[0].toxml()
                logging.info("La NOTA esta alterada en " + alter)
            else:
                alter = 0

            altura = note2number(step, octave, alter)

        else:
            logging.info("Es un silencio.")

        logging.info("Buscamos su duracion.")

        duracion_xml = nota_xml.getElementsByTagName('duration')
        duracion = int(duracion_xml[0].childNodes[0].toxml()) / 256

        nota_fake = Nota(altura, 0, duracion, voice, chord)

        lista_notas_fake.append(nota_fake)

    lista_notas = asigna_inicio(lista_notas_fake)

    logging.info("La lista de notas es " + str(lista_notas))
    logging.info(detecta_ambito(lista_notas))

    return lista_notas


def asigna_inicio(lista_notas_fake):

    lista_notas = list()

    voces = list()

    for nota_fake in lista_notas_fake:
        if nota_fake.voz not in voces:
            voces.append(nota_fake.voz)

    for i in voces:
        t = 0
        for n in range(0, len(lista_notas_fake), 1):
            nota_fake = lista_notas_fake[n]
            if nota_fake.voz == i:
                if nota_fake.chord:
                    nota_ant = lista_notas_fake[n - 1]
                    t -= nota_ant.duracion

                nota = Nota(nota_fake.altura, t, nota_fake.duracion, nota_fake.voz, nota_fake.chord)
                t += nota_fake.duracion
                lista_notas.append(nota)

    return lista_notas


def detecta_ambito(lista_notas):

    lista_alturas = list()

    for nota in lista_notas:
        altura = nota.altura
        if altura != 0:
            lista_alturas.append(altura)

    minimo = min(lista_alturas)
    maximo = max(lista_alturas)

    return "La NOTA mas grave es " + str(minimo) + " y la NOTA mas aguda es " + str(maximo)
