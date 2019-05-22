def note2number(step, octave, alter):

    altura = 3 + int(octave)*12

    if step == "C":
        altura += 0
    elif step == "D":
        altura += 2
    elif step == "E":
        altura += 4
    elif step == "F":
        altura += 5
    elif step == "G":
        altura += 7
    elif step == "A":
        altura += 9
    elif step == "B":
        altura += 11

    altura += int(alter)

    return altura


def numero2nota(n):

    nota = ""

    resto = (n - 4) % 12

    if resto == 0:
        nota = "Do"
    elif resto == 1:
        nota = "Do#"
    elif resto == 2:
        nota = "Re"
    elif resto == 3:
        nota = "Mib"
    elif resto == 4:
        nota = "Mi"
    elif resto == 5:
        nota = "Fa"
    elif resto == 6:
        nota = "Fa#"
    elif resto == 7:
        nota = "Sol"
    elif resto == 8:
        nota = "Lab"
    elif resto == 9:
        nota = "La"
    elif resto == 10:
        nota = "Sib"
    elif resto == 11:
        nota = "Si"

    octava = int((n-resto)/12)
    nota += str(octava)

    return nota
