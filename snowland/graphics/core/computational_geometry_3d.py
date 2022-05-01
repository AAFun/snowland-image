# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 深圳星河软通科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.astar.ltd
# @file: solid_geometry_3d.py
# @time: 2019/8/17 17:13
# @Software: PyCharm

from abc import abstractmethod

from astartool.number import equals_zero_all
from scipy.spatial.distance import pdist
import numpy as np

from snowland.graphics.core.computational_geometry_base import Point, LineString, Shape, Stereographic
from snowland.graphics.core.computational_geometry_base import UNITVECTORZ

npa = np.array
npm = np.mat

__all__ = [
    'Circle3D',
    'ConvexPolygon3D',
    'Cylinder',
    'Ellipse3D',
    'LineSegment3D',
    'LineString3D',
    'Point3D',
    'Polygon3D',
    'PolygonWithoutHoles3D',
    'Sphere',
    'Square3D',
    'StraightCone',
    'StraightCylinder',
    'StraightEllipsoid',
    'StraightPrism',
    'Triangle3D',
    'Vertebrae'
]


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


class LineString3D(LineString):
    def __init__(self, X=None):
        super(LineString3D, self).__init__(X=X)
        assert self.X.shape[0] == 3

    def length(self, metric='euclidean', *args, **kwargs):
        m, n = self.X.shape
        return sum(
            pdist(self.X[ind:ind + 2, :], metric=metric, *kwargs) for ind in range(m - 1))

    def is_ring(self, eps=1e-8):
        """
        判断是否成环
        :return:
        """
        return equals_zero_all(self.X[0, :] - self.X[-1, :], eps=eps)


class LineSegment3D(LineString3D):
    def __init__(self, X=None, p1=None, p2=None):
        if p1 is not None and p2 is not None:
            if isinstance(p1, Point):
                p1 = p1[:3]
            if isinstance(p2, Point):
                p2 = p2[:3]
            X = np.vstack((p1, p2))
        super(LineSegment3D, self).__init__(X)

    def length(self, metric='euclidean', *args, **kwargs):
        return np.sum(pdist(self.X, metric, *args, **kwargs))


class Shape3D(Shape):
    """
    三维面
    """
    pass


class Polygon3D(Shape3D):
    def __init__(self, p=None, holes=None):
        # TODO:
        super(Polygon3D, self).__init__()
        self.p = p
        self.holes = holes

    def area(self):
        # TODO:
        pass

    def girth(self):
        # TODO
        pass

    def without_holes(self):
        return self.holes is None or not self.holes

    def is_convex(self):
        if not self.without_holes():
            return False
        # TODO, check


class PolygonWithoutHoles3D(Polygon3D):
    def __init__(self, p):
        super(PolygonWithoutHoles3D, self).__init__(p, holes=None)

    def area(self):
        """
        面积
        :return:
        """
        # TODO 计算面积

    def girth(self):
        """
        周长
        :return:
        """
        p_ring = np.vstack((self.p, self.p[:1, :]))
        return LineString3D(p_ring).length()


class ConvexPolygon3D(PolygonWithoutHoles3D):

    def area(self):
        # 面积
        # 参考 https://blog.csdn.net/cymy001/article/details/81366033
        points = self.p
        area = 0
        if len(points) < 3:
            raise Exception("error")

        for i in range(0, len(points) - 1):
            p1 = points[i]
            p2 = points[i + 1]

            triArea = (p1[0] * p2[1] - p2[0] * p1[1]) / 2
            # print(triArea)
            area += triArea

        fn = (points[-1][0] * points[0][1] - points[0][0] * points[-1][1]) / 2
        # print(fn)
        return abs(area + fn)


class Triangle3D(ConvexPolygon3D):
    """
    三角形
    """
    pass


class Square3D(ConvexPolygon3D):
    """
    正方形
    """
    pass


