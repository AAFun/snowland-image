# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 深圳星河软通科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.astar.ltd
# @file:
# @time:
# @Software: PyCharm

from scipy.spatial.distance import pdist, cdist
from skimage.draw.draw import *

from snowland.graphics.core.base import Point, LineString, Shape

npa = np.array
npm = np.mat


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


class LineString2D(LineString):
    def __init__(self, X=None):
        super(LineString2D, self).__init__(X=X)
        assert self.X.shape[0] is 2


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

    def length(self, metric='euclidean', *args, **kwargs):
        return np.sum(pdist(self.X, metric, *args, **kwargs))



class Polygon(Shape):
    def __init__(self, p=None, holes=None):
        self.p = np.zeros((0, 2))
        if p:
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

    def is_convex(self):
        if not self.without_holes():
            return False
        # TODO, check


class PolygonWithoutHoles(Polygon):
    def __init__(self, p):
        super(PolygonWithoutHoles, self).__init__(p, holes=None)

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
        return LineString(p_ring).length()


class ConvexPolygon(PolygonWithoutHoles):
    def __init__(self, p, *args, **kwargs):
        super(PolygonWithoutHoles, self).__init__(p, holes=None)

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


class Triangle(ConvexPolygon):
    """
    三角形
    """

    def __init__(self, p):
        super(Triangle, self).__init__(p)


class Rectangle(ConvexPolygon):
    def __init__(self, p):
        super(Rectangle, self).__init__(p)


class BoundingBox(Rectangle):
    def __init__(self, p=None, left_bottom=None, top_right=None):
        super(PolygonWithoutHoles, self).__init__(p=None)
        if p:
            assert len(p) == 2, "len(p) must be 2"
            if p[0][0] > p[1][0]:
                min_px, max_px = p[1][0], p[0][0]
            else:
                max_px, min_px = p[1][0], p[0][0]
            if p[0][1] > p[1][1]:
                min_py, max_py = p[1][1], p[0][1]
            else:
                max_py, min_py = p[1][1], p[0][1]
            self.left_bottom = Point2D((min_px, min_py))
            self.top_right = Point2D((max_px, max_py))
        else:
            if left_bottom[0] > top_right[0]:
                min_px, max_px = top_right[0], left_bottom[0]
            else:
                max_px, min_px = top_right[0], left_bottom[0]
            if left_bottom[1] > top_right[1]:
                min_py, max_py = top_right[1], left_bottom[1]
            else:
                max_py, min_py = top_right[1], left_bottom[1]
            self.left_bottom = Point2D((min_px, min_py))
            self.top_right = Point2D((max_px, max_py))

    def to_bbox(self):
        return self.left_bottom[0], self.left_bottom[1], self.top_right[0] - self.left_bottom[0], self.top_right[1] - self.left_bottom[1]


class Diamond(ConvexPolygon):
    def __init__(self, p):
        super(PolygonWithoutHoles, self).__init__(p)
        m, n = self.p.shape
        dist = [pdist(self.p[ind:ind + 2, :]) for ind in range(m - 1)]
        d = cdist(self.p[:1, :], self.p[-1:, :])
        assert np.all(dist == d)


class Square(Rectangle, Diamond):
    """
    正方形
    """

    def __init__(self, *args, eps=1e-8, **kwargs):
        super(Square, self).__init__(*args, **kwargs)
        # TODO 判断方形


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
        return np.fabs(self.a - self.b) <= eps


class Circle(Ellipse):
    def __init__(self, centre, r=0):
        super(Circle, self).__init__(centre, r, r)

    @property
    def r(self):
        return self.a

    @r.setter
    def set_r(self, r):
        self.a = self.b = r


class Capsule(Shape):
    # 胶囊体
    # 即，所有距离线段距离为r的点组成的图形
    def __init__(self, line_segment, r, p1=None, p2=None, *args, **kwargs):
        super(Capsule, self).__init__(*args, **kwargs)
        self.r = r
        self.line_segment = LineSegment2D(line_segment, p1, p2)

    def area(self):
        """
        面积
        :return:
        """
        return np.pi * self.r * self.r + 2 * self.r * self.line_segment.length()

    def girth(self):
        """
        周长
        :return:
        """
        return self.line_segment.length() * 2 + 2 * self.r * np.pi


