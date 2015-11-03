__author__ = 'nikita'

import random
from solution1 import f


def solution2(a, b, n=100000, max_y=None, min_y=0):
    max_y = max([f(random.uniform(a, b)) for i in xrange(10 * n)]) if not None else max_y
    print max_y
    coordinates = [(random.uniform(a, b), random.uniform(min_y, max_y)) for i in xrange(n)]

    file2_b = open('test2_b.txt', 'r+')
    k = 0
    for x, y in coordinates:
        print >> file2_b, (x, y)
        if f(x) >= y:
            k += 1
    file2_b.close()

    return (max_y - min_y) * (b - a) * (float(k) / n)


if __name__ == '__main__':
    print solution2(0, 5, n=100000)
