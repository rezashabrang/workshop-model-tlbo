from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent / 'MODEL'))
from MODEL.model import TEC
from MODEL.model import check_all_constraints
from initialization import X, Y, Z

print(X)
