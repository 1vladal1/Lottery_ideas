#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def is_exist_pattern(vector, pattern):
    result = False
    for i in range(len(vector)-len(pattern)):
        if vector[i:i+len(pattern)] == pattern:
            result = True
            break
    return result

def value(vector, pattern):
    for i in range(len(vector)-len(pattern)):
        if vector[i:i+len(pattern)] == pattern:
            result = vector[i+len(pattern)]
            break
    return result

def next_value(vector):
    flag = False
    for i in range(1,len(vector)+1):
        pattern = vector[-i:]
        if not is_exist_pattern(vector, pattern) and not flag:
            result = vector[1]
            break
        elif is_exist_pattern(vector, pattern):
            flag = True
            tmp = pattern
        elif not is_exist_pattern(vector, pattern) and flag:
            break
    if flag:
        result = value(vector, tmp)
    else:
        result = vector[1]
    return result


def main():
    s = "IT WILL BE PROVEN IN A NEXT PAPER THAT PATTERN MATCHING PREDICTORS ARE ALL ASYMPTOTICALLY LOCALLY OPTIMAL FOR A VERY LARGE CLASS OF RANDOM SOURCES (MIXING MODEL) THE AIM OF THIS SHORT NOTE IS TO PROVE THAT LEFT PATTERN MATCHING PREDICTOR IS GLOBALLY PERFECT (AND THEREFORE OPTIMAL) FOR BERNOULLI MODEL AND RIGHT PATTERN MATCHING PREDICTOR IS NOT"
    k = 0
    print(s)
    for i in range(len(s)-3):
        if s[3+i] == next_value(s[:3+i]):
            k += 1
        print(s[3+i], next_value(s[:3+i]))
    print(k, len(s), k/len(s))

#main()