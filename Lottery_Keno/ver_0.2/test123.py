#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 20:44:51 2013

@author: vlad
"""

vector = (1,0,1,0,0,1,0,1,1,0,1,0,1,0,1,1)
pattern = (1,0,1)
lp = len(pattern)
for i in range(0,len(vector)-len(pattern)):
    print(vector[i:i+lp])
    if  vector[i:i+lp] == pattern:
        print("i =",i, "next =",vector[i+lp])