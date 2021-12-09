import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / 'MODEL'))
import random
from MODEL.model import TEC
from initialization import generate_initial_randoms
from MODEL.model import check_all_constraints
from initialization import generate_empties
from tqdm import tqdm
from random_nudge import generate_new_sol
from pprint import pprint


# Student class
class Student:
    def __init__(self):
        while True:
            X, Y, Z, B, EE, S, F, C_max = generate_initial_randoms()
            list_exc, situation = check_all_constraints(X, Y, Z, B, S, F, EE, C_max)
            if situation:
                break

        self.VARS = {
            'X': X,
            'Y': Y,
            'Z': Z,
            'B': B,
            'S': S,
            'F': F,
            'EE': EE,
            'C_max': C_max
        }
        self.FITNESS = TEC(
            C_max, Z, S, F, X
        )


# --------------------- START OF TLBO ---------------------

# ------------------------ Initialization ------------------------
n = 5  # Number of students
n_iter = 20  # Number of iterations
FBest = sys.float_info.max  # Setting max number possible
C_max = 0  # End of the all works
X, Y, Z, B, S, F, EE = generate_empties()
VAR_Best = {
    'X': X,
    'Y': Y,
    'Z': Z,
    'B': B,
    'S': S,
    'F': F,
    'EE': EE,
    'C_max': C_max
}
classroom = [Student() for j in tqdm(range(n), desc='Initial Value Generation')]  # Classroom initialization
# Getting best X & TEC from students
for student in classroom:
    if student.FITNESS < FBest:
        FBest = student.FITNESS
        VAR_Best = student.VARS

# ------------------------ Main Loop ------------------------
for iteration in tqdm(range(n_iter), desc='Main Loop'):

    # for every student
    for i in range(n):
        # ------------- Teaching Phase -------------
        VAR_Teacher = VAR_Best
        FTeacher = FBest
        TF = random.randint(1, 3)
        TF_rand = 0.9 if TF == 2 else 0.6
        vars_new = generate_new_sol(
            VARS_ST=classroom[i].VARS,
            VARS_T=VAR_Teacher,
            random_val=TF_rand
        )
        new_fitness = TEC(
            C_max=vars_new['C_max'],
            Z=vars_new['Z'],
            F=vars_new['F'],
            X=vars_new['X'],
            S=vars_new['S']
        )
        if classroom[i].FITNESS < new_fitness:
            classroom[i].VARS = vars_new
            classroom[i].FITNESS = new_fitness

        # ------------- Partner Phase -------------
        # Partner Index
        p = random.randint(0, n - 1)
        while p != i:
            # If the partner TEC is better then generate new sol
            if classroom[p].FITNESS < classroom[i].FITNESS:
                vars_new = generate_new_sol(
                    VARS_ST=classroom[i].VARS,
                    VARS_T=VAR_Teacher,
                    random_val=random.random()
                )
                new_fitness = TEC(
                    C_max=vars_new['C_max'],
                    Z=vars_new['Z'],
                    F=vars_new['F'],
                    X=vars_new['X'],
                    S=vars_new['S']
                )
            if new_fitness < classroom[i].FITNESS:
                classroom[i].VARS = vars_new
                classroom[i].FITNESS = new_fitness
            p = random.randint(0, n - 1)

        if classroom[i].FITNESS < FBest:
            FBest = classroom[i].FITNESS
            VAR_Best = classroom[i].VARS

pprint(VAR_Best)
print(f'F BEST = {FBest}')
