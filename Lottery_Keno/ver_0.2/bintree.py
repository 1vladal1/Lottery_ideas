#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import decimal

def dec(number):
    return decimal.Decimal(number)

class Node(object):
    """Counter a counts 0s;
       Counter b counts 1s;
       left is 1;
       right is 0;
    """
    def __init__(self, left=None, right=None):
        self.counters = {"0":0, "1":0}
        self.Pe = 1
        self.Pw = 1
        self.left = left
        self.right = right
        #self.update_Pe_Pw()

    def update_counter(self, bit):
        self.counters[str(bit)] += 1

    def update_Pe_Pw(self, bit):
        self.Pe = self.zero_redundacy(bit)

    def Pe(self, bit):
        pe = dec(self.counters[str(bit)])+dec(0.5)
        pe /= dec(sum(self.counters.values())+1)
        return pe

    def zero_redundacy(self, bit=None):
        if self.counters["0"] > 0 and self.counters["1"] > 0:
            return dec(0.5) * self.Pe(bit)
        elif ((self.counters["0"] > 0 and self.counters["1"] == 0) or
           (self.counters["0"] == 0 and self.counters["1"] > 0)):
            return dec(0.5) * self.Pe(bit) + dec(0.25)
        elif self.counters["0"] == 0 and self.counters["1"] == 0:
            return 1

class BinTree(object):

    def __init__(self):
        self.root = None

    def newNode(self):
        temp = Node()
        return temp

    def addTree(self, node, depth):
        if self.getDepth(node) < depth:
            node.left = self.newNode()
            node.right = self.newNode()
            self.addTree(node.left, depth-1)
            self.addTree(node.right, depth-1)

    def printTree(self, node, level=0):
        if node is None:
            return
        self.printTree(node.right, level+1)
        print(" "*15*level, node.counters, node.Pe)
        print("")
        self.printTree(node.left, level+1)

    def getDepth(self, node):
        if node is None:
            return 0
        else:
            l_depth = self.getDepth(node.left)
            r_depth = self.getDepth(node.right)
        if l_depth > r_depth:
            return l_depth+1
        else:
            return r_depth+1

    def getWidth(self, node, level):
      if node is None:
        return 0
      if level == 1:
        return 1
      elif level > 1:
          return self.getWidth(node.left, level-1) +  self.getWidth(node.right, level-1)
      self.getWidth(node.right, level-1)

    def update_counters(self, node, context, bit):
        node.update_counter(bit)
        if len(context) > 0:
            context_bit = context[len(context)-1]
            context = context[0:len(context)-1]
            if context_bit == 1:
                self.update_counters(node.left, context, bit)
            else:
                self.update_counters(node.right, context, bit)