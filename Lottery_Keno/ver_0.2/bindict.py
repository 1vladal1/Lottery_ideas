#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import decimal
import math
import copy

class Node(object):
    def __init__(self, code, parent=None, left=None, right=None):
        self.__code = code
        self.parent = parent
        self.left = left
        self.right = right
        self.__a = 0 #counts of 0s
        self.__b = 0 #counts of 1s
        self.__Pe = 1
        self.__Pw = 1

    def isRoot(self):
        if self.parent is None:
            return True
        else:
            return False

    def isLeaf(self):
        if self.left is None and self.right is None:
            return True
        else:
            return False

    def pe(self, bit):
        if bit == 1:
            result = dec(self.b + 0.5)
        else:
            result = dec(self.a + 0.5)
        result /= dec(self.a + self.b + 1)
        result *= dec(self.Pe)
        return result

    def zero_redundancy(self):
        result = self.Pe
        if self.a > 0 and self.b > 0:
            result = dec(0.5) * result
        elif (self.a > 0 and self.b == 0) or (self.a == 0 and self.b > 0):
            result = dec(0.5) * result + dec(0.25)
        elif self.a == self.b == 0:
            result = dec(1)
        return result

    def pw(self):
        if self.isLeaf():
            return self.Pe
        else:
            result = (self.Pe + self.left.Pw * self.right.Pw)
            result *= dec(0.5)
        return result

    def update_counter(self, bit):
        if bit == 1:
            self.__b += 1
        else:
            self.__a += 1

    @property
    def a(self):
        return self.__a

    @property
    def b(self):
        return self.__b

    @property
    def code(self):
        return self.__code

    @property
    def Pe(self):
        return self.__Pe

    @Pe.setter
    def Pe(self, value):
        self.__Pe = value

    @property
    def Pw(self):
        return self.__Pw

    @Pw.setter
    def Pw(self, value):
        self.__Pw = value


class BinDict(dict):
    def __init__(self, depth):
        register = init_register(depth)
        for i in range (0, pow(2,depth)):
            self.__addNode(tuple(register), depth)
            register = add_1(register)
        self.__relations()

    def __addNode(self, code, depth):
        if depth >= 0:
            if self.get(code) is None:
                self[code] = Node(code)
            depth -= 1
            self.__addNode(code[1:], depth)

    def __relations(self):
        for key in self.keys():
            parent = parents(key)
            if parent is None:
                self[key].parent = parent
            else:
                self[key].parent = self[parent]
                if self[key].code[:1] == (0,):
                    self[parent].left = self[key]
                elif self[key].code[:1] == (1,):
                    self[parent].right = self[key]

    def getDepth(self):
        return len(max(self.keys()))

    def update_counters(self, code, bit):
        self[code].update_counter(bit)
        if self[code].parent is not None:
            code = self[code].parent.code
            self.update_counters(code, bit)
        else:
            return

    def pe(self, code, bit):
        self[code].Pe = self[code].pe(bit)
        self[code].Pe = self[code].zero_redundancy()
        if self[code].parent is not None:
            code = self[code].parent.code
            self.pe(code, bit)

    def pw(self, code):
        self[code].Pw = self[code].pw()
        if self[code].parent is not None:
            code = self[code].parent.code
            self.pw(code)

    def ctw(self, sequence):
        depth = self.getDepth()
        if len(sequence) > depth:
            for i in range(0, len(sequence)-depth):
                context = sequence[i:i+depth]
                bit = sequence[i+depth]
                print(context,bit)
                self.pe(context, bit)
                self.pw(context)
                self.update_counters(context, bit)

    def duplicate(self):
        result = copy.deepcopy(self)
        return result

    def prediction(self, context, eps):
        #bdict0 = self.duplicate()
        bdict1 = self.duplicate()
        #bdict0.pe(context, 0)
        bdict1.pe(context, 1)
        #bdict0.pw(context)
        bdict1.pw(context)
        #print(dec(0.5+eps), dec(0.5-eps))
        #print(bdict1[()].Pw, self[()].Pw, bdict1[()].Pw/self[()].Pw)
        #print(bdict0[()].Pw/self[()].Pw)
        if bdict1[()].Pw/self[()].Pw > dec(0.5+eps):
            return 1
        elif ((bdict1[()].Pw/self[()].Pw <= dec(0.5+eps)) and
            (bdict1[()].Pw/self[()].Pw >= dec(0.5-eps))):
            return 1
        else:
            return 0
        #if bdict1[()].Pw > bdict0[()].Pw:
        #    return 1
        #else:
        #    return 0
        #print(bdict0[()].Pw)
        #print(bdict1[()].Pw)

"""
class BinDict(dict):
    def __init__(self, depth):
        register = init_register(depth)
        for i in range(0, pow(2,depth)):
            self.__addNode(tuple(register))
            register = add_1(register)
        #self["depth"] = depth

    def __addNode(self, node, child=None):
        if node is not None:
            if self.get(node) is None:
                self[node] = {}
                self[node]["parent"] = parent(node)
                self[node]["left_child"] = None
                self[node]["right_child"] = None
                self[node]["Pe"] = 1
                self[node]["Pw"] = 1
                self[node]["0"] = 0
                self[node]["1"] = 0
            if child is not None:
                if child[:1] == (0,):
                    self[node]["left_child"] = child
                if child[:1] == (1,):
                    self[node]["right_child"] = child
            self.__addNode(parent(node), node)

    def isRoot(self, node):
        if self[node]["parent"] is None:
            return True
        else:
            return False

    def isLeaf(self, node):
        if ((self[node]["left_child"] is None) and
           (self[node]["right_child"] is None)):
            return True
        else:
            return False

    def Pe(self, node, bit):
        if node is not None:
            temp = dec(self[node]["Pe"])
            temp *= dec(self[node][str(bit)] + 0.5)/dec(self[node]["0"]+self[node]["1"]+1)
            self[node]["Pe"] = dec(temp)
            node = self[node]["parent"]
            self.Pe(node, bit)

    def Pw(self, node):
        if node is not None:
            if self.isLeaf(node):
                self[node]["Pw"] = dec(self[node]["Pe"])
                node = self[node]["parent"]
                self.Pw(node)
            else:
                left = self[node]["left_child"]
                right = self[node]["right_child"]
                left_Pw = dec(self[left]["Pw"])
                right_Pw = dec(self[right]["Pw"])
                temp = dec(0.5) * dec(self[node]["Pe"])
                temp += dec(0.5) * dec(left_Pw) * dec(right_Pw)
                self[node]["Pw"] = dec(temp)
                node = self[node]["parent"]
                self.Pw(node)

    def update_counters(self, node, bit):
        if node is not None:
            self[node][str(bit)] += 1
            node = self[node]["parent"]
            self.update_counters(node, bit)

    def getDepth(self):
        return len(max(self.keys()))

    def ctw(self, sequence):
        depth = self.getDepth()
        if len(sequence) > depth:
            for i in range(0, len(sequence)-depth):
                context = sequence[i:i+depth]
                bit = sequence[i+depth]
                self.Pe(context, bit)
                self.Pw(context)
                self.update_counters(context, bit)
"""

def init_register(depth):
    register = []
    for i in range(0, depth):
        register.append(0)
    return register

def add_1(register):
    if register[-1:] == [1]:
        register[-1:] = [0]
        temp = add_1(register[:-1])
        register = temp + register[-1:]
    else:
        register[-1:] = [1]
    return register

def parents(key):
    if len(key) == 1:
        result = tuple()
        return result
    elif key == ():
        return None
    else:
        return key[1:len(key)]

def dec(num):
    return decimal.Decimal(num)