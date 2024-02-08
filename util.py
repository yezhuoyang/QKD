
from random import randint



def create_random_binary_string(Np:int):
    randomnum = randint(0, (1 << (Np)) - 1)
    randomnum = randomnum | (1 << Np)
    bin_str = bin(randomnum)[2:]
    bin_str = bin_str[:Np]
    return bin_str