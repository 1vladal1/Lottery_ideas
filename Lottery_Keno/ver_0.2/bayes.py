#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import collections
import math

class NaiveBayes(object):
    def __init__(self):
        self.classes = collections.Counter()
        self.features = collections.Counter()
        self.freq_classes = collections.Counter()
        self.freq_features = collections.Counter()

    def add(self, features, class_):
        self.classes[class_] += 1
        for feature in features:
            self.features[feature, class_] += 1

    def de_log(self, log_value):
        return pow(2, log_value)

    def freq_class(self):
        s = sum(self.classes.values())
        for class_ in list(self.classes):
            self.freq_classes[class_] = math.log(self.classes[class_], 2) - math.log(s, 2)

    def freq_feat(self):
        for feat, class_ in list(self.features):
            self.freq_features[feat, class_] = (
            math.log(self.features[feat, class_], 2) - math.log(self.classes[class_], 2))

    def train(self, learn):
        for features, class_ in learn:
            self.add(features, class_)
        self.freq_class()
        self.freq_feat()

    def classify(self, features):
        min_ = 10000
        for class_ in self.classes.keys():
            r_sum = -self.freq_classes[class_]
            for feat in features:
                r_sum += -self.freq_features.get((feat, class_), math.log(pow(10, -7), 2))
            if r_sum < min_:
                result = class_
                min_ = r_sum
        return result

def get_features(sample):
    return (
        'll: %s' % sample[-1],          # get last letter
        'fl: %s' % sample[0],           # get first letter
        'sl: %s' % sample[1],           # get second letter
        )
"""
def main():
    nb = NaiveBayes()
    samples = (line.split() for line in open('names.txt'))
    features = [(get_features(feat), label) for feat, label in samples]
    nb.train(features)
    print(nb.classify(get_features(u'Владимир')))
    nb = None

main()
"""