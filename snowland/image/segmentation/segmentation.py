# -*- coding: utf-8 -*-


from collections import Counter
import numpy as np


def otsu(counter: Counter, colors=256):
    """
    基于统计进行大津法阈值分割
    """
    c_array = np.zeros(colors)
    for k, v in counter.items():
        c_array[k] = v

    p_array = c_array / np.sum(c_array)
    p1 = np.cumsum(p_array)
    range_k = np.arange(colors)
    mk = p_array * range_k
    temp_m = mk / p1
    temp_m[np.isnan(temp_m)] = 0
    m1 = np.cumsum(temp_m)
    mG = m1[-1]
    omega2_b = (mG * p1 - m1) / (p1 * (1 - p1)) * (mG * p1 - m1)
    omega2_b[np.isnan(omega2_b)] = 0
    return np.argmax(omega2_b)

