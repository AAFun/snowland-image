# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 深圳星河软通科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.astar.ltd
# @file: 
# @time: 
# @Software: PyCharm

from abc import ABCMeta
from typing import List

from astartool.error import ParameterTypeError, ParameterValueError
from astartool.number import equals_zero
import numpy as np

from snowland.graphics.core.analytic_geometry_base import Line
from snowland.graphics.core.computational_geometry_2d import Point2D

npa = np.array
npl = np.linalg

__all__ = [
    'Line2D',
    'ConicalSection',
    'Ellipse',
    'Circle',
    'Hyperbola',
    'Parabola',
    'Polynomial',

    'LEFT',
    'ON',
    'RIGHT'
]

LEFT = -1
ON = 0
RIGHT = 1


class Line2D(Line):
    def __init__(self, a=None, b=0, c=0, p1: (Point2D, np.ndarray) = None, p2: (Point2D, np.ndarray) = None, *args,
                 **kwargs):
        if a is not None and b is not None and c is not None:
            # ax+by+c=0方式定义的线
            self.a, self.b, self.c = a, b, c
        elif p1 is not None and p2 is not None:
            # 两点式定义的直线
            p1, p2 = Point2D(p1), Point2D(p2)
            self.a, self.b, self.c = p2.y - p1.y, p1.x - p2.x, p2.x * p1.y - p1.x * p2.y
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
            return npa([self.__distance_point(each) for each in points])
        elif isinstance(points, np.ndarray):
            if len(points.shape) == 2:
                return npa([self.__distance_point(each) for each in points])
            else:
                return self.__distance_point(points)
        else:
            raise ValueError('points 参数错误')

    def is_parallel(self, other, eps=1e-8):
        """
        判断直线平行
        """
        if isinstance(other, Line2D):
            return -eps < (self.a - other.a) < eps and -eps < self.b - other.b < eps
        elif isinstance(other, (list, tuple, np.ndarray)):
            return -eps < (self.a - other[0]) < eps and -eps < self.b - other[1] < eps
        else:
            raise ParameterTypeError("输入类型错误")

    def intersection(self, other, eps=1e-8):
        """
        直线交点
        :param other:
        :param eps:
        :return:
        """
        if isinstance(other, Line2D):
            if -eps < (self.a - other.a) < eps and -eps < self.b - other.b < eps:
                return None  # 不相交的两条直线
            else:
                return Point2D([-(self.b * other.c - self.c * other.b) / (other.a * self.b - self.a * other.b), \
                                (self.a * other.c - self.c * other.a) / (other.a * self.b - self.a * other.b)])
        elif isinstance(other, (list, tuple, np.ndarray)):
            assert len(other) == 3
            if -eps < (self.a - other[0]) < eps and -eps < self.b - other[1] < eps:
                return None  # 不相交的两条直线
            return Point2D([-(self.b * other[2] - self.c * other[1]) / (other[0] * self.b - self.a * other[1]), \
                            (self.a * other[2] - self.c * other[0]) / (other[0] * self.b - self.a * other[1])])
        else:
            raise ParameterTypeError("输入类型错误")

    def get(self, x: (float, np.ndarray) = None, y: (float, np.ndarray) = None, eps=1e-10):
        """
        获得对应的取值
        :param x: x值
        :param y: y值
        :param eps: 在此精度下认为是 0
        :return:
        """
        assert (x is None) ^ (y is None), "x和y不全为None"
        if x is None:
            if isinstance(y, (int, float, np.float, np.int)):
                if equals_zero(self.a, eps):
                    return np.inf
                else:
                    return (-self.c - self.b * y) / self.a
            else:
                y = npa(y)
                return (-self.c - self.b * y) / self.a
        else:
            if isinstance(x, (int, float, np.float, np.int)):
                if equals_zero(self.b, eps):
                    return np.inf
                else:
                    return (-self.c - self.a * x) / self.b
            else:
                x = npa(x)
                return (-self.c - self.a * x) / self.b

    def location(self, point: (Point2D, np.ndarray), eps=1e-8):
        point = Point2D(point)
        res = self.a * point.x + self.b * point.y + self.c
        if -eps < res < eps:
            return ON
        elif res > eps:
            return RIGHT
        else:
            return LEFT

    def locations(self, points: (List[Point2D], np.ndarray), eps=1e-8):
        if isinstance(points, list):
            return [self.location(point, eps) for point in points]
        elif isinstance(points, np.ndarray):
            result = np.ones(len(points)) * ON
            res = self.a * points[:, 0] + self.b * points[:, 1] + self.c
            result[res > eps] = RIGHT
            result[res < -eps] = LEFT
            return result
        else:
            raise ParameterTypeError("不支持的points类型")


