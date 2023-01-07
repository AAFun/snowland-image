# -*- coding: utf-8 -*-


import unittest

import numpy as np
from astartool.project import std_logging
from snowland.graphics.core.analytic_geometry_2d import *

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
        line2d_1 = Line2D(1, 2, 3)
        line2d_2 = Line2D(p1=(0, 0), p2=(1, 1))
        points = [[0, 0], [0.5, 0.5], [1, 1]]
        res = line2d_2.locations(points)
        for each in res:
            self.assertEqual(ON, each)

        points = npa([[0, 0], [0.5, 0.5], [1, 1]])
        res = line2d_2.locations(points)
        for each in res:
            self.assertEqual(ON, each)

    def test_polynomial(self):
        poly = Polynomial({2: 1, 3: 4})
        new_poly = poly.diff()
        self.assertEqual(new_poly.polynomial_dict, {1: 2, 2: 12})

        poly = Polynomial({4: 1, 3: 4, 0: 6, -1: 7, -2: 4})
        new_poly = poly.diff()
        self.assertEqual(new_poly.polynomial_dict, {3: 4, 2: 12, -2: -7, -3: -8})

    def test_polynomial_init(self):
        poly = Polynomial(coefficient=[2, 3, -5, 1, -4.0])
        new_poly = poly.diff()
        self.assertEqual(new_poly.polynomial_dict, {1: 2, 2: 12})

        poly = Polynomial({4: 1, 3: 4, 0: 6, -1: 7, -2: 4})
        new_poly = poly.diff()
        self.assertEqual(new_poly.polynomial_dict, {3: 4, 2: 12, -2: -7, -3: -8})
