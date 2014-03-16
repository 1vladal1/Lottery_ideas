#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import collections
import itertools

"""Класс LotteryFilter:
    start -- с какого тиража начинать
    stop -- каким тиражом заканчивать
    template -- по каким лототронам и наборам шаров фильтровать тиражи
"""

class LotteryFilter(object):

    __UP = "UP"
    __DOWN = "DOWN"

    def __init__(self, start_pos=None, stop_pos=None, lototron=None,
                 balls_set=None):
        self.__start = start_pos
        self.__stop = stop_pos
        self.__template = []
        self.__template.append({"lototron": lototron, "balls_set": balls_set})

    def add(self, lototron=None, balls_set=None, index=-1):
        if index > len(self.__template) or index < 0:
            index = len(self.__template)
        self.__template.insert(index, {"lototron": lototron, "balls_set": balls_set})

    def delete(self, index=-1):
        if len(self.__template) > 1:
            if index > len(self.__template) or index < 0:
                index = None
            if index is None:
                self.__template.pop()
            else:
                self.__template.pop(index)

    def move(self, index, direction):
        if direction == "UP":
            if index - 1 >= 0 and index < len(self.__template):
                self.__template[index], self.__template[index-1] = self.__template[index-1], self.__template[index]
        elif direction == "DOWN":
            if index + 1 < len(self.__template) and index >= 0:
                self.__template[index], self.__template[index+1] = self.__template[index+1], self.__template[index]

    def moveto(self, pos1, pos2):
        if pos1 < pos2:
            tmp_pos = pos1
            while tmp_pos < pos2:
                self.move(tmp_pos, self.__DOWN)
                tmp_pos += 1
        elif pos1 > pos2:
            tmp_pos = pos1
            while tmp_pos > pos2:
                self.move(tmp_pos, self.__UP)
                tmp_pos -= 1

    def show(self):
        print("Filter is:")
        print("[", self.__start, ":", self.__stop, "]")
        for item in self.__template:
            print(item["lototron"], item["balls_set"])
        print("")
        return None

    @property
    def DOWN(self):
        return self.__DOWN

    @property
    def UP(self):
        return self.__UP

    @property
    def length(self):
        return len(self.__template)

    @property
    def start(self):
        return self.__start

    @property
    def stop(self):
        return self.__stop

    @property
    def template(self):
        return self.__template

"""Класс Tirazh:
    number -- номер тиража (число);
    date -- дата тиража (строка);
    lototron -- лототрон (строка);
    balls_set -- набор шаров (строка);
    balls -- шары выпавшие в тираже (кортеж)
"""
class Tirazh(object):

    def __init__(self, line=None):
        if line is None:
            self.__number = None
            self.__date = None
            self.__lototron = None
            self.__balls_set = None
            self.__balls = ()
        elif type(line) is list:
            self.__number = int(line[0])
            self.__date = line[1]
            self.__lototron = line[2]
            self.__balls_set = int(line[3])
            self.__balls = ()
            for ball in line[4:]:
                self.__balls += (int(ball), )

    def __sort(self):
        self.__balls = tuple(sorted(self.__balls))

    def __str__(self):
        return "%s %s %s %s %s" % (str(self.__number), self.__date,
                self.__lototron, str(self.__balls_set), str(self.__balls))

    def shortinfo(self):
        print(self.__number, self.__date, self.__lototron, self.__balls_set)

    def get_combinations(self, n=2):
        result = itertools.combinations(sorted(self.__balls), n)
        return list(result)

    @property
    def length(self):
        return len(self.__balls)

    @property
    def number(self):
        return self.__number

    @property
    def date(self):
        return self.__date

    @property
    def lototron(self):
        return self.__lototron

    @property
    def balls_set(self):
        return self.__balls_set

    @property
    def balls(self):
        return self.__balls


