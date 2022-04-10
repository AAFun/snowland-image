# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 深圳星河软通科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.astar.ltd
# @file: demo_polygon.py
# @time: 2019/8/16 18:52
# @Software: PyCharm


# if __name__ == '__main__':

from snowland.graphics.core.computational_geometry_2d import Circle, Square, Point2D
from snowland.graphics.solid_geometry._ploygon import in_polygon

unit_circle = Circle((0, 0), 1)
print("单位圆面积", unit_circle.area())
print("单位圆周长", unit_circle.girth())
print("单位圆圆心", unit_circle.centre)

square = Square([[0, 0], [0, 1], [1, 1], [1, 0]])
print("正方形面积", square.area())
print("正方形周长", square.girth())

p = Point2D((0.4, 0.5))

print("p in square?", in_polygon(p, square))
