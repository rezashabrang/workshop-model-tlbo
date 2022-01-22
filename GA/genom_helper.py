import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / 'MODEL'))
sys.path.append(str(Path(__file__).parent.parent / 'TLBO'))
from MODEL.model import (n, S_i, m, p_k)


def encode_genome(
        X: list,
        Y: list
):
    """Packing genomes
    Passed args must be flatted."""
    packed_X = {}
    packed_Y = {}

    for i in range(1, n + 1):
        packed_X[i] = {}
        packed_Y[i] = {}
        for j in range(1, S_i[i] + 1):
            packed_X[i][j] = {}
            packed_Y[i][j] = {}
            for k in range(1, m + 1):
                packed_X[i][j][k] = {}
                packed_Y[i][j][k] = {}
                for k_prime in range(1, m + 1):
                    packed_X[i][j][k][k_prime] = X[(i - 1) * n * S_i[i] * m + (j - 1) * S_i[i] * m + (k - 1) * m + k_prime - 1]
                for t in range(1, p_k[k] + 1):
                    packed_Y[i][j][k][t] = Y[(i - 1) * n * S_i[i] * m + (j - 1) * S_i[i] * m + (k - 1) * m + t - 1]

    return packed_X, packed_Y


# For flattening X and Y
def decode_genome(
        X: dict,
        Y: dict
):
    """Flattening genomes"""
    flatted_X = []
    flatted_Y = []
    for i in range(1, n + 1):
        for j in range(1, S_i[i] + 1):
            for k in range(1, m + 1):
                for k_prime in range(1, m + 1):
                    flatted_X.append(
                        X[i][j][k][k_prime]
                    )
                for t in range(1, p_k[k] + 1):
                    flatted_Y.append(
                        Y[i][j][k][t]
                    )
    return flatted_X, flatted_Y
