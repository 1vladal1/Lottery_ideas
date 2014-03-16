#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class BWT(object):
    def __init__(self, data):
        self.data = data
        self.index = None

    def shift(self):
        result = []
        tmp = self.data
        for i in range(len(self.data)):
            result.append(tmp)
            tmp = tmp[1:]+tmp[0]
        return result

    def proceed(self):
        array = self.shift()
        array.sort()
        self.index = array.index(self.data)
        result = []
        for item in array:
            result.append(item[-1:])

        return result

def main():
    test_str = "aaababbbbbaabccddcbaaaa"
    bwt = BWT(test_str)
    print()
    res = bwt.proceed()
    print(res, bwt.index)

#main()