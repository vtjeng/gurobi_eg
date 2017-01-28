from gurobipy import *
import numpy as np

try:

    # Create a new model
    m = Model("mip1")

    s = m.addVars(2, 2, name="s", lb=-GRB.INFINITY)

    m.setObjective(7*s[0,0]+3*s[0,1]+7*s[1,0]+3*s[1,1], GRB.MAXIMIZE)

    m.addConstr(2 * s[0, 0] + 3 * s[0, 1], GRB.LESS_EQUAL, 28)
    m.addConstr(2 * s[1, 0] + 3 * s[1, 1], GRB.LESS_EQUAL, 38)
    m.addConstr(-1 * s[0, 0] - 4 * s[0, 1], GRB.LESS_EQUAL, -29)
    m.addConstr(-1 * s[1, 0] - 4 * s[1, 1], GRB.LESS_EQUAL, -39)

    m.optimize()

    for v in m.getVars():
        print('%s %g' % (v.varName, v.x))

    print('Obj: %g' % m.objVal)

except GurobiError as e:
    print('Error code ' + str(e.errno) + ": " + str(e))

except AttributeError:
    print('Encountered an attribute error')