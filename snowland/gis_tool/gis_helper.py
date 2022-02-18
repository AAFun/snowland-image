import numpy as np
from snowland.gis_tool import EARTH_RADIUS

class GisHelper:

    @staticmethod
    def get_point_by_rate(line: np.ndarray, meters):
        """
        在line组成的折线中,获得距离起点距离为metres的点
        """
        return GisHelper.get_point_by_rate_index(line, meters)[0]

    @staticmethod
    def get_point_by_rate_index(line: np.ndarray, meters):
        """
        在line组成的折线中,获得距离起点距离为metres的点和小于这个点的最大节点编号
        """
        meters_all = [meters(a, b) for a, b in zip(line[:-1], line[1:])]
        s = np.cumsum(meters_all)
        if s[-1] < meters:
            return line[-1], len(s)
        ind = np.sum(s < meters)
        s = np.insert(s, 0, 0)
        delta_meters = meters - s[ind]
        vector_line = line[1:] - line[:-1]
        return line[ind] + delta_meters / meters_all[ind] * vector_line[ind], ind
