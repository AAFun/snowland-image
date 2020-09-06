# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 深圳星河软通科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.astar.ltd
# @file: 
# @time: 
# @Software: PyCharm


import numpy as np

from snowland.graphics.core.solid_geometry_2d import Point2D
from snowland.graphics.core.solid_geometry_3d import Point3D
from snowland.graphics.core.solid_geometry_base import Vector, Vector3
from snowland.graphics.core.analytic_geometry_base import Line, Surface
npa = np.array

__all__ = [
    'Line2D'
]

class Line2D(Line):
    def __init__(self, a=None, b=0, c=0, p1: Point2D = None, p2: Point2D = None, *args, **kwargs):
        if a is not None and b is not None and c is not None:
            # ax+by+c=0方式定义的线
            self.a, self.b, self.c = a, b, c
        elif p1 is not None and p2 is not None:
            # 两点式定义的直线
            if isinstance(p1, Point2D) or isinstance(p2, Point2D):
                raise ValueError("p1, p2应为二维点Point2D的子类")
            self.a, self.b, self.c = p2.y - p1.y, p1.x - p2.x, -a * p1.x - b * p1.y
        else:
            # TODO: 其他方式确定的直线
            pass

    def __distance_point(self, point):
        """
        计算点到直线距离
        :param point: 点
        :return:
        """
        p = Point2D(point)
        return np.fabs(self.a * p.x + self.b * p.y + self.c) / np.sqrt(self.a ** 2 + self.b ** 2)

    def distance_points(self, points):
        """
        计算多点到直线的距离
        :param points: 可以是np.ndarray, 也可以是list(Point2D)
        :return:
        """
        # TODO: 这里可以用矩阵进行运算的，以后补上
        if isinstance(points, list):
            return npa([self.__distance_point(self, each) for each in points])
        elif isinstance(points, np.ndarray):
            if len(points.shape) == 2:
                return npa([self.__distance_point(self, each) for each in points])
            else:
                return self.__distance_point(self, points)
        else:
            raise ValueError('points 参数错误')

    def intersection(self, other, eps=1e-8):
        """
        直线交点
        :param other:
        :param eps:
        :return:
        """
        if not isinstance(other, Line2D):
            pass
        if -eps < (self.a - other.a) < eps and -eps < self.b - other.b < eps:
            return None  # 不相交的两条直线
        else:
            return Point2D([-(self.b * other.c - self.c * other.b) / (other.a * self.b - self.a * other.b), \
                            (self.a * other.c - self.c * other.a) / (other.a * self.b - self.a * other.b)])

