#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import collections
import decimal

class LZ78(object):

    def __init__(self):
        self.dictionary = collections.Counter()
        self.sufixes = collections.Counter()
        self.string = tuple()
        self.max_lz_length = 0
        self.window = tuple()

    def add_symbol(self, symb):
        symb = tuple(symb)
        self.string += symb
        if self.string not in self.dictionary:
            self.dictionary[self.string] = 0
            if len(self.string) > self.max_lz_length:
                self.max_lz_length = len(self.string)
            self.string = tuple()

        self.window += symb
        if len(self.window) > self.max_lz_length:
            self.window = self.window[1:]
        for i in range(len(self.window)):
            self.sufixes[self.window[i:]] += 1

    def order(self):
        return self.max_lz_length - 1

    def child(self, parent=tuple()):
        result = collections.Counter()
        for item in list(self.sufixes):
            if item[:-1] == parent:
                result[item] = self.sufixes[item]
        if len(parent) > 0:
            lambda_count = self.sufixes[parent] - sum(result.values())
            result["lambda"] = lambda_count
        return result

    def get_sufix(self, window):
        return window[1:]

    def probability(self, symbol, window=None):
        if window is None:
            window = self.window
        if type(symbol) is not tuple:
            symbol = tuple(symbol)
        sufix = self.get_sufix(window)
        childs = self.child(sufix)
        if sufix == tuple():
            result = dec(self.sufixes[symbol])/dec(sum(childs.values()))
        else:
            result = dec(self.sufixes[sufix+symbol])/dec(self.sufixes[sufix])
            result += dec(childs["lambda"])/dec(self.sufixes[sufix]) * dec(self.probability(symbol, sufix))
        return dec(result)

def dec(number):
    return decimal.Decimal(number)

def main():
    s = ((0,),(0,),(0,),(1,),(0,),(0,),(0,))#"aaababbbbbaabccddcbaaaa"#"abababcdcbdab"#
    lz = LZ78()
    symbols = tuple()
    for symb in s:
        lz.add_symbol(symb)
        #print("sss", symb, lz.string)
        if symb not in symbols:
            symbols += (symb,)

    for symb in sorted(symbols):
        print(symb, lz.probability(symb))
    print(lz.window)

#main()