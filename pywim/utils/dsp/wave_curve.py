import peakutils
import pandas as pd


def select_curve_by_threshold(
    signal_data: pd.Series,
    threshold: float, delta_x: int
) -> [pd.Series]:
    """

    """
    Δx = delta_x

    indexes = peakutils.indexes(signal_data, thres=0.5, min_dist=30)
    curves = []

    for ind_axle in indexes:
        i_start = ind_axle - Δx
        i_end = ind_axle + Δx

        p_start = Δx
        while i_start >= p_start:
            i_start -= 1
            if signal_data.iloc[i_start] <= threshold:
                break

        p_end = signal_data.size - Δx
        while i_end <= p_end:
            i_end += 1
            if signal_data.iloc[i_end] <= threshold:
                break
        curves.append(signal_data.iloc[i_start - Δx:i_end + Δx])

    return curves
