import instances
from aco import ACO
from os import listdir
from termcolor import colored  
from os.path import isfile, join

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
    "Instancje z błędami negatywnymi losowymi",
    "Instancje z błędami negatywnymi wynikającymi z powtórzeń",
    "Instancje z błędami pozytywnymi losowymi",
    "Instancje z błędami pozytywnymi, przekłamania na końcach oligonukleotydów"
]

# Testujemy algorytm dla każdej podgrupy instancji 
for index, instance_group in enumerate(instance_groups):
    print("\n--------------------------------------------------")
    print(f"{colored(instance_groups_names[index], 'yellow')}")
    print("--------------------------------------------------\n")
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
        new = ACO(instance_files_path + '\\' + name_of_file)
        new.run()

        print("\n--------------------------------------------------\n")
