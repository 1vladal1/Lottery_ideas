#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ualottery
import statistics
import binominal
import ctw
import collections
import pylab
import bayes
import math
import decimal
import random
import activelezi
import bwt
import sys

def open_lottery():
    LOTTERY_FILE_NAME = "/home/vlad/PythonProjects/Lottery_Keno/ver_0.2/keno_results.csv"
    basis_ltr = ualottery.UALottery(LOTTERY_FILE_NAME)
    #basis_ltr.view_info()

    filter1 = ualottery.LotteryFilter(None, basis_ltr.length)
    #filter1.add("А", 3)
    #filter1.add("А", 2)
    #filter1.add("А", 3)
    #filter1.add(None, None)
    #filter1.moveto(0,10)
    #filter1.delete(0)
    filter1.show()
    f_ltr = basis_ltr.get_lottery_by_filter(filter1)

    return f_ltr

def filtered(vector, template):
    new = ()
    size = len(template)
    for i in range(len(vector)-size-1):
        if vector[i:i+size] == template:
            new += (vector[i+size],)
    return new

def filtered2(vector, step):
    new = ()
    for i in range(0, len(vector)-step, step):
        new += (vector[i+step],)
    return new

def test_ctw(vector, d):
    tree = ctw.CTWTree()
    depth = d
    zr = True
    d7 = round(0.7*len(vector))
    learn = vector[:d7]
    test = vector[d7:]
    eps = 1/pow(len(learn), 0.5)

    for i in range(len(learn)-depth):
        context = learn[i:i+depth]
        bit = learn[i+depth]
        tree.update(context, bit, zr)

    err = 0
    win = 0
    for i in range(len(test)-depth):
        predict = tree.predict(test[i:i+depth], eps, zr)
        bit = test[i+depth]
        print(predict, bit)
        if predict == bit:
            win += 1
        err +=abs(predict - bit)
    err /= (len(test)-depth)

    print(tree.size(), len(vector)-depth, len(test)-depth, win, "ACC:", 100*(1-err), collections.Counter(vector))
    tree = None
    learn = None
    test = None

class Predictor(object):
    def __init__(self):
        self.cxt = 1
        self.ct = collections.Counter()
    def p(self):
        return ((self.ct[(self.cxt,1)]+1))/(self.ct[(self.cxt,0)]+self.ct[(self.cxt,1)]+2)

    def update(self, y):
        self.ct[(self.cxt,y)]+=1
        if self.ct[(self.cxt,y)] > 2000000000:
            self.ct[(self.cxt,0)] >>= 1
            self.ct[(self.cxt,1)] >>= 1
        self.cxt+=self.cxt+y
        if self.cxt >= 2048:
            self.cxt = 1

def bits2bytes(bits):
    b = bytearray()
    i = 0
    while (i+8<=len(bits)):
        byte = bits[i:i+8]
        s = "0b"
        for bit in byte:
            s += str(bit)
        b.append(int(s,2))
        i += 8

    if i<len(bits):
        s = "0b"
        for k in range(i+8-len(bits)):
            s += str(0)
        byte = bits[i:len(bits)]
        for bit in byte:
            s += str(bit)

        b.append(int(s,2))
    return b

def probability_AB(lottery):
    lz = activelezi.LZ78()
    k = 0
    for tirazh in lottery.results:
        k += 1
        if k == lottery.filter_length:
            lz.add_symbol((tirazh.lototron,))
            k = 0

    print("А", lz.probability(("А",)))
    print("Б", lz.probability(("Б",)))

    lz = activelezi.LZ78()
    k = 0
    for tirazh in lottery.results:
        k += 1
        if k == lottery.filter_length:
            lz.add_symbol((tirazh.balls_set,))
            k = 0

    for i in range(1,5):
        print(i, lz.probability((i,)))
    print()
    print(15*" " + "А", 30*" " + "Б")

    lz = activelezi.LZ78()
    k = 0
    for tirazh in lottery.results:
        k += 1
        if k == lottery.filter_length:
            lz.add_symbol(((tirazh.lototron, tirazh.balls_set),))
            k = 0

    for i in range(1,5):
         print(i, lz.probability((("А", i),)), lz.probability((("Б", i),)))

