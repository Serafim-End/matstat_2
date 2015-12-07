import re
import os

import numpy as np
import statsmodels.api as sm
from statsmodels.graphics.api import abline_plot
from scipy import stats
from matplotlib import pyplot as plt
from statsmodels import graphics
from statsmodels.stats.outliers_influence import reset_ramsey


def make_model(draw=True):
    dict_data = get_data()
    y = dict_data['y_param']

    sparse_matrix, i = [], 1
    for name, value in dict_data.iteritems():
        if name != 'y_param':
            print 'x{} = {}'.format(i, name)
            sparse_matrix.append(value)
            i += 1

    ones = np.ones(len(sparse_matrix[0]))
    X = sm.add_constant(np.column_stack((sparse_matrix[0], ones)))
    for ele in sparse_matrix[1:]:
        X = sm.add_constant(np.column_stack((ele, X)))

    glm_binom = sm.GLM(y, X)
    res = glm_binom.fit()

    # general info about Gaussian Model (Exp model)
    print res.summary()

    # This is a general specification test,
    # for additional non-linear effects in a model.
    # If the p-value of the f-test is below a threshold, e.g. 0.1, then this
    # indicates that there might be additional non-linear effects in the model
    # and that the linear model is mis-specified.
    print reset_ramsey(res, len(sparse_matrix))

    check_sum_params(res.params)

    if draw:
        y_sum = sum(y)
        y = [float(item) / y_sum for item in y]
        yhat = res.mu
        make_observed_values(yhat, y)
        make_residual_dependence(yhat, res.resid_pearson)
        make_normalised_distribution(res.resid_deviance.copy())


def check_sum_params(params):
    if sum(params[:len(params) - 2:]) < 1:
        print 'Ho error'
    else:
        print 'Ho possible'


def make_normalised_distribution(resid):
    fig, ax = plt.subplots()
    resid_std = stats.zscore(resid)
    ax.hist(resid_std, bins=25)
    ax.set_title('Histogram of standardized deviance residuals');
    graphics.gofplots.qqplot(resid, line='r')
    plt.show()


def make_observed_values(yhat, y):
    fig, ax = plt.subplots()
    ax.scatter(yhat, y)
    line_fit = sm.OLS(y, sm.add_constant(yhat, prepend=True)).fit()
    abline_plot(model_results=line_fit, ax=ax)
    ax.set_title('Model Fit Plot')
    ax.set_ylabel('Observed values')
    ax.set_xlabel('Fitted values')
    plt.show()


def make_residual_dependence(yhat, resid_pearson):
    fig, ax = plt.subplots()
    ax.scatter(yhat, resid_pearson)
    ax.hlines(0, min(yhat), max(yhat), color='r')
    ax.set_title('Residual Dependence Plot')
    ax.set_ylabel('Pearson Residuals')
    ax.set_xlabel('Fitted values')
    plt.show()


def get_data_from_file(filename):
    return [float(re.sub('\n', '', line)) for line in open(filename, 'r')]


def get_data():
    dict_data = {}
    for filename in ['k_param.txt', 'l_param.txt',
                     'y_param.txt']:
        dict_data[filename.split('.')[0]] = get_data_from_file(
            os.path.join('DATA', filename))
    return dict_data


if __name__ == '__main__':
    make_model(draw=False)