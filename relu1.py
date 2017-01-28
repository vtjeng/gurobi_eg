from gurobipy import *
import numpy as np

try:

    # Create a new model
    m = Model("mip1")

    s = m.addVars(2, name="s", lb=-GRB.INFINITY)
    t = m.addVars(2, name="t", lb=-GRB.INFINITY)
    u = m.addVars(2, name="u", lb=-GRB.INFINITY)

    m.addConstr(s[0] + 50, GRB.LESS_EQUAL, t[0])
    m.addConstr(s[1] + 100, GRB.LESS_EQUAL, t[1])

    m.addGenConstrMax(u[0], [t[0]], constant=0)
    m.addGenConstrMax(u[1], [t[1]], constant=0)

    m.setObjective(u[0]+u[1], GRB.MINIMIZE)

    m.optimize()

    for v in m.getVars():
        print('%s %g' % (v.varName, v.x))

    print('Obj: %g' % m.objVal)

except GurobiError as e:
    print('Error code ' + str(e.errno) + ": " + str(e))

except AttributeError:
    print('Encountered an attribute error')