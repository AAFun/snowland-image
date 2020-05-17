# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 深圳星河软通科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.astar.ltd
# @file: base.py
# @time: 2019/8/17 0:04
# @Software: PyCharm


from abc import ABCMeta, abstractmethod
from numbers import Number

from scipy.spatial.distance import pdist
import numpy as np
from astartool.number import equals_zero_all
npa = np.array
npl = np.linalg


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
        pass

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
        # TODO

    def is_unit_vector(self, eps=1e-8):
        """
        是否是单位向量
        :return:
        """
        return equals_zero_all(self.length() - 1, eps)

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
    pass


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
            [pdist(self.X[ind:ind+2, :], metric=metric, *args, **kwargs) for ind in range(m - 1)])

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


class Stereograph(Graphic):
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
