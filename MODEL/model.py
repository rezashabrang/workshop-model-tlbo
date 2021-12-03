from formulas import (
    create_energy_cost_matrix,
    create_energy_time_matrix,
    generate_r,
    generate_pidle,
    generate_energy
)

# ------------- Global Parameters -------------
P0 = 10  # General consumed energy per time unit
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


def EQ_10(X: dict):
    # TODO complete later
    global m
    global n
    res = 0
    for i in range(1, n + 1):
        for k in range(1, m + 1):
            res += X[i][1][k][k]
    pass


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

def EQ_12():
    pass


def EQ_15():
    pass


def EQ_16():
    pass


def EQ_17():
    pass


def EQ_18():
    pass


def EQ_19():
    pass


def EQ_20():
    pass


def EQ_21():
    pass


def EQ_22():
    pass


def EQ_23():
    pass


def EQ_24():
    pass


def EQ_25():
    pass


def EQ_26():
    pass


def EQ_27():
    pass


def EQ_28():
    pass


def check_all_constraints():
    if EQ_9() and EQ_10() and EQ_11() and EQ_12() and EQ_15() and EQ_16() and EQ_17() and EQ_18() and EQ_19() and EQ_20() and EQ_21() and EQ_22() and EQ_23() and EQ_24() and EQ_25() and EQ_26() and EQ_27() and EQ_28():
        return True

    return False
