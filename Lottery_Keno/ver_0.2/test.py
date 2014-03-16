#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ualottery
import statistics
import collections
import math
import decimal
import binominal
import binregister
import random
import pylab
import ctw

LOTTERY_FILE_NAME = "/home/vlad/PythonProjects/Lottery_Keno/ver_0.2/keno.csv"

basis_ltr = ualottery.UALottery(LOTTERY_FILE_NAME)

print("______________________________________________________________________")
print("-= BASIC INFORMATION ABOUT LOTTERY =-")
print("min_ball      ", basis_ltr.min_ball)
print("max_ball      ", basis_ltr.max_ball)
print("tirazh_length ", basis_ltr.tirazh_length)
print("lottery_length", basis_ltr.length)
print("is_sort       ", basis_ltr.is_sort)
print("")
print("Last Tirazh in basis lottery is:")
print(basis_ltr.results[-1:][0])
print("______________________________________________________________________")

filter1 = ualottery.LotteryFilter(None, basis_ltr.length)
#filter1.add("Б", 2)
#filter1.moveto(0,10)
#filter1.delete(0)
filter1.show()

f_ltr = basis_ltr.get_lottery_by_filter(filter1)
#f_ltr.sort()

last_tirazh = f_ltr.results[-1:][0]
print("Last tirazh in filtred lottery is:")
print(last_tirazh)
print("")

compare1 = f_ltr.compare_tirazhs_in_lottery()
compare2 = f_ltr.compare_tirazhs_with_last()

print("compare1", statistics.min_avg_max(compare1))
print("compare2", statistics.min_avg_max(compare2))
print("")

stat1 = statistics.vector_stat(statistics.h_sum(compare1))
stat2 = statistics.vector_stat(statistics.h_sum(compare2))

for item in stat1:
    s = "|" * 1 * int(stat1[item]/50.0)
    print(item, stat1[item], s)
print("")

for item in stat2:
    s = "|" * 1 * int(stat2[item]/50.0)
    print(item, stat2[item], s)
print("")

#for row in compare1:
#    print(row, sum(row))
#print("")

#for col in range(1, f_ltr.tirazh_length+1):
#    vector = statistics.get_col(compare1, col)
#vector = []
#for line in compare1:
#    for item in line:
#        vector.append(item)
#print(len(vector))
#learn = tuple(vector[:4000])
#test = tuple(vector[4000:])
#for i in range(1):
"""
    depth = 1
    zr = True
    learn = vector[:len(vector)-depth-1]
    test = vector[len(vector)-depth-1:]
    eps = 1/pow(len(learn), 0.5)
    tree = ctw.CTWTree()

    for i in range(len(learn)-depth):
        context = learn[i:i+depth]
        bit = learn[i+depth]
        tree.update(context, bit, zr)

    win1 = 0
    win0 = 0
    hardfail = 0
    softfail = 0

    for i in range(len(test)-depth):
        context = test[i:i+depth]
        bit = test[i+depth]
        predict = tree.predict(context, eps, zr)
        if predict == bit == 1:
            win1 += 1
        elif predict == bit == 0:
            win0 += 1
        elif predict == 1 and bit == 0:
            hardfail += 1
        elif predict == 0 and bit == 1:
            softfail += 1
        print(i+1, win0, win1, softfail, "H", hardfail, "Win", win0+win1, "Fail", softfail+hardfail, predict, bit, depth)
#print("SUM", sum(test[depth:]), win1/sum(test[depth:]), (win1+win0)/len(test[depth:]), len(test[depth:]))
#    print(tree.size())
    tree = None
    vector = None
    learn = None
    test = None
#tree.printInOrder()
#print(tree.predict((0,0,1), eps, zr))"""