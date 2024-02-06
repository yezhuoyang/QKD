'''
Simulate the B92 Protocol
'''
import numpy as np
from qutip import *
from random import randint

Hstate = basis(2, 0)
Vstate = basis(2, 1)
Pstate = 1 / np.sqrt(2) * (Hstate + Vstate)
Mstate = 1 / np.sqrt(2) * (Hstate - Vstate)

'''
Input Np: An integer which is the number of bits that Alice send to Bob
using the quantum channel

Return: A table with Np rows and two columns
The first column is the index number of the event
The second column is a qutip quantum object that 
'''


def Alice(Np: int):
    result = []
    randomnum = randint(0, (1 << (Np)) - 1)
    randomnum = randomnum | (1 << Np)
    bin_str = bin(randomnum)[2:]
    index = 1
    print(bin_str)
    for i in range(0, Np):
        if bin_str[i] == '0':
            result.append((index, Hstate))
        else:
            result.append((index, Pstate))
        index += 1
    return result


'''
Input: A table generate by Alice function.

Return: (Only return the events where he gets a click) A list with two columns, the first column
is the index (event number) and the second column is the bit that Bob thinks Alice sent
'''


def Bob(table):
    return


def private_key(photonnum: int):
    return


def Eve():
    return


if __name__ == "__main__":
    result = Alice(10)