""" Класс лотерея -- имеет такую структуру:
    1. Свойство min_ball -- минимальный номер шара в лотерее
    2. Свойство max_ball -- максимальный номер шара в лотерее
    3. Свойство tirazh_length -- количество выпадающих шаров в тираже
    4. Свойство lottery_length -- всего тиражей
    5. lottery_result -- результаты тиражей
"""
class UALottery(object):

    def __init__(self, filename=None):
        self.__is_sort = False
        self.__min_ball = None
        self.__max_ball = None
        self.__tirazh_length = None
        self.__length = None
        self.filter_length = 0
        self.__results = []
        if type(filename) is str:
            with open(filename, newline="") as lottery_file:
                lottery_reader = csv.reader(lottery_file, delimiter=";")
                for line in lottery_reader:
                    tirazh = Tirazh(line)
                    self.__results.append(tirazh)
            self.set_lottery_info()

    def view_info(self):
        print("______________________________________________________________________")
        print("-= INFORMATION ABOUT LOTTERY =-")
        print("min_ball      ", self.min_ball)
        print("max_ball      ", self.max_ball)
        print("tirazh_length ", self.tirazh_length)
        print("lottery_length", self.length)
        print("is_sort       ", self.is_sort)
        print("repeats       ", self.repeats_teor())
        print("lototron stat", self.lototron_balls_set_statistics())
        print("")
        print("Last Tirazh in basis lottery is:")
        print(self.results[-1:][0])
        print("______________________________________________________________________")

    def set_lottery_info(self, lottery = None):
        if lottery is None:
            self.__tirazh_length = self.__results[0].length
            self.__length = len(self.__results)
            min_max_ball = self.__find_min_max_ball()
            self.__min_ball = min_max_ball["min"]
            self.__max_ball = min_max_ball["max"]
        elif type(lottery) is UALottery:
            self.__tirazh_length = lottery.tirazh_length
            self.__min_ball = lottery.min_ball
            self.__max_ball = lottery.max_ball
            self.__length = len(self.__results)

    def __find_min_max_ball(self):
        result = {"min": 1000, "max": 0}
        for tirazh in self.__results:
            tmp_min = min(tirazh.balls)
            tmp_max = max(tirazh.balls)
            if result["min"] > tmp_min:
                result["min"] = tmp_min
            if result["max"] < tmp_max:
                result["max"] = tmp_max
        return result

       # def print_tirazh(self, id=1):

    """Матрица выпавших шаров"""
    def get_balls_array(self):
        result = tuple()
        for tirazh in self.results:
            result += (tirazh.balls,)
        return result

    """Вектор выпавших шаров"""
    def get_balls_vector(self):
        result = tuple()
        for tirazh in self.results:
            for ball in tirazh.balls:
                result += (ball,)
        return result

    """Вектор шаров в определенной колонке (начиная с нулевой)"""
    def get_balls_in_column(self, column):
        result = []
        for tirazh in self.results:
            result.append(tirazh.balls[column])
        return result

    """Выбор тиража (по id при flag == False, и по номеру тиража при True)"""
    def get_tirazh_by_number(self, position, flag = True):
        if flag:
            if position >= 1:
                for tirazh in self.__results:
                    if position == tirazh.number:
                        return tirazh
            else:
                return None
        else:
            if position < 0 or position > self.__length:
                return None
            else:
                return self.__results[position]

    """Сортировка шаров в тиражах по возрастанию"""
    def sort(self):
        if not self.__is_sort:
            for tirazh in self.__results:
                tirazh._Tirazh__sort()
            self.__is_sort = True

    """Фильтрация по заданому шаблону (лототрон, набор шаров) лотереи.
    Результат -- новый объект UALottery
    Значение None в шаблоне указывает на любой лототрон или набор шаров.
    """
    def get_lottery_by_filter(self, filter_):
        if filter_.start is None:
            start_pos = 0
        else:
            start_pos = filter_.start - 1

        if filter_.stop is None:
            end_pos = self.__length - 1
        else:
            end_pos = filter_.stop - 1

        i = start_pos
        result = UALottery()
        while i <= end_pos: #- filter_.length + 1:
            flag = False
            k = i
            for item in filter_.template:
                if ((k >= end_pos + 1) and (item["lototron"] is None) and
                   (item["balls_set"] is None)):
                    flag = True
                    break
                if k >= end_pos + 1:
                    break
                if ((self.__results[k].lototron == item["lototron"] or
                    item["lototron"] is None) and (item["balls_set"] is None or
                    self.__results[k].balls_set == item["balls_set"])):
                    flag = True
                    k += 1
                else:
                    flag = False
                    break
            if flag:
                for z in range(i,i+filter_.length):
                    if z <= end_pos:
                        tirazh = self.get_tirazh_by_number(z, False)
                        result._UALottery__results.append(tirazh)
                i += len(filter_.template)
            else:
                i += 1
        result.set_lottery_info(self)
        result.filter_length = filter_.length
        return result

    """Считает количество пар лототрон - набор шаров"""
    def lototron_balls_set_statistics(self):
        result = collections.Counter()
        for tirazh in self.__results:
            pair = tirazh.lototron + str(tirazh.balls_set)
            result.update((pair, ))
        return result

    """Сколько раз выпал каждый шар в лотерее"""
    def balls_statistics(self):
        result = collections.Counter()
        for tirazh in self.__results:
            result.update(tirazh.balls)
        return result

    """Подсчитывает сколько необходимо тиражей для выпадания >= threshold шаров"""
    def threshold_balls_out(self, threshold=None):
        m = 1
        min_, max_ = 1000, 0
        if (threshold is None or threshold > self.__max_ball or
            threshold <= self.__tirazh_length):
            threshold = self.__max_ball
        ball_matrix = [0 for i in range(0, self.__max_ball)]
        result = []
        tirazhs = ()
        for tirazh in self.__results:
            for ball in tirazh.balls:
                if ball_matrix[ball-1] == 0:
                    ball_matrix[ball-1] = 1
            if sum(ball_matrix) >= threshold:
                tirazhs += (tirazh.number, )
                result.append({"BallsCount": sum(ball_matrix), "TirazhCount": m, "Tirazhs": tirazhs})
                if m < min_:
                    min_ = m
                if m > max_:
                    max_ = m
                ball_matrix = [0 for i in range(0, self.__max_ball)]
                m = 1
                tirazhs = ()
            else:
                m += 1
                tirazhs += (tirazh.number, )
        result.append((min_, max_))
        return result

    """Подсчитывает сколько выпало шаров при tirazh_count тиражей"""
    def tirazh_balls_out(self, tirazh_count = 1):
        if tirazh_count < 1 or tirazh_count > self.__length:
            tirazh_count = 1
        result = []
        ball_matrix = [0 for i in range(0, self.__max_ball)]
        m = 1
        tirazhs = ()
        for tirazh in self.__results:
            for ball in tirazh.balls:
                if ball_matrix[ball-1] == 0:
                    ball_matrix[ball-1] = 1
            if m == tirazh_count:
                tirazhs += (tirazh.number, )
                result.append({"BallsCount": sum(ball_matrix), "TirazhCount": m, "Tirazhs": tirazhs})
                ball_matrix = [0 for i in range(0, self.__max_ball)]
                m = 1
                tirazhs = ()
            else:
                m += 1
                tirazhs += (tirazh.number, )
        return result

    def t_balls(self, res):
        ball_matrix = [0 for i in range(0, self.__max_ball)]
        for tirazh in res:
            for ball in tirazh.balls:
                if ball_matrix[ball-1] == 0:
                    ball_matrix[ball-1] = 1
        result = {"Balls": ball_matrix, "BallsCount": sum(ball_matrix)}
        return result

    def sum_balls_out(self, balls_out):
        ball_matrix = [0 for i in range(0, self.__max_ball)]
        result = []
        for item in balls_out:
            for tirazh_number in item["Tirazhs"]:
                tmp = self.get_tirazh_by_number(tirazh_number)
                for ball in tmp.balls:
                    ball_matrix[ball-1] += 1
            result.append(tuple(ball_matrix))
            ball_matrix = [0 for i in range(0, self.__max_ball)]
        return result

    def lottery_map(self):
        result = []
        for tirazh in self.__results:
            ball_matrix = [0 for i in range(0, self.__max_ball)]
            for ball in tirazh.balls:
                ball_matrix[ball-1] = 1
            result.append(tuple(ball_matrix))
        return result

    def position_map(self, position=1):
        result = []
        for tirazh in self.__results:
            ball_matrix = [0 for i in range(0, self.__max_ball)]
            ball = tirazh.balls[position-1]
            ball_matrix[ball-1] = 1
            result.append(tuple(ball_matrix))
        return result

    def compare_tirazhs_in_lottery(self, window=1):
        if window < 1:
            window = 1
        k = 0
        result = []
        while (k + window) < self.__length:
            tmp = compare_tirazhs(self.__results[k], self.__results[k+window])
            result.append(tmp)
            k += 1
        return result

    def compare_block_tirazhs_in_lottery(self):
        result = []
        if self.filter_length > 1:
            for i in range(self.filter_length-1):
                result.append([])
            for i in range(0, self.length - self.filter_length, self.filter_length):
                for j in range(self.filter_length-1):
                    #print(self.__results[i+j].number, self.__results[i+self.filter_length-1].number)
                    tmp = compare_tirazhs(self.__results[i+j], self.__results[i+self.filter_length-1])
                    result[j].append(tmp)

        return result

    def compare_tirazhs_with_last(self):
        result = []
        last_tirazh = self.__results[-1:][0]
        for tirazh in self.__results[:-1]:
            tmp = compare_tirazhs(tirazh, last_tirazh)
            result.append(tmp)
        return result

    def compare_tirazhs_with_static(self, tirazh_number):
        result = []
        static = self.get_tirazh_by_number(tirazh_number, False)
        for tirazh in self.__results[tirazh_number+1:]:
            tmp = compare_tirazhs(static, tirazh)
            result.append(tmp)
        return result

    def combinations_statistics(self, n=2):
        result = collections.Counter()
        for tirazh in self.__results:
            combinations = tirazh.get_combinations(n)
            for combination in combinations:
                result.update((combination,))
        return result

    """Среднее число повторов и предидущего тиража в следующий"""
    def repeats_teor(self):
        return (self.tirazh_length**2)/self.max_ball

    """Теоретическая вероятность появления комбинаций 1,2,3,... в лотерее"""
    def probability_of_combination_teor(self, m=1):
        if m > self.tirazh_length:
            m = self.tirazh_length
        a = 1
        b = 1
        for i in range(self.tirazh_length-m+1, self.tirazh_length+1):
            a *= i
        for i in range(self.max_ball-m+1, self.max_ball+1):
            b *= i
        return a/b

    @property
    def min_ball(self):
        return self.__min_ball

    @property
    def max_ball(self):
        return self.__max_ball

    @property
    def tirazh_length(self):
        return self.__tirazh_length

    @property
    def length(self):
        return self.__length

    @property
    def results(self):
        return self.__results

    @property
    def is_sort(self):
        return self.__is_sort


def compare_tirazhs(tirazh1, tirazh2):
    result = [0 for i in range(0, tirazh1.length)]
    for ball in tirazh1.balls:
        if ball in tirazh2.balls:
            result[tirazh1.balls.index(ball)] = 1
    return tuple(result)