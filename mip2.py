#!/usr/bin/python

# Copyright 2016, Gurobi Optimization, Inc.

# Modifying http://www.gurobi.com/documentation/7.0/examples/mip1_py.html

from gurobipy import *
import numpy as np

try:

    # Create a new model
    m = Model("mip1")
    
    # Create variables
    # s[0] = m.addVar(name="x")
    # s[1] = m.addVar(name="y")
    # s[2] = m.addVar(name="z")

    s = []

    s.append(m.addVar(name="x"))
    s.append(m.addVar(name="y"))
    s.append(m.addVar(name="z"))

    # Set objective
    m.setObjective(s[0] + s[1] + 2 * s[2], GRB.MAXIMIZE)

    # Add constraint: x + 2 y + 3 z <= 4
    # m.addConstr(s[0] + 2 * s[1] + 3 * s[2] <= 4, "c0")

    # Add constraint: x + y >= 1
    m.addConstr(s[0] + s[1] >= 1, "c1")

    # Add constraint: x + y + z >= 5
    m.addConstr(LinExpr([1, 1, 1], s) <= 2.5, "c2")

    m.optimize()

    for v in m.getVars():
        print('%s %g' % (v.varName, v.x))

    print('Obj: %g' % m.objVal)

except GurobiError as e:
    print('Error code ' + str(e.errno) + ": " + str(e))

except AttributeError:
    print('Encountered an attribute error')