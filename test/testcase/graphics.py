#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 深圳星河软通科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.astar.ltd
# @file: graphics .py
# @time: 2020/9/6 23:48
# @Software: PyCharm


import unittest
from astartool.project import std_logging
from snowland.graphics.core.computational_geometry_2d import *


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


class TestComputationalGeometry2D(unittest.TestCase):

    def test_square(self):
        ps = [(0, 0), (0, 1), (1, 1), (1, 0), (0, 0)]
        square = Square(ps)
        self.assertTrue(isinstance(square, Diamond))
        self.assertTrue(isinstance(square, Rectangle))
        self.assertEqual(square.area(), 1)
        self.assertEqual(square.girth(), 4)
