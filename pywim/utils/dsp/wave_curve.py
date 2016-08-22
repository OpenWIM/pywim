import peakutils
import pandas as pd


def select_curve_by_threshold(
    signal_data: pd.Series,
    threshold: float, delta_x: int
) -> [pd.Series]:
    """
    
    """
    indexes = peakutils.indexes(signal_data, thres=0.5, min_dist=30)
    curves = []
    
    for ind_axle in indexes:
        i_start = ind_axle - delta_x
        i_end = ind_axle + delta_x
        
        p_start = Δx
        while i_start >= p_start:
            i_start -= 1
            if data[k].iloc[i_start] <= threshold:
                break
        
        p_end = signal_data.size - delta_x
        while i_end <= p_end:
            i_end += 1
            if data[k].iloc[i_end] <= threshold:
                break
        curves.append(data[k].iloc[i_start-delta_x:i_end+delta_x])

    return curves
