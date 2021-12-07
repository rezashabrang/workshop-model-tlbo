import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent / 'MODEL'))
from initialization import generate_initial_randoms
from MODEL.model import check_all_constraints
from collections import Counter
from pprint import pprint

exceptions = []
for i in range(1000):
    X, Y, Z, B, EE, S, F, C_max = generate_initial_randoms()
    list_exc, situation = check_all_constraints(X, Y, Z, B, S, F, EE, C_max)
    for item in list_exc:
        exceptions.append(item)
    if situation:
        print("PASHMAM Found an answer")
        break
    else:
        print('GOING ON')
    # print('-------------- EE -------------- ')
    # pprint(EE)
    # print('------------- F -------------- ')
    # pprint(F)
    print('------------- Y -------------- ')
    pprint(Y)


print(Counter(exceptions))