def main():
    lottery = open_lottery()
    #lottery.sort()
    lottery.view_info()
    #probability_AB(lottery)
    print()
    n = 3
    models = []
    for i in range(lottery.tirazh_length):
        lz = activelezi.LZ78()
        models.append(lz)
        lz = None

    for tirazh in lottery.results:
        for col in range(lottery.tirazh_length):
            if tirazh.balls[col] % n == 0 and n != 1:
                model_num = int(tirazh.balls[col]/n)-1
            else:
                model_num = int(tirazh.balls[col]/n)
            models[col].add_symbol((model_num,))
            #print(model_num+1, tirazh.balls[col])

    for col in range(lottery.tirazh_length):
        #min_ = 1000
        #nn = 0
        for num in range(int(lottery.max_ball/n)):
            probability = models[col].probability((num,))
            #if probability < min_:
            #    min_ = probability
            #    nn = num
            if probability > 0.5:
                print(col+1, n*num+1, n*(num+1), probability)
        #print(col+1, nn*n+1, (nn+1)*n, min_)

    """
    for i in range(int(lottery.max_ball/n)):
        lz = activelezi.LZ78()
        models.append(lz)
        lz = None

    for tirazh in lottery.results:
        for ball in tirazh.balls:
            for k in range(len(models)):
                if ball>=k*n+1 and ball<=(k+1)*n:
                    models[k].add_symbol((ball,))

    for k in range(len(models)):
        for ball in range(k*n+1, (k+1)*n+1):
            probability = models[k].probability((ball,))
            if probability > 0.0:
                print(k+1, ball, probability)
    """
    """c = collections.Counter()
    for j in range(lottery.tirazh_length):
        lz = activelezi.LZ78()
        for tirazh in lottery.results:
            lz.add_symbol((tirazh.balls[j],))
        max_ = 0
        z = 0
        for i in range(lottery.max_ball):
            probability = lz.probability((i+1,))
            if probability > max_:
                max_ = probability
                z = i+1
        if max_ > 0.0:
            print(z, max_)
            c.update((z,))
        lz = None"""
    """lottery.sort()
    for j in range(lottery.tirazh_length):
        lz = activelezi.LZ78()
        for tirazh in lottery.results:
            lz.add_symbol((tirazh.balls[j],))
        max_ = 0
        z = 0
        for i in range(lottery.max_ball):
            probability = lz.probability((i+1,))
            if probability > max_:
                max_ = probability
                z = i+1
        if max_ > 0.5:
            print(z, max_)
            c.update((z,))
        lz = None"""
    #print(c, len(c))
    """for item in lottery.results:
        print(item.number)"""
    """compare = lottery.compare_block_tirazhs_in_lottery()
    for i in range(lottery.filter_length-1,0,-1):
        prediction = collections.Counter()
        counter = collections.Counter()
        for col in range(1, lottery.tirazh_length+1):
            lz = activelezi.LZ78()
            vector = statistics.get_col(compare[lottery.filter_length-1-i], col)
            bernoulli = binominal.Bernoulli(vector)
            for item in vector:
                lz.add_symbol((item,))
            probability = lz.probability((1,))
            if probability > 0.5:
            #if abs(probability-bernoulli.p) <= abs(bernoulli.p1 - bernoulli.p):
                prediction.update(((lottery.results[-i:][0].balls[col-1],probability),))
                counter.update((lottery.results[-i:][0].balls[col-1],))
            print(col, probability, "P =", bernoulli.p1)
        #print(lottery.results[-i:][0].number)
        for item in sorted(prediction.items()):
            print(item)
        print(sorted(counter), len(counter))
        print()

    for i in range(lottery.filter_length-1):
        for col in range(1, lottery.tirazh_length+1):
            vector = statistics.get_col(compare[i], col)
            bernoulli = binominal.Bernoulli(vector)
            lz = activelezi.LZ78()
            for item in vector:
                lz.add_symbol((item,))
            prob = lz.probability((1,))
            print(col, prob, "P =", bernoulli.p)
        print()
    """
    """i = 0
    for tirazh in lottery.results:
        i += 1
        print(tirazh.number, tirazh.lototron, tirazh.balls_set)
        if i == lottery.filter_length:
            print()
            i = 0
    print()
    prediction = collections.Counter()
    counter = collections.Counter()
    for window in range(lottery.length-400):
        compare = lottery.compare_tirazhs_in_lottery(window+1)
        for col in range(1, lottery.tirazh_length+1):
            lz = activelezi.LZ78()
            vector = statistics.get_col(compare, col)
            bernoulli = binominal.Bernoulli(vector)
            for item in vector:
                lz.add_symbol((item,))
            probability = lz.probability((1,))
            if ((probability > 0.99)):# and probability <= 1)): #or
               #(abs(probability - bernoulli.p) <= 0.00002 and probability - bernoulli.p > 0)):
                prediction.update(((lottery.results[-window-1:][0].balls[col-1],probability,bernoulli.p1),))
                counter.update((lottery.results[-window-1:][0].balls[col-1],))
            #print(col, lz.probability((1,)), "P =", bernoulli.p)
    for item in sorted(prediction.items()):
        print(item)
    print(counter, len(counter))
    """
    """c = collections.Counter()
    for window in range(lottery.length-100):
        compare = lottery.compare_tirazhs_in_lottery(window+1)
        for col in range(lottery.tirazh_length):
            vector = statistics.get_col(compare,col+1)
            s = ""
            for item in vector:
                s += str(item)
            b = bwt.BWT(s)
            result = b.proceed()
            lz = activelezi.LZ78()
            for item in result:
                lz.add_symbol((item,))
            probability = lz.probability(("1",))
            if probability > 0.997:
                print(lottery.results[-window-1:][0].balls[col], probability)
                c.update((lottery.results[-window-1:][0].balls[col],))
            lz = None
            b = None
    print(c, len(c))"""
main()