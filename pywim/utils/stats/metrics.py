from sklearn import metrics

import numpy as np


def score_95_calc(metric_score, y, y_pred):
    if y.shape[0] < 1:
        print('size calc 0')
        return 0.0

    y_true = np.array([True] * y.shape[0])

    lb = y - y * 0.05
    ub = y + y * 0.05

    y_pred_95 = (lb < y_pred) == (y_pred < ub)
    y_pred_95 = y_pred_95 == True

    return metric_score(y_true, y_pred_95)


def score_95_base(metric_score, estimator, X_test, y_test):
    if y_test.shape[0] < 1:
        print('size base 0')
        return 0.0

    y_pred = estimator.predict(X_test)
    return score_95_calc(metric_score, y_test, y_pred)


def score_95_accuracy(estimator, X, y):
    return score_95_base(metrics.accuracy_score, estimator, X, y)


def score_95_precision(estimator, X, y):
    return score_95_base(metrics.precision_score, estimator, X, y)


def score_95_recall(estimator, X, y):
    return score_95_base(metrics.recall_score, estimator, X, y)


def score_95_f1_score(estimator, X, y):
    return score_95_base(metrics.f1_score, estimator, X, y)
