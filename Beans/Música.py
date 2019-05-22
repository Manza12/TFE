from Utilidades.Transformaciones import *


LOG_LEVEL = "info"


class Obra:

    def __init__(self, nombre, mindiv, notas):
        self.nombre = nombre
        self.mindiv = mindiv
        self.notas = notas

    def __str__(self):
        lista_notas = "[ "
        for i in range(len(self.notas)):
            if i != 0:
                lista_notas += ", "
            lista_notas += str(self.notas[i])
        lista_notas += " ]"

        frase = ""
        if LOG_LEVEL == "debug":
            frase = "Tipo : Obra, nombre : "+self.nombre+", mindiv : "+str(self.mindiv)+" notas : "+lista_notas
        elif LOG_LEVEL == "info":
            frase = "Mindiv : "+str(self.mindiv)+", Obra : "+lista_notas
        return frase


class Nota:

    def __init__(self, altura, inicio, duracion, voz, chord):
        self.altura = altura
        self.inicio = inicio
        self.duracion = duracion
        self.voz = voz
        self.chord = chord

        self.nombre = numero2nota(altura)

    def __str__(self):
        frase = ""
        if LOG_LEVEL == "debug":
            frase = "Tipo : Nota, nombre : " + self.nombre+", altura :" + str(self.altura) + ", inicio : " + \
                    str(self.inicio) + " duracion : " + str(self.duracion) + " voz : " + str(self.voz)
        if LOG_LEVEL == "info":
            frase = "[ "+str(self.altura) \
                    + "; "+str(self.inicio) + ", " + str(self.duracion) + ", " + str(self.voz) + " ]"
        return frase

    def __repr__(self):
        return self.__str__()


class Acorde:

    def __init__(self, alturas, intensidades, inicio, duracion):
        self.alturas = alturas
        self.intensidades = intensidades
        self.inicio = inicio
        self.duracion = duracion

    def __str__(self):
        frase = ""
        if LOG_LEVEL == "debug":
            frase = "Tipo : Acorde, alturas :"+str(self.alturas) + "intensidades : " + str(self.intensidades) \
                    + ", inicio : " + str(self.inicio) + " duracion : " + str(self.duracion)
        if LOG_LEVEL == "info":
            frase = "[ "+str(self.alturas) + "; "+str(self.intensidades) + "; "+str(self.inicio) + ", " + str(self.duracion)+" ]"
        return frase

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.__dict__ == other.__dict__