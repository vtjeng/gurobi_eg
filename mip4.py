#!/usr/bin/python

# Copyright 2016, Gurobi Optimization, Inc.

# Modifying http://www.gurobi.com/documentation/7.0/examples/mip1_py.html

from gurobipy import *
import numpy as np

def add_conv2d_constraint(model, input, output, weights):
    """

    :param model:
    :param input: Tensor of size (width, height, num_input_channels)
    :param output: Tensor of size (width, height, num_output_channels)
    :param weights: Tensor of size (kernel_width, kernel_height, num_input_channels, num_output_channels). Must match input.
    :return:
    """
    # We determine the input dimensions by checking the maximum key seen. This is slightly
    # hacky, but we're expecting the input to have been of the form that would be generated
    # by model.addVars
    (width, height, num_in_channels) = map(lambda x: x+1, max(input.keys()))
    w = np.array(weights)
    (kernel_width, kernel_height, wq, num_out_channels) = w.shape
    assert(wq==num_in_channels, "Number of input channels in input and weights do not match.")
    nx = (kernel_width-1)//2
    ny = (kernel_height-1)//2
    # TODO: May want to change to addConstrs for performance reasons.
    # TODO: Add name to constraint, and consider whether the function should return
    for i in range(width):
        for j in range(height):
            for k in range(num_out_channels):
                d = tupledict()
                for u in range(-nx, nx+1):
                    for v in range(-ny, ny+1):
                        for z in range(num_in_channels):
                            d[i+u,j+v,z] = w[nx+u, ny+v, z, k]
                model.addConstr(output[i, j, k], GRB.EQUAL, input.prod(d))

# TODO: Write ReLU function
# TODO: Write max-pooling function
# TODO: Investigate re-indexing - is there a significant cost?
# TODO: Investigate matrix multiplication constraint

try:

    # Create a new model
    m = Model("mip1")

    ni = 3
    nj = 3
    s = m.addVars(ni, nj, 1, name="s")
    t = m.addVars(ni, nj, 1, name="t")

    # Set objective
    m.setObjective(s[0,0,0] + s[0,1,0] + 3 * s[1,0,0] + s[1,1,0] + s[2,0,0] + s[2,1,0], GRB.MAXIMIZE)

    # Add constraint: x + y >= 1
    m.addConstr(s[1,0,0] <= 1, "c1")

    # m.addConstr(s[0,0,0] + s[0,1,0] + s[1,0,0] + s[1,1,0] <= 5, "c2")
    # m.addConstr(s[1,0,0] + s[1,1,0] + s[2,0,0] + s[2,1,0] <= 5, "c2")

    convKernel = [[[[1]], [[1]], [[1]]], [[[1]], [[1]], [[1]]], [[[1]], [[1]], [[1]]]]
    add_conv2d_constraint(m, s, t, convKernel)
    m.addConstr(t[0,0,0] <= 5)
    m.addConstr(t[2,0,0] <= 5)


    m.optimize()

    for v in m.getVars():
        print('%s %g' % (v.varName, v.x))

    print('Obj: %g' % m.objVal)

except GurobiError as e:
    print('Error code ' + str(e.errno) + ": " + str(e))

except AttributeError:
    print('Encountered an attribute error')