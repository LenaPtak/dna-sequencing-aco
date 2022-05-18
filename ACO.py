from msilib import sequence
from termcolor import colored
import numpy as np
import datetime
import random
import time
import math
import sys

class ACO(object):
    
    def __init__(self, file_name):
        # Próby otworzenia pliku
        try:
            with open(file_name, "r+") as f:
                spektrum = list(f.read().split('\n'))
                spektrum.pop()
                spektrum = list(map(str, spektrum))
        except:
            print(colored("Error while reading file. Check the name of file or it's content.", "red"))
            sys.exit()
        
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
        # Liczba iteracji
        self.liczba_iteracji = 10

        # Nazwa pliku
        self.file_name = file_name
        # Spektrum - cały zbiór podanych słów 
        self.spektrum = spektrum
        # Długość sekwencji
        self.length_of_sequence = 209
        # Długość pojedynczego słowa w spektrum
        self.length_of_word = len(spektrum[0])
        # Liczba wszystkich slów w spektrum
        self.number_of_words = len(spektrum)
        # Liczba wierzchołków
        self.number_of_verticles = self.number_of_words  
        # Macierz feromonów wypełniona jedynkami
        self.pheromone = np.ones([self.number_of_verticles, self.number_of_verticles])  
        # Kolonia mrówek, czyli każda mrówka i jej skończona droga
        self.ant_colony = [[0 for _ in range(self.number_of_verticles)] for _ in range(self.number_of_ants)]
        # Oblicz macierz sąsiedztwa (odległości między miastami)
        self.graph = self.calculate_weights_between_verticles()  
        # Funkcja heurystyczna (do wzoru na prawdopodobieństwo)   
        # Ilość śladu feromonowego                                           
        self.eta = 10. / self.graph     

        # Tablica dystansów zrobionych przez mrówki.
        self.paths = None  
        self.iter_x = []
        self.iter_y = []

        self.budget = [self.length_of_sequence - self.length_of_word for _ in range(self.number_of_ants)]


    # Cij -> Funkcja sprawdzajaca wagi pomiedzy podanymi wierzcholkami (slowami)
    def check_weight_between(self, Si, Sj):
        if Si == Sj: return -1  # Zakłada się, że Si != Sj
        """
        Powyższy warunek powoduje, że ZAWSZE:
            0 <= Oij <= length_of_word -1
            1 <= Cij <= length_of_word
        """   
        
        Oij = 0 # oznacza liczbę końcowych symboli (długość sufiksu) słowa Si
    
        for index in range(self.length_of_word-1, -1, -1):
            if Sj[:self.length_of_word-index] == Si[index:]:
                Oij = self.length_of_word - index
        
        Cij = self.length_of_word - Oij
        return Cij


    # Tworzenie macierzy sąsiedztwa
    def calculate_weights_between_verticles(self): 
        # graph = [[0 for j in range(self.number_of_words)] for i in range(self.number_of_words)]
        graph = np.zeros((self.number_of_words, self.number_of_words))
        for Si in range(self.number_of_words):
            for Sj in range(self.number_of_words):
                x = self.spektrum[Si]
                y = self.spektrum[Sj]
                # Dodajemy wagę krawędzi między wierzchołami do grafu
                graph[Si][Sj] = self.check_weight_between(x, y)
        
        return graph


    # Ostateczny krok wybrania wierzchołka
    def random(self, probability_of_next_verticle):
        x = np.random.rand()
        # Enumerate umożliwia  iterację po obiektach takich jak lista
        # przy jednoczesnej informacji, którą iterację wykonujemy.
        # TODO: sprawdzić czy lepsze wyniki są z posortowaną tablicą czy nie
        for index, t in enumerate(probability_of_next_verticle): 
            x -= t
            if x <= 0: break
        # zwraca indeks następnego miasta do odwiedzenia.
        return index  

    # Stwórz kolonię mrówek - kolejne słowa ze spektrum przypisane są liczbom od <0 do len(spektrum)>
    def ant_run(self):
        # TODO: uzględnić przerwanie gdy skończy się budżet
        for current_ant_index in range(self.number_of_ants):  
            # Losuje liczbę w zakresie liczby miast
            start_verticle = random.randint(0, self.number_of_verticles - 1)  
            # Zaczynamy zapisywanie ścieżki dla mrówki inicjując pierwszy wierzchołek
            self.ant_colony[current_ant_index][0] = start_verticle  
            # Lista wierzchołków do odwiedzenia
            not_visited_verticles = list(verticle for verticle in range(self.number_of_verticles) if verticle != start_verticle) 
            # Ustawiamy aktualny wierzchołek 
            current_verticle = start_verticle
            # Zmienna pomocnicza
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
                        self.eta[current_verticle][possible_verticle] ** 
                        self.beta
                    )  
                # Suma pradopodobieństw w powyższej listy
                probability_list_sum = sum(probability_of_next_verticle)
                # Bierzemy prawdopodobienstwo jednego wierzchołka  i dzielimy przez sumę prawdopodobieństw wszystkich wierzchołków
                probability_of_next_verticle = [v / probability_list_sum for v in probability_of_next_verticle]
                
                #---------------------BUDGET PART START---------------------------
                # Ruletka wybiera miasto
                possible_next_verticle = not_visited_verticles[self.random(probability_of_next_verticle)]
                # Nie chcemy przejść do samego siebie
                if self.graph[current_verticle][possible_next_verticle] == 0:
                    not_visited_verticles.remove([possible_next_verticle])
                    continue
                # Jeśli budżet do przejścia między tymi dwoma jest za mały
                elif self.budget[current_ant_index] < self.graph[current_verticle][possible_next_verticle]:
                    not_visited_verticles.remove(possible_next_verticle)
                    continue

                # Jeżeli wybieramy się do nowego wierzchołka i mamy na to budżet
                self.budget[current_ant_index] -= self.graph[current_verticle][possible_next_verticle]
                # Przechodzimy, więc to nasz nowy obecny wierzchołek
                current_verticle = possible_next_verticle
                # Tworzymy więc dla każdej mrówkę jej ścieżkę.
                self.ant_colony[current_ant_index][helper_index] = current_verticle
                # Usuwamy wierzchołek z listy nieodwiedzonych 
                not_visited_verticles.remove(current_verticle)
                helper_index += 1

                #---------------------BUDGET PART END---------------------------

                #---------------------DZIAŁAJĄCA STARA CZĘŚĆ START---------------------------
                # # Ruletka wybiera miasto
                # next_verticle_index = self.random(probability_of_next_verticle)
                # current_verticle = not_visited_verticles[next_verticle_index]
                # # Tworzymy więc dla każdej mrówkę jej ścieżkę.
                # self.ant_colony[current_ant_index][helper_index] = current_verticle
                # not_visited_verticles.remove(current_verticle)
                # helper_index += 1
                #---------------------DZIAŁAJĄCA STARA CZĘŚĆ END---------------------------

    
    # Oblicz długość ścieżki
    def calculate_one_path_cost(self, path):
        cost = 0
        for index in range(len(path) - 1):
            a = path[index]
            b = path[index + 1]
            cost += self.graph[a][b]
        # Zwraca dystans pokonany przez mrówkę.
        return cost  

    # Oblicz koszt ścieżek
    def calculate_cost_of_paths(self): 
        list_of_path_costs = []
        # Dla każdej ścieżki mrówki:
        for path in self.ant_colony:  
            cost = self.calculate_one_path_cost(path)
            list_of_path_costs.append(cost)
        # Tablica dystansów zrobionych przez mrówki.
        return list_of_path_costs  

    # Zaktualizuj feromon
    def update_pheromone(self):
        # Macierz feromonów
        delta_pheromone = np.zeros([self.number_of_verticles, self.number_of_verticles]) 
        # Tablica kosztów ścieżek przebytych przez mrówki.
        # TODO: sprawdzić czy poniższa linia nie jest nadmiarowa - raczej nie trzeba liczyć jeszcze raz
        paths = self.calculate_cost_of_paths()  
        for i in range(self.number_of_ants):  # m - liczba mrówek
            for j in range(self.number_of_verticles - 1):
                a = self.ant_colony[i][j]
                b = self.ant_colony[i][j + 1]
                # Zostawianie feromonów.
                delta_pheromone[a][b] = delta_pheromone[a][b] + self.q / paths[i]  

            # TODO: prawdopodobnie trzeba usunąć domknięcie ścieżki
            a = self.ant_colony[i][0]
            b = self.ant_colony[i][-1]
            # Domknięcie ścieżki z zostawianiem feromonu.
            delta_pheromone[a][b] = delta_pheromone[a][b] + self.q / paths[i]  
                                              
        # Na początku paruje i dodaje te nowe zostawione pheromone.
        # Wszystkie ścieżki parują tzn wszystkie wartości w tablicy feromonów mnożymy razy (1 - self.rho), czyli 0,9. I dodajemy wartość feromonow.
        self.pheromone = (1 - self.rho) * self.pheromone + delta_pheromone
        
    def time_to_finish(self, iteracja, czas):
        sekundyDoKonca = czas * (iteracja - self.liczba_iteracji)
        return str(datetime.timedelta(seconds=sekundyDoKonca))

    def run(self):
        # Wartość najtańszej ścieżki ustawiamy na plus nieskończoność.
        cheapest_cost = math.inf  
        # Najtańsza ścieżka.
        cheapest_path = None  

        for iteracja in range(self.liczba_iteracji):
            start_verticle = time.time()
            # Tworzymy nową grupę składającą się z self.number_of_ants mrówek
            self.ant_run()  
            # Tablica kosztów przebytych przez powyższe mrówki ścieżek
            self.paths = self.calculate_cost_of_paths()  
            # Najmniejszy koszt z aktualnej grupy mrówek
            current_cheapest_cost = min(self.paths)  
            # Najtańsza ścieżka z aktualnej grupy mrówek - lista wierzchołków
            current_cheapest_path = self.ant_colony[self.paths.index(current_cheapest_cost)]  
            # Zaktualizuj optymalne rozwiązanie
            if current_cheapest_cost < cheapest_cost:
                cheapest_cost = current_cheapest_cost
                cheapest_path = current_cheapest_path

            # Zaktualizuj feromon
            self.update_pheromone()

            end = time.time()
            print("Iteracja: ", iteracja, "     " if len(str(iteracja))==1 else "    ", colored(str(int(iteracja / self.liczba_iteracji * 100)) + ("%     " if len(str(iteracja))==1 else "%    "), "green"),
                  "Czas do końca: ", colored(str(self.time_to_finish(iteracja, start_verticle - end)), "yellow"))

        print(f"\nNajmniejszy koszt ścieżki {self.file_name}: {colored(cheapest_cost, 'green')}")
        print("\nKolejność indeksów wierzchołków:", *cheapest_path)


        shift = ""
        sequence_list = []
        sequence_matrix = []

        for visited in range(len(cheapest_path)-1):
            Si = cheapest_path[visited]
            Sj = cheapest_path[visited+1]
            word = shift + self.spektrum[Si]
            sequence_list.append(word)
            # print(word)
            next_shift = self.graph[Si][Sj]
            shift += " " * int(next_shift)
            if (visited == len(cheapest_path)-2):
                word = shift + self.spektrum[Sj]
                sequence_list.append(word)

        size = 0
        for i in sequence_list:
            if len(i) > size: size = len(i)
        
        for i in sequence_list:
            temp = i
            while len(temp) != size:
                temp += " "
            sequence_matrix.append(list(temp))
        
        with open("results.txt", "w+") as file:
            sequence = ""
            for j in range(size):
                for i in reversed(range(self.number_of_verticles)):
                    letter = sequence_matrix[i][j]
                    if letter != " ":
                        sequence += letter
                        file.write(f'{"".join(sequence_matrix[i])}\n')
                        break

        print("\nSekwencja: " + colored(sequence, "green"))
        print("\nDługość sekwencji: " + colored(len(sequence), "yellow"))

        print("\nPrzejścia w sekwencji z wagami: ")
        for visited in range(len(cheapest_path)-1):
            Si = cheapest_path[visited]
            Sj = cheapest_path[visited+1]
            print(self.spektrum[Si], colored("--", "green"), colored(self.graph[Si][Sj], "yellow"), colored("->", "green"), self.spektrum[Sj])
                

# Tutaj bedzie miejsca na przetestowanie wszystkich instancji w pętli tworząc dla każdej obiekt
file_names = ["instance.txt"]  
for file_name in file_names:
    new = ACO(file_name)
    new.run()