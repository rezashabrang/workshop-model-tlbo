import os
from pathlib import Path
import sys
from numpy.random import randint
from random import random
from pprint import pprint
from collections import Counter

sys.path.append(str(Path(__file__).parent.parent / 'MODEL'))
from MODEL.model import (
    n, S_i, m, p_k, r, Pt, St, trans, TB
)


def generate_empties():
    empty_X = {}
    for i in range(1, n + 1):
        empty_X[i] = {}
        for j in range(1, S_i[i] + 1):
            empty_X[i][j] = {}
            for k in range(1, m + 1):
                empty_X[i][j][k] = {}
                for k_prime in range(1, m + 1):
                    empty_X[i][j][k][k_prime] = 0

    empty_Y = {}
    for i in range(1, n + 1):
        empty_Y[i] = {}
        for j in range(1, S_i[i] + 1):
            empty_Y[i][j] = {}
            for k in range(1, m + 1):
                empty_Y[i][j][k] = {}
                for t in range(1, p_k[k] + 1):
                    empty_Y[i][j][k][t] = 0

    empty_Z = {}
    for k in range(1, m + 1):
        empty_Z[k] = {}
        for t in range(1, p_k[k] + 1):
            empty_Z[k][t] = 0

    empty_B = {}
    for i in range(1, n + 1):
        empty_B[i] = {}
        for j in range(1, S_i[i] + 1):
            empty_B[i][j] = 0

    empty_S = {}
    for k in range(1, m + 1):
        empty_S[k] = {}
        for t in range(1, p_k[k] + 1):
            empty_S[k][t] = 0

    empty_F = {}
    for k in range(1, m + 1):
        empty_F[k] = {}
        for t in range(1, p_k[k] + 1):
            empty_F[k][t] = 0

    empty_EE = {}
    for i in range(1, n + 1):
        empty_EE[i] = {}
        for j in range(1, S_i[i] + 1):
            empty_EE[i][j] = 0
    return empty_X, empty_Y, empty_Z, empty_B, empty_S, empty_F, empty_EE


def generate_ini_X(X):
    occupied_machines = []
    for i in range(1, n + 1):
        for j in range(1, S_i[i] + 1):
            while True:
                rand_k = randint(1, m + 1)
                if rand_k in occupied_machines:
                    if (Counter(occupied_machines))[rand_k] >= 3:
                        continue
                    else:
                        rand_k_prime = randint(1, m + 1)
                        X[i][j][rand_k][rand_k_prime] = 1
                        occupied_machines.append(rand_k)
                        break
                else:
                    rand_k_prime = randint(1, m + 1)
                    X[i][j][rand_k][rand_k_prime] = 1
                    occupied_machines.append(rand_k)
                    break
    return X


def generate_ini_Y(Y, X):
    occupied_positions = []
    for i in range(1, n + 1):
        for j in range(1, S_i[i] + 1):
            for k in range(1, m + 1):
                for k_prime in range(1, p_k[k] + 1):
                    if X[i][j][k][k_prime] == 1:
                        while True:
                            rand_t = randint(1, p_k[k] + 1)
                            temp_position = f'{k}_{rand_t}'
                            if temp_position not in occupied_positions:
                                occupied_positions.append(temp_position)
                                Y[i][j][k][rand_t] = 1
                                break
    return Y


def generate_ini_Z(Z):
    for k in range(1, m + 1):
        for t in range(1, p_k[k] + 1):
            Z[k][t] = 0 if random() >= 0.5 else 1

    return Z


def generate_ini_B(B, X, EE_temp):
    """
    Generate B, EE, F, S
    :param B:
    :return:
    """
    for i in range(1, n + 1):
        for j in range(1, S_i[i] + 1):
            if j == 1:
                B[i][j] = r[i]
                EE_temp = calculate_EE(X, EE_temp, B)
            else:
                B[i][j] = EE_temp[i][j - 1]
                EE_temp = calculate_EE(X, EE_temp, B)
    return B


def calculate_EE(X, EE, B):
    for i in range(1, n + 1):
        for j in range(1, S_i[i] + 1):
            sigma_term = 0
            for k in range(1, m + 1):
                for k_prime in range(1, m + 1):
                    sigma_term += (Pt[i][j][k] + St[i][j][k]) * X[i][j][k][k_prime]
            # print(f'EE = {sigma_term}')
            EE[i][j] = B[i][j] + sigma_term

    return EE


def calculate_F(F, S, Y):
    for k in range(1, m + 1):
        for t in range(1, p_k[k] + 1):
            sigma_term = 0
            for i in range(1, n + 1):
                for j in range(1, S_i[i] + 1):
                    for k_prime in range(1, m + 1):
                        sigma_term += (Pt[i][j][k] + St[i][j][k]) * Y[i][j][k][t]
            # print(f'F = {sigma_term}')
            F[k][t] = S[k][t] + sigma_term

    return F


