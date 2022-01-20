import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / 'MODEL'))
sys.path.append(str(Path(__file__).parent.parent / 'TLBO'))

from TLBO.algorithm import Student
from MODEL.model import TEC
from tqdm import tqdm


# Creating Genome class (Population)
class Genome(Student):
    def __init__(self):
        super(Genome, self).__init__()

    def tec(self):
        new_fitness = TEC(
            self.VARS["C_max"],
            self.VARS["Z"],
            self.VARS["S"],
            self.VARS["F"],
            self.VARS["X"],
        )
        self.FITNESS = new_fitness
        return new_fitness


if __name__ == "__main__":
    n = 1  # Population size
    population = [Genome() for j in tqdm(range(n), desc='Population generation')]  # Population initialization
    print(population[0].tec())
