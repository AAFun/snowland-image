# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 深圳星河软通科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.astar.ltd
# @file:
# @time:
# @Software: PyCharm

from typing import Iterable

from astartool.error import ParameterError
from scipy.spatial.distance import pdist, cdist, euclidean
import numpy as np
from snowland.graphics.core.computational_geometry_base import Point, LineString, Shape, MultiPoint, Line
from snowland.graphics.utils import get_angle_rad, get_intersect_by_two_point, get_lines, get_arc

npa = np.array
npm = np.mat


__all__ = [
    'Arc2D',
    'Circle',
    'ConvexPolygon',
    'Diamond',
    'Ellipse',
    'LineSegment2D',
    'LineString2D',
    'Point2D',
    'Polygon',
    'PolygonWithoutHoles',
    'Rectangle',
    'Square',
    'Triangle'
]


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
    def x(self, px):
        self.p[0] = px

    @property
    def y(self):
        return self.p[1]

    @y.setter
    def y(self, py):
        self.p[1] = py


class MultiPoint2D(MultiPoint):
    def __init__(self, points):
        super().__init__(points)
        assert self.p.shape[1] == 2


class MultiPolygon2D(Shape):

    def __init__(self, polygons):
        if isinstance(polygons, MultiPolygon2D):
            self.polygons = polygons.polygons
        elif isinstance(polygons, Iterable):
            self.polygons = [Polygon(p) for p in polygons]

    def area(self):
        return sum(p.area() for p in self.polygons)

    def girth(self):
        return sum(p.girth() for p in self.polygons)


class LineString2D(LineString):
    def __init__(self, X=None):
        super(LineString2D, self).__init__(X=X)
        assert self.X.shape[1] == 2

    def length(self, metric=euclidean, *args, **kwargs):
        return sum(metric(u, v) for u, v in zip(self.X[:-1], self.X[1:]))

    def intersects(self, other):
        if isinstance(other, LineSegment2D):
            lines = get_lines(self.X)
            point_1 = np.hstack((other.X[:-1, :], [[1]])).T
            point_2 = np.hstack((other.X[1:, :], [[1]])).T
            flag1 = (lines @ point_1)
            flag2 = (lines @ point_2)
            if np.all(flag1 * flag2 > 0):
                lines = get_lines(other.X)
                point_1 = np.hstack((self.X[:-1, :], np.ones((len(self.X) - 1, 1)))).T
                point_2 = np.hstack((self.X[1:, :], np.ones((len(self.X) - 1, 1)))).T
                flag1 = (lines @ point_1)
                flag2 = (lines @ point_2)
                if np.all(flag1 * flag2 > 0):
                    return False
            for p1, p2 in zip(self.X[:-1], self.X[1:]):
                if get_intersect_by_two_point(p1, p2, other.X[0], other.X[1]) != (None, None):
                    return True
            return False
        elif isinstance(other, LineString2D):
            for p1, p2 in zip(self.X[:-1], self.X[1:]):
                for p3, p4 in zip(other.X[:-1], other.X[1:]):
                    if get_intersect_by_two_point(p1, p2, p3, p4) != (None, None):
                        return True
            return False
        elif isinstance(other, np.ndarray):
            for p1, p2 in zip(self.X[:-1], self.X[1:]):
                for p3, p4 in zip(other[:-1], other[1:]):
                    if get_intersect_by_two_point(p1, p2, p3, p4) != (None, None):
                        return True
            return False
        else:
            raise ParameterError("type of other error")


class LineSegment2D(LineString2D):
    def __init__(self, X=None, p1=None, p2=None):
        if p1 is not None and p2 is not None:
            if isinstance(p1, Point):
                p1 = p1[:2]
            if isinstance(p2, Point):
                p2 = p2[:2]
            X = np.vstack((p1, p2))
        assert X is not None
        super(LineSegment2D, self).__init__(X)

    def intersection(self, other):
        if isinstance(other, LineSegment2D):
            other = other.X
        return Point2D(get_intersect_by_two_point(self.X[0], self.X[1], other[0], other[1]))

    def intersects(self, other):
        if isinstance(other, LineSegment2D):
            other = other.X
        return Point2D(get_intersect_by_two_point(self.X[0], self.X[1], other[0], other[1])) != (None, None)


