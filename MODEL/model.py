from formulas import (
    create_energy_cost_matrix,
    create_energy_time_matrix,
    create_setup_matrix,
    create_trans_matrix,
    generate_TB,
    generate_O,
    generate_r,
    generate_pidle,
    generate_energy
)

# ------------- Global Parameters -------------
P0 = 5  # General consumed energy per time unit
n = 3  # Number of works

# Dict of number of operations assigned to each work
S_i = {
    1: 3,
    2: 3,
    3: 3
}

m = 3  # Number of machines

# Dict number of positions in each machine
p_k = {
    1: 3,
    2: 3,
    3: 3
}

# Consumed energy per pair
P_i_j_k = create_energy_cost_matrix(n, S_i, p_k)

# Pt
Pt = create_energy_time_matrix(n, S_i, p_k)

# r(i)
r = generate_r(n)

# pidle(k)
pidle = generate_pidle(m)

# Energy(k)
energy = generate_energy(m)

# Setup(i,j,k)
St = create_setup_matrix(n, S_i, p_k)

# O(k)
O = generate_O(m)

# TB(k)
TB = generate_TB(O, energy, pidle, m)

# Transportation Matrix
trans = create_trans_matrix(n, m)

# Big M
M = 100


# ---------------------------------- OBJECTVICE FUNCTION ----------------------------------
def TEC(
        C_max: float,
        Z: dict,
        S: dict,
        F: dict,
        X: dict

):
    """
    TEC Formula.
    :arg
    :return TEC
    """
    global n
    global m
    global p_k
    global S_i
    global pidle
    global P_i_j_k
    global P0
    # ------------------ First Term ------------------
    first_term = 0
    for k in range(1, m + 1):
        for t in range(1, p_k[k]):
            first_term += (1 - Z[k][t]) * (S[k][t + 1] - F[k][t]) * pidle[k] + Z[k][t] * energy[k]

    # ------------------ Second Term ------------------
    second_term = 0
    for i in range(1, n + 1):
        for j in range(1, S_i[i] + 1):
            for k in range(1, m + 1):
                for k_prime in range(1, m + 1):
                    second_term += P_i_j_k[i][j][k] * Pt[i][j][k] * X[i][j][k][k_prime]

    # ------------------ Third Term ------------------
    third_term = P0 * C_max

    # ------------------ Final Result ------------------
    result = first_term + second_term + third_term

    return result


# ---------------------------------- CONSTRAINTS ----------------------------------
def EQ_9(X: dict):
    global m
    global n
    global S_i
    res = 0
    for i in range(1, n + 1):
        for j in range(1, S_i[i]):
            for k in range(1, m + 1):
                for k_prime in range(1, m + 1):
                    res += X[i][j][k][k_prime]
            if res == 1:
                res = 0
                continue
            else:
                return False
    return True


# def EQ_10(X: dict):
#     global m
#     global n
#     res = 0
#     for i in range(1, n + 1):
#         for k in range(1, m + 1):
#             res += X[i][1][k][k]
#     pass


def EQ_11(
        X: dict,
        Y: dict
):
    global n
    global S_i
    global m
    global p_k
    res_y = 0
    res_x = 0
    for i in range(1, n + 1):
        for j in range(1, S_i[i]):
            for k in range(1, m + 1):
                for t in range(1, p_k[k] + 1):
                    res_y += Y[i][j][k][t]
                for k_prime in range(1, m + 1):
                    res_x += X[i][j][k][k_prime]
            if res_y == res_x:
                res_y = 0
                res_x = 0
                continue
            else:
                return False

    return True


