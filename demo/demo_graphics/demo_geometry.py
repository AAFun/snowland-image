# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 深圳星河软通科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.astar.ltd
# @file: 
# @time: 
# @Software: PyCharm

from snowland.graphics.core.computational_geometry_2d import Point2D, LineSegment2D

if __name__ == '__main__':
    p0_2d = Point2D((1, 3))
    p1_2d = Point2D(x=2, y=3)

    linesegment0_2d = LineSegment2D(p1=p0_2d, p2=p1_2d)
    linesegment1_2d = LineSegment2D([p0_2d, p1_2d])

    print("line0:", linesegment0_2d.length())
    print("line1:", linesegment1_2d.length())

