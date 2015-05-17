from scipy import stats
import numpy as np
import sys


def peakdet(
    v, delta: float, threshold: float=None, threshold_margin_factor=4,
    max_threshold_min_distance=120, x=None, filter_by_area=False
):
    """

    :param threshold:
    :param max_threshold_min_distance:
    :param v:
    :param delta:
    :param threshold_margin_factor:
    :param x:

    Converted from MATLAB script at http://billauer.co.il/peakdet.html

    Returns two arrays

    function [maxtab, mintab]=peakdet(v, delta, x)
    %PEAKDET Detect peaks in a vector
    %        [MAXTAB, MINTAB] = PEAKDET(V, DELTA) finds the local
    %        maxima and minima ("peaks") in the vector V.
    %        MAXTAB and MINTAB consists of two columns. Column 1
    %        contains indices in V, and column 2 the found values.
    %
    %        With [MAXTAB, MINTAB] = PEAKDET(V, DELTA, X) the indices
    %        in MAXTAB and MINTAB are replaced with the corresponding
    %        X-values.
    %
    %        A point is considered a maximum peak if it has the maximal
    %        value, and was preceded (to the left) by a value lower by
    %        DELTA.

    % Eli Billauer, 3.4.05 (Explicitly not copyrighted).
    % This function is released to the public domain; Any use is allowed.

    """
    maxtab = []
    mintab = []

    if x is None:
        x = np.arange(len(v))

    v = np.asarray(v)

    if len(v) != len(x):
        sys.exit('Input vectors v and x must have same length')

    if not np.isscalar(delta):
        sys.exit('Input argument delta must be a scalar')

    if delta <= 0:
        sys.exit('Input argument delta must be positive')

    mn, mx = np.Inf, -np.Inf
    mnpos, mxpos = np.NaN, np.NaN

    lookformax = True

    if delta*threshold_margin_factor > v.max():
        # minimun threshold
        delta = v.max()/(threshold_margin_factor*2)

    if threshold is None:
        threshold = v.max()*delta
    else:
        threshold *= v.max()

    for i in np.arange(len(v)):
        this = v[i]
        if this > mx:
            mx = this
            mxpos = x[i]
        if this < mn:
            mn = this
            mnpos = x[i]

        if lookformax:
            if this < mx-delta and mx:
                maxtab.append((mxpos, mx))
                mn = this
                mnpos = x[i]
                lookformax = False
        else:
            if this > mn+delta:
                mintab.append((mnpos, mn))
                mx = this
                mxpos = x[i]
                lookformax = True
    # remove the first item if its position is equal to zero
    if maxtab and maxtab[0][0] == 0:
        maxtab.pop(0)

    # threshold
    if maxtab:
        maxtab_with_threshold = []
        for i, local_max_value in enumerate(maxtab):
            if local_max_value[1] > delta and local_max_value[1] > threshold:
                if filter_by_area and v.shape[0]:
                    peak = local_max_value[0]
                    lb = peak - 120
                    ub = peak + 120

                    if lb < 0:
                        lb = 0

                    if ub > v.shape[0]:
                        ub = v.shape[0]

                    curve = v[lb:ub]

                    try:
                        curve -= curve.min()
                    except:
                        import traceback

                        print(curve)
                        print(v)
                        print(lb, ub)
                        print(traceback.format_exc())
                        raise Exception('XXXX')

                    if (curve.sum()**2/curve.max()**2)/100 > 120.0:
                        continue

                if i == 0:
                    maxtab_with_threshold.append(local_max_value)
                elif local_max_value[0] - maxtab[i-1][0] > (
                    max_threshold_min_distance
                ):
                    maxtab_with_threshold.append(local_max_value)
                elif local_max_value[1] > maxtab[i-1][1]:
                    if not maxtab_with_threshold:
                        maxtab_with_threshold.append(local_max_value)
                    else:
                        maxtab_with_threshold[-1] = local_max_value
        maxtab = maxtab_with_threshold

    return np.array(maxtab), np.array(mintab)