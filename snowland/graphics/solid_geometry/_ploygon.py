# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 深圳星河软通科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.astar.ltd
# @file: _ploygon.py
# @time: 2019/8/12 20:48
# @Software: PyCharm

from snowland.graphics.core.computational_geometry_2d import Point2D, Polygon, PolygonWithoutHoles, LineString2D, ConvexPolygon, Rectangle
from snowland.graphics.core.computational_geometry_base import Vector
from snowland.graphics.core.analytic_geometry_2d import Line2D
import numpy as np

npl = np.linalg
npa = np.array
npr = np.random

def __in_polygon(p: Point2D, polygon):
    """
    判断点是否在多边形内（不包含边上）
    :param point:
    :param polygon:
    :return:
    """
    for point in polygon.p:
        if p == point:  # 使用重载的等于方法
            return True

    for hole in polygon.holes:
        for point in hole:
            if p == point:  # 使用重载的等于方法
                return True
    count = 0
    flag = False
    for i, point in enumerate(polygon.p[:, :]):  # 注意，这个i取0的时候，i-1值是-1，所以这个是循环到所有的边
        if (point[1] <= p[1] < polygon.p[i - 1, 1] or polygon.p[i - 1, 1] <= p[1] < point[1]) and \
                (p[0] < (polygon.p[i - 1, 0] - point[0]) * (p[1] - point[1]) / (polygon.p[i - 1, 1] - point[1]) + point[
                    1]):
            flag = not flag
            count += 1

    for hole in polygon.holes:
        polygon_temp = PolygonWithoutHoles(hole)
        for i, point in enumerate(polygon_temp.p[:, :]):  # 注意，这个i取0的时候，i-1值是-1，所以这个是循环到所有的边
            if (point[1] <= p[1] < polygon_temp.p[i - 1, 1] or polygon_temp.p[i - 1, 1] <= p[1] < point[1]) and \
                    (p[0] < (polygon_temp.p[i - 1, 0] - point[0]) *
                     (p[1] - point[1]) / (polygon_temp.p[i - 1, 1] - point[1]) + point[1]):
                flag = not flag
                count += 1
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


# 使用Graham扫描法计算凸包
# 网上的代码好多运行效果并不好
# 算法参见《算法导论》第三版 第605页
# https://blog.csdn.net/john_bian/article/details/85221039


def get_bottom_point(points):
    """
    返回points中纵坐标最小的点的索引，如果有多个纵坐标最小的点则返回其中横坐标最小的那个
    :param points:
    :return:
    """
    min_index = 0
    n = len(points)
    for i in range(0, n):
        if points[i][1] < points[min_index][1] or (
                points[i][1] == points[min_index][1] and points[i][0] < points[min_index][0]):
            min_index = i
    return min_index


def sort_polar_angle_cos(points, center_point: Point2D):
    """
    按照与中心点的极角进行排序，使用的是余弦的方法
    :param points: 需要排序的点
    :param center_point: 中心点
    :return:
    """
    n = len(points)
    cos_value = []
    rank = []
    norm_list = []
    for i in range(0, n):
        point_ = points[i]
        point = [point_[0] - center_point[0], point_[1] - center_point[1]]
        rank.append(i)
        norm_value = npl.norm(point)
        norm_list.append(norm_value)
        if norm_value == 0:
            cos_value.append(1)
        else:
            cos_value.append(point[0] / norm_value)

    for i in range(0, n - 1):
        index = i + 1
        while index > 0:
            if cos_value[index] > cos_value[index - 1] or (
                    cos_value[index] == cos_value[index - 1] and norm_list[index] > norm_list[index - 1]):
                temp = cos_value[index]
                temp_rank = rank[index]
                temp_norm = norm_list[index]
                cos_value[index] = cos_value[index - 1]
                rank[index] = rank[index - 1]
                norm_list[index] = norm_list[index - 1]
                cos_value[index - 1] = temp
                rank[index - 1] = temp_rank
                norm_list[index - 1] = temp_norm
                index = index - 1
            else:
                break
    sorted_points = []
    for i in rank:
        sorted_points.append(points[i])

    return sorted_points


def vector_angle(vector):
    """
    返回一个向量与向量 [1, 0]之间的夹角， 这个夹角是指从[1, 0]沿逆时针方向旋转多少度能到达这个向量
    :param vector:
    :return:
    """
    norm_ = npl.norm(vector)
    if norm_ == 0:
        return 0

    angle = np.arccos(vector[0] / norm_)
    if vector[1] >= 0:
        return angle
    else:
        return 2 * np.pi - angle


def coss_multi(v1, v2):
    """
    计算两个向量的叉乘
    :param v1:
    :param v2:
    :return:
    """
    return v1[0] * v2[1] - v1[1] * v2[0]


def graham_scan(points):
    # print("Graham扫描法计算凸包")
    bottom_index = get_bottom_point(points)
    bottom_point = points.pop(bottom_index)
    sorted_points = sort_polar_angle_cos(points, bottom_point)

    m = len(sorted_points)
    if m < 2:
        print("点的数量过少，无法构成凸包")
        return

    stack = []
    stack.append(bottom_point)
    stack.append(sorted_points[0])
    stack.append(sorted_points[1])

    for i in range(2, m):
        length = len(stack)
        top = stack[length - 1]
        next_top = stack[length - 2]
        v1 = [sorted_points[i][0] - next_top[0], sorted_points[i][1] - next_top[1]]
        v2 = [top[0] - next_top[0], top[1] - next_top[1]]

        while coss_multi(v1, v2) >= 0:
            stack.pop()
            length = len(stack)
            top = stack[length - 1]
            next_top = stack[length - 2]
            v1 = [sorted_points[i][0] - next_top[0], sorted_points[i][1] - next_top[1]]
            v2 = [top[0] - next_top[0], top[1] - next_top[1]]

        stack.append(sorted_points[i])

    return ConvexPolygon(stack)

