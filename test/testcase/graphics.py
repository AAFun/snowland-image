#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 深圳星河软通科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.astar.ltd
# @file: graphics .py
# @time: 2020/9/6 23:48
# @Software: PyCharm


import unittest

import numpy as np
from astartool.project import std_logging
from snowland.graphics.core.computational_geometry_2d import *
from snowland.graphics.solid_geometry._ploygon import in_polygon, on_polygon_edge
npa = np.array


class TestLine2D(unittest.TestCase):
    @classmethod
    @std_logging()
    def setup_class(cls):
        pass

    @classmethod
    @std_logging()
    def teardown_class(cls):
        print('teardown_class()')

    @std_logging()
    def setup_method(self, method):
        pass

    @std_logging()
    def teardown_method(self, method):
        pass

    def test_line2d(self):
        line2d = LineString2D([(0, 0), (0, 1), (1, 1), (1, 0), (0, 0)])
        segment2d = LineSegment2D(p1=[0, 1], p2=[1, 0])
        self.assertEqual(line2d.length(), 4)
        self.assertTrue(np.isclose(segment2d.length(), np.sqrt(2)))
        self.assertTrue(line2d.is_ring())
        self.assertTrue(line2d.intersects(segment2d))
        segment2d_2 = LineSegment2D(p1=[0.1, 0.1], p2=[0.9, 0.9])
        self.assertFalse(line2d.intersects(segment2d_2))

    def test_in_polygon(self):
        ring = npa([(0, 0), (0, 1), (1, 1), (1, 0), (0, 0)])
        polygon = PolygonWithoutHoles(ring)
        p = [0.5, 0.5]
        self.assertTrue(in_polygon(p, polygon))
        for each in ring:
            self.assertTrue(in_polygon([each], polygon))
        for a, b in zip(ring[:-1], ring[1:]):
            each = (a + b) / 2
            self.assertTrue(on_polygon_edge(each, polygon))
        self.assertFalse(in_polygon([-1, 1], polygon))


class TestComputationalGeometry2D(unittest.TestCase):

    def test_square(self):
        ps = [(0, 0), (0, 1), (1, 1), (1, 0), (0, 0)]
        square = Square(ps)
        self.assertTrue(isinstance(square, Diamond))
        self.assertTrue(isinstance(square, Rectangle))
        self.assertEqual(square.area(), 1)
        self.assertEqual(square.girth(), 4)
