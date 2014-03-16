#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random

def main():
    year = 2013
    month = 11
    day = 23
    hour = 22
    for minute in range(60):
        for second in range(60):
            d = (year, month, day, hour, minute, second)
            random.seed(d)
            r = random.randint(0,9)
            print(d, r)


main()

