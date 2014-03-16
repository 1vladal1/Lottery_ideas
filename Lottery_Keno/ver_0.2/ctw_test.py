#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ctw
import random
import collections
import binominal

def main():

    depth = 3
    zr = True
    tree = ctw.CTWTree()
    #print("NEW TREE SIZE", tree.__sizeof__())

    #seq = (1,1,0,0,1,0,0,1,1,0)
    #seq = (1,1,0,0,0,1,1,1,0,0,0,1,1,1,0,0,0,0,1,1,0,1,0,0,1,0,0,0,0,0,1,
    #       1,0,1,1,0,1,0,1,0,0,0,0,1,0,0,0,0,0,1,0,0,1,0,1,0,0,1,1,0,0,0,
    #       1,1,0,1,1,0,0,0,0,1,0,1,0,1,1,1,0,0)
    #seq = (0,1,0,0,0,0,1,1,1,1,0,1,1,1,1,0,
    #       0,1,0,0,1,0,0,0,1,0,1,0,1,0,1,0,
    #       1,1,1,0,1,1,1,1,1,0,1,0,0,0,1,0,
    #       1,1,0,1,1,1,1,0,0,1)
    seq = ()
    for i in range(10000):
        seq += (random.randint(0,1),)
    binom = binominal.Bernoulli(seq)
    print(binom.entropy())
    d7 = round(0.7*len(seq))
    d3 = round(0.3*len(seq))
    print(len(seq), d7, d3)
    learn = seq[:d7]
    test = seq[d7:]
    #test= learn
    eps = 1/pow(len(learn), 0.5)
    #print(eps)
    for i in range(len(learn)-depth):
        context = learn[i:i+depth]
        bit = learn[i+depth]
        tree.update(context, bit, zr)

    #tree.printInOrder()
    err = 0
    win = 0
    for i in range(len(test)-depth):
        predict = tree.predict(test[i:i+depth], eps, zr)
        bit = test[i+depth]
        #print(predict, bit)
        if predict == bit:
            win += 1
        err +=abs(predict - bit)
    err /= (len(test)-depth)
    #print("FILLED TREE SIZE", tree.__sizeof__())
    print(tree.size(), len(seq)-depth, len(test)-depth, win, "ACC:", 100*(1-err), collections.Counter(seq))
    tree = None
    seq = None
    learn = None
    test = None

main()

