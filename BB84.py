'''
Simulate the BB84 Protocol
'''
import numpy as np
from qutip import *
from random import randint
from qutip.measurement import measure
from util import create_random_binary_string
from util import Hstate, Vstate, Pstate, Mstate, project_D, project_V

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
    bin_str = create_random_binary_string(Np)
    '''
    Generate another random binary string as 
    basis Alice use to encode each digit 
    in the message
    When basis_str[index]=0, Alice will use HV basis to 
    encode the data digit
    When basis_str[index]=1, Alice will use PM basis to 
    encode the data digit
    '''
    basis_str = create_random_binary_string(Np)
    basis_str = basis_str.replace('0', '+')
    basis_str = basis_str.replace('1', '/')
    for index in range(0, Np):
        '''
        Case1: Alice use HV basis to encode the data
        '''
        if basis_str[index] == '+':
            if bin_str[index] == '0':
                result.append((index, Hstate))
            else:
                result.append((index, Vstate))
        else:
            '''
            Case2: Alice use PM basis to encode the data
            '''
            if bin_str[index] == '0':
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
    basis_str = create_random_binary_string(Np)
    basis_str = basis_str.replace('0', '+')
    basis_str = basis_str.replace('1', '/')
    output = []
    for (index, Qstate) in result:
        '''
        When basis_str[index]=0, Bob will use HV basis to 
        measure the data digit.
        When basis_str[index]=1, Bob will use PM basis to 
        measure the data digit.       
        '''
        if basis_str[index] == '+':
            value, new_state = measure(Qstate, project_V)
            if round(value) == 1:
                output.append((index, 1))
            else:
                output.append((index, 0))
        else:
            value, new_state = measure(Qstate, project_D)
            if round(value) == 1:
                output.append((index, 0))
            else:
                output.append((index, 1))
    return basis_str, output


'''
Simulate the Eve for BB84 protocal
'''


def Eve(result):
    Np = len(result)
    '''
    The random binary string denotes 
    the basis of measurement that Eve 
    Use to hack
    '''
    basis_str = create_random_binary_string(Np)
    basis_str = basis_str.replace('0', '+')
    basis_str = basis_str.replace('1', '/')
    fabricate_result = []
    hacked_info = []
    for (index, Qstate) in result:
        '''
        When basis_str[index]=0, Eve will use HV basis to 
        measure the data digit.
        When basis_str[index]=1, Eve will use PM basis to 
        measure the data digit.       
        '''
        if basis_str[index] == '+':
            value, new_state = measure(Qstate, project_V)
            '''
            When Eve measure 1 in HV basis, he will fabricate a V
            When Eve measure 0 in HV basis, he will fabricate a H
            '''
            if round(value) == 1:
                hacked_info.append((index, 1))
                fabricate_result.append((index, Vstate))
            else:
                hacked_info.append((index, 0))
                fabricate_result.append((index, Hstate))
        else:
            value, new_state = measure(Qstate, project_D)
            '''
            When Eve measure 1 in PM basis, he will fabricate a P
            When Eve measure 0 in PM basis,  he will fabricate a M
            '''
            if round(value) == 1:
                hacked_info.append((index, 0))
                fabricate_result.append((index, Mstate))
            else:
                hacked_info.append((index, 1))
                fabricate_result.append((index, Pstate))
    return fabricate_result


'''
Compare the two basis that Alice and Bob used
Return a list of index that two basis matches
'''


def compare_basis(basis_Alice, basis_Bob, Np):
    correct_index = []
    for i in range(0, Np):
        if basis_Alice[i] == basis_Bob[i]:
            correct_index.append(i)
    return correct_index


'''
Alice and Bob will exchange first half of the digit which 
they are assured that they use the same basis
'''


def success_rate(bin_str, output, correct_index):
    N_total = len(correct_index) // 2
    N_success = 0
    for i in range(0, N_total):
        if bin_str[correct_index[i]] == '1' and output[correct_index[i]][1] == 1:
            N_success = N_success + 1
        if bin_str[correct_index[i]] == '0' and output[correct_index[i]][1] == 0:
            N_success = N_success + 1
    return N_success / N_total


def secrete_key(Np):
    bin_str, basis_Alice, result = Alice(Np)
    basis_Bob, output = Bob(result)
    correct_index = compare_basis(basis_Alice, basis_Bob, Np)
    L = len(correct_index)
    key = ''
    for i in range(L // 2, L):
        if output[correct_index[i]][1] == 0:
            key = key + '0'
        else:
            key = key + '1'
    return key


def error_with_eve(Np):
    bin_str, basis_Alice, result = Alice(Np)
    fab_result = Eve(result)
    basis_Bob, output = Bob(fab_result)
    correct_index = compare_basis(basis_Alice, basis_Bob, Np)
    return 1 - success_rate(bin_str, output, correct_index)


if __name__ == "__main__":
    print(error_with_eve(40))