def EQ_12(
        Y: dict,
        X: dict
):
    global m
    global p_k
    global n
    global S_i
    res_y = 0
    res_y_prime = 0
    for k in range(1, m + 1):
        for t in range(1, p_k[k]):

            # Y part
            for i in range(1, n + 1):
                for j in range(1, S_i[i] + 1):
                    res_y += Y[i][j][k][t]

            # Y_prime part
            for i_prime in range(1, n + 1):
                for j_prime in range(1, S_i[i_prime] + 1):
                    res_y_prime += Y[i_prime][j_prime][k][t + 1]

            # Checking condition
            if res_y >= res_y_prime:
                res_y = 0
                res_y_prime = 0
                continue
            else:
                return False

    return True


def EQ_15(Y: dict):
    global n
    global S_i
    global m
    global p_k
    res_y = 0
    for i in range(1, n + 1):
        for j in range(1, S_i[i] + 1):
            for k in range(1, m + 1):
                for t in range(1, p_k[k] + 1):
                    res_y += Y[i][j][k][t]
            if res_y == 1:
                res_y = 0
                continue
            else:
                return False

    return True


def EQ_16(Y: dict):
    global n
    global S_i
    global m
    global p_k
    res_y = 0
    for k in range(1, m + 1):
        for t in range(1, p_k[k] + 1):
            for i in range(1, n + 1):
                for j in range(1, S_i[i] + 1):
                    res_y += Y[i][j][k][t]
            if res_y <= 1:
                res_y = 0
                continue
            else:
                return False

    return True


def EQ_17(
        EE: dict,
        B: dict,
        X: dict
):
    global Pt
    global St
    global n
    global S_i
    global m
    sigma_term = 0
    for i in range(1, n + 1):
        for j in range(1, S_i[i] + 1):
            for k in range(1, m + 1):
                for k_prime in range(1, m + 1):
                    sigma_term += (Pt[i][j][k] + St[i][j][k]) * X[i][j][k][k_prime]
            if EE[i][j] == B[i][j] + sigma_term:
                sigma_term = 0
                continue
            else:
                return False

    return True


def EQ_18(
        F: dict,
        S: dict,
        Y: dict
):
    global m
    global p_k
    global n
    global S_i
    global Pt
    global St
    sigma_term = 0
    for k in range(1, m + 1):
        for t in range(1, p_k[k] + 1):
            for i in range(1, n + 1):
                for j in range(1, S_i[i] + 1):
                    for k_prime in range(1, m + 1):
                        sigma_term += (Pt[i][j][k] + St[i][j][k]) * Y[i][j][k][t]
            if F[k][t] == S[k][t] + sigma_term:
                sigma_term = 0
                continue
            else:
                return False

    return True


def EQ_19(
        S: dict,
        B: dict,
        Y: dict
):
    global n
    global S_i
    global m
    global p_k
    global M
    for i in range(1, n + 1):
        for j in range(1, S_i[i] + 1):
            for k in range(1, m + 1):
                for t in range(1, p_k[k] + 1):
                    if S[k][t] <= B[i][j] + M * (1 - Y[i][j][k][t]):
                        continue
                    else:
                        return False

    return True


def EQ_20(
        S: dict,
        B: dict,
        Y: dict
):
    global n
    global S_i
    global m
    global p_k
    global M
    for i in range(1, n + 1):
        for j in range(1, S_i[i] + 1):
            for k in range(1, m + 1):
                for t in range(1, p_k[k] + 1):
                    if S[k][t] + M * (1 - Y[i][j][k][t]) >= B[i][j]:
                        continue
                    else:
                        return False

    return True


def EQ_21(
        S: dict,
        F: dict,
        Z: dict
):
    global TB
    global M
    global p_k
    global m
    for k in range(1, m + 1):
        for t in range(1, p_k[k]):
            if S[k][t + 1] - F[k][t] >= TB[k] - M * (1 - Z[k][t]):
                continue
            else:
                return False

    return True


def EQ_22(
        S: dict,
        F: dict,
        Z: dict
):
    global TB
    global M
    global p_k
    global m
    for k in range(1, m + 1):
        for t in range(1, p_k[k]):
            if S[k][t + 1] - F[k][t] <= TB[k] - M * Z[k][t]:
                continue
            else:
                return False

    return True


