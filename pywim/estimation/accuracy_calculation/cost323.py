from scipy.stats import norm
from scipy.optimize import fsolve
from scipy import stats

import numpy as np
import pandas as pd


def calc_min_confidence(
    data: pd.DataFrame, test_plan: str, env_condition: str
):
    """
    =100*(2*NORMDIST(\\
      IF(\$B\$5="r1";2,675/IF(\$D\$5="III";1,1;IF(\$D\$5="II";1,05;1));\\
      IF(\$B\$5="r2";2,36/IF(\$D\$5="III";1,1;IF(\$D\$5="II";1,05;1));\\
        IF(\$B\$5="RR1";2,155/IF(\$D\$5="III";1,1;IF(\$D\$5="II";1,05;1));\\
          IF(\$B\$5="RR2";2/IF(\$D\$5="III";1,1;IF(\$D\$5="II";1,05;1));0))\\
      ))-TINV(0,05;B9-1)/SQRT(B9);0;1;TRUE())-1)

    """

    # data = data.copy()

    def _calc(v: float):

        if env_condition == 'I':
            _v = 1
        elif env_condition == 'II':
            _v = 1.05
        elif env_condition == 'III':
            _v = 1.1
        else:
            raise Exception('INVALID_ENV_CONDITION')

        if test_plan == 'R1':
            _v = 2.675 / _v
        elif test_plan == 'R2':
            _v = 2.36 / _v
        elif test_plan == 'RR1':
            _v = 2.155 / _v
        elif test_plan == 'RR2':
            _v = 2 / _v
        else:
            raise Exception('INVALID_TEST_PLAN')

        # in isf, the probabity is divided by 2
        # because in excel TINV is 2-side tail
        return 100 * (
            2 * norm.cdf(_v - stats.t.isf(0.05 / 2, v - 1) / np.sqrt(v), 0,
                         1) - 1
        )

    test_plan = test_plan.upper()
    env_condition = env_condition.upper()

    data['min_confidence'] = data.number.apply(_calc)

    return data


def calc_best_acceptable_class(
    data: pd.DataFrame, initial_verification: bool
) -> pd.DataFrame:
    """

    """
    # data = data.copy()
    # IF(M$4=0;1;1,25)
    factor = 1.25 if initial_verification else 1
    best_acceptable_class = []

    # gwv
    # =I9∗IF(M$4=0;1;1,25)
    best_acceptable_class.append(data.loc['gwv', 'min_tolerance'] * factor)

    # group of axles
    # =IF(I10<10; 0,7∗I10∗IF(M$4=0;1;1,25); I10∗IF(M$4=0;1;1,25)−3)
    v = data.loc['group_axles', 'min_tolerance']
    v = v * 0.7 * factor if v < 10 else v * factor - 3
    best_acceptable_class.append(v)

    # single axle
    # =IF(I11<15;
    #     I11∗(I11∗IF(M$4=0;1;1,25)+97)∗IF(M$4=0;1;1,25)/168;
    #     I11∗IF(M$4=0;1;1,25)−5)
    v = data.loc['single_axle', 'min_tolerance']
    v = v * (v * factor + 97) * factor / 168 if v < 15 else v * factor - 5
    best_acceptable_class.append(v)

    # axle of a group
    # =IF(I12<20;I12∗IF(M$4=0;1;1,25)/2;(I12∗IF(M$4=0;1;1,25)−10))
    v = data.loc['axle_group', 'min_tolerance']
    v = v * factor / 2 if v < 20 else v * factor - 10
    best_acceptable_class.append(v)

    data['best_acceptable_class'] = best_acceptable_class
    return data


def calc_classification(data: pd.DataFrame) -> pd.DataFrame:
    """
    =IF(OR(J9<=5;J9>7);ROUNDUP((J9/5);0)*5;7)

    """

    def _calc(v: float):
        # =IF(OR(J9<=5;J9>7);ROUNDUP((J9/5);0)*5;7)
        return np.ceil(v / 5) * 5 if v <= 5 or v > 7 else 7

    data['class_value'] = data.best_acceptable_class.apply(_calc)

    return data


def resolve_class_name(data: pd.DataFrame) -> pd.DataFrame:
    """
    =IF(K9<=5;CONCATENATE("A(";TEXT(K9;"0");")");\\
      IF(K9<=7;CONCATENATE("B+(";TEXT(K9;"0");")");\\
        IF(K9<=10;CONCATENATE("B(";TEXT(K9;"0");")");\\
          IF(K9<=15;CONCATENATE("C(";TEXT(K9;"0");")");\\
            IF(K9<=20;CONCATENATE("D+(";TEXT(K9;"0");")");\\
              IF(K9<=25;CONCATENATE("D(";TEXT(K9;"0");")");\\
                CONCATENATE("E(";TEXT(K9;"0");")")))))))
    """

    def _resolve(v: int):
        c = (
            'A' if v <= 5 else
            'B+' if v <= 7 else
            'B' if v <= 10 else
            'C' if v <= 15 else
            'D+' if v <= 20 else
            'D' if v <= 25 else
            'E'
        )
        return '%s(%s)' % (c, int(v))

    data['class_name'] = data.class_value.apply(_resolve)
    return data


