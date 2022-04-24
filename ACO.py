import time
import math
import numpy as np
import random

class ACO(object):
    
    def __init__(self, number_of_verticles, coordinates, file_name):
        # Nazwa pliku
        self.file_name = file_name 
        # Liczba wierzchołków
        self.number_of_verticles = number_of_verticles  
        # Współrzędne miast
        self.coordinates = coordinates  
        # Macierz feromonów wypełniona jedynkami
        self.pheromone = np.ones([number_of_verticles, number_of_verticles])  
        # Kolonia mrówek, czyli każda mrówka i jej skończona droga
        self.ant_colony = [[0 for _ in range(number_of_verticles)] for _ in range(self.m)]
                               
        # Liczba mrówek
        self.number_of_ants = 30  
        # Współczynnik ważności feromonów
        self.alpha = 1 
        # Ważny czynnik funkcji heurystycznej
        self.beta = 5  
        # Lotny czynnik feromonów
        self.rho = 0.1  
        # Stały współczynnik
        self.q = 1  
        self.iter = 1
        # Liczba iteracji
        self.liczba_iteracji = 1000  
        # Oblicz macierz sąsiedztwa (odległości między miastami)
        self.macierz_sasiedztwa = self.oblicz_macierz_sasiedztwa(number_of_verticles, self.coordinates)  
        # Funkcja heurystyczna (do wzoru na prawdopodobieństwo)                                              
        self.eta = 10. / self.macierz_sasiedztwa  
        # Tablica dystansów zrobionych przez mrówki.
        self.paths = None  
        self.iter_x = []
        self.iter_y = []

    # Ostateczny krok wybrania wierzchołka
    def random(self, probability_of_next_verticle):
        x = np.random.rand()
        # Enumerate umożliwia  iterację po obiektach takich jak lista
        # przy jednoczesnej informacji, którą iterację wykonujemy.
        for index, t in enumerate(probability_of_next_verticle):
            x -= t
            if x <= 0: break
        # zwraca indeks następnego miasta do odwiedzenia.
        return index  

    # Stwórz kolonię mrówek
    def ant_run(self, number_of_verticles):
        for current_ant_index in range(self.number_of_ants):  
            # Losuje liczbę w zakresie liczbie miast.
            start_verticle = random.randint(number_of_verticles - 1)  
            # Wierzchołek startowy.
            self.ant_colony[current_ant_index][0] = start_verticle  
            # Lista wierzchołków do odwiedzenia
            not_visited_verticles = list([v for v in range(number_of_verticles) if v != start_verticle]) 
            current_verticle = start_verticle
            helper_index = 1
            while len(not_visited_verticles) != 0:
                # Tablica zawierająca prawodopodobieństwa przejść do kolejno nieodwiedzonych wierzchołków
                probability_of_next_verticle = []
                # Oblicz prawdopodobieństwo przejścia między wierzchołkami przez feromon
                for possible_verticle in not_visited_verticles:
                    # nasz wzór na prawdopodobieństwo
                    probability_of_next_verticle.append(
                        self.pheromone[current_verticle][possible_verticle] ** 
                        self.alpha * 
                        self.Eta[current_verticle][possible_verticle] ** 
                        self.beta
                    )  
                # Suma pradopodobieństw w powyższej listy
                probability_list_sum = sum(probability_of_next_verticle)
                # Bierzemy prawdopodobienstwo jednego wierzchołka  i dzielimy przez sumę prawdopodobieństw wszystkich wierzchołków
                probability_of_next_verticle = [v / probability_list_sum for v in probability_of_next_verticle]
                # Ruletka wybiera miasto
                next_verticle_index = self.random(probability_of_next_verticle)

                current_verticle = not_visited_verticles[next_verticle_index]
                # W macierzy "ant_colony[current_ant_index][helper_index]"
                # Współrzędna current_ant_index to numer mrówki, 
                # a helper_index to nr wierzcholka, do ktorego przeszła mrówka.
                # Tworzymy więc dla każdej mrówkę jej ścieżkę.
                self.ant_colony[current_ant_index][helper_index] = current_verticle
                
                not_visited_verticles.remove(current_verticle)
                helper_index += 1

    # Oblicz odległość między różnymi miastami
    def oblicz_macierz_sasiedztwa(self, number_of_verticles, coordinates):  # liczba miast, tablica ze współrzędnymi.
        macierz_sasiedztwa = np.zeros(
            (number_of_verticles, number_of_verticles))  # Tworzy macierz liczba miast x liczba miast wypełnioną zerami.
        for i in range(number_of_verticles):
            for j in range(number_of_verticles):
                if i == j:
                    macierz_sasiedztwa[i][j] = np.inf
                    # zmiennoprzecinkowa reprezentacja (dodatniej) nieskończoności.
                    continue
                a = coordinates[i]
                b = coordinates[j]
                tmp = np.sqrt(sum([(x[0] - x[1]) ** 2 for x in zip(a, b)]))
                macierz_sasiedztwa[i][j] = tmp
        # print("\nMACIERZ SĄSIEDZTWA: \n", macierz_sasiedztwa)
        return macierz_sasiedztwa  # Zwraca macierz sąsiedztwa.

    # Oblicz długość ścieżki
    def oblicz_dlugosc_paths(self, droga, macierz_sasiedztwa):
        a = droga[0]
        b = droga[-1]
        wyn = macierz_sasiedztwa[a][b]  # Droga mrówki przy domykaniu ścieżki.
        for i in range(len(droga) - 1):
            a = droga[i]
            b = droga[i + 1]
            wyn += macierz_sasiedztwa[a][b]
        return wyn  # Zwraca dystans pokonany przez mrówkę.

    # Oblicz długość grupy
    def oblicz_paths(self, paths):  # paths to teraz kolonia mrówek.
        wyn = []
        for one in paths:  # dla każdej ścieżki mrówki:
            dlugosc = self.oblicz_dlugosc_paths(one, self.macierz_sasiedztwa)
            wyn.append(dlugosc)
        return wyn  # Tablica dystansów zrobionych przez mrówki.

    # Zaktualizuj feromon
    def aktualizuj_pheromone(self):
        delta_pheromone = np.zeros([self.number_of_verticles, self.number_of_verticles])  # Macierz feromonów
        paths = self.oblicz_paths(self.ant_colony)  # Tablica dystansów zrobionych przez mrówki.
        for i in range(self.m):  # m - liczba mrówek
            for j in range(self.number_of_verticles - 1):
                a = self.ant_colony[i][j]
                b = self.ant_colony[i][j + 1]
                delta_pheromone[a][b] = delta_pheromone[a][b] + self.q / paths[i]  # Zostawianie feromonów.
            a = self.ant_colony[i][0]
            b = self.ant_colony[i][-1]
            delta_pheromone[a][b] = delta_pheromone[a][b] + self.q / paths[
                i]  # Domknięcie ścieżki z zostawianiem feromonu.
        self.pheromone = (
                                    1 - self.rho) * self.pheromone + delta_pheromone  # Na początku paruje i dodaje te nowe zostawione pheromone.
        # Wszystkie ścieżki parują tzn wszystkie wartości w tablicy feromonów mnożymy razy (1 - self.rho), czyli 0,9. I dodajemy wartość feromonow.

    def aco(self):
        najlepszy_dystans = math.inf  # Wartość najlepszej ścieżki ustawiamy na plus nieskończoność.
        najlepsza_sciezka = None  # Najlepsza ścieżka.
        for iteracja in range(self.liczba_iteracji):
            start_verticle = time.time()
            # Wygeneruj nową kolonię
            self.ant_run(self.number_of_verticles)  # out>>self.ant_colony, puszczamy mrówki i zapisujemy ich ścieżki.
            self.paths = self.oblicz_paths(self.ant_colony)  # Tablica dystansów.
            # Weź optymalny roztwór kolonii mrówek
            tmp_dlugosc = min(self.paths)  # Najmniejszy dystans.
            tmp_sciezka = self.ant_colony[self.paths.index(tmp_dlugosc)]  # I ścieżka miast od niego.

            # Zaktualizuj optymalne rozwiązanie
            if tmp_dlugosc < najlepszy_dystans:
                najlepszy_dystans = tmp_dlugosc
                najlepsza_sciezka = tmp_sciezka

            # Wizualizuj początkową ścieżkę  (wykresy)
            if iteracja == 0:
                init_show = self.coordinates[tmp_sciezka]
                init_show = np.vstack([init_show, init_show[0]])  # dodaje pierwszy wierzcholek na koniec paths
                x, y = init_show[:, 0], init_show[:, 1]
                self.plotTSP([(x[i], y[i]) for i in range(len(x))], 2, najlepszy_dystans)

            if iteracja == int(self.liczba_iteracji / 10):
                init_show = self.coordinates[tmp_sciezka]
                init_show = np.vstack([init_show, init_show[0]])  # dodaje pierwszy wierzcholek na koniec paths
                x, y = init_show[:, 0], init_show[:, 1]
                self.plotTSP([(x[i], y[i]) for i in range(len(x))], int(self.liczba_iteracji / 2), najlepszy_dystans)

            # Zaktualizuj feromon
            self.aktualizuj_pheromone()

            # Zapisz wynik
            self.iter_x.append(iteracja)
            self.iter_y.append(najlepszy_dystans)

            end = time.time()
            print("Iteracja: ", iteracja, "     ", int(iteracja / self.liczba_iteracji * 100), "%   ",
                  "Czas do końca: ", self.czasDoKonca(iteracja, start_verticle - end))

        init_show = self.coordinates[najlepsza_sciezka]
        init_show = np.vstack([init_show, init_show[0]])  # dodaje pierwszy wierzcholek na koniec paths
        x, y = init_show[:, 0], init_show[:, 1]
        self.plotTSP([(x[i], y[i]) for i in range(len(x))], 3, najlepszy_dystans)

        print(f"Najlepszy wynik {self.file_name} to: {najlepszy_dystans}")

        print("Kolejność wierzchołków:")
        print(*najlepsza_sciezka, najlepsza_sciezka[0])

        print("\nWspółrzędne x i y:")
        print(*x)
        print(*y)

        return najlepszy_dystans, najlepsza_sciezka

    # Główna funkcja.
    def run(self):
        NAJ_dystans, NAJ_sciezka = self.aco()
        return self.coordinates[NAJ_sciezka], NAJ_dystans, NAJ_sciezka