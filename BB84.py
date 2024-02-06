'''
Simulate the BB84 Protocol
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
The convention for encoding:
H:0
V:1
M:0
P:1
'''


def Alice(Np: int):
    result = []
    '''
    Generate a random binary string as the 
    information to send to Bob
    '''
    randomnum = randint(0, (1 << (Np)) - 1)
    randomnum = randomnum | (1 << Np)
    bin_str = bin(randomnum)[2:]
    bin_str = bin_str[:Np]
    '''
    Generate another random binary string as 
    basis Alice use to encode each digit 
    in the message
    When basis_str[index]=0, Alice will use HV basis to 
    encode the data digit
    When basis_str[index]=1, Alice will use PM basis to 
    encode the data digit
    '''
    randomnum2 = randint(0, (1 << (Np)) - 1)
    randomnum2 = randomnum2 | (1 << Np)
    basis_str = bin(randomnum2)[2:]
    basis_str = basis_str[:Np]

    for index in range(0, Np):
        '''
        Case1: Alice use HV basis to encode the data
        '''
        if bin_str[index] == '0':
            if basis_str[index] == '0':
                result.append((index, Hstate))
            else:
                result.append((index, Vstate))
        else:
            '''
            Case2: Alice use PM basis to encode the data
            '''
            if basis_str[index] == '0':
                result.append((index, Mstate))
            else:
                result.append((index, Pstate))
    return bin_str, basis_str, result


'''
Input: A table generate by Alice function.
Return: (Only return the events where he gets a click) A list with two columns, the first column
is the index (event number) and the second column is the bit that Bob thinks Alice sent
'''


def Bob(result):
    Np = len(result)
    '''
    The random binary string denotes 
    the basis of measurement that Bob 
    Use to measure
    '''
    randomnum = randint(0, (1 << (Np)) - 1)
    randomnum = randomnum | (1 << Np)
    basis_str = bin(randomnum)[2:]
    basis_str = basis_str[:Np]
    output = []
    for (index, Qstate) in result:
        '''
        When basis_str[index]=0, Bob will use HV basis to 
        measure the data digit.
        When basis_str[index]=1, Bob will use PM basis to 
        measure the data digit.       
        '''
        if basis_str[index] == '0':
            value, new_state = measure(Qstate, project_V)
            if round(value) == 1:
                output.append((index, 1))
            else:
                output.append((index, 0))
        else:
            value, new_state = measure(Qstate, project_D)
            # When there is a click, Bob is sure he is measuring H and the data is 0
            if round(value) == 1:
                output.append((index, 0))
            else:
                output.append((index, 1))
    return basis_str,output



def Eve():
    return


'''
Compare the two basis that Alice and Bob used
Return a list of index that two basis matches
'''


def compare_basis(basis_Alice, basis_Bob):
    return
