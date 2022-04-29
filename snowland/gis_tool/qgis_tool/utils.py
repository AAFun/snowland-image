# -*- coding: utf-8 -*-
from snowland.gis_tool import ELLIPSOID
from snowland.graphics.utils import simple_line, get_rotate_angle_rad, rotate_geometry
from snowland.gis_tool.qgis_tool.distance_area import DistanceArea
import numpy as np

npa = np.array
npl = np.linalg


def move_distance(geo_points, dist, flag, ellipsoid=ELLIPSOID):
    """
    此函数带有端点
    flag: 左侧为-1，右侧为1
    dist: 单位是米
    """
    dist_class = DistanceArea(ellipsoid=ellipsoid)
    if len(geo_points) <= 1:
        return None, None

    firstPoint = 2 * geo_points[0] - geo_points[1]
    lastPoint = 2 * geo_points[-1] - geo_points[-2]
    geo_points = np.vstack((firstPoint, geo_points, lastPoint))

    vectors = geo_points[1:] - geo_points[:-1]
    ps = []
    for i, (vec10, vec12) in enumerate(zip(vectors[:-1], vectors[1:]), start=1):
        vec10_norm = -vec10 / npl.norm(vec10)
        vec12_norm = vec12 / npl.norm(vec10)
        angle = get_rotate_angle_rad(vec10_norm, vec12_norm)
        if flag > 0:
            half_angle = angle / 2
        else:
            half_angle = angle / 2 - np.pi
        vecCenter = rotate_geometry(vec12_norm, half_angle)
        realLen = dist / np.sin(half_angle)

        vecCenter = vecCenter / npl.norm(vecCenter)
        real_point = vecCenter + geo_points[i]
        unitLen = dist_class.distance_metres_by_two_points(geo_points[i], real_point)

        vecCenter = realLen / unitLen * vecCenter if flag > 0 else -realLen / unitLen * vecCenter
        resultVec = vecCenter + geo_points[i]
        ps.append(resultVec)
    ps_array = npa(ps)
    x_array = ps_array[:, 0]
    y_array = ps_array[:, 1]
    return x_array, y_array