def calculate_S(B, S, Y):
    for i in range(1, n + 1):
        for j in range(1, S_i[i] + 1):
            for k in range(1, m + 1):
                for t in range(1, p_k[k] + 1):
                    if Y[i][j][k][t] == 1:
                        S[k][t] = B[i][j]
    return S


def calculate_c_max(EE):
    C_max = 0
    for first_level in EE.values():
        for second_level in first_level.values():
            C_max = max(second_level, C_max)
    return C_max


def generate_ini_X_Y(X, Y):
    generate_empties()
    temp_X = X
    temp_Y = Y
    not_restart = False
    restart_permanent = True
    while not not_restart or restart_permanent:
        empty_X, empty_Y, empty_Z, empty_B, empty_S, empty_F, empty_EE = generate_empties()
        X = empty_X
        Y = empty_Y
        restart_permanent = False
        not_restart = True
        occupied_positions = {}
        for k in range(1, m + 1):
            occupied_positions[k] = []
        occupied_machines = []
        last_k_prime = 0  # Saving the last machine of j-1
        for i in range(1, n + 1):
            task_based_occ = []  # Occupied machine for a work
            for j in range(1, S_i[i] + 1):
                while True:
                    rand_k = randint(1, m + 1)
                    if rand_k in occupied_machines:
                        if (Counter(occupied_machines))[rand_k] >= 3:
                            continue
                        else:
                            # If it is the first operation then generate rand_k_prime else it is the last operation index
                            if j == 1:
                                rand_k_prime = randint(1, m + 1)
                                last_k_prime = rand_k_prime
                            else:
                                rand_k_prime = last_k_prime
                                last_k_prime = rand_k

                            # X allocation
                            X[i][j][rand_k][rand_k_prime] = 1
                            occupied_machines.append(rand_k)

                            # Y allocation
                            # Try it for 10 times
                            c_debug = 0
                            for s in range(10):
                                c_debug += 1
                                if c_debug == 8:
                                    restart_permanent = True
                                rand_t = randint(1, p_k[rand_k_prime] + 1)
                                if rand_t not in occupied_positions[rand_k]:
                                    if rand_k in task_based_occ and not all(
                                            rand_t > val for val in occupied_positions[rand_k]):
                                        not_restart = False
                                        continue
                                    occupied_positions[rand_k].append(rand_t)
                                    Y[i][j][rand_k][rand_t] = 1
                                    task_based_occ.append(rand_k)
                                    not_restart = True
                                    break
                                else:
                                    not_restart = False
                                    continue
                            break
                    else:
                        # If it is the first operation then generate rand_k_prime else it is the last operation index
                        if j == 1:
                            rand_k_prime = randint(1, m + 1)
                            last_k_prime = rand_k_prime
                        else:
                            rand_k_prime = last_k_prime
                            last_k_prime = rand_k

                        # X allocation
                        X[i][j][rand_k][rand_k_prime] = 1
                        occupied_machines.append(rand_k)

                        # Y allocation
                        # Try it for 10 times
                        while True:
                            rand_t = randint(1, p_k[rand_k_prime] + 1)
                            if rand_t not in occupied_positions[rand_k]:
                                if rand_k in task_based_occ and not all(
                                        rand_t > val for val in occupied_positions[rand_k]):
                                    not_restart = False
                                    continue
                                occupied_positions[rand_k].append(rand_t)
                                Y[i][j][rand_k][rand_t] = 1
                                task_based_occ.append(rand_k)
                                not_restart = True
                                break
                            else:
                                not_restart = False
                                continue
                        break
    return X, Y


