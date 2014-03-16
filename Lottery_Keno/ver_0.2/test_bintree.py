#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import bindict

def main():
    d = 1
    sequence = (1,0,1,0,1,1,0)
    bdict = bindict.BinDict(d)
    print(bdict.__sizeof__())
    #bdict.ctw(sequence)
    #for key in sorted(bdict.keys()):
    #    print(key, bdict[key]["parent"], bdict[key]["Pe"], bdict[key]["Pw"],
    #          "counters:", bdict[key]["0"], bdict[key]["1"])
    #for key in sorted(bdict.keys()):
    #    print(bdict[key].code, bdict[key].a, bdict[key].b, bdict[key].Pe, bdict[key].Pw)
    #eps = 1/pow(len(sequence),0.5)
    #print(bdict.prediction(sequence[-d:],eps))
    #print(len(bdict), bdict.getDepth())

main()