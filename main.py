from termcolor import colored
import sys
import numpy as np
import matplotlib.pyplot as plt


# Proby otworzenia pliku
try:
    with open("test.txt", "r+") as f:
        spektrum = list(f.read().split('\n'))
        spektrum.pop()
        spektrum = list(map(str, spektrum))
        length_of_word = len(spektrum[0])
        number_of_words = len(spektrum)
        # Tworzenie grafu (macierzy) wypełnionej zerami
        graph = [[0 for j in range(number_of_words)] for i in range(number_of_words)]
except:
    print(colored("Error while reading file. Check the name of file or it's content.", "red"))
    sys.exit()


# Cij -> Funkcja sprawdzajaca wagi pomiedzy podanymi wierzcholkami (slowami)
def check_weight_between(Si, Sj):
    
    if Si == Sj: return -1  # Zakłada się, że Si != Sj
    """
    Powyższy warunek powoduje, że ZAWSZE:
         0 <= Oij <= length_of_word -1
         1 <= Cij <= length_of_word
    """   
    Oij = 0 # oznacza liczbę końcowych symboli (długość sufiksu) słowa Si
    
    for index in range(length_of_word-1, -1, -1):
        if Sj[:length_of_word-index] == Si[index:]:
            Oij = length_of_word - index
    
    Cij = length_of_word - Oij
    return Cij


def create_graph():
    # Tworzymy słownik z kluczami (wagami krawędzi) i wartościami (liczbą wystąpień takiej wagi krawędzi)
    list_of_keys = list(map(lambda num: num, range(-1, length_of_word+1)))
    dictionary = {}
    for key in list_of_keys:
        dictionary[key] = 0
    
    for Si in range(number_of_words):
        for Sj in range(number_of_words):
            x = spektrum[Si]
            y = spektrum[Sj]
            # Dodajemy wagę krawędzi między wierzchołami do grafu
            graph[Si][Sj] = check_weight_between(x, y)
            # Dodajemy wagę krawędzi do słownika z ich częstotliwością występowania
            dictionary[check_weight_between(x, y)] += 1

create_graph()

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