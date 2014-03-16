#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ualottery
import statistics
import activelezi
import collections
import binominal
import itertools
import math


def bits2bytes(bits):
    b = []
    i = 0
    while (i+8<=len(bits)):
        byte = bits[i:i+8]
        s = "0b"
        for bit in byte:
            s += str(bit)
        b.append(bytes([int(s,2)]))
        i += 8

    if i<len(bits):
        s = "0b"
        for k in range(i+8-len(bits)):
            s += str(0)
        byte = bits[i:len(bits)]
        for bit in byte:
            s += str(bit)

        b.append(bytes([int(s,2)]))
    return b

def compute(vector, pattern):
    result = statistics.get_next_by_pattern_vect(vector, pattern)
    print(result, len(result))
    print(collections.Counter(result))
    print()
    return result


def main():
    basis_lottery = ualottery.UALottery("keno_results.csv")
    #basis_lottery = ualottery.UALottery("SuperLoto_Results.csv")
    filter1 = ualottery.LotteryFilter(None, None)
    #filter1.add("А", 4)
    #filter1.moveto(0,10)
    #filter1.delete()
    filter1.show()
    lottery = basis_lottery.get_lottery_by_filter(filter1)
    lottery.sort()
    lottery.view_info()
    lmap = lottery.lottery_map()
    vector = []
    """for line in lmap:
        for item in line:
            vector.append(item)
    bernoulli = binominal.Bernoulli(vector)
    print(bernoulli.p)
    for i in range(lottery.tirazh_length):
        print(i+1, bernoulli.most_probable_number_of_experiment(i+1))
    print(bernoulli.number_of_experiments_with_Pz(0.8))
    print(statistics.get_next_by_pattern(vector, vector[-18:]))
    print(vector[-80:])"""
    result = []
    for window in range(1, 2):
        #lmap = lottery.compare_tirazhs_in_lottery(window)
        for col in range(len(lmap[0])):
            if len(lmap[0]) == lottery.tirazh_length:
                print("--------", col+1, "----------","[",lottery.results[-window:][0].balls[col],"]")
            else:
                print("--------", col+1, "----------")
            vector = statistics.vector_without_last_zeros(statistics.get_col(lmap, col+1))
            bernoulli = binominal.Bernoulli(vector)
            lenvect = len(vector)
            numb_of_exper = bernoulli.most_probable_number_of_experiment(1)
            numb_with_pz = math.ceil(bernoulli.number_of_experiments_with_Pz(0.8))
            print(lenvect, sum(vector), bernoulli.p,
                  len(vector)+math.ceil(numb_of_exper[0]),":",
                  len(vector)+int(numb_of_exper[1]),
                  len(vector)+numb_with_pz)
            print(bernoulli.most_probable_number_of_experiment(1))
            print(bernoulli.most_probable_number_of_success(3))
            print(bernoulli.most_probable_number_of_success(4))
            print(bernoulli.most_probable_number_of_success(5))
            print(bernoulli.most_probable_number_of_success(6))
            print(bernoulli.most_probable_number_of_success(7))
        #print()
            print(numb_with_pz)
            print()
        #if (len(vector)+numb_with_pz <= lottery.length+1) or (
        #    len(vector)+int(numb_of_exper[1]) <= lottery.length+1):
            if lottery.length+1-window+1 - (lenvect+int(numb_of_exper[1])) >= 4:
                if len(lmap[0]) == lottery.tirazh_length:
                    result.append(lottery.results[-window:][0].balls[col])
                else:
                    result.append(col+1)
    print(sorted(result), len(result))
    print(sorted(collections.Counter(result)), len(sorted(collections.Counter(result))))


    print("Done!")

main()
