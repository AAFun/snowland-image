# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 深圳星河软通科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.astar.ltd
# @file: 
# @time: 
# @Software: PyCharm


from snowland.graphics.core.geometry2d import Point2D
from snowland.graphics.core.geometry3d import Point3D
from snowland.graphics.core.base import Vector

class Line:
    pass


class Surface:
    pass


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


class Line3D(Line):
    def __init__(self, x0=0, y0=0, z0=0, p: Point3D = None, a=None, b=None, c=None, p1: Point3D = None,
                 p2: Point3D = None, *args, **kwargs):
        if a is not None and b is not None and c is not None:
            # ax+by+c=0方式定义的线
            self.a, self.b, self.c, self.d = a, b, c
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
            # TODO: 两平面夹线的处理
            pass


class Plane(Surface):
    def __init__(self, a=None, b=None, c=None, d=None, v=None, p0=None, p1=None, p2=None, p3=None, *args, **kwargs):
        if a is not None and b is not None and c is not None and d is not None:
            self.a, self.b, self.c, self.d = a, b, c, d
        elif v is not None and p0 is not None:
            # TODO: 点向量的确定方法
            if isinstance(v, Vector):
                pass
        else:
            # TODO: 三点式
            pass
        pass
