"""
    Ten plik zawiera informacje o instacjach ze strony Pani Profesor
    https://www.cs.put.poznan.pl/mkasprzak/bio/testy.html
"""

# Instancje z błędami negatywnymi losowymi
# [name_of_instance, n, l, number_of_negative_mistakes]
instances_negative_first_type = [
    ["9.200-40.txt", 209, 10, 40],
    ["9.200-80.txt", 209, 10, 80],
    ["18.200-40.txt", 209, 10, 40],
    ["18.200-80.txt", 209, 10, 80],
    ["35.200-40.txt", 209, 10, 40],
    ["35.200-80.txt", 209, 10, 80],
    ["20.300-60.txt", 309, 10, 60],
    ["20.300-120.txt", 309, 10, 120],
    ["55.300-60.txt", 309, 10, 60],
    ["55.300-120.txt", 309, 10, 120],
    ["58.300-60.txt", 309, 10, 60],
    ["58.300-120.txt", 309, 10, 120],
    ["55.400-80.txt", 409, 10, 80],
    ["55.400-160.txt", 409, 10, 160],
    ["62.400-80.txt", 409, 10, 80],
    ["62.400-160.txt", 409, 10, 160],
    ["68.400-80.txt", 409, 10, 80],
    ["68.400-160.txt", 409, 10, 160],
    ["10.500-100.txt", 509, 10, 100],
    ["10.500-200.txt", 509, 10, 200],
    ["25.500-100.txt", 509, 10, 100],
    ["25.500-200.txt", 509, 10, 200],
    ["53.500-100.txt", 509, 10, 100],
    ["53.500-200.txt", 509, 10, 200]
]


# Instancje z błędami negatywnymi wynikającymi z powtórzeń
# [name_of_instance, n, l, number_of_negative_mistakes]
instances_negative_second_type = [
    ["59.500-2.txt", 509, 10, 2],
    ["113.500-8.txt", 509, 10, 8],
    ["144.500-12.txt", 509, 10, 12],
    ["28.500-18.txt", 509, 10, 18],
    ["34.500-32.txt", 509, 10, 32]
]


# Instancje z błędami pozytywnymi losowymi
# [name_of_instance, n, l, number_of_positive_mistakes]
instances_positive_first_type = [
    ["9.200+80.txt", 209, 10, 80],
    ["18.200+80.txt", 209, 10, 80],
    ["35.200+80.txt", 209, 10, 80],
    ["20.300+120.txt", 309, 10, 120],
    ["55.300+120.txt", 309, 10, 120],
    ["58.300+120.txt", 309, 10, 120],
    ["55.400+160.txt", 409, 10, 160],
    ["62.400+160.txt", 409, 10, 160],
    ["68.400+160.txt", 409, 10, 160],
    ["10.500+200.txt", 509, 10, 200],
    ["25.500+200.txt", 509, 10, 200],
    ["53.500+200.txt", 509, 10, 200]
]


# Instancje z błędami pozytywnymi, przekłamania na końcach oligonukleotydów
# [name_of_instance, n, l, number_of_positive_mistakes]
instances_positive_second_type = [
    ["9.200+20.txt", 209, 10, 20],
    ["18.200+20.txt", 209, 10, 20],
    ["35.200+20.txt", 209, 10, 20],
    ["20.300+30.txt", 309, 10, 30],
    ["55.300+30.txt", 309, 10, 30],
    ["58.300+30.txt", 309, 10, 30],
    ["55.400+40.txt", 409, 10, 40],
    ["62.400+40.txt", 409, 10, 40],
    ["68.400+40.txt", 409, 10, 40],
    ["10.500+50.txt", 509, 10, 50],
    ["25.500+50.txt", 509, 10, 50],
    ["53.500+50.txt", 509, 10, 50]
]
