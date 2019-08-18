# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 深圳星河软通科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.astar.ltd
# @file: demo_sphere.py
# @time: 2019/8/17 23:13
# @Software: PyCharm


from snowland.graphics.core.geometry3d import Sphere

ball = Sphere(1, [1, 3, 4])

print("球的体积", ball.volume())
print("球的表面积", ball.surface_area())
