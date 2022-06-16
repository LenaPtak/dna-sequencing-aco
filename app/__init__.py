import instances
from aco import ACO
from os import listdir
from termcolor import colored  
from os.path import isfile, join
import time


instance_files_path = 'app\instances'
listed_files = [f for f in listdir(instance_files_path) if isfile(join(instance_files_path, f))]

# lista list z pliku instances.py
instance_groups = [
    instances.instances_negative_first_type,
    instances.instances_negative_second_type,
    instances.instances_positive_first_type,
    instances.instances_positive_second_type
]
instance_groups_names = [
    "Instancje z bledami negatywnymi losowymi",
    "Instancje z bledami negatywnymi wynikającymi z powtorzen",
    "Instancje z bledami pozytywnymi losowymi",
    "Instancje z bledami pozytywnymi, przekłamania na koncach oligonukleotydow"
]

POJEDYNCZY_TEST = True

if POJEDYNCZY_TEST:
    # Testujemy algorytm dla JEDNEJ instancji
    name_of_file = "35.200-40.txt"
    n = 209
    l = 10
    number_of_mistakes = 40
    new = ACO(instance_files_path + '\\' + name_of_file, name_of_file, n, l, number_of_mistakes, "POZY")
    new.run()

else:
    # Testujemy algorytm dla każdej podgrupy instancji (do zostawienia na przyklad na noc)
    for index, instance_group in enumerate(instance_groups):
        print("\n--------------------------------------------------")
        print(f"{colored(instance_groups_names[index], 'yellow')}")
        print("--------------------------------------------------\n")
        instance_type = instance_groups_names[index]
        for instance in instance_group:

            name_of_file = instance[0] 
            # Jeżeli nie ma odpowiedniego pliku w folderze "instances" to pomijamy
            if name_of_file not in listed_files:
                continue
            n = instance[1]
            l = instance[2]
            number_of_mistakes = instance[3]

            print(f"Instancja: {colored(name_of_file, 'green')}")
            print(f"Liczba bledow: {colored(number_of_mistakes, 'green')}")
            print(f"n: {colored(n, 'green')}\nl: {colored(l, 'green')}\n")

            start = time.time()
            new = ACO(instance_files_path + '\\' + name_of_file, name_of_file, n, l, number_of_mistakes, instance_type)
            new.run()
            end = time.time()