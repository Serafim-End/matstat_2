__author__ = 'nikita'

import random
import math
import numpy as np
import matplotlib.pyplot as plt


def f(x):
    return float(x) / ((1 + math.exp(x)) ** 2)


def solution1(a, b, test_number=100000, draw=False):
    function_array = []
    x_array = []

    file2_a = open("test2_a.txt", 'r+')
    for i in xrange(test_number):
        x = random.uniform(a, b)
        function_array.append(f(x))
        x_array.append(x)
        print >> file2_a, function_array[i]
    file2_a.close()

    if draw:
        draw_graph(f, range(a, b), x_coordinates=x_array, y_coordinates=function_array)

    result = sum(function_array) * (float(b - a) / test_number)
    print result
    return result


def draw_graph(formula, x_range, x_coordinates=None, y_coordinates=None):
    x = np.array(x_range)
    y = [formula(i) for i in x]
    plt.plot(x, y)

    if x_coordinates and y_coordinates:
        plt.plot(x_coordinates, y_coordinates)

    plt.show()

if __name__ == '__main__':
    print solution1(0, 5, test_number=100000, draw=True)
