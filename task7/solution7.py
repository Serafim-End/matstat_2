import os

import numpy as np
import statsmodels.api as sm


def get_data(filename, variant):
    with open(filename, 'r') as raw_file:
        type_parameters = raw_file.readline()
        type_parameters = type_parameters.split(';')
        to_find = '_v{}'.format(str(variant))
        prm_indexes = [i for i in xrange(len(type_parameters))
                       if type_parameters[i].find(to_find) > -1]
        data = {type_parameters[i].split('_')[0]: [] for i in prm_indexes}
        for line in raw_file:
            prms = line.split(';')
            for j in xrange(len(prms)):
                if j in prm_indexes:
                    tprm_name = type_parameters[j].split('_')[0]
                    data[tprm_name].append(float(prms[j]))
        return data


def make_models(filename, variant):
    data = get_data(filename, variant)
    matrix, i = [], 1
    for k, v in data.iteritems():
        if k != 'survived' and k != 'class4':
            print 'x_{}: {}'.format(i, k)
            matrix.append(v)
            i += 1
    models_pattern(data, matrix)


def models_pattern(data, matrix):
    y = np.array(data['survived'])
    ones = np.ones(len(matrix[0]))
    X = sm.add_constant(np.column_stack((matrix[0], ones)))
    for ele in matrix[1:]:
        X = sm.add_constant(np.column_stack((ele, X)))
    logit_model = sm.Logit(y, X)
    logit_res = logit_model.fit(maxiter=2000)
    print logit_res.summary()
    print logit_res.wald_test('1*x1 + 1*x2 + 1*x3')
    print
    probit_model = sm.Probit(y, X)
    probit_res = probit_model.fit(maxiter=2000)
    print probit_res.summary()
    print logit_res.wald_test('1*x1 + 1*x2 + 1*x3')
    print
    linear_model = sm.OLS(y, X)
    linear_res = linear_model.fit(maxiter=2000)
    result = 0.
    for array in X:
        for i, item in enumerate(array):
            result += linear_res.params[i] * item
    result /= (len(X))
    print 'Linear function value: {}'.format(result)
    print linear_res.summary()
    print linear_res.wald_test('1*x1 + 1*x2 + 1*x3')
    print


def make_add_models(filename, variant):
    data = get_data(filename, variant)
    sex = data['sex']
    new_data = {}
    for k, v in data.iteritems():
        if k.find('class') > -1:
            new_data['sex_{}'.format(k)] =\
                [sex[i] * v[i] for i in xrange(len(v))]

    for k, v in new_data.iteritems():
        data[k] = v

    matrix = [v for k, v in data.iteritems()
              if k != 'survived' and k != 'class4' and k !='sex_class4']

    i = 0
    for k, v in data.iteritems():
        if k != 'survived' and k != 'class4' and k != 'sex_class4':
            print 'x_{} = {}'.format(i + 1, k)
            i += 1

    models_pattern(data, matrix)

if __name__ == '__main__':
    make_models(os.path.join('DATA', 'auto.txt'), 5)
    make_add_models(os.path.join('DATA', 'auto.txt'), 5)