class Polygon(Shape):
    def __init__(self, p=None, holes=None):
        self.p = np.zeros((0, 2))
        if isinstance(p, Polygon):
            self.p = p.p
        elif isinstance(p, (list, np.ndarray)):
            if isinstance(p, np.ndarray):
                self.p = p
            else:
                if isinstance(p[0], Point2D):
                    for point in p:
                        self.p = np.vstack((self.p, [point.p]))
                else:
                    for point in p:
                        self.p = np.vstack((self.p, [point]))
            if np.all(self.p[0, :] == self.p[-1, :]):
                self.p = self.p[:-1, :]
        self.holes = []
        if holes:
            for hole in holes:
                if isinstance(hole, np.ndarray):
                    h = hole
                else:
                    h = np.zeros((0, 2))
                    if isinstance(hole[0], Point2D):
                        for point in h:
                            h = np.vstack((h, [point.p]))
                    else:
                        for point in p:
                            h = np.vstack((h, [point]))
                if h[0, :] == h[-1, :]:
                    h = h[:-1, :]
                self.holes.append(h)

    def area(self):
        p = PolygonWithoutHoles(self.p)
        area_p = p.area()
        area_holes = [PolygonWithoutHoles(h).area() for h in self.holes]
        return area_p - np.sum(area_holes)

    def girth(self):
        p = PolygonWithoutHoles(self.p)
        girth_p = p.girth()
        girth_holes = [PolygonWithoutHoles(h).girth() for h in self.holes]
        return girth_p - np.sum(girth_holes)

    def without_holes(self):
        return self.holes is None or not self.holes

    def is_convexhull(self):
        if not self.without_holes():
            return False
        # TODO, check
        raise NotImplementedError


class PolygonWithoutHoles(Polygon):
    def __init__(self, p):
        super(PolygonWithoutHoles, self).__init__(p, holes=None)

    def area(self):
        """
        面积
        :return:
        """
        # TODO 计算面积
        raise NotImplementedError

    def girth(self):
        """
        周长
        :return:
        """
        p_ring = np.vstack((self.p, self.p[:1, :]))
        return LineString(p_ring).length()


class ConvexPolygon(PolygonWithoutHoles):

    def area(self):
        # 面积
        # 参考 https://blog.csdn.net/cymy001/article/details/81366033
        points = np.vstack((self.p, self.p[0]))
        if len(points) < 3:
            raise Exception("error")
        return np.sum(np.fabs(points[:-1, 0] * points[1:, 1] - points[1:, 0] * points[:-1, 1])) / 2


class Triangle(ConvexPolygon):
    """
    三角形
    """
    def __init__(self, p):
        super().__init__(p)
        assert len(self.p) == 3


class Rectangle(ConvexPolygon):
    def __init__(self, p, *args, **kwargs):
        super().__init__(p)
        assert len(self.p) == 4
        vectors = self.p[1:] - self.p[:-1]
        for vi, vj in zip(vectors[:-1], vectors[1:]):
            assert np.isclose(abs(get_angle_rad(vi, vj) * 2), np.pi)


class Diamond(ConvexPolygon):
    def __init__(self, p, *args, **kwargs):
        super(PolygonWithoutHoles, self).__init__(p, holes=None)
        assert len(self.p) == 4
        m, n = self.p.shape
        dist = [pdist(self.p[ind:ind + 2, :]) for ind in range(m - 1)]
        d = cdist(self.p[:1, :], self.p[-1:, :])
        assert np.all(dist == d)


class Square(Rectangle, Diamond):
    """
    正方形
    """

    def __init__(self, p, eps=1e-8, *args, **kwargs):
        super(Square, self).__init__(p, *args, **kwargs)


class Ellipse(Shape):
    def __init__(self, centre, a=0, b=0):
        self.centre = Point2D(centre)
        self.a = a
        self.b = b

    def area(self):
        """
        面积
        :return:
        """
        return self.a * self.b * np.pi

    def girth(self):
        """
        周长
        :return:
        """
        return 4 * self.a * self.b * np.pi

    def is_circle(self, eps=1e-8):
        return -eps <= (self.a - self.b) <= eps


class Circle(Ellipse):
    def __init__(self, centre, r=0):
        super(Circle, self).__init__(centre, r, r)

    @property
    def r(self):
        return self.a

    @r.setter
    def r(self, radius):
        self.a = self.b = radius


class Arc2D(Line):
    def __init__(self, centre, r, theta_start=-np.pi, theta_end=np.pi, direction=1):
        super().__init__()
        self.centre = centre
        self.r = r
        self.theta_start = theta_start
        self.theta_end = theta_end
        self.direction = direction

        if self.direction > 0:
            assert self.theta_start < self.theta_end
        elif self.direction < 0:
            assert self.theta_start > self.theta_end

    def length(self, metric=euclidean, *args, **kwargs):
        return np.abs(self.theta_end - self.theta_start) * self.r

    def as_linestring2d(self, points_count=30):
        x, y = get_arc(self.centre, self.r, self.theta_start, self.theta_end, points_count)
        points = np.vstack((x, y)).T
        return LineString2D(points)
