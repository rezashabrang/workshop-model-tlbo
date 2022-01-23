from tqdm import tqdm
from ga_initialization import Genome
from ga_helper_functions import selection, crossover, mutation

if __name__ == "__main__":
    # ----------------- Globals -----------------
    n_pop = 10  # Population size
    n_selection = 4  # Selection size (children size)
    mutation_rate = 0.05  # Rate of mutation

    # ----------------- Initializing population -----------------
    population = [Genome() for j in tqdm(range(n_pop), desc='Population generation')]  # Population initialization

    # ----------------- Selecting parents -----------------
    parents = selection(population, n_selection)

    # ----------------- Cross over -----------------
    children = []
    for i in range(0, n_pop, 2):
        p1, p2 = parents[i], parents[i + 1]
        cx_1, cx_2 = crossover(
            p1.flatted_X,
            p2.flatted_X
        )

        cy_1, cy_2 = crossover(
            p1.flatted_Y,
            p2.flatted_Y
        )

        # crossover
        for c in crossover(p1, p2):
            # mutation
            mutation(c, mutation_rate)
