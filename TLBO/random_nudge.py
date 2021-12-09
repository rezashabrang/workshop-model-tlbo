import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / 'MODEL'))
from initialization import generate_ini_B_EE_S_F_Z, calculate_c_max
from collections import Counter
from MODEL.model import n, m, S_i, p_k
import random
from initialization import generate_empties, generate_ini_Z
from MODEL.model import check_all_constraints


def generate_new_sol(
        VARS_ST: dict,
        VARS_T: dict,
        random_val
):
    while True:
        try:
            empty_X, empty_Y, empty_Z, empty_B, empty_S, empty_F, empty_EE = generate_empties()
            X, Y = generate_new_X_Y(
                X_st=VARS_ST['X'],
                Y_st=VARS_ST['Y'],
                X_t=VARS_T['X'],
                Y_t=VARS_T['Y'],
                random_val=random_val
            )
            Z = generate_new_Z(
                Z_st=VARS_ST['Z'],
                Z_T=VARS_T['Z'],
                rand_val=random_val
            )
            B, EE, S, F, Z = generate_ini_B_EE_S_F_Z(
                empty_B,
                empty_EE,
                empty_S,
                empty_F,
                X,
                Y,
                Z
            )
            C_max = calculate_c_max(EE)
            s, situation = check_all_constraints(X, Y, Z, B, S, F, EE, C_max)
            if situation:
                break
        except Exception as e:
            print(e)
            continue
    final_res = {
        'X': X,
        'Y': Y,
        'Z': Z,
        'B': B,
        'S': S,
        'F': F,
        'EE': EE,
        'C_max': C_max
    }
    return final_res


def generate_new_X_Y(
        X_st: dict,
        Y_st: dict,
        X_t: dict,
        Y_t: dict,
        random_val: float

):
    for i in range(1, n + 1):
        for j in range(1, S_i[i] + 1):
            for k in range(1, m + 1):
                if random.random() < random_val:
                    X_st[i][j][k] = X_t[i][j][k]
                    Y_st[i][j][k] = Y_t[i][j][k]

    return X_st, Y_st


def generate_new_Z(
        Z_st: dict,
        Z_T: dict,
        rand_val
):
    for k in range(1, m + 1):
        for t in range(1, p_k[k] + 1):
            if random.random() < rand_val:
                Z_st[k][t] = Z_T[k][t]

    return Z_st
