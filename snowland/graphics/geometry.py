# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 深圳星河软通科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.astar.ltd
# @file: 
# @time: 
# @Software: PyCharm

import numpy as np
from skimage.draw.draw import *
from abc import ABCMeta, abstractmethod
from snowland.exceptions import ParamsError
from scipy.spatial.distance import pdist, cdist
from numbers import Number

npa = np.array


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


class Point2D(Point):
    def __init__(self, p=None, x=None, y=None):
        if x is not None and y is not None:
            p = (x, y)
        assert p is not None
        super(Point2D, self).__init__(p)

    @property
    def x(self):
        return self.p[0]

    @x.setter
    def set_x(self, px):
        self.p[0] = px

    @property
    def y(self):
        return self.p[1]

    @y.setter
    def set_y(self, py):
        self.p[1] = py


class Point3D(Point):
    def __init__(self, p=None, x=None, y=None, z=None):
        if x is not None and y is not None and z is not None:
            p = npa((x, y, z))
        assert p is not None
        super(Point3D, self).__init__(p)

    @property
    def x(self):
        return self.p[0]

    @x.setter
    def set_x(self, px):
        self.p[0] = px

    @property
    def y(self):
        return self.p[1]

    @y.setter
    def set_y(self, py):
        self.p[1] = py

    @property
    def z(self):
        return self.p[0]

    @z.setter
    def set_z(self, px):
        self.p[0] = px


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
        return np.sum(pdist(self.X, metric, *args, **kwargs))


class LineSegment2D(LineString):
    def __init__(self, X=None, p1=None, p2=None):
        if p1 is not None and p2 is not None:
            if isinstance(p1, Point):
                p1 = p1[:2]
            if isinstance(p2, Point):
                p2 = p2[:2]
            X = np.vstack((p1, p2))
        assert X is not None
        super(LineSegment2D, self).__init__(X)


class LineSegment3D(LineString):
    def __init__(self, X=None, p1=None, p2=None):
        if p1 is not None and p2 is not None:
            if isinstance(p1, Point):
                p1 = p1[:3]
            if isinstance(p2, Point):
                p2 = p2[:3]
            X = np.vstack((p1, p2))
        super(LineSegment3D, self).__init__(X)


class Shape(Graphic):
    pass


class Stereograph(Graphic):
    pass

