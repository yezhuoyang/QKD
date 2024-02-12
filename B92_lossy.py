'''
Simulate the B92 Protocol with channel loss
'''
import numpy as np
from qutip import *
from random import randint
from qutip.measurement import measure
from util import create_random_binary_string
from util import Hstate, Vstate, Pstate, Mstate, project_D, project_V, dice_with_prob

'''
The noisy channel than only remain psuccess part of the original
list.
'''


def noisy_channel(signal: list, psuccess: float):
    output_list = []
    for i in range(0, len(signal)):
        if dice_with_prob(psuccess):
            output_list.append(signal[i])
    print(len(output_list) / len(signal))
    return output_list


'''
We need to consider photon number now
Now the Alice has some probability p2 to generate 2 photons at
the same time.
'''


def Alice(Np: int, p2: float):
    result = []
    bin_str = create_random_binary_string(Np)
    for index in range(0, Np):
        if bin_str[index] == '0':
            if dice_with_prob(p2):
                result.append((index, Hstate, 2))
            else:
                result.append((index, Hstate, 1))
        else:
            if dice_with_prob(p2):
                result.append((index, Pstate, 2))
            else:
                result.append((index, Pstate, 1))
    return bin_str, result


def Bob(result):
    Np = len(result)
    '''
    The random binary string denotes 
    the basis of measurement that Bob 
    Use to measure
    '''
    bin_str = create_random_binary_string(Np)
    output = []
    received = []
    pointer = 0
    for (index, Qstate, photon_num) in result:
        if bin_str[pointer] == '0':
            value, new_state = measure(Qstate, project_V)
            # When there is a click, Bob is sure he is measuring P and the data is 1

            if round(value) == 1:
                output.append((index, 1))
                received.append((index, 1))
            else:
                received.append((index, 0))
        else:
            value, new_state = measure(Qstate, project_D)
            # When there is a click, Bob is sure he is measuring H and the data is 0
            if round(value) == 1:
                output.append((index, 0))
                received.append((index, 0))
            else:
                received.append((index, 0))
        pointer += 1
    return output, received


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
    return result


'''
Check the ratio of photons between:
1. The number of photons Bob receive and use the same basis to measure. The measured data also match with Alice.
2. The number of photons Bob receive and use the same basis to measure
'''


def success_rate(original_str, check_list):
    Ncheck = len(check_list)
    Nsuccess = 0
    for (index, data) in check_list:
        if str(data) == original_str[index]:
            Nsuccess += 1
    return Nsuccess / Ncheck


def calc_channel_rate(Np, p2, pchannel):
    bin_str, result = Alice(Np, p2)
    result = noisy_channel(result, pchannel)
    fabricated_result = Eve(result)
    output, received = Bob(fabricated_result)
    '''
    Bob send back half of the received data and measured result 
    to Alice to check the correctness
    '''
    L = len(received)
    check_data = received[:L//2]
    '''
    Alice estimate the channel loss
    '''
    maximum_index = check_data[-1][0]
    return len(check_data) / maximum_index


def error_with_eve(Np, p2, pchannel):
    bin_str, result = Alice(Np, p2)
    # result = noisy_channel(result, pchannel)
    fabricated_result = Eve(result)
    output = Bob(fabricated_result)
    L = len(output)
    rate = success_rate(bin_str, output[:(L // 2)])
    return 1 - rate


if __name__ == "__main__":
    print(calc_channel_rate(30000, 0.2, 0.1))