def EQ_23(
        F: dict,
        S: dict
):
    global p_k
    global m
    for k in range(1, m + 1):
        for t in range(1, p_k[k]):
            if F[k][t] <= S[k][t + 1]:
                continue
            else:
                return False

    return True


def EQ_24(
        EE: dict,
        B: dict
):
    global n
    global S_i
    for i in range(1, n + 1):
        for j in range(1, S_i[i]):
            if EE[i][j] <= B[i][j + 1]:
                continue
            else:
                return False

    return True


def EQ_25(
        EE: dict,
        C_max: int
):
    global n
    for i in range(1, n + 1):
        if C_max >= EE[i][S_i[i]]:
            continue
        else:
            return False

    return True


# def EQ_26(
#         B: dict
# ):
#     global n
#     global r
#     res_B = 0
#     for i in range(1, n + 1):
#         res_B += B[i][1]
#     if res_B >


# def EQ_27(
#         EE: dict,
#         B: dict,
#         X: dict
# ):
#     try:
#         global n
#         global S_i
#         global m
#         global trans
#         for i in range(1, n + 1):
#             for j in range(1, S_i[i]):
#                 for k in range(1, m + 1):
#                     for k_prime in range(1, m + 1):
#                         if EE[i][j] + trans[i][k][k_prime] <= B[i + 1][j] - Pt[i][j][k] + M * (1 - X[i][j][k][k_prime]):
#                             continue
#                         else:
#                             return False
#     except:
#         return False
#
#     return True


def EQ_28(
        B: dict,
        S: dict
):
    global n
    global S_i
    global m
    global p_k
    for i in range(1, n + 1):
        for j in range(1, S_i[i] + 1):
            for k in range(1, m + 1):
                for t in range(1, p_k[k] + 1):
                    if B[i][j] >= 0 and S[k][t] >= 0:
                        continue
                    else:
                        return False

    return True


def new_nest_dict(m):
    for val in m.values():
        if isinstance(val, dict):
            yield from new_nest_dict(val)
        else:
            yield val


def B_checking(B):
    """Checking that all B values are not 0"""
    B_vals = list(new_nest_dict(B))
    for val in B_vals:
        if val == 0:
            return False

    return True


def check_all_constraints(
        X: dict,
        Y: dict,
        Z: dict,
        B: dict,
        S: dict,
        F: dict,
        EE: dict,
        C_max: int
):
    const_err = {
        0: 'EQ_9',
        1: 'EQ_11',
        2: 'EQ_12',
        3: 'EQ_15',
        4: 'EQ_16',
        # 5: 'EQ_17',
        # 5: 'EQ_18',
        5: 'EQ_19',
        6: 'EQ_20',
        7: 'EQ_21',
        8: 'EQ_22',
        9: 'EQ_23',
        10: 'EQ_24',
        11: 'EQ_25',
        # 14: 'EQ_27',
        12: 'EQ_28',
        13: "B_NULL"
    }
    constraints = [EQ_9(X),
                   EQ_11(X, Y),
                   EQ_12(Y, X),
                   EQ_15(Y),
                   EQ_16(Y),
                   # EQ_17(EE, B, X),
                   # EQ_18(F, S, Y),
                   EQ_19(S, B, Y),
                   EQ_20(S, B, Y),
                   EQ_21(S, F, Z),
                   EQ_22(S, F, Z),
                   EQ_23(F, S),
                   EQ_24(EE, B),
                   EQ_25(EE, C_max),
                   # EQ_27(EE, B, X),
                   EQ_28(B, S),
                   B_checking(B)
                   ]
    if all(constraints):
        return True, True
    else:
        list_exceptions = []
        for i, cons in enumerate(constraints):
            if not cons:
                list_exceptions.append(const_err[i])
        return list_exceptions, False
