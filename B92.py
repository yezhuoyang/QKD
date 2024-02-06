'''
Simulate the B92 Protocol
'''
import numpy as np
from qutip import *
from random import randint
from qutip.measurement import measure

Hstate = basis(2, 0)
Vstate = basis(2, 1)
Pstate = 1 / np.sqrt(2) * (Hstate + Vstate)
Mstate = 1 / np.sqrt(2) * (Hstate - Vstate)

project_V = ket2dm(Vstate)
project_D = ket2dm(Mstate)

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
    for index in range(0, Np):
        if bin_str[index] == '0':
            result.append((index, Hstate))
        else:
            result.append((index, Pstate))
    return result


'''
Input: A table generate by Alice function.

Return: (Only return the events where he gets a click) A list with two columns, the first column
is the index (event number) and the second column is the bit that Bob thinks Alice sent
'''


def Bob(result):
    Np = len(result)
    randomnum = randint(0, (1 << Np) - 1)
    randomnum = randomnum | (1 << Np)
    bin_str = bin(randomnum)[2:]
    output = []
    for (index, Qstate) in result:
        if bin_str[index] == '0':
            value, new_state = measure(Qstate, project_V)
            # When the value
            if round(value) == 1:
                output.append((index, 1))
        else:
            value, new_state = measure(Qstate, project_D)
            if round(value) == 1:
                output.append((index, 0))
    return output


def private_key(photonnum: int):
    key_list = Bob(Alice(photonnum))
    key = ''
    for (index, value) in key_list:
        if value == 1:
            key = key + '1'
        else:
            key = key + '0'
    '''
    Use first half of the string to verify the channel
    '''
    verifylength=(len(key_list)//2)
    return key[verifylength:]


def Eve():
    return


if __name__ == "__main__":
    result = private_key(100)
    print(result)
