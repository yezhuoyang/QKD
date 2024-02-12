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
    data_str = create_random_binary_string(Np)
    for index in range(0, Np):
        if data_str[index] == '0':
            if dice_with_prob(p2):
                result.append((index, Hstate, 2))
            else:
                result.append((index, Hstate, 1))
        else:
            if dice_with_prob(p2):
                result.append((index, Pstate, 2))
            else:
                result.append((index, Pstate, 1))
    return data_str, result


def Bob(result):
    Np = len(result)
    '''
    The random binary string denotes 
    the basis of measurement that Bob 
    Use to measure
    '''
    basis_str = create_random_binary_string(Np)
    output = []
    received = []
    pointer = 0
    for (index, Qstate, photon_num) in result:
        if basis_str[pointer] == '0':
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
    return output, received, basis_str


def private_key(key_output):
    keystr = ""
    for (index, bit) in key_output:
        if bit == 0:
            keystr = keystr + '0'
        else:
            keystr = keystr + '1'
    return keystr


'''
After Bob announce the basis that he use to measure the quantum data,
eve will use the same basis to measure the quantum memory and recover the 
secrete key.
'''


def Eve_hack_measure(bob_output_index, eve_memory):
    pointer = 0
    secret_key = ""
    '''
    Eve don't know that basis that Bob use, so 
    he has to generate a new random basis
    '''
    basis_str = create_random_binary_string(len(eve_memory))

    for (index, Qstate, photon_num) in eve_memory:
        if index in bob_output_index:
            if basis_str[pointer] == '0':
                value, new_state = measure(Qstate, project_V)
                # When there is a click, Bob is sure he is measuring P and the data is 1
                if round(value) == 1:
                    secret_key = secret_key + "1"
                else:
                    '''
                    Although Eve know exactly which index Bob succeed, he might not
                    successfully reproduce the result, in that case, we add an X
                    '''
                    secret_key = secret_key + "X"
            else:
                value, new_state = measure(Qstate, project_D)
                # When there is a click, Bob is sure he is measuring H and the data is 0
                if round(value) == 1:
                    secret_key = secret_key + "0"
                else:
                    '''
                    Although Eve know exactly which basis Bob use, he might not
                    successfully reproduce the result, in that case, we add an X
                    '''
                    secret_key = secret_key + "X"
        pointer += 1
    L = len(secret_key)
    return secret_key[L//2:]


'''
The eve has the same output as Bob has.
He will fabricate the result and send it to Bob

Now the Eve can measure the number of photon  
He will use a photon number attack 
'''


def Eve(result):
    '''
    The random binary string denotes 
    the basis of measurement that Eve 
    Use to hack
    '''
    fabricate_result = []
    quantum_memory = []
    for (index, Qstate, photonnum) in result:
        '''
        The Eve will simply block the single photon state
        If there are two photon, the Eve will save 
        one of the photon into his quantum memory.
        '''
        if photonnum == 2:
            quantum_memory.append((index, Qstate, 1))
            fabricate_result.append((index, Qstate, 1))

    return fabricate_result, quantum_memory


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


def calc_channel_rate(received):
    '''
    Bob send back half of the received data and measured result
    to Alice to check the correctness
    '''
    L = len(received)
    check_data = received[:L // 2]
    '''
    Alice estimate the channel loss
    '''
    maximum_index = check_data[-1][0]
    return len(check_data) / maximum_index


def error_with_eve(Np, p2, pchannel):
    data_str, result = Alice(Np, p2)
    result_theory = noisy_channel(result, pchannel)
    '''
    We assume that Eve can do anything, he has 
    a perfect quantum channel without noise
    '''
    fabricated_result, eve_memory = Eve(result)

    output, revceived, bob_basis = Bob(fabricated_result)

    '''
    Bob must make the index that he makes successful measurement public
    '''
    output_index = [x[0] for x in output]

    channel_rate = calc_channel_rate(revceived)
    '''
    Alice and Bob also run the simulation of a noisy lossy channel without Eve
    '''
    output_theory, revceived_theory, bob_basis_theory = Bob(result_theory)
    channel_rate_theory = calc_channel_rate(revceived_theory)

    '''
    Use the first half of the measured data to check the 
    correctness of the protocal
    '''
    L = len(output)

    '''
    The check data is made public between Alice and Bob
    '''
    check_data = output[:(L // 2)]
    key_data = output[(L // 2):]

    rate = success_rate(data_str, check_data)

    secret_key = private_key(key_data)
    print(secret_key)
    '''
    Eve now has all the basis that Bob use
    '''
    eve_secret_key = Eve_hack_measure(output_index , eve_memory)
    print(eve_secret_key)

    '''
    Also calculate the correctness when there is a powerful Eve
    '''
    L_theory = len(output_theory)
    rate_theory = success_rate(data_str, output_theory[:(L_theory // 2)])

    return 1 - rate, channel_rate, 1 - rate_theory, channel_rate_theory


if __name__ == "__main__":
    # rint(calc_channel_rate(1000, 0.2, 0.1))
    print(error_with_eve(500, 0.3, 0.1))
