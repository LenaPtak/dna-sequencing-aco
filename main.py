from termcolor import colored
import sys
import numpy as np
import matplotlib.pyplot as plt

try:
    with open("test.txt", "r+") as f:
        spektrum = list(f.read().split('\n'))
        spektrum.pop()
        spektrum = list(map(str, spektrum))
        length_of_word = len(spektrum[0])
        number_of_words = len(spektrum)
except:
    print(colored("Error while reading file. Check the name of file or it's content.", "red"))
    sys.exit()

def check_weight_between(x, y):
    weight = 0 #O ij
    for i in range(length_of_word-1, -1, -1):
        if y[:length_of_word-i] == x[i:]:
            # print(y[:length_of_word-i], x[i:])
            weight = length_of_word - i

    return length_of_word - weight



# # Tworzenie grafu
graph = [[0 for j in range(number_of_words)] for i in range(number_of_words)]
d = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0}

spektrum.sort()
for i in spektrum:
    print(i)

for i in range(number_of_words):
    for j in range(number_of_words):
        x = spektrum[i]
        y = spektrum[j]
        graph[i][j] = check_weight_between(x, y)
        
        d[graph[i][j]] += 1


print(graph)

# # Czytaj dane
# def wczytaj_dane(nazwaPliku):
#     plik = open(nazwaPliku, "r")
#     liczbaPunktow = int(plik.readline())
#     macierz = []  # [[1,421,423], [2, 12, 982], ...]
#     for i in plik:
#         macierz.append(list(map(int, i.split())))

#     return macierz, liczbaPunktow


# # Otwarcie pliku
# nazwaPliku = 'berlin52.txt'
# wspolrzedne, liczbaPunktow = wczytaj_dane(nazwaPliku)
# wspolrzedne = np.array(wspolrzedne)  # Z biblioteki numpy. Z tablicy [1, 2, 3] robi [1 2 3].
# wspolrzedne = wspolrzedne[:, 1:]  # [[51 30 40] ...] --> [[30 40] ...]
# pokaz_wspolrzedne = np.vstack(
#     [wspolrzedne, wspolrzedne[0]])  # dodaje wierzcholek startowy na koniec --> .append([37, 89])

# # wywołanie klasy ACO:
# aco = ACO(liczba_miast=liczbaPunktow, wspolrzedne=wspolrzedne.copy(), nazwaPliku=nazwaPliku)
# ostateczna_sciezka, ostateczny_wynik, naj_droga = aco.run()

# # Wykres
# f1 = plt.figure(1)
# plt.title(f'Współrzędne miast {nazwaPliku}')
# x, y = wspolrzedne[:, 0], wspolrzedne[:, 1]
# plt.plot(x, y, '.', color='black')
# plt.grid(True)
# plt.xlim(0, max(x) * 1.1)
# plt.ylim(0, max(y) * 1.1)
# plt.xlabel('x', fontweight='bold')
# plt.ylabel('y', fontweight='bold')

# plt.show()