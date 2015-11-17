# coding: utf-8
from math import sqrt
import re

def get_data():
    x_numbs = []
    y_numbs = []

    for line in open('data_files.txt', 'r'):
        x, y = line.strip().split()
        x = re.sub(',', '.', x)
        y = re.sub(',', '.', y)
        x = re.sub('-', '-', x)
        y = re.sub('-', '-', y)
        x = float(x)
        y = float(y)
        x_numbs.append(x)
        y_numbs.append(y)

    return x_numbs, y_numbs


def pirson():
    x_numbs, y_numbs = get_data()

    middle_x = float(sum(x_numbs)) / len(x_numbs)
    middle_y = float(sum(y_numbs)) / len(y_numbs)

    cov = 0
    sx = 0
    sy = 0
    for i in xrange(len(x_numbs)):
        cov += (x_numbs[i] - middle_x) * (y_numbs[i] - middle_y)
        sx += (x_numbs[i] - middle_x) ** 2
        sy += (y_numbs[i] - middle_y) ** 2

    return float(cov) / sqrt(sx * sy)


def prepare_dict(x_numbs):
    x_dict = {}
    x_numbs_copy = [abs(x) for x in x_numbs]
    for i in xrange(1, len(x_numbs) + 1):
        minimum = min(x_numbs_copy)
        for el in x_numbs:
            if abs(el) == minimum:
                x_dict[i] = el
        if i > 1 and x_dict[i - 1] == x_dict[i]:
            pass
        x_numbs_copy.remove(minimum)
    return x_dict


def prepare2(x_numbs):
    x_dict0 = {i + 1: x for i, x in enumerate(x_numbs)}
    x_dict = prepare_dict(x_numbs)

    x_true = []
    for k, v in x_dict0.iteritems():
        for k1, v1 in x_dict.iteritems():
            if v == v1:
                x_true.append(k1)
    return x_true


def spirmen():
    x_numbs, y_numbs = get_data()
    x_true = prepare2(x_numbs)
    y_true = prepare2(y_numbs)

    dsquare = []
    for i in xrange(len(x_true)):
        dsquare.append((x_true[i] - y_true[i]) ** 2)
    return 1 - float(6 * sum(dsquare)) / (len(x_numbs) * ((len(x_numbs) ** 2) - 1))


def t_statistics():
    x_numbs, y_numbs = get_data()
    pirson_value = pirson()
    spirmen_value = spirmen()
    tkr1 = t_kr(pirson_value, len(x_numbs))
    tkr2 = t_kr(spirmen_value, len(x_numbs))

    tstable = 2.021
    if -tstable < tkr1 < tstable:
        print 'H0 верна с ошибкой первого рода (Ковариация Пирсона)'
    else:
        print 'H0 отвергается (Ковариация Пирсона)'

    if -tstable < tkr2 < tstable:
        print 'H0 верна с ошибкой первого рода(Ковариация Спирмена)'
    else:
        print 'H0 отвергается (Ковариация Пирсона)'


def t_kr(value, count):
    return float(abs(value) * sqrt(count - 1)) / sqrt(1 - (value ** 2))

if __name__ == '__main__':
    t_statistics()
    # print pirson()
    # print spirmen()