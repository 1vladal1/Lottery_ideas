#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import operator
import collections
import numpy.linalg

def binreg_matrix(vector):
    matrix = []
    b = []
    for i in range(0, int(len(vector)/2)):
        matrix.append(vector[i:int(i+len(vector)/2)])
        b.append(vector[int(i+len(vector)/2): int(i+len(vector)/2)+1])
    """i = 0
    for item in matrix:
        print(item, b[i])
        i += 1"""
    solve = numpy.linalg.solve(matrix, b)
    #for item in solve:
    #    print(item)
    #print(len(solve))
    return solve

def binreg(initial):
    c = [1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1]
    result = None
    for i in range(0, len(c)):
        if c[i] == 1 and result is None:
            result = c[i]
        elif c[i] == 1:
            result = operator.xor(result, initial[i])
    return result

def main():
    result = []
    initial = [1,0,0,0,0,0,0,1,0,0,1,1,0,0,0,0]
    for i in range(0, 2*(pow(2,len(initial))-1)):
        right = binreg(initial)
        result.append(initial[0])
        initial = initial[1:]
        initial.append(right)
        #print(initial, "-->", result[i], len(result))
    #print(initial, "-->", result, len(result))
    col = collections.Counter()
    col.update(result)
    print(col)

#main()

