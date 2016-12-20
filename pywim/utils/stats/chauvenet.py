# Demonstrate criterion of Chauvenet to exclude poor data
from scipy.special import erf, erfc
import numpy as np
import pandas as pd


def chauvenet(y, mean=None, stdv=None) -> np.Array:
    #-----------------------------------------------------------
    # Input:  NumPy arrays x, y that represent measured data
    #         A single value of a mean can be entered or a
    #         sequence of means with the same length as
    #         the arrays x and y. In the latter case, the
    #         mean could be a model with best-fit parameters.
    # Output: It returns a boolean array as filter.
    #         The False values correspond to the array elements
    #         that should be excluded
    #
    # First standardize the distances to the mean value
    # d = abs(y-mean)/stdv so that this distance is in terms
    # of the standard deviation.
    # Then the  CDF of the normal distr. is given by
    # phi = 1/2+1/2*erf(d/sqrt(2))
    # Note that we want the CDF from -inf to -d and from d to +inf.
    # Note also erf(-d) = -erf(d).
    # Then the threshold probability = 1-erf(d/sqrt(2))
    # Note, the complementary error function erfc(d) = 1-erf(d)
    # So the threshold probability pt = erfc(d/sqrt(2))
    # If d becomes bigger, this probability becomes smaller.
    # If this probability (to obtain a deviation from the mean)
    # becomes smaller than 1/(2N) than we reject the data point
    # as valid. In this function we return an array with booleans
    # to set the accepted values.
    #
    # use of filter:
    # xf = x[filter]; yf = y[filter]
    # xr = x[~filter]; yr = y[~filter]
    # xf, yf are cleaned versions of x and y and with the valid entries
    # xr, yr are the rejected values from array x and y
    #-----------------------------------------------------------
    """
    source: https://www.astro.rug.nl/software/kapteyn/
    :param x:
    :param y:
    :param mean:
    :param stdv:
    :return:
    """
    if mean is None:
        mean = y.mean()           # Mean of incoming array y
    if stdv is None:
        stdv = y.std()            # Its standard deviation

    N = len(y)                   # Lenght of incoming arrays
    criterion = 1.0/(2*N)        # Chauvenet's criterion
    d = abs(y-mean)/stdv         # Distance of a value to mean in stdv's
    d /= 2.0**0.5                # The left and right tail threshold values

    prob = erfc(d)               # Area normal dist.
    mask = prob >= criterion   # The 'accept' filter array with booleans

    return mask                # Use boolean array outside this function


def reject_outliers(data: pd.Series) -> pd.Series:
    return data[chauvenet(data)].reset_index(drop=True)
