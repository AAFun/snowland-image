# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 深圳星河软通科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.astar.ltd
# @file: _ploygon.py
# @time: 2019/8/12 20:48
# @Software: PyCharm

from snowland.graphics.core.geometry2d import Point2D, Polygon, PolygonWithoutHoles
import numpy as np

npa = np.array


def __in_polygon(p: Point2D, polygon):
    """
    判断点是否在多边形内
    :param point:
    :param polygon:
    :return:
    """
    for point in polygon.p:
        if np.all(p.p == point):
            return True

    for hole in polygon.holes:
        for point in hole:
            if np.all(p.p == point):
                return True
    flag = False
    for i, point in enumerate(polygon.p[:, :]):
        if (point[1] <= p[1] < polygon.p[i - 1, 1] or polygon.p[i - 1, 1] <= p[1] < point[1]) and \
                (p[0] < (polygon.p[i - 1, 0] - point[0]) * (p[1] - point[1]) / (polygon.p[i - 1, 1] - point[1]) + point[
                    1]):
            flag = not flag

    for hole in polygon.holes:
        polygon_temp = PolygonWithoutHoles(hole)
        for i, point in enumerate(polygon_temp.p[:, :]):
            if (point[1] <= p[1] < polygon_temp.p[i - 1, 1] or polygon_temp.p[i - 1, 1] <= p[1] < point[1]) and \
                    (p[0] < (polygon_temp.p[i - 1, 0] - point[0]) *
                     (p[1] - point[1]) / (polygon_temp.p[i - 1, 1] - point[1]) + point[1]):
                flag = not flag
    return flag


def in_polygon(point, polygon: Polygon):
    """
    判断点是否在多边形内
    :param point:
    :param polygon:
    :return:
    """
    if isinstance(point, Point2D):
        return __in_polygon(point, polygon)
    if isinstance(point, np.ndarray) and len(point.shape) == 1:
        return __in_polygon(Point2D(point), polygon)
    else:
        # 多个点判断， 返回多个值
        if isinstance(point[0], Point2D):
            return npa([__in_polygon(p, polygon) for p in point])
        if isinstance(point[0], np.ndarray) and len(point.shape) == 1:
            return npa([__in_polygon(Point2D(p), polygon) for p in point])
        raise ValueError('error')


