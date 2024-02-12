'''
Simulate the B92 Protocol
'''
import numpy as np
from qutip import *
from random import randint
from qutip.measurement import measure
from util import create_random_binary_string
from util import Hstate, Vstate, Pstate, Mstate, project_D, project_V

'''
Input Np: An integer which is the number of bits that Alice send to Bob
using the quantum channel

Return: A table with Np rows and two columns
The first column is the index number of the event
The second column is a qutip quantum object that 
'''


def Alice(Np: int):
    result = []
    bin_str = create_random_binary_string(Np)
    for index in range(0, Np):
        if bin_str[index] == '0':
            result.append((index, Hstate))
        else:
            result.append((index, Pstate))
    return bin_str, result


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
    bin_str = create_random_binary_string(Np)
    output = []
    for (index, Qstate) in result:
        if bin_str[index] == '0':
            value, new_state = measure(Qstate, project_V)
            # When there is a click, Bob is sure he is measuring P and the data is 1
            if round(value) == 1:
                output.append((index, 1))
        else:
            value, new_state = measure(Qstate, project_D)
            # When there is a click, Bob is sure he is measuring H and the data is 0
            if round(value) == 1:
                output.append((index, 0))
    return output


def private_key(photonnum: int):
    key_list = Bob(Alice(photonnum)[1])
    key = ''
    for (index, value) in key_list:
        if value == 1:
            key = key + '1'
        else:
            key = key + '0'
    '''
    Use first half of the string to verify the channel
    '''
    verifylength = (len(key_list) // 2)
    return key[verifylength:]


'''
The eve has the same output as Bob has.
He will fabricate the result and send it to Bob
'''


def Eve(result):
    Np = len(result)
    fabricated_result = []
    hacked_info = []
    '''
    The random binary string that Eve 
    use the hack the quantum data
    '''
    bin_str = create_random_binary_string(Np)

    for (index, Qstate) in result:
        if bin_str[index] == '0':
            value, new_state = measure(Qstate, project_V)
            # When there is a click, Eve is sure he is measuring P and the data is 1
            if round(value) == 1:
                hacked_info.append((index, 1))
                fabricated_result.append((index, Pstate))
            else:
                '''
                If the Eve make a wrong guess, he has to decide which state to
                generate and send to Bob
                Now Eve measure 0 on V projector, the state can be both H or P
                However, it is more likely that the state is in H.
                '''
                fabricated_result.append((index, Hstate))
        else:
            value, new_state = measure(Qstate, project_D)
            # When there is a click, Bob is sure he is measuring H and the data is 0
            if round(value) == 1:
                hacked_info.append((index, 0))
                fabricated_result.append((index, Hstate))
            else:
                '''
                If the Eve make a wrong guess, he has to decide which state to
                generate and send to Bob
                Now Eve measure 0 on M projector, the state can be both H or P
                However, it is more likely that the state is in P.
                '''
                fabricated_result.append((index, Pstate))
    return fabricated_result


def success_rate(original_str, check_list):
    Ncheck = len(check_list)
    Nsuccess = 0
    for (index, data) in check_list:
        if str(data) == original_str[index]:
            Nsuccess += 1
    return Nsuccess / Ncheck


def error_with_eve(Np):
    bin_str, result = Alice(Np)
    fabricated_result = Eve(result)
    output = Bob(fabricated_result)
    L = len(output)
    rate = success_rate(bin_str, output[:(L // 2)])
    return 1 - rate


if __name__ == "__main__":
    print(error_with_eve(100))
