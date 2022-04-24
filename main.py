from termcolor import colored
import sys
import numpy as np
import matplotlib.pyplot as plt
from ACO import ACO

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

