import random


POPULACJA = 1000
ITERACJE = 10
wyniki = [(-5, -150), (4, 77), (-1, -30), (-2, 0), (-1, 10), (1 / 2, 131 / 8), (1, 18), (2, 25), (3, 32), (4, 75),
          (5, 130)]


def bin_to_int(bin_string):
    a = (int(bin_string[1:5], 2))
    if bin_string[0] == '1':
        a *= -1
    b = int(bin_string[6:10], 2)
    if bin_string[5] == '1':
        b *= -1
    c = int(bin_string[11:15], 2)
    if bin_string[10] == '1':
        c *= -1
    d = int(bin_string[16:], 2)
    if bin_string[15] == '1':
        d *= -1
    return a, b, c, d


def int_to_bin(data):
    a, b, c, d = data
    a = bin(a).replace('-0b', '1').replace('0b', '0')
    b = bin(b).replace('-0b', '1').replace('0b', '0')
    c = bin(c).replace('-0b', '1').replace('0b', '0')
    d = bin(d).replace('-0b', '1').replace('0b', '0')
    bin_string = ""
    for x in [a, b, c, d]:
        if len(x) == 2:
            x = f"{x[0]}000{x[1]}"
        elif len(x) == 3:
            x = f"{x[0]}00{x[1:]}"
        elif len(x) == 4:
            x = f"{x[0]}0{x[1:]}"
        bin_string += x
    return bin_string


def wielomian(a, b, c, d, x):
    return a * x ** 3 + b * x ** 2 + c * x + d


def funkcja_oceny(osobnik):
    a, b, c, d = osobnik
    suma = 0
    for x, y in wyniki:
        suma += (wielomian(a, b, c, d, x) - y) ** 2
    return suma


def generuj_osobnika():
    a = random.randint(-15, 15)
    b = random.randint(-15, 15)
    c = random.randint(-15, 15)
    d = random.randint(-15, 15)
    return a, b, c, d


def krzyzuj(osobnik1, osobnik2):
    if random.random() < 0.5:
        return osobnik1
    osobnik1, osobnik2 = int_to_bin(osobnik1), int_to_bin(osobnik2)
    index = random.randint(1, len(osobnik1)-1)
    osobnik = f"{osobnik1[:index]}{osobnik2[index:]}"
    # print("k", end="")
    return bin_to_int(osobnik)



def mutuj(osobnik):
    a, b, c, d = osobnik
    if random.random() > 0.1:
        return a, b, c, d
    x = random.randint(0, 3)
    if x == 0:
        a = random.randint(-15, 15)
    elif x == 1:
        b = random.randint(-15, 15)
    elif x == 2:
        c = random.randint(-15, 15)
    else:
        d = random.randint(-15, 15)
    # print("M", end="")
    return a, b, c, d


def main():
    populacja = []
    for _ in range(POPULACJA):
        populacja.append(generuj_osobnika())

    for _ in range(ITERACJE):
        # selekcja
        populacja.sort(key=funkcja_oceny)

        populacja = populacja[:int(POPULACJA / 2)]
        ruletka = [funkcja_oceny(o1) / sum([funkcja_oceny(oM) for oM in populacja]) for o1 in populacja]
        print(ruletka)
        # krzyżowanie
        for i in range(0, len(populacja), 2):
            r1, r2 = random.random(), random.random()
            h1, h2 = 0, 0

            j = 0
            while r1 > 0:
                r1 -= ruletka[j]
                h1 = j
                j += 1

            j = 0
            while r2 > 0:
                r2 -= ruletka[j]
                h2 = j
                j += 1
            populacja.append(krzyzuj(populacja[h1], populacja[h2]))

        # mutacja
        for i in range(len(populacja)):
            populacja[i] = mutuj(populacja[i])

    # wydruk najlepszego wyniku
    a, b, c, d = populacja[0]
    for x, y in wyniki:
        print(f"{x}: algorytm= {wielomian(a, b, c, d, x)} podany wynik= {y}")

    print()
    print(f"{populacja[0][0]}*x^3 + {populacja[0][1]}*x^2 + {populacja[0][2]}*x + {populacja[0][3]}")


if __name__ == "__main__":
    main()
