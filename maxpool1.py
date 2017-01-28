from gurobipy import *
import numpy as np

try:

    # Create a new model
    m = Model("mip1")

    s = m.addVars(4, 4, name="s", lb=-GRB.INFINITY)
    t = m.addVars(2, 2, name="t", lb=-GRB.INFINITY)

    m.addGenConstrMin(t[0, 0], [s[0, 0], s[0, 1], s[1, 0], s[1, 1]])
    m.addGenConstrMin(t[0, 1], [s[0, 2], s[0, 3], s[1, 2], s[1, 3]])
    m.addGenConstrMin(t[1, 0], [s[2, 0], s[2, 1], s[3, 0], s[3, 1]])
    m.addGenConstrMin(t[1, 1], [s[2, 2], s[2, 3], s[3, 2], s[3, 3]])

    m.setObjective(t[0,0]+t[0,1]+t[1,0]+t[1,1], GRB.MAXIMIZE)
    # m.setObjective(1*t[0,0]+2*t[0,1]+3*t[1,0]+4*t[1,1], GRB.MAXIMIZE)

    m.addConstr(s[0, 0] + s[0, 1] + s[0, 2] + s[0, 3], GRB.LESS_EQUAL, 14)
    m.addConstr(s[2, 0] + s[2, 1] + s[2, 2] + s[2, 3], GRB.LESS_EQUAL, 6)
    m.addConstr(s[0, 0] + s[1, 0] + s[2, 0] + s[3, 0], GRB.LESS_EQUAL, 12)

    m.addConstr(s[0, 0] + s[1, 1] + s[2, 2] + s[3, 3], GRB.LESS_EQUAL, 10)
    m.addConstr(s[1, 0] + s[2, 1] + s[3, 2] + s[0, 3], GRB.LESS_EQUAL, 10)
    m.addConstr(s[2, 0] + s[3, 1] + s[0, 2] + s[1, 3], GRB.LESS_EQUAL, 10)
    m.addConstr(s[3, 0] + s[0, 1] + s[1, 2] + s[2, 3], GRB.LESS_EQUAL, 10)


    m.optimize()

    for v in m.getVars():
        print('%s %g' % (v.varName, v.x))

    print('Obj: %g' % m.objVal)

except GurobiError as e:
    print('Error code ' + str(e.errno) + ": " + str(e))

except AttributeError:
    print('Encountered an attribute error')