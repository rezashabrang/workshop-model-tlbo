import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / 'MODEL'))
sys.path.append(str(Path(__file__).parent.parent / 'TLBO'))

from TLBO.algorithm import Student
from MODEL.model import TEC, n, S_i, m, p_k, check_all_constraints
from genom_helper import decode_genome, encode_genome
from TLBO.initialization import generate_ini_B_EE_S_F_Z, calculate_c_max, generate_empties


# Creating Genome class (Population)
class Genome(Student):
    def __init__(self):
        super(Genome, self).__init__()
        self.flatted_X = []
        self.flatted_Y = []
        self.tec()
        self.decode()

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

    def decode(self):
        """Flattening genom"""
        f_X, f_Y = decode_genome(
            self.VARS["X"],
            self.VARS["Y"],
        )
        self.flatted_X = f_X
        self.flatted_Y = f_Y
        return f_X, f_Y

    def encode(self):
        """Packing genome"""
        p_X, p_Y = encode_genome(
            self.flatted_X,
            self.flatted_Y
        )
        self.VARS["X"] = p_X
        self.VARS["Y"] = p_Y
        return p_X, p_Y

    def check_constraints(self):
        list_exc, check_res = check_all_constraints(
            X=self.VARS["X"],
            Y=self.VARS["Y"],
            Z=self.VARS["Z"],
            B=self.VARS["B"],
            S=self.VARS["S"],
            F=self.VARS["F"],
            EE=self.VARS["EE"],
            C_max=self.VARS["C_max"],
        )
        return check_res

    def generate_results(self):
        self.encode()
        dummy_X, dummy_Y, Z, B, S, F, EE = generate_empties()
        self.VARS["B"], self.VARS["EE"], self.VARS["S"], self.VARS["F"], self.VARS["Z"] = generate_ini_B_EE_S_F_Z(
            B=B,
            EE=EE,
            S=S,
            F=F,
            X=self.VARS["X"],
            Y=self.VARS["Y"],
            Z=Z,
        )
        self.VARS["C_max"] = calculate_c_max(EE)
