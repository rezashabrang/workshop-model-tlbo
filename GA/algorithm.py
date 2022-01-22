from tqdm import tqdm
from ga_initialization import Genome
from pprint import pprint

if __name__ == "__main__":
    n = 1  # Population size
    population = [Genome() for j in tqdm(range(n), desc='Population generation')]  # Population initialization
    X, Y = population[0].decode()
    print("============================== Flatted X ==============================")
    pprint(X)
    print("============================== Flatted Y ==============================")
    pprint(Y)

    X, Y = population[0].encode()
    print("============================== Packed X ==============================")
    pprint(X)
    print("============================== Packed Y ==============================")
    pprint(Y)


