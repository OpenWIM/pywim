"""
Nmrglue is a module for working with NMR data in Python.
When used with the NumPy, SciPy, and matplotlib packages nmrglue provides a
robust environment for rapidly developing new methods for processing,
analyzing, and visualizing NMR data. Nmrglue also provides a
framework for connecting existing NMR software packages.

A collection of NMR processing functions for filtering, smoothing, and
correcting spectral baselines.

J.J. Helmus, C.P. Jaroniec, Nmrglue:
An open source Python package for the analysis of multidimensional NMR data,
J. Biomol. NMR 2013, 55, 355-367. 10.1007/s10858-013-9718-x.

@see: https://code.google.com/p/nmrglue/

"""
import numpy as np
import scipy
import scipy.ndimage
import scipy.signal


def base(data, nl, nw=0):
    """
    Linear (first-order) Baseline Correction based on node list.

    Parameters:

    * data  Array of spectral data.
    * nl    List of baseline nodes.
    * nw    Node half-width in points.

    """

    if data.ndim == 1:
        data -= calc_bl_linear(data, nl, nw)
    else:   # for 2D array loop over traces
        for i, vec in enumerate(data):
            data[i] -= calc_bl_linear(vec, nl, nw)
    return data


def calc_bl_linear(x, nl, nw=0):
    """
    Calculate a baseline using linear approximation between nodes

    Parameters:

    * x     1D data
    * nl    List of baseline nodes
    * nw    Node half-width in points

    """
    bl = np.zeros_like(x)
    for i in range(len(nl)-1):
        # minimum and maximum index
        _min = nl[i]
        _max = nl[i+1]

        # linspace s1 and s2
        s1 = x[_min-nw:_min+nw+1].mean()
        s2 = x[_max-nw:_max+nw+1].mean()
        bl[_min:_max+1] = np.linspace(s1, s2, _max-_min+1)
    return bl


def cbf(data, last=10, apply=slice(None)):
    """
    Constant Baseline correction

    Parameters:

    * data  Array of spectral data.
    * last  Percent of -1 axis used to calculate correction.
    * apply Slice describing 0th-axis region(s) to apply correction to.
            Ignored in 1D data.

    """
    # calculate the correction
    n = data.shape[-1]*last/100.+1.
    corr = data[..., int(-n):].sum(axis=-1)/n

    # apply correction
    if data.ndim == 2:
        data[apply] = data[apply] - np.array([corr]).transpose()[apply]
        return data
    else:
        return data-corr


def cbf_explicit(data, calc=slice(None), apply=slice(None)):
    """
    Constant Baseline - explicit region

    Parameters:

    * data  Array of spectral data.
    * calc  Slice describing region to use for calculating correction.
    * apply Slice describing 0th-axis region(s) to apply correction to.
            Ignored in 1D data.

    """
    # calculate correction
    n = len(range(data.shape[-1])[calc])
    corr = data[..., calc].sum(axis=-1)/n

    # apply correction
    if data.ndim == 2:
        data[apply] = data[apply] - np.array([corr]).transpose()[apply]
        return data
    else:
        return data-corr


def med(data, mw=24, sf=16, sigma=5.0):
    """
    Median baseline correction

    Algorith described in:
    Friedrichs, M.S. JBNMR 1995 5 147-153.

    Parameters:

    * data  Array of spectral data.
    * mw    Median Window size in pts.
    * sf    Smooth window size in pts.
    * sigma Standard-deviation of Gaussian in convolution

    """
    if data.ndim == 1:
        data -= calc_bl_med(data, mw, sf, sigma)
    else:
        for i, vec in enumerate(data):
            data[i] = vec - calc_bl_med(vec, mw, sf, sigma)
    return data


def calc_bl_med(x, mw, sf, sigma):
    """
    Calculate a baseline using median baseline correction.

    Algorithm described in:
    Friedrichs, M.S. JBNMR 1995 5 147-153

    Parameter:

    x       1D data
    mw      Median Window size in pts.
    sf      Smooth window size in pts.
    sigma   Standard-deviation of Gaussian in convolution.

    """

    # create extrema array (non extrema values are masked out)
    mask = x == scipy.ndimage.median_filter(x, size=3)
    mask[0] = False  # first pt always extrema
    mask[-1] = False  # last pt always extrema
    e = np.ma.masked_array(x, mask)

    # fill in the median vector
    # half_mw = mw/2
    m = scipy.ndimage.median_filter(e, mw+1, mode="mirror")
    # using the median_filter might give slightly different results than
    # described algorithm but is MUCH faster

    # convolve with a gaussian
    g = scipy.signal.gaussian(sf, sigma)
    g = g/g.sum()

    return scipy.signal.convolve(m, g, mode='same')


def sol_general(data, _filter, w=16, mode='same'):
    """
    Solvent filter with generic filter.

    Algorithm described in:
    Marion et al. JMR 1989 84 425-430

    Parameters:

    * data   Array of spectral data.
    * filter filter to convolve with data
    * mode   mode for output ('valid','same', or 'full')

    """
    A = _filter.sum()
    if data.ndim == 2:
        _filter = np.atleast_2d(_filter)
    return data-scipy.signal.convolve(data, _filter, mode=mode)/A


def sol_boxcar(data, w=16, mode='same'):
    """
    Solvent filter with boxcar filter.

    Parameters:

    * data   Array of spectral data.
    * w      Width of convolution window.
    * mode   mode for output ('valid','same', or 'full')

    """
    _filter = scipy.signal.boxcar(w)
    return sol_general(data, _filter, w=w, mode=mode)


def sol_sine(data, w=16, mode='same'):
    """
    Solvent filter with sine-bell filter.

    Parameters:

    * data   Array of spectral data.
    * w      Width of convolution window.
    * mode   mode for output ('valid','same', or 'full')

    """
    _filter = np.cos(np.pi*np.linspace(-0.5, 0.5, w))
    return sol_general(data, _filter, w=w, mode=mode)


def sol_sine2(data, w=16, mode='same'):
    """
    Solvent filter with square sine-bell filter.

    Parameters:

    * data   Array of spectral data.
    * w      Width of convolution window.
    * mode   mode for output ('valid','same', or 'full')

    """
    _filter = np.cos(np.pi*np.linspace(-0.5, 0.5, w))**2
    return sol_general(data, _filter, w=w, mode=mode)


def sol_gaussian(data, w=16, mode='same'):
    """
    Solvent filter with square gaussian filter.

    Parameters:

    * data   Array of spectral data.
    * w      Width of convolution window.
    * mode   mode for output ('valid','same', or 'full')

    """
    _filter = scipy.signal.gaussian(w, w/2.)
    return sol_general(data, _filter, w=w, mode=mode)
