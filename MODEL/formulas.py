import pandas as pd
from numpy.random import randint


def create_base_3d_matrix(i, j, k):
    matrix = {}
    for i in range(1, i + 1):
        matrix[i] = {}
        for j in range(1, j + 1):
            matrix[i][j] = {}
            for k in range(1, k + 1):
                matrix[i][j][k] = 0
    return matrix


def create_energy_cost_matrix(
        n: int,
        S_i: dict,
        p_k: dict,
):
    """
    Creating energy cost matrix for each (work, operation, machine) pair.
    :arg
        n: Number of works,
        S_i: Dictionary of operations per work,
        p_k: Dictionary of positions for each machine
    :return
        P_i_j_k: Dictionary of energy costs.
    """
    # TODO change the counter variable to a uniform dist
    P_i_j_k = {}
    counter = 1
    for i in range(1, n + 1):
        P_i_j_k[i] = {}
        for j in range(1, S_i[i] + 1):
            P_i_j_k[i][j] = {}
            for k in range(1, p_k[j] + 1):
                P_i_j_k[i][j][k] = counter
                counter += 1
    return P_i_j_k


def create_energy_time_matrix(
        n: int,
        S_i: dict,
        p_k: dict,
):
    """
    Fetching energy for each (work, operation, machine) pair
    and creating related dictionary
    :arg
        n: Number of works,
        S_i: Dictionary of operations per work,
        p_k: Dictionary of positions for each machine
    :return
        Pt_i_j_k: Dictionary of durations.
    """
    # Creating base dictionary
    Pt_i_j_k = create_energy_cost_matrix(n, S_i, p_k)

    Pt_df = pd.read_excel('glob_tables/Pt.xlsx')
    # Number of works
    n_works = len(Pt_df.columns) - 1
    for row in Pt_df.iterrows():
        # Removing index
        row = row[1]

        # Fetching k and j
        k, j = map(int, str(row['k.j/i']).split('.'))

        # Updating values in dictionary
        for i in range(1, n_works + 1):
            Pt_i_j_k[i][j][k] = row[i]

    return Pt_i_j_k


def create_trans_matrix(
        n: int,
        m: int
):
    """
    Creates transportation matrix
    :param n: number of works
    :param m: number of machines
    :return:
        Transportation dictionary.
    """
    trans_mat = create_base_3d_matrix(n, m, m)
    trans_df = pd.read_excel('glob_tables/Trans.xlsx')
    for row in trans_df.iterrows():
        # Removing index
        row = row[1]

        # Fetching k and k prime
        k, k_prime = map(int, str(row['k.k_prime/i']).split('.'))

        # Updating values in dictionary
        for i in range(1, n + 1):
            trans_mat[i][k][k_prime] = row[i]

    return trans_mat


def create_setup_matrix(
        n: int,
        S_i: dict,
        p_k: dict
):
    """
    Creating setup matrix
    :arg
        n: Number of works,
        S_i: Dictionary of operations per work,
        p_k: Dictionary of positions for each machine
    :return:
        Setup matrix
    """
    # Creating base dictionary
    st_mat = create_energy_cost_matrix(n, S_i, p_k)

    St_df = pd.read_excel('glob_tables/Setup.xlsx')
    # Number of works
    for row in St_df.iterrows():
        # Removing index
        row = row[1]

        # Fetching k and j
        j, k = map(int, str(row['j.k/i']).split('.'))

        # Updating values in dictionary
        for i in range(1, n + 1):
            st_mat[i][j][k] = row[i]

    return st_mat


def generate_r(n):
    """
    Clearance time
    :param n: Number of works
    :return: List of clearance time
    """
    r_dict = {
        1: 5,
        2: 3,
        3: 6
    }
    return r_dict


def generate_pidle(m):
    """
    Energy consumed during standby
    :param m: Number of machines
    :return:Dict of random energy unit.
    """
    pidle_dict = {}
    random_energy = randint(1, 4, size=m + 1)
    for k in range(1, m + 1):
        pidle_dict[k] = random_energy[k]
    return pidle_dict


def generate_O(m):
    """
    Time needed for turning on machine k
    :param m: Number of machines
    :return: Random O values
    """
    O_dict = {}
    random_O = randint(8, 17, size=m + 1)
    for k in range(1, m + 1):
        O_dict[k] = random_O[k]
    return O_dict


def generate_energy(m):
    """
    Energy needed for turning on/off machine k
    :param m: Number of machines
    :return: Random Energy values
    """
    energy_dict = {}
    random_energy = randint(10, 21, size=m + 1)
    for k in range(1, m + 1):
        energy_dict[k] = random_energy[k]
    return energy_dict


def generate_TB(
        O,
        Energy,
        Pidle,
        m
):
    """

    :param O:
    :param Energy:
    :param Pidle:
    :param m:
    :return:
    """
    TB_dict = {}
    for k in range(1, m + 1):
        TB_dict[k] = max(O[k], Energy[k] / Pidle[k])

    return TB_dict
