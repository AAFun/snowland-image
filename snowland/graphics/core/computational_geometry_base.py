# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 深圳星河软通科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.astar.ltd
# @file: solid_geometry_base.py
# @time: 2019/8/17 0:04
# @Software: PyCharm


from abc import ABCMeta, abstractmethod
from numbers import Number

from scipy.spatial.distance import pdist
import numpy as np
from astartool.number import equals_zero_all

npa = np.array
npl = np.linalg

__all__ = [
    'Graphic',
    'LineString',
    'Point',
    'Shape',
    'Stereographic',
    'UnitVector',
    'UnitVector3',
    'UNITVECTORX',
    'UNITVECTORY',
    'UNITVECTORZ',
    'Vector',
    'Vector2',
    'Vector3',
]


class Vector(object):
    def __init__(self, x=None, dim=None, start=None, end=None):
        if isinstance(x, Vector):
            x = x.x
        elif dim is not None:
            x = np.zeros(dim)
        elif x is not None:
            # TODO: 判断x是一维的
            x = npa(x)
        elif start is not None and end is not None:
            x = Point(end) - Point(start)

        self.x = x

    def __mul__(self, other):
        v2 = Vector(other)
        return v2.x * self.x

    def __add__(self, other):
        v2 = Vector(other)
        return Vector(v2.x + self.x)

    def __sub__(self, other):
        v2 = Vector(other)
        return Vector(self.x - v2.x)

    def __str__(self):
        itor = [str(_) for _ in self.x]
        return "Vector <" + ', '.join(itor) + ">"

    def length(self):
        """
        向量模长
        :return:
        """
        return npl.norm(self.x)

    def dot_product(self, other):
        v2 = Vector(other)
        return self.x.dot(v2.x)

    def cross_product(self, other):
        # TODO: 向量积
        raise NotImplemented

    def cos_angle(self, other):
        v2 = Vector(other)
        return self.dot_product(v2) / (self.length() * v2.length())

    def angle(self, other):
        """
        向量夹角
        :param other:
        :return:
        """
        return np.arccos(self.cos_angle(other))

    def is_vertical(self, other, eps=1e-8):
        """
        判断垂直
        :param other:
        :param eps:
        :return:
        """
        return equals_zero_all(self * other, eps=eps)

    def is_parallel(self, other, eps):
        """
        判断共线
        :return:
        """
        if isinstance(other, Vector):
            nv2 = other.x
        else:
            nv2 = np.asarray(other)
        nv1 = self.x
        return np.rank([nv1, nv2]) == 1

    def is_unit_vector(self, eps=1e-8):
        """
        是否是单位向量
        :return:
        """
        return -eps < self.length() - 1 < eps

    def norm(self):
        """
        返回其单位向量
        :return:
        """
        return Vector(self.x / self.length())

    def to_norm(self):
        """
        转化到单位向量
        :return:
        """
        self.x /= self.length()
        return self


class Vector2(Vector):
    @staticmethod
    def get_angle_pi(a, b):
        """
        a, b 为一维向量， 多点会错！！！
        返回 向量a和b之间的夹角， 值域是 -pi ~ pi
        """
        a = npa(a)
        b = npa(b)
        norm_a = npl.norm(a, axis=1) if len(a.shape) == 2 else npl.norm(a)
        norm_b = npl.norm(b, axis=1) if len(b.shape) == 2 else npl.norm(b)
        # 单位化（可以不用这一步）
        # a = a / norm_a  # 不能写成 a /= norm_a
        # b = b / norm_b  # 不能写成 b /= norm_b
        # 夹角cos值
        cos_ = np.dot(a, b) / (norm_a * norm_b)
        # 夹角sin值
        sin_ = np.cross(a, b) / (norm_a * norm_b)
        arctan2_ = np.arctan2(sin_, cos_)
        return arctan2_

    @staticmethod
    def get_angle(a: (list, np.ndarray), b: (list, np.ndarray)):
        """
        返回量向量之间的夹角，值域是 0~180，单位是度
        """
        # 初始化向量
        degree = np.rad2deg(Vector2.get_angle_pi(a, b))
        return np.abs(degree)

    @staticmethod
    def get_rotate_angle(v1, v2):
        """
        v1旋转到v2经历的角度， 值域0~360, 单位是度
        """
        return np.rad2deg(Vector2.get_angle_pi(v1, v2)) % 360



class Vector3(Vector):
    pass


class UnitVector(Vector):
    def __init__(self, x=None, dim=None, start=None, end=None, eps=1e-8):
        super(UnitVector, self).__init__(x, dim, start, end)
        assert self.is_unit_vector()


class UnitVector3(Vector3):
    def __init__(self, x=None, dim=None, start=None, end=None, eps=1e-8):
        super(UnitVector3, self).__init__(x, dim, start, end)
        assert self.is_unit_vector()


UNITVECTORX = UnitVector3((1, 0, 0))
UNITVECTORY = UnitVector3((0, 1, 0))
UNITVECTORZ = UnitVector3((0, 0, 1))


class Graphic(metaclass=ABCMeta):
    pass


class Point(Graphic):
    def __init__(self, p):
        if isinstance(p, Point):
            self.p = p
        else:
            self.p = npa(p)

    def __setitem__(self, instance, value):
        if isinstance(isinstance(instance, Number)):
            self.p[instance] = value
        else:
            raise ValueError('键值异常')

    def __getitem__(self, item):
        return self.p[item]

    def __eq__(self, other):
        if isinstance(other, np.ndarray):
            # TODO: check it
            if len(self.p) != len(other):
                return False
            else:
                return equals_zero_all(self.p - other)
        elif isinstance(other, Point):
            if len(self.p) != len(other.p):
                return False
            else:
                return equals_zero_all(self.p - other.p)

    def __sub__(self, other):
        if isinstance(other, Point):
            return Vector(self.p - other.p)
        else:
            raise ValueError('Error in Point')

    def __str__(self):
        itor = [str(_) for _ in self.p]
        return "Point <" + ', '.join(itor) + ">"


class LineString(Graphic):
    def __init__(self, X=None):
        if isinstance(X, LineString):
            self.X = X.X
        else:
            if len(X) == 0:
                X = []
            elif isinstance(X[0], Point):
                X = [each.p for each in X]
            self.X = npa(X)

    def length(self, metric='euclidean', *args, **kwargs):
        m, n = self.X.shape
        return np.sum(
            [pdist(self.X[ind:ind + 2, :], metric=metric, *args, **kwargs) for ind in range(m - 1)])

    def is_ring(self, eps=1e-8):
        """
        判断是否成环
        :return:
        """
        return equals_zero_all(self.X[0, :] - self.X[-1, :], eps=eps)


class Shape(Graphic):
    @abstractmethod
    def area(self):
        """
        面积
        :return:
        """
        pass

    @abstractmethod
    def girth(self):
        """
        周长
        :return:
        """
        pass


class Stereographic(Graphic):
    @abstractmethod
    def surface_area(self):
        """
        表面积
        :return:
        """
        pass

    @abstractmethod
    def volume(self):
        """
        体积
        :return:
        """
        pass
