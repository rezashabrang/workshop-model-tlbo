import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / 'MODEL'))
sys.path.append(str(Path(__file__).parent.parent / 'TLBO'))
from MODEL.model import (n, S_i, m, p_k)
from ga_initialization import Genome

from random import random
from random import randint
from typing import List


def selection(
        population: List[Genome],
        n_selection: int
):
    """Random selection
    :param population: Whole population list.
    :param n_selection: Number of parents to be chosen.
    :return: List of randomly selected parents.
    """
    # -------------------- Initializing --------------------
    selected_indices = []
    list_selected = []

    # -------------------- Selection --------------------
    while len(list_selected) < n_selection:
        random_index = randint(0, len(population) + 1)
        if random_index not in selected_indices:
            list_selected.append(population[random_index])
            selected_indices.append(random_index)

    return list_selected


# crossover two parents to create two children
def crossover(
        p1: Genome,
        p2: Genome
):
    # children are copies of parents by default
    c1, c2 = p1.VARS(), p2.copy()
    # select crossover point that is not on the end of the string
    pt = randint(1, len(p1) - 2)
    # perform crossover
    c1 = p1[:pt] + p2[pt:]
    c2 = p2[:pt] + p1[pt:]
    return [c1, c2]


def mutation(bitstring, r_mut):
    for i in range(len(bitstring)):
        # check for a mutation
        if random() < r_mut:
            # flip the bit
            bitstring[i] = 1 - bitstring[i]
    return bitstring


