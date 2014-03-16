#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
import copy

""" Узел дерева """
class CTWNode(object):
    def __init__(self, code, parent=None, left=None, right=None):
        self.code = code
        self.counts = [0,0]
        self.logPe = 0.0
        self.logPw = 0.0
        self.parent = parent
        self.child = [left, right]

    def delete(self):
        key = self.code[0]
        if self.parent is not None:
            self.parent.child[key] = None

    def __update(self, bit, zr=False):
        self.logPe += self.logProbEstimated(bit, zr)
        if self.isLeaf():
            self.logPw = self.logPe
        else:
            self.logPw = self.logProbWeighted()
        self.counts[bit] += 1

    def isRoot(self):
        return self.parent is None

    def isLeaf(self):
        return self.child[0] == self.child[1] is None

    def nType(self):
        if self.isLeaf():
            return "Leaf"
        elif self.isRoot():
            return "Root"
        else:
            return "Node"

    def logProbEstimated(self, bit, zr=False):
        if zr:
            return self.__logZeroRedundancy(bit)
        else:
            return self.__logKT(bit)

    def __logKT(self, bit):
        return math.log(2*self.counts[bit]+1, 2)+math.log(0.5,2)-math.log(sum(self.counts)+1, 2)

    def __logZeroRedundancy(self, bit):
        if sum(self.counts) == 0:
            return 0.0
        log_result = self.__logKT(bit) - 1
        if self.counts[0] == 0 or self.counts[1] == 0:
            log_result = logAdd(math.log(0.25, 2), log_result)

        return log_result

    def logProbWeighted(self):
        logPw_tmp = [0.0, 0.0]
        for i in range(2):
            if self.child[i] is not None:
                logPw_tmp[i] = self.child[i].logPw
        log_Pw = logAdd(self.logPe, sum(logPw_tmp)) - 1
        #log_tmp = sum(logPw_tmp) - self.logPe
        #if log_tmp < 100:
        #    log_tmp = math.log(1+pow(2, log_tmp),2)
        #log_Pw = self.logPe + log_tmp - 1
        return log_Pw

    def size(self):
        result = 1
        if self.child[0] is not None:
            result += self.child[0].size()
        if self.child[1] is not None:
            result += self.child[1].size()
        return result

""" Бинарное дерево """
class CTWTree(object):
    def __init__(self):
        self.root = CTWNode(())

    def __addNodesInContext(self, context):
        node = self.root
        code = []
        created = []
        for c in reversed(context):
            code.insert(0, c)
            if node.child[c] is None:
                node.child[c] = CTWNode(tuple(code), node)
                created.append(node.child[c])
                #print(created, node.child[c])
            node = node.child[c]
        return created

    def size(self):
        return self.root.size()

    def update(self, context, bit, zr=False):
        self.__addNodesInContext(context)
        context_path = [self.root]
        node = self.root
        for c in reversed(context):
            node = node.child[c]
            context_path.insert(0, node)

        for context_node in context_path:
            context_node._CTWNode__update(bit, zr)

    def predict(self, context, eps, zr=False):
        r = self.root.logPw
        r1 = self.__calculate(context, 1, zr)
        #r0 = self.__calculate(context, 0, zr)
        #print(r, r0, r1)
        """Прогноз"""
        r = r1 - r
        r = pow(2, r)
        #r11 = r1 - r
        #r00 = r0 - r
        #r11 = pow(2, r11)
        #r00 = pow(2, r00)
        if (r > 0.5 + eps) or (r <= 0.5 + eps and r >= 0.5 - eps):
        #if r11 - r00 > 0:
            result = 1
        else:
            result = 0

        return result

    def __calculate(self, context, bit, zr=False):
        created = self.__addNodesInContext(context)
        node = self.root
        context_path = [node]
        for c in reversed(context):
            node = node.child[c]
            context_path.insert(0, node)

        """Сохранить параметры текущего дерева"""
        before_logPe = []
        before_logPw = []
        before_counts = []
        for context_node in context_path:
            before_logPe.append(copy.deepcopy(context_node.logPe))
            before_logPw.append(copy.deepcopy(context_node.logPw))
            before_counts.append(copy.deepcopy(context_node.counts))

        """Расчет новых параметров, с учетом что будет бит=bit"""
        for context_node in context_path:
            context_node._CTWNode__update(bit, zr)

        result = self.root.logPw

        """Восстановить предидущие параметры дерева"""
        for context_node in context_path:
            context_node.logPe = before_logPe.pop(0)
            context_node.logPw = before_logPw.pop(0)
            context_node.counts = before_counts.pop(0)
            if context_node in created:
                context_node.delete()
        return result


    def printInOrder(self):
        self.__inOrder(self.root)

    def __inOrder(self, node, level=0):
        if node is not None:
            self.__inOrder(node.child[0], level+1)
            print((pow(2,level)+10*level)*" ", node.code, node.counts)
            self.__inOrder(node.child[1], level+1)

""" Дано log(x) и log(y), вычислить log(x+y). log с основание 2.
log(x + y) = log(x) + log(1 + y/x) = log(x) + log(1+2^(log(y)-log(x)))"""
def logAdd(log_x, log_y):
    if log_x > log_y:
        tmp = log_x
        log_x = log_y
        log_y = tmp

    result = log_y - log_x
    if result < 100.0:
        result = math.log(1.0 + pow(2,result),2)
    result += log_x
    return result