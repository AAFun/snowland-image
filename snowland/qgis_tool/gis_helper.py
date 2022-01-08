

import numpy as np


class GisHelper:

    @staticmethod
    def get_point_by_rate(line: np.ndarray, meters):
        return GisHelper.get_point_by_rate_index(line, meters)[0]

    @staticmethod
    def get_point_by_rate_index(line: np.ndarray, meters):
        meters_all = [meters(a, b) for a, b in zip(line[:-1], line[1:])]
        s = np.cumsum(meters_all)
        if s[-1] < meters:
            return line[-1], len(s)
        ind = np.sum(s < meters)
        s = np.insert(s, 0, 0)
        delta_meters = meters - s[ind]
        vector_line = line[1:] - line[:-1]
        return line[ind] + delta_meters / meters_all[ind] * vector_line[ind], ind