def generate_ini_B_EE_S_F(B: dict,
                          EE: dict,
                          S: dict,
                          F: dict,
                          X: dict,
                          Y: dict,
                          Z: dict
                          ):
    """
    Generating time related parameters
    :return:
    """
    global n
    global S_i
    global m
    global p_k
    # Operations that related times are calculated. FORMAT (i, j)
    calculated_ops = []
    calculated_places = []
    N_operations = 0
    for i in range(1, n + 1):
        N_operations += S_i[i]
    counter = 0
    while True:
        counter += 1
        if counter > 10:
            break
        for i in range(1, n + 1):
            for j in range(1, S_i[i] + 1):
                if (i, j) in calculated_ops:
                    continue
                for k in range(1, m + 1):
                    for k_prime in range(1, m + 1):
                        for t in range(1, p_k[k] + 1):
                            if Y[i][j][k][t] != 1:
                                continue
                            # if it is the first operation of a work
                            # And in the first place of a machine then start calculating
                            if j == 1 and t == 1 and (i, j) not in calculated_ops:
                                # Start time: B & S
                                B[i][j] = r[i]
                                S[k][t] = r[i]

                                # End time: E & F
                                EE[i][j] = Pt[i][j][k] + St[i][j][k]
                                F[k][t] = EE[i][j]

                                # Appending calculated operation and place
                                calculated_ops.append((i, j))
                                calculated_places.append((k, t))

                            # Operations in the first place of the machines
                            elif t == 1 and (i, j - 1) in calculated_ops and (i, j) not in calculated_ops:
                                # Start time
                                B[i][j] = EE[i][j - 1] + trans[i][k][k_prime] + Z[k][t] * TB[k]
                                S[k][t] = B[i][j]
                                # End time
                                EE[i][j] = Pt[i][j][k] + St[i][j][k]
                                F[k][t] = EE[i][j]
                                # Appending
                                calculated_ops.append((i, j))
                                calculated_places.append((k, t))

                            # Second and above operations of a machine
                            elif (i, j - 1) in calculated_ops and (k, t - 1) in calculated_places and (
                                    i, j) not in calculated_ops:
                                # Start time
                                B[i][j] = EE[i][j - 1] + trans[i][k][k_prime] + Z[k][t] * TB[k]
                                S[k][t] = B[i][j]
                                # End time
                                EE[i][j] = Pt[i][j][k] + St[i][j][k]
                                F[k][t] = EE[i][j]
                                # Appending
                                calculated_ops.append((i, j))
                                calculated_places.append((k, t))

                            # First operations of a work not in first place of a machine
                            elif j == 1 and (k, t - 1) in calculated_places and (i, j) not in calculated_ops:
                                # Start time
                                B[i][j] = F[k][t - 1] + trans[i][k][k_prime] + Z[k][t] * TB[k]
                                S[k][t] = B[i][j]
                                # End time
                                EE[i][j] = Pt[i][j][k] + St[i][j][k]
                                F[k][t] = EE[i][j]
                                # Appending
                                calculated_ops.append((i, j))
                                calculated_places.append((k, t))
        # print(f'ops= {calculated_ops}')
        # print(f'places= {calculated_places}')

        # If all operations are found then quit
        if len(set(calculated_ops)) == N_operations:
            break

    return B, EE, S, F


def generate_initial_randoms():
    """
    Generating random first solutions for X, Y, Z, B
    Calculation for  EE, S, F
    :return:
    """
    empty_X, empty_Y, empty_Z, empty_B, empty_S, empty_F, empty_EE = generate_empties()
    # X = generate_ini_X(empty_X)
    # Y = generate_ini_Y(empty_Y, X)
    X, Y = generate_ini_X_Y(empty_X, empty_Y)
    Z = generate_ini_Z(empty_Z)
    # B = generate_ini_B(empty_B, X, empty_EE)
    # EE = calculate_EE(X, empty_EE, B)
    # S = calculate_S(B, empty_S, Y)
    # F = calculate_F(empty_F, S, Y)
    # Y = {1: {1: {1: {1: 0, 2: 1, 3: 0}, 2: {1: 0, 2: 0, 3: 0}, 3: {1: 0, 2: 0, 3: 0}},
    #          2: {1: {1: 0, 2: 0, 3: 1}, 2: {1: 0, 2: 0, 3: 0}, 3: {1: 0, 2: 0, 3: 0}},
    #          3: {1: {1: 0, 2: 0, 3: 0}, 2: {1: 0, 2: 0, 3: 0}, 3: {1: 0, 2: 1, 3: 0}}},
    #      2: {1: {1: {1: 0, 2: 0, 3: 0}, 2: {1: 0, 2: 0, 3: 0}, 3: {1: 1, 2: 0, 3: 0}},
    #          2: {1: {1: 0, 2: 0, 3: 0}, 2: {1: 1, 2: 0, 3: 0}, 3: {1: 0, 2: 0, 3: 0}},
    #          3: {1: {1: 0, 2: 0, 3: 0}, 2: {1: 0, 2: 1, 3: 0}, 3: {1: 0, 2: 0, 3: 0}}},
    #      3: {1: {1: {1: 0, 2: 0, 3: 0}, 2: {1: 0, 2: 0, 3: 1}, 3: {1: 0, 2: 0, 3: 0}},
    #          2: {1: {1: 1, 2: 0, 3: 0}, 2: {1: 0, 2: 0, 3: 0}, 3: {1: 0, 2: 0, 3: 0}},
    #          3: {1: {1: 0, 2: 0, 3: 0}, 2: {1: 0, 2: 0, 3: 0}, 3: {1: 0, 2: 0, 3: 1}}}}

    B, EE, S, F = generate_ini_B_EE_S_F(
        empty_B,
        empty_EE,
        empty_S,
        empty_F,
        X,
        Y,
        Z
    )

    C_max = calculate_c_max(EE)
    return X, Y, Z, B, EE, S, F, C_max
