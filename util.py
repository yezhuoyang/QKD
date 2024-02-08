
from random import randint
from qutip import *
import numpy as np

def create_random_binary_string(Np:int):
    randomnum = randint(0, (1 << (Np)) - 1)
    randomnum = randomnum | (1 << Np)
    bin_str = bin(randomnum)[2:]
    bin_str = bin_str[:Np]
    return bin_str


Hstate = basis(2, 0)
Vstate = basis(2, 1)
Pstate = 1 / np.sqrt(2) * (Hstate + Vstate)
Mstate = 1 / np.sqrt(2) * (Hstate - Vstate)

project_V = ket2dm(Vstate)
project_D = ket2dm(Mstate)