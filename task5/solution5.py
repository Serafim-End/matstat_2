import re
import os

import numpy as np
import statsmodels.api as sm

F_table = 3.06  # F(n - m - 1, m) = 3.06 = F(15, 4) where n = 20, m = 4


def make_model(params):
    dict_data = get_data()
    y = dict_data['prices']

    sparse_matrix, i = [], 1
    for name, value in dict_data.iteritems():
        if name != 'prices':
            print 'x{} = {}'.format(i, name)
            sparse_matrix.append(value)
            i += 1

    ones = np.ones(len(sparse_matrix[0]))
    X = sm.add_constant(np.column_stack((sparse_matrix[0], ones)))
    for ele in sparse_matrix[1:]:
        X = sm.add_constant(np.column_stack((ele, X)))
    regression = sm.OLS(y, X).fit()
    model_significance(F_table, regression.fvalue)
    make_example(params, coef=regression.params,)
    print regression.summary()

    # Akaike information criterion aic
    # Bayesian information criterion bik


def model_significance(f_table, f_model):
    print '=' * 78
    template = 'Significance of the model: {}'
    if f_model > f_table:
        print template.format('model is significant')
    else:
        print template.format('model is not significant')
    print '=' * 78


def make_example(params, coef):
    print '=' * 78
    print 'Expected price of Ceylon tea: {}'.format(
        sum([params[i] * coef[i] for i in xrange(len(params))]) + coef[-1]
    )
    print '=' * 78


def get_data_from_file(filename):
    return [float(re.sub('\n', '', line)) for line in open(filename, 'r')]


def get_data():
    dict_data = {}
    for filename in ['prices.txt', 'prchinas.txt',
                     'prcoffees.txt', 'prkenias.txt', 'prindians.txt']:
        dict_data[filename.split('.')[0]] = get_data_from_file(
            os.path.join('DATA', filename))
    return dict_data


if __name__ == '__main__':
    make_model(params=[14, 13, 17, 15])  # coffee, kenia, china, india

