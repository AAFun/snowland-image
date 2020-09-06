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
npl = np.linalg
__all__ = [
    'Line3D',
    'Plane3D'
]


class Line3D(Line):
    def __init__(self, x0=0, y0=0, z0=0, p: Point3D = None, a=None, b=None, c=None, p1: Point3D = None,
                 p2: Point3D = None, plane1=None, plane2=None, *args, **kwargs):
        if a is not None and b is not None and c is not None:
            # (x-x0)/a = (y-y0)/b = (z-z0)/c
            self.a, self.b, self.c = a, b, c
            if p is None:
                # TODO: 判断x0, y0, z0是不是为空
                p = x0, y0, z0
            self.p = Point3D(p)
        elif p1 is not None and p2 is not None:
            # 两点式定义的直线
            if isinstance(p1, Point3D) or isinstance(p2, Point3D):
                raise ValueError("p1, p2应为三维点Point3D的子类")
            self.a, self.b, self.c = p2.x - p1.x, p2.y - p1.y, p2.z - p1.z
            if p is None:
                # TODO: 判断x0, y0, z0是不是为空
                p = x0, y0, z0
            self.p = Point3D(p)
        else:

            if isinstance(plane1, Plane3D) and isinstance(plane2, Plane3D):
                # TODO: 两平面夹线的处理， 此方法有局限 A.Star<astar@snowland.ltd> 2020-9-7
                # 参考资料： http://www.360doc.com/content/15/1222/10/17164483_522220811.shtml
                a1, b1, c1, d1 = plane1.a, plane1.b, plane1.c, plane1.d
                a2, b2, c2, d2 = plane2.a, plane2.b, plane2.c, plane2.d
                self.a, self.b, self.c = npl.det([[b1, c1], [b2, c2]]), npl.det([[a1, c1], [a2, c2]]), npl.det([[a1, b1], [a2, b2]])
                self.p = Point3D((b1*d2-b2*d1)/(a1*b2-a2*b1), (a1*d2-a2*d1)/(a2*b1-a1*b2), 0)

    def feature_vector(self):
        """
        特征向量
        :return: 
        """
        return Vector3([self.a, self.b, self.c])


class Plane3D(Surface):
    def __init__(self, a=None, b=None, c=None, d=None, v=None, p0=None, p1=None, p2=None, p3=None, *args, **kwargs):
        if a is not None and b is not None and c is not None and d is not None:
            # ax + by + cz + d = 0
            self.a, self.b, self.c, self._d = a, b, c, d
        elif v is not None and p0 is not None:
            if isinstance(v, Vector3):
                self.a, self.b, self.c = v.x[0], v.x[1], v.x[2]
            elif isinstance(v, (list, np.ndarray)):
                self.a, self.b, self.c = v[0], v[1], v[2]
                v = Vector3(v)
            else:
                raise ValueError('类型不匹配')

            if isinstance(p0, Point3D):
                p = p0.p
            elif isinstance(p0, (list, np.ndarray)):
                p = Point3D(p0)
            else:
                raise ValueError('类型不匹配')
            self.d = - v.x @ p.p
        else:
            # TODO: 三点式
            pass
        pass

    def normal_vector(self):
        """
        特征向量
        :return:
        """
        return Vector3([self.a, self.b, self.c])

    def is_vector_parallel(self, vector: (Vector3, np.ndarray, list)):
        """
        判断直线是否与平面是否平行
        :param plane1:
        :param plane2:
        :return:
        """
        return self.normal_vector().is_vertical(vector)

    def is_vector_vertical(self, vector: (Vector3, np.ndarray, list)):
        """
        判断向量是否与平面是否垂直
        :param vector:
        :return:
        """
        return self.normal_vector().is_parallel(vector)

    def angle_plane(self, plane):
        """
        平面间夹角
        :param plane:
        :return:
        """
        return self.normal_vector().angle(plane.normal_vector())
