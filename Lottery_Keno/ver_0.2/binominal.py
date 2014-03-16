#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import decimal
import math

def dec(number):
    return decimal.Decimal(str(number))

class Bernoulli(object):

    def __init__(self, arg):
        if type(arg) is tuple or type(arg) is list:
            n = len(arg)
            self.__p = dec(sum(arg))/dec(n)
            self.__p1 = dec(sum(arg)+1)/dec(n+1)
            self.__q = dec(1) - self.__p
        else:
            self.__p = dec(arg)
            self.__q = dec(1) - self.__p

    #Математическое ожидание
    def mx(self, n=1):
        return dec(n) * self.p

    #Дисперсия
    def dx(self, n=1):
        return dec(n) * self.p * self.q

    def __combinations(self, k, n):
        result = dec(math.factorial(n))
        result /= dec(math.factorial(k))
        result /= dec(math.factorial(n-k))
        return result

    def combinations2(self, k, n):
        result = dec(1)
        for i in range(n-k+1, n+1):
            result *= dec(i)
        result /= dec(math.factorial(k))
        return result

    #Вероятность ровно K удач в N испытаниях
    def probability(self, k, n):
        result = self.__combinations(k, n) * pow(self.p, k) * pow(self.q, n-k)
        return dec(result)

    def probability2(self, k, n):
        result = self.__combinations(k-1, n-1) * pow(self.p, k) * pow(self.q, n-k)
        return dec(result)

    #Теоритеческое количество успехов и неудач при N испытаний
    def teor_number_of_success_failure(self, n):
        result = {}
        result["1"] = dec(n) * self.p
        result["0"] = dec(n) * self.q
        return result

    #Вероятность не менее K1 и не более K2 удач в N испытаниях
    def probability_at_k1_k2_success(self, k1, k2, n):
        if k1 >= 0 and k2 <= n:
            prob = []
            for k in range(k1, k2+1):
                prob.append(self.probability(k, n))
            return dec(sum(prob))
        else:
            return None

    #Наиболее вероятное количество удач в N испытаниях
    def most_probable_number_of_success(self, n):
        result = []
        result.append(dec(n) * self.p - self.q)
        result.append(dec(n) * self.p + self.p)
        return result

    #Наиболее вероятное количество испытаний при K удач
    def most_probable_number_of_experiment(self, k):
        result = []
        result.append((dec(k)-self.p)/self.p)
        result.append((dec(k)+self.q)/self.p)
        return result

    #Вероятность первого успеха в K-ом испытании
    def probability_first_success(self, k=1):
        if k <= 0:
            k = 1
        return self.p * pow(self.q, k-1)

    #Количество испытаний при хотя бы 1 удачи с верояностью Pз
    def number_of_experiments_with_Pz(self, pz):
        return math.log(1-pz,math.e)/math.log(self.q, math.e)

    #Вероятность того, что модуль разности относительной частоты и
    #теоретической вероятности будет <= eps
    def probability_eps(self, n, eps):
        return dec(1)-self.dx(1)/dec(n*pow(eps,2))

    #Вероятность того, что отклонение случ. величины от мат. ожидания
    #будет <= eps
    def probability_eps2(self, n, eps):
        return dec(1)-self.dx(n)/dec(pow(eps,2))

    #Энтропия
    def entropy(self):
        result = []
        h1 = -self.p * dec(math.log(self.p, 2))
        h0 = -self.q * dec(math.log(self.q, 2))
        result.append(h0)
        result.append(h1)
        result.append(h1 + h0)
        return result

    def coding(self):
        result = []
        result.append(-dec(math.log(self.q, 2)))
        result.append(-dec(math.log(self.p, 2)))
        return(result)

    @property
    def p(self):
        return self.__p

    @property
    def p1(self):
        return self.__p1

    @property
    def q(self):
        return self.__q