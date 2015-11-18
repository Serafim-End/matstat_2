# coding: utf-8
from math import exp, log, sqrt
from random import randint
import matplotlib.pyplot as plt


def distribution_func(m, low=1, high=100):
    x = randint(low, high)
    if x < 0:
        return 0
    return m * exp(-m * x)


def back_distribution_func(y, m):
    return log(y / m) / (- m)


def distribution(count, teta=2., m=1.):
    x_numbs = []
    for i in xrange(count):
        real_x = back_distribution_func(distribution_func(m), m)
        x_numbs.append(real_x + teta)
    return x_numbs


def hypothesis(value=3, distribution_n=8,  test_numb=10000, t_kr=2.365):
    '''
    check whether m (lambda) equals value
    H0: m == 3
    Ha: m != 3
    :return:
    '''
    hypothesis_error_1 = 0
    for i in xrange(test_numb):
        x_numbs = distribution(distribution_n)
        middle_x = float(sum(x_numbs)) / len(x_numbs)
        # print 'middle x value: {}'.format(middle_x)
        s = sqrt(
            sum([(x_numbs[i] - middle_x) ** 2 for i in xrange(len(x_numbs))])
        )
        left_part = middle_x - t_kr * s / sqrt(distribution_n)
        right_part = middle_x + t_kr * s / sqrt(distribution_n)
        # print 'left part of t distribution: {}'.format(left_part)
        # print 'right part of t distribution: {}'.format(right_part)
        if left_part < 3 < right_part:
            hypothesis_error_1 += 1
    # print 'hypothesis error 1: {}'.format(hypothesis_error_1)
    pos_error_1 = 1 - float(hypothesis_error_1) / test_numb
    print 'possibility of first error: {}'.format(pos_error_1)


def solution_part_b(distribution_n=8, test_numb=10000, t_kr=2.365):
    '''
    Ha - m != ? get alternative hypothesis as true
    H0 - m == ?
    :param distribution_n:
    :param test_numb:
    :param t_kr:
    :return:
    '''
    result = {'real_m': [], 'pos': []}
    teta = 2
    for i in xrange(9):
        real_m = 1 + (teta - 2)
        teta += 0.5
        hypothesis_error_2 = 0
        for j in xrange(test_numb):
            x_numbs = distribution(distribution_n, teta=teta, m=real_m)
            middle_x = float(sum(x_numbs)) / len(x_numbs)
            s = sqrt(
                sum(
                    [(x_numbs[i] - middle_x) ** 2
                     for i in xrange(len(x_numbs))]
                )
            )
            left_part = middle_x - t_kr * s / sqrt(distribution_n)
            right_part = middle_x + t_kr * s / sqrt(distribution_n)
            if left_part < 3 < right_part:  # check this moment
                hypothesis_error_2 += 0
            else:
                hypothesis_error_2 += 1
        value = 1 - float(hypothesis_error_2) / test_numb
        result['pos'].append(value)
        result['real_m'].append(real_m)
        print 'real extension: {}'.format(real_m)
        print 'possiblity of alternative ' \
              'hypothesis will pick as wrong: {}'.format(value)
        print 'hypothesis error 2: {}'.format(hypothesis_error_2)

    plt.plot(result['pos'], result['real_m'])
    plt.xlabel('possibility')
    plt.ylabel('real extension')
    plt.show()

if __name__ == '__main__':
    # hypothesis()
    solution_part_b()
