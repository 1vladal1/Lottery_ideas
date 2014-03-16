#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#import ualottery
import collections

def zeros(line):
    result = []
    k = 0
    for item in line:
        if item == 0:
            k += 1
        else:
            result.append(k)
            k = 0
    return result

def vector_without_last_zeros(vector):
    result = []
    for i in range(1, len(vector)):
        if vector[-i:][0] != 0:
            if i > 1:
                result = vector[:-i+1]
            else:
                result = vector
            break
    return result

def last_zeros(vector):
    for i in range(1, len(vector)):
        if vector[-i:][0] != 0:
            result = i-1
            break
    return result

def v_sum(list_arr):
    if type(list_arr[0]) is int:
        result = sum(list_arr)
        return result
    else:
        result = [0 for i in range(0, len(list_arr[0]))]
        for item_i in list_arr:
            k = 0
            for item in item_i:
                result[k] += item
                k += 1
        return tuple(result)

def h_sum(list_arr):
    result = []
    for item in list_arr:
        result.append(sum(item))
    return tuple(result)

def min_avg_max(list_arr):
    result = {"min": 1000, "avg": 0.0, "max": 0}
    for item in list_arr:
        if result["min"] > sum(item):
            result["min"] = sum(item)
        if result["max"] < sum(item):
            result["max"] = sum(item)
        result["avg"] += sum(item)
    result["avg"] = 1.0 * result["avg"] / len(list_arr)
    return result

def get_next_by_pattern(vector, pattern):
    result = collections.Counter()
    lp = len(pattern)
    for i in range(0, len(vector)-lp):
        if  vector[i:i+lp] == pattern:
            result.update(str(vector[i+lp]))
    return result

def get_next_by_pattern_vect(vector, pattern):
    result = tuple()
    lp = len(pattern)
    for i in range(0, len(vector)-lp):
        if  vector[i:i+lp] == pattern:
            result +=(vector[i+lp],)
    return result

def get_pattern_next(vector, pattern):
    result = tuple()
    lp = len(pattern)
    for i in range(0, len(vector)-lp):
        if  vector[i:i+lp] == pattern:
            result += (vector[i:i+lp+1],)
    #result += pattern
    return result

def get_col(arr, col):
    result = ()
    for vector in arr:
        result += (vector[col-1], )
    return result

def nevypad_stat(vector):
    result = collections.Counter()
    tmp = ()
    flag = False
    for item in vector:
        if item == 0 and not flag:
            tmp += (item, )
        elif item == 0 and flag:
            if len(tmp) != 0:
                result.update((tmp,))
                tmp = ()
                tmp += (item, )
                flag = False
        if item == 1 and not flag:
            if len(tmp) != 0:
                result.update((tmp,))
                tmp = ()
                tmp += (item, )
                flag = True
        elif item == 1 and flag:
            tmp += (item, )

    return result

def vector_stat(vector):
    result = collections.Counter()
    for item in vector:
        result.update((item, ))
    return result

def predict(lottery, window, threshold=5, porog=1):
    result = []
    compare = lottery.compare_tirazhs_in_lottery(window)
    last_tirazh = lottery.results[-window:][0]

    for col in range(1, len(compare[0])+1):
        vector = get_col(compare, col)
        tmp = []
        for i in range(0, 40):
            pattern = tuple(vector[-40+i:])
            next_ = get_next_by_pattern(vector, pattern)
            if len(next_) > 0 and next_["1"] >= porog and next_["0"] == 0:
                tmp.append({"pattern_length": len(pattern), "counter": next_,
                            "col": col, "ball": last_tirazh.balls[col-1],
                            "tirazh": last_tirazh.number, "window": window})
        if len(tmp) >= threshold:
            result.append(tmp)
    return result