def calc_delta(data: pd.DataFrame, initial_verification: bool):
    """

    """
    d = []
    # factor
    # IF(M$4=0;1;0,8)
    factor = 0.8 if initial_verification else 1

    # gwv
    # =K9*IF(M$4=0;1;0,8)
    d.append(data.loc['gwv', 'class_value'] * factor)

    # group of axles
    # =IF(K10<7;K10/0,7;IF(K10<30;K10+3;K10*1,1))*IF(M$4=0;1;0,8)
    v = data.loc['group_axles', 'class_value']
    v = v / 0.7 if v < 7 else v + 3 if v < 30 else v * 1.1
    d.append(v * factor)

    # single axle
    # =IF(K11<10;K11*(85-K11)/50;IF(K11<25;K11+5;6*K11/5))*IF(M$4=0;1;0,8)
    v = data.loc['single_axle', 'class_value']
    v = v * (85 - v) / 50 if v < 10 else v + 5 if v < 25 else 6 * v / 5
    d.append(v * factor)

    # axle of group
    # =IF(K12<10;2*K12;IF(K12<25;K12+10;6*K12/5+5))*IF(M$4=0;1;0,8)
    v = data.loc['axle_group', 'class_value']
    v = 2 * v if v < 10 else v + 10 if v < 25 else 6 * v / 5 + 5
    d.append(v * factor)

    data['d'] = d
    return d


def calc_confidence_level(data: pd.DataFrame) -> pd.DataFrame:
    """
    * Number  (column B) [Input],
    * Identified (column C) [Input],
    * Mean (column D) [Input],
    * Std deviat (column E) [Input],
    * p_o (column F),
    * Class (column G),
    * d (column H),
    * d_min (column I) [Input/Minimization Solver Output],
    * d_c (column J),
    * class (column K),
    * p (column L) - related to column I,
    * p (column M) -  related to column H,
    * Accepted (column O)

    =100*(
        1-TDIST((H9/E9-D9/E9)-TINV(0,05;B9-1)/SQRT(B9);B9-1;1)-
        TDIST((H9/E9+D9/E9)-TINV(0,05;B9-1)/SQRT(B9);B9-1;1)
    )
    """

    def _calc(v: pd.Series) -> pd.Series:
        return 100 * (
            1 - stats.t.sf(
                (v.d / v['std'] - v['mean'] / v['std']) -
                stats.t.isf(0.05 / 2, v.number - 1) /
                np.sqrt(v.number),
                v.number - 1
            ) - stats.t.sf(
                (v.d / v['std'] + v['mean'] / v['std']) -
                stats.t.isf(0.05 / 2, v.number - 1) /
                np.sqrt(v.number), v.number - 1
            )
        )

    data['confidence_level'] = data.T.apply(_calc)
    return data


def resolve_accepted_class(data: pd.DataFrame) -> str:
    """
    O12 = MAX(K11:K12)

    =IF(O12<=5;CONCATENATE("A(";TEXT(O12;"0");")");\\
      IF(O12<=7;CONCATENATE("B+(";TEXT(O12;"0");")");\\
        IF(O12<=10;CONCATENATE("B(";TEXT(O12;"0");")");\\
          IF(O12<=15;CONCATENATE("C(";TEXT(O12;"0");")");\\
            IF(O12<=20;CONCATENATE("D+(";TEXT(O12;"0");")");\\
              IF(O12<=25;CONCATENATE("D(";TEXT(O12;"0");")");\\
                CONCATENATE("E(";TEXT(O12;"0");")")))))))
    """
    v = data['class_value'].max()
    c = (
        'A' if v <= 5 else
        'B+' if v <= 7 else
        'B' if v <= 10 else
        'C' if v <= 15 else
        'D+' if v <= 20 else
        'D' if v <= 25 else
        'E'
    )
    return '%s(%s)' % (c, int(v))


def solver_min_tolerance(data: pd.DataFrame) -> pd.DataFrame:
    """
    * Number  (column B) [Input],
    * Identified (column C) [Input],
    * Mean (column D) [Input],
    * Std deviat (column E) [Input],
    * p_o (column F),
    * Class (column G),
    * d (column H),
    * d_min (column I) [Input/Minimization Solver Output],
    * d_c (column J),
    * class (column K),
    * p (column L) - related to column I,
    * p (column M) -  related to column H,
    * Accepted (column O)

    =100*(
        1-
        TDIST((I9/E9-D9/E9)-TINV(0,05;B9-1)/SQRT(B9);B9-1;1)-
        TDIST((I9/E9+D9/E9)-TINV(0,05;B9-1)/SQRT(B9);B9-1;1)
    )
    """

    for i in data.index:
        s = data.loc[i, :]
        _number = s['number']
        _mean = s['mean']
        _std = s['std']
        _min_confidence = s['min_confidence']
        _factor = stats.t.isf(0.05 / 2, _number - 1) / np.sqrt(_number)
        _dof = _number - 1

        def func(_min_tolerance):
            return _min_confidence - 100 * (
                1 -
                stats.t.sf(
                    (_min_tolerance / _std - _mean / _std) - _factor, _dof) -
                stats.t.sf(
                    (_min_tolerance / _std + _mean / _std) - _factor, _dof)
            )

        try:
            data.loc[i, 'min_tolerance'] = fsolve(func, [1])[0]
        except:
            data.loc[i, 'min_tolerance'] = np.nan

    return data
