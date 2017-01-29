"""
This method was based on these papers:

[1] OOMMEN, B. John; LOKE, Richard KS. Pattern recognition of strings with
substitutions, insertions, deletions and generalized transpositions.
Pattern Recognition, 1997, vol. 30, no 5, p. 789-800.

[2] D.W. van Boxel, MSc and Ing. R.A. van Lieshout, MSc. Optimization Vehicle
Classification, 2003.

[3] VAN BOXEL, D. W.; VAN LIESHOUT, R. A.; VAN DOORN, R. A.
Weigh-in-Motion–Categorising vehicles.

"""
import numpy as np
import numba as nb


def layout(data):
    """
    Distances data in meters (veh_length, *axle_sep)

    The first value of the list is the vehicle's length.

    :param data: values of vehicle's length and axles distances
    :type data: tuple of float
    """
    ms_layout = '-O'
    cum_length = 100

    veh_length, *axle_sep = data
    veh_length *= 100
    axle_sep = [x*100 for x in axle_sep]

    axle_count = len(axle_sep) + 1

    i = 0
    limit_i = axle_count - 1
    while i < limit_i:
        j = 0
        limit_j = axle_sep[i] // 50
        while j < limit_j:
            ms_layout += '-'
            j += 1
        ms_layout += 'O'
        cum_length = cum_length + axle_sep[i] + 50
        i += 1

    ms_layout += '-'
    cum_length += 50

    i = 0
    limit_i = ((veh_length - cum_length) // 50) - 0
    while i < limit_i:
        ms_layout += '-'
        i += 1

    return ms_layout


def layout_to_int(vehicle_layout):
    layout_int = []
    for letter in vehicle_layout:
        layout_int.append(ord(letter))
    return np.array(layout_int, dtype=int)


@nb.njit(nb.i8(nb.int8, nb.int8))
def d_s(a, b):
    """
    d_s is a map from A X A -> R^+ and is called the Substitution Map. In
    particular, d_s(a, b) is the distance associated with substituting
    b for a, a,b ∈ A. For all a ∈ A, d_s(a,a) is generally assigned the value
    zero, although this is not Mandatory.

    """
    tilde = 126  # ~ 126
    hyphen = 45  # - 45
    star = 42  # * 42
    return (
        0 if a == b else
        0 if a == tilde and b == hyphen else  # '~' '-'
        0 if a == hyphen and b == tilde else  # '-' '~'
        0 if a == star and b == hyphen else  # '*' '-'
        0 if a == hyphen and b == star else  # '-' '*'
        100
    )


@nb.njit(nb.i8(nb.int8))
def d_i(a):
    """
    d_i(.) is a map from A -> R^+ and is called the Insertion Map. The quantity
    d_i(a) is the distance associated with inserting the symbol a ∈ A.

    """
    tilde = 126  # ~ 126
    hyphen = 45  # - 45
    star = 42  # * 42
    return (
        2 if a == hyphen else  # '-'
        1 if a == tilde else  # '~'
        3 if a == star else  # '*'
        100
    )


@nb.njit(nb.i8(nb.int8))
def d_e(a):
    """
    d_e(.) is a map from A -> R^+ and is called the Deletion or Erasure Map.
    The quantity d e (a) is the distance associated with deleting (or erasing)
    the symbol a ∈ A.

    """
    tilde = 126  # ~ 126
    hyphen = 45  # - 45
    star = 42  # * 42
    return (
        2 if a == hyphen else  # '-'
        1 if a == tilde else  # '~'
        3 if a == star else  # '*'
        100
    )


@nb.njit(nb.i8(nb.int8, nb.int8, nb.int8, nb.int8))
def d_t(a, b, c, d):
    """
    d t (.,.) is a map from A 2 X A 2 -> R^+ called the Transposition Map. The
    quantity d t (ab,cd) is the distance associated with transposing the string
    "ab" into "cd". This can be thought of as a "serial" operation: "ab" is
    first transposed to "ba" and subsequently the individual characters are
    substitute d.

    """
    return (
        0 if a == b and a == c and a == d else
        2 if a == d and b == c else
        d_s(a, d) + d_s(b, c)
    )


@nb.njit()
def D(x, y, Z):
    """

    Input: The strings X = x 1 ...x N and Y = y 1 ...y M , and the set of
        elementary edit distances defined using the five elementary functions
        d s (.,.), d i (.), d e (.,.), d t (.,.).
    Output : The distance D(X, Y) associated with editing X to Y using the SID
        and GT operations.
    :param x:
    :param y:
    :param Z: np.zeros((N, M))
    """
    N = len(x)
    M = len(y)

    # Z = np.zeros((N, M))
    i = 1
    while i < N:
        Z[i, 0] = Z[i-1, 0] + d_e(x[i])
        i += 1

    j = 1
    while j < M:
        Z[0, j] = Z[0, j-1] + d_i(y[j])
        j += 1

    i = 1
    while i < N:
        Z[i, 1] = min(
            Z[i-1, 1] + d_e(x[i]), Z[i, 0] + d_i(y[1]),
            Z[i-1, 0] + d_s(x[i], y[1])
        )
        i += 1

    j = 2
    while j < M:
        Z[1, j] = min(
            Z[1, j-1] + d_i(y[j]), Z[0, j] + d_e(x[1]),
            Z[0, j-1] + d_s(x[1], y[j])
        )
        j += 1

    i = 2
    while i < N:
        j = 2
        while j < M:
            Z[i, j] = min(
                Z[i-1, j] + d_e(x[i]),
                Z[i, j-1] + d_i(y[j]),
                Z[i-1, j-1] + d_s(x[i], y[j]),
                Z[i-2, j-2] + d_t(x[i-1], x[i], y[j-1], y[j])
            )
            j += 1
        i += 1
    return Z[N-1, M-1]
