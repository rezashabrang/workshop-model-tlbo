from tqdm import tqdm
from ga_initialization import Genome
from ga_helper_functions import selection, crossover, mutation
from pprint import pprint

if __name__ == "__main__":
    # ----------------- Globals -----------------
    n_pop = 20  # Population size
    n_selection = 10  # Selection size (children size)
    crossover_rate = 0.1  # Rate of crossover
    mutation_rate = 0.01  # Rate of mutation
    n_iteration = 3  # Number of times to iterate overall

    # ----------------- Initializing population -----------------
    population = [Genome() for j in tqdm(range(n_pop), desc='Population generation')]  # Population initialization
    for iteration in tqdm(range(n_iteration), position=0, leave=True, desc="Overall iteration"):

        # ----------------- Selecting parents -----------------
        parents = selection(population, n_selection)

        # ----------------- Altering Genomes -----------------
        children = []
        for i in range(0, n_selection - 2, 2):
            p1, p2 = parents[i], parents[i + 1]
            temp_children = []

            # Continue until two valid children are found from parents.
            while len(temp_children) < 2:
                # ------------------------- CROSS OVER -------------------------
                # Calculating cross over for X
                cx_1, cx_2 = crossover(
                    p1.flatted_X,
                    p2.flatted_X,
                    crossover_rate
                )

                # Calculating cross over for Y
                cy_1, cy_2 = crossover(
                    p1.flatted_Y,
                    p2.flatted_Y,
                    crossover_rate
                )

                # ------------------------- MUTATION -------------------------
                # X mutation
                p1.flatted_X = mutation(cx_1, mutation_rate)
                p2.flatted_X = mutation(cx_2, mutation_rate)
                # Y mutation
                p1.flatted_Y = mutation(cy_1, mutation_rate)
                p2.flatted_Y = mutation(cy_2, mutation_rate)

                # -------------- Result Generating & Checking Constraints --------------
                p1.generate_results()
                check_stat_p1 = p1.check_constraints()
                if check_stat_p1:
                    p1.tec()
                    temp_children.append(p1)
                    children.append(p1)

                p2.generate_results()
                check_stat_p2 = p2.check_constraints()
                if check_stat_p2:
                    p2.tec()
                    temp_children.append(p2)
                    children.append(p2)

        # Adding children to the population
        population += children

        # Sorting based on fitness
        population = sorted(population, key=lambda genom: genom.FITNESS)
        population = population[0:n_pop]


    # Outputing best results
    pprint(population[0].VARS)
    print(f"TEC = {population[0].FITNESS}")