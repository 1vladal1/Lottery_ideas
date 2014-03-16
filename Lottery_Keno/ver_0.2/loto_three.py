#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ualottery
import statistics
import activelezi
import collections
import binominal
import itertools
import math
import pylab
import random

def convert(vector, *args):
    result = []
    for item in vector:
        if item in args:
            result.append(1)
        else:
            result.append(0)
    return result

def conv_var(results, variant):
    result = []
    for tirazh in results:
        if variant == tuple(tirazh.balls):
            result.append(1)
        else:
            result.append(0)
    return result

def get_d(tv, tirazh):
    flag = False
    date = tirazh.date.split("-")
    for hour in range(22,24):
        if flag:
            break
        for minute in range(60):
            if flag:
                break
            for second in range(60):
                d = (int(date[0]), int(date[1]), int(date[2]), hour, minute, second)
                random.seed(d)
                r = random.choice(tv)
                if r == tirazh.balls:
                    flag = True
                    break
    return d

def get_k(tv, tirazh):
    date = tirazh.date.split("-")
    k = 0
    r = 0
    d = (int(date[0]), int(date[1]), int(date[2]))
    random.seed(d)
    while r != tirazh.balls:
        r = random.choice(tv)
        k += 1
    return k

def get_k2(tv, tirazh1, tirazh2):
    date = tirazh1.date.split("-")
    k1 = 0
    r = 0
    d = (int(date[0]), int(date[1]), int(date[2]))
    random.seed(d)
    while r != tirazh1.balls:
        r = random.choice(tv)
        k1 += 1
    r = 0
    k2 = 0
    while r != tirazh2.balls:
        r = random.choice(tv)
        k2 += 1
    return (k1, k2)

def main():
    basis_lottery = ualottery.UALottery("loto_three_results.csv")
    filter1 = ualottery.LotteryFilter(None, None)
    #filter1.add("А", 1)
    #filter1.moveto(0,10)
    #filter1.delete()
    #filter1.show()
    lottery = basis_lottery.get_lottery_by_filter(filter1)
    #lottery.view_info()

    #s = "IT WILL BE PROVEN IN A NEXT PAPER THAT PATTERN MATCHING PREDICTORS ARE ALL ASYMPTOTICALLY LOCALLY OPTIMAL FOR A VERY LARGE CLASS OF RANDOM SOURCES (MIXING MODEL) THE AIM OF THIS SHORT NOTE IS TO PROVE THAT LEFT PATTERN MATCHING PREDICTOR IS GLOBALLY PERFECT (AND THEREFORE OPTIMAL) FOR BERNOULLI MODEL AND RIGHT PATTERN MATCHING PREDICTOR IS NOT"
    #balls = lottery.get_balls_in_column(0)
    #vector = convert(balls,3)

    for item in lottery.results:
        print(item)
    print()
    variants = itertools.product(range(10),repeat=3)
    tv = tuple(variants)
    print(get_k(tv, lottery.results[-3:][0]))
    print(get_k(tv, lottery.results[-2:][0]))
    print(get_k2(tv, lottery.results[-3:][0], lottery.results[-2:][0]))

    exit()

    vector = []
    for i in range(3000, lottery.length-1):
        d = get_k(tv, lottery.results[i])
        random.seed(d)
        r = random.choice(tv)
        #print(d, r)
        k = 0
        while r != lottery.results[i+1].balls:
            k += 1
            r = random.choice(tv)
        vector.append(k)

    print(len(vector))
    print(vector)
    print(collections.Counter(vector).most_common())

        #print(d, r, result.balls)

    print("Done!")

main()