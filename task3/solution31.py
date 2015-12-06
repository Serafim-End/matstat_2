# coding: utf-8

import random
import matplotlib.pyplot as plt
import math


def gen(n, lambd, check_nu):
    """
    генерирование статистики
    :param lambd: ожидание
    :return: список с элементами статистики
    """
    return [random.expovariate(lambd=lambd) + check_nu for i in xrange(n)]


def calc_average(x):
    """
    расчет среднего элемента в массиве
    :param x:
    :return:
    """
    return float(sum(x)) / len(x)


def calc_dispersion(av, x):
    """
    расчет выборочной дисперсии (несмещенной)
    :param av:
    :param x:
    :return:
    """
    return float(sum([(av - el) ** 2 for el in x])) / (len(x) - 1)


def calc_student(x, nu):
    """
    найти t статиcтику
    :param x:
    :param nu:
    :return:
    """
    qu = 1.895
    t = (float(calc_average(x) - nu) /
         (calc_dispersion(calc_average(x), x) / math.sqrt(len(x))))
    return qu <= abs(t)


def find_probability(n, cnt, nu, check_nu, crit=3):
    """
    На уровне значимости 5% проверьте гипотезу о
    равенстве математического ожидания трём против двусторонней альтернативы
    с помощью обычной t-статистики.
    :param n:
    :param cnt:
    :param nu:
    :param check_nu:
    :return:
    """
    result = 0
    crit += 0.5
    for i in xrange(n):
        gen_array = gen(cnt, nu, check_nu)
        if calc_student(gen_array, crit):
            result += 1
    return float(result) / n


def solve(n, cnt):
    """
    Оцените функцию мощности используемого критерия.
    Для этого варьируйте параметр θ данного вам распределения так,
    чтобы математическое ожидание изменялось в пределах от 1 до 5 с шагом 0.5.
    :param n: количество повторений
    :param cnt: размер выборки
    :return: строит график зависимости ожидания от вероятности
    """
    nu = 1
    values = []
    probabilities = []
    for i in xrange(9):
        values.append(nu)
        probabilities.append(find_probability(n, cnt, 3, nu))
        nu += 0.5
    #
    plt.plot(values, probabilities)
    plt.show()

if __name__ == '__main__':
    print("N = 1000 T = 8 E = 1: " + str(find_probability(10000, 8, 1, 2)))
    solve(10000, 8)

    print("N = 1000 T = 50 E = 1: " + str(find_probability(10000, 50, 1, 2)))
    solve(10000, 50)

    # print("N = 1000 T = 50 E = 1: " + str(find_probability(10000, 50, 1, 2)))
    # solve(10000, 50)
    #
    # print("N = 1000 T = 50 E = 1: " + str(find_probability(10000, 50, 1, 2)))
    # solve(10000, 50)





