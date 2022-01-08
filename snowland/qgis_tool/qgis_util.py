# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 深圳星河软通科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.astar.ltd
# @file: qgis_utils.py
# @time: 2022/01/06 20:52
# @Software: PyCharm


from functools import reduce

import numpy as np
from qgis.core import QgsGeometry, QgsPoint

from snowland.qgis_tool.haversine import length_metres

npa = np.array
npl = np.linalg


__all__ = [
    'points',
    'pointsXY',
    'vector',
    'vector_start',
    'vector_end',
    'point_to_ndarray',
    'start_pointXY',
    'end_pointXY'
]


def points(geometry: QgsGeometry):
    vertices = geometry.vertices()
    return npa([(v.x(), v.y(), v.z()) for v in vertices])


def pointsXY(geometry: QgsGeometry):
    vertices = geometry.vertices()
    return npa([(v.x(), v.y()) for v in vertices])


def vector(geometry: QgsGeometry):
    """
    起点到终点的向量
    """
    start = geometry.vertexAt(0)
    line_nodes = geometry.asPolyline()
    end = line_nodes[-1]
    return npa([end.x() - start.x(), end.y() - start.y()])


def vector_start(geometry: QgsGeometry):
    """
    第一条折线的向量
    """
    start = geometry.vertexAt(0)
    end = geometry.vertexAt(1)
    return npa([end.x() - start.x(), end.y() - start.y()])


def vector_end(geometry: QgsGeometry):
    """
    倒数第一条折线的向量
    """
    line_nodes = geometry.asPolyline()
    start = line_nodes[-2]
    end = line_nodes[-1]
    return npa([end.x() - start.x(), end.y() - start.y()])


def thinning_by_step_method(points, step=2):
    """
    步长法
    :param points:
    :return:
    """
    result = [points[0]]
    delta_length = length_metres(points[:-1], points[1:])
    delta = 0
    for i, d in enumerate(delta_length, start=1):
        if delta + d > step:
            result.append(points[i])
            delta = 0
        else:
            delta += d
    if delta != 0:
        result.append(points[-1])
    return reduce(lambda a, b: np.vstack((a, b)), result)


def douglas_peuker(points, d=5e-7):
    """
    Douglas Peuker
    :param points:
    :return:
    """
    if len(points) < 2:
        return points
    p1 = points[0]
    p2 = points[-1]
    line = npa([p2[1] - p1[1], p1[0] - p2[0], p2[0] * p1[1] - p1[0] * p2[1]])

    dist = np.abs(points[:, 0] * line[0] + points[:, 1] * line[1] + line[2]) / npl.norm(line[:2])
    d_ind = np.argmax(dist)
    if dist[d_ind] < d:
        return npa((p1, p2))
    else:
        return np.vstack((douglas_peuker(points[:d_ind + 1], d), douglas_peuker(points[d_ind:], d)[1:]))


def vertical_distance_limit(points, d=5e-7):
    """
    垂距限值法
    :param points:
    :return:
    """
    p0 = points[0]
    if len(points) < 3:
        return points
    result = [p0]

    for p1, p2 in zip(points[1:-1, :], points[2:, :]):
        line = npa([p2[1] - p0[1], p0[0] - p2[0], p2[0] * p0[1] - p0[0] * p2[1]])
        dist = p1[0] * line[0] + p1[1] * line[1] + line[2]
        print(dist)
        if dist > d:
            result.append(p1)
            p0 = p1
    result.append(points[-1])
    return reduce(lambda a, b: np.vstack((a, b)), result)


def start_pointXY(geometry: QgsGeometry):
    v = geometry.vertexAt(0)
    return npa([v.x(), v.y()])


def end_pointXY(geometry: QgsGeometry):
    v = geometry.asPolyline()[-1]
    return npa([v.x(), v.y()])


def point_to_ndarray(p: QgsPoint):
    return npa([p.x(), p.y()])
