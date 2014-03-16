#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Shannon(object):

    def __init__(self, width=5):
        self.array = {}
        self.supervisor = {}
        self.vector = ()
        self.step = 0
        self.N = width

    def add_element(self, element):
        self.step += 1
        if len(self.vector) < self.N:
            self.vector += (element, )
        if len(self.vector) == self.N:
            self.__add_vector()
            self.vector = self.vector[1:]

    def __add_vector(self):
        if self.array.get(self.vector) is None:
            self.array[self.vector] = pow(1+0.1, self.step)
        else:
            self.array[self.vector] += pow(1+0.1, self.step)

    def predict(self):
        d0 = 0
        d1 = 0
        v0 = self.vector + (0, )
        v1 = self.vector + (1, )
        if len(v0) and len(v1) == self.N:
            if self.array.get(v0) is not None:
                d0 = self.array[v0]
            if self.array.get(v1) is not None:
                d1 = self.array[v1]
            if self.array.get(v0) is None and self.array.get(v1) is None:
                return "None"
            elif d0 > d1:
                return 0
            elif d1 > d0:
                return 1
            elif d0 == d1 and d0 > 0 and d1 > 0:
                return "=="

    def update_supervisor(self, item):
        v = self.vector + (item, )
        if self.supervisor.get(v) is None:
            self.supervisor[v] = 0
        else:
            self.supervisor[v] = pow(1+0.01, self.step)

"""def main():

    d = Shannon()

    print("")
    for key in sorted(d.array):
        print(key, d.array[key])
    print(d.predict())
main()"""