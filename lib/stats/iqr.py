from scipy.stats import scoreatpercentile
import pandas as pd
import numpy as np


def iqr(data: pd.Series, min_value=None) -> (float, float):
    """
    IQR: Q3-Q1
    Outlier: Q3 + 1.5*(IQR) > DATA < Q1 - 1.5*IQR

    :param data: pd.Series
    :return: mask considering lower bound and upper bound

    """
    _data = data.copy()

    if min_value is not None:
        _data = data[data >= min_value]

    q1 = scoreatpercentile(_data, 25)
    q3 = scoreatpercentile(_data, 75)
    _iqr = q3-q1

    lb = q1 - _iqr*1.5
    ub = q3 + _iqr*1.5

    return np.all(((lb <= data.values), (data.values <= ub)), 0)


def reject_outliers(data: pd.Series) -> pd.Series:
    """

    :param data:
    :return:
    """
    return data[iqr(data)].reset_index(drop=True)