class Ellipse3D(Shape3D):
    def __init__(self, centre, a=0, b=0, v=UNITVECTORZ):
        self.centre = Point3D(centre)
        self.a = a
        self.b = b
        self.v = v

    def area(self):
        """
        面积
        :return:
        """
        return self.a * self.b * np.pi

    @abstractmethod
    def girth(self):
        """
        周长
        :return:
        """
        # TODO: 椭圆周长数值解

    def is_circle(self, eps=1e-8):
        return np.fabs(self.a - self.b) <= eps


class Circle3D(Ellipse3D):
    def __init__(self, centre, r=0, v=UNITVECTORZ):
        super(Circle3D, self).__init__(centre, r, r, v)

    @property
    def r(self):
        return self.a

    @r.setter
    def set_r(self, ra):
        self.a = self.b = ra

    def girth(self):
        """
        周长
        :return:
        """
        return 2 * self.r * np.pi


class Vertebrae(Stereographic):
    """
    椎体
    """

    def __init__(self, underside: Shape3D = None, h=0, v=UNITVECTORZ, t=UNITVECTORZ):
        self.underside = underside
        self.h = h
        self.v = v  # 底面法向量
        self.t = t  # 中线向量

    @abstractmethod
    def surface_area(self):
        """
        表面积
        :return:
        """
        pass

    def volume(self):
        """
        体积
        :return:
        """
        return self.underside.area() * self.h / 3


class StraightCone(Vertebrae):
    # 圆锥
    def __init__(self, underside: Circle3D = None, h=0, v=UNITVECTORZ, centre=None, r=0):
        """
        :param underside:
        :param centre: 底面圆心
        :param r: 底面半径
        :param h: 圆锥高度
        :param v: 方向向量
        """
        if underside is None:
            underside = Circle3D(centre, r, v)

        super(StraightCone, self).__init__(underside=underside, h=h, v=v, t=v)

    def surface_area(self):
        """
        表面积
        :return:
        """
        return self.underside.area() + self.underside.r * np.sqrt(self.h * self.h + self.underside.r * self.underside.r)


class Cylinder(Stereographic):
    """
    柱体
    """

    def __init__(self, underside: Shape3D = None, h=0, v=UNITVECTORZ, t=UNITVECTORZ):
        self.underside = underside
        self.h = h
        self.v = v
        self.t = t

    def surface_area(self):
        """
        表面积
        :return:
        """
        return 2 * self.underside.area() + self.underside.girth() * self.h

    def volume(self):
        """
        体积
        :return:
        """
        return self.underside.area() * self.h


class StraightCylinder(Cylinder):
    def __init__(self, underside: Circle3D = None, h=0, v=UNITVECTORZ, centre=None, r=0):
        """
        :param centre: 底面圆心
        :param r: 底面半径
        :param h: 圆柱高度
        :param v: 方向向量
        """
        if underside is None:
            underside = Circle3D(centre, r)

        super(StraightCylinder, self).__init__(underside, h, v, t=v)


class StraightPrism(Cylinder):
    def __init__(self, underside: ConvexPolygon3D = None, h=0, v=UNITVECTORZ, p=None):
        """
        :param underside: 底面
        :param h: 圆柱高度
        :param v: 方向向量
        """
        if underside is None:
            if p is not None:
                underside = Polygon3D(p)
            else:
                raise ValueError('初始化异常')

        super(StraightPrism, self).__init__(underside, h, v, t=v)


class StraightEllipsoid(Stereographic):
    def __init__(self, a=1, b=1, c=1, p=(0, 0, 0)):
        # (x-x0)**2 / a**2 + (y-y0)**2 / b**2+(z-z0)**2 / c**2=1
        self.p = Point3D(p)
        self.a = a
        self.b = b
        self.c = c

    def volume(self):
        return 4 * np.pi * self.a * self.b * self.c / 3

    def surface_area(self):
        return 4 * np.pi * (self.a * self.b + self.b * self.c + self.c * self.a) / 3


class Sphere(StraightEllipsoid):
    # 球体
    def __init__(self, r=1, p=(0, 0, 0)):
        super(Sphere, self).__init__(r, r, r, p)

    @property
    def r(self):
        return self.a