class ConicalSection(Line, metaclass=ABCMeta):
    """
    圆锥曲线
    """
    pass


class Ellipse(ConicalSection):
    """
    椭圆
    """

    def __init__(self, params, *args, **kwargs):
        # AX2+By2+Cxy+Dx+Ey+F=0
        self.params = params

    @property
    def a(self):
        return self.params[0]

    @property
    def b(self):
        return self.params[1]

    @property
    def c(self):
        return self.params[2]

    @property
    def d(self):
        return self.params[3]

    @property
    def e(self):
        return self.params[4]

    @property
    def f(self):
        return self.params[5]

    @property
    def eccentricity(self):
        e = (self.a / self.b) ** 0.5
        if e > 1:
            return 1 / e
        return e

    @property
    def major_axis(self):
        return max(self.a, self.b) ** 0.5

    @property
    def minor_axis(self):
        return min(self.a, self.b) ** 0.5

    @property
    def focal_length(self):
        return 2 * abs(self.a - self.b) ** 0.5


class Circle(Ellipse):
    def __init__(self, param, *args, **kwargs):
        # x^2+y^2+Dx+Ey+F=0
        if len(param) == 6:
            super(Circle, self).__init__(param)
        elif len(param) == 3:
            p = np.ones(6)
            p[3:] = param
            super(Circle, self).__init__(p)
        else:
            raise ParameterValueError("param参数应为3个或者6个")


class Hyperbola(ConicalSection):
    """
    双曲线
    """

    def __init__(self, params, eps=1e-8, *args, **kwargs):
        # Ax2+2Bxy+Cy2+2Dx+2Ey+F=0
        self.params = params
        if equals_zero(np.linalg.det([[self.a, self.b, self.d],
                                      [self.b, self.c, self.e],
                                      [self.d, self.e, self.f]]), eps):
            raise ParameterValueError("参数矩阵非满秩")

        if self.b * self.b - self.a * self.c <= eps:
            raise ParameterValueError("b^2-ac应该大于0")

    @property
    def a(self):
        return self.params[0]

    @property
    def b(self):
        return self.params[1]

    @property
    def c(self):
        return self.params[2]

    @property
    def d(self):
        return self.params[3]

    @property
    def e(self):
        return self.params[4]

    @property
    def f(self):
        return self.params[5]


class Parabola(ConicalSection):
    """
    抛物线
    """
    def __init__(self, params, eps=1e-8):
        # ax2 +2hxy +by2 +2gx +2fy+c =0
        self.params = params

    @property
    def a(self):
        return self.params[0]

    @property
    def b(self):
        return self.params[2]

    @property
    def h(self):
        return self.params[1]

    @property
    def g(self):
        return self.params[3]

    @property
    def c(self):
        return self.params[5]

    @property
    def f(self):
        return self.params[4]


class Polynomial(Line):
    """
    多项式
    """
    def __init__(self, polynomial=None, coefficient=None, exponent=None):
        """
        coefficient: 系数
        exponent: 指数
        """
        if polynomial is not None:
            if isinstance(polynomial, Polynomial):
                self.polynomial_dict = polynomial.polynomial_dict
            elif isinstance(polynomial, dict):
                self.polynomial_dict = polynomial
            else:
                raise ParameterTypeError("参数类型错误")
        elif coefficient is not None and exponent is not None:
            self.polynomial_dict = dict(zip(exponent, coefficient))
        else:
            self.polynomial_dict = {}

    def diff(self, eps=1e-8):
        """
        导函数
        """
        return Polynomial({k - 1: k * v for k, v in self.polynomial_dict.items() if not (-eps < k < eps)})

    def get(self, x):
        """
        获得x对应的值
        """
        y = np.zeros_like(x)
        for k, v in self.polynomial_dict.items():
            y += v * x ** k
        return y
