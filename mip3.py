#!/usr/bin/python

# Copyright 2016, Gurobi Optimization, Inc.

# Modifying http://www.gurobi.com/documentation/7.0/examples/mip1_py.html

from gurobipy import *
import numpy as np

try:

    # Create a new model
    m = Model("mip1")

    pad = 1 #zero padding of one on either side.
    ni = 3
    nj = 3
    s = []
    for i in range(ni):
        t = []
        for j in range(nj):
            t.append(m.addVar(name="v{},{}".format(i, j)))
        s.append(t)

    # Set objective
    m.setObjective(s[0][0] + s[0][1] + 3 * s[1][0] + s[1][1] + s[2][0] + s[2][1], GRB.MAXIMIZE)

    # Add constraint: x + y >= 1
    m.addConstr(s[1][0] <= 1, "c1")

    m.addConstr(s[0][0] + s[0][1] + s[1][0] + s[1][1] <= 5, "c2")
    m.addConstr(s[1][0] + s[1][1] + s[2][0] + s[2][1] <= 5, "c2")

    convKernel = [[1, 1, 1], [1, 1, 1]]

    m.optimize()

    for v in m.getVars():
        print('%s %g' % (v.varName, v.x))

    print('Obj: %g' % m.objVal)

except GurobiError as e:
    print('Error code ' + str(e.errno) + ": " + str(e))

except AttributeError:
    print('Encountered an attribute error')