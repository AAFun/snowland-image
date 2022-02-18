#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 深圳星河软通科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.astar.ltd
# @file: qgis_tool.py
# @time: 2022/01/06 23:48
# @Software: PyCharm

import sys
import unittest

import pathlib

this_file = pathlib.Path(__file__)
path_pathlib = this_file.parent.parent.parent
path = str(path_pathlib)
print("path:", path)

if path not in sys.path:
    sys.path.insert(0, path)

pathlib_snowland = path_pathlib / "snowland"
path_snowland = str(pathlib_snowland)

if path_snowland not in sys.path:
    sys.path.insert(0, path_snowland)

import numpy as np
from astartool.project import std_logging
from astartool.number import equals_zero
from qgis.core import QgsDistanceArea, QgsUnitTypes, QgsPointXY

npa = np.array

# from snowland.gis_tool.qgis_tool import distance_area
from snowland.gis_tool import haversine, nds


class TestHaversine(unittest.TestCase):

    @classmethod
    @std_logging()
    def setup_class(cls):
        pass

    @classmethod
    @std_logging()
    def teardown_class(cls):
        pass

    @std_logging()
    def setup_method(self, method):
        pass

    @std_logging()
    def teardown_method(self, method):
        pass

    @std_logging()
    def setUp(self):
        Ellipsoid = (haversine.EARTH_RADIUS * 1000, haversine.EARTH_RADIUS * 1000)
        disClass = QgsDistanceArea()
        disClass.setEllipsoid(Ellipsoid[0], Ellipsoid[1])

        self.module = haversine
        self.disClass = disClass

    @std_logging()
    def tearDown(self):
        pass

    def test_1(self):
        """
        经度上加一个值
        """
        p1 = [118, 40]
        p2 = [118.1, 40]
        p1_pointxy = QgsPointXY(*p1)
        p2_pointxy = QgsPointXY(*p2)
        line = self.disClass.measureLine(p1_pointxy, p2_pointxy)
        qgis_meters = self.disClass.convertLengthMeasurement(line, QgsUnitTypes.DistanceMeters)
        haversine_meters = self.module.haversine_metres(*p1_pointxy, *p2_pointxy)
        self.assertTrue(np.isclose(qgis_meters - haversine_meters, 0))  # 毫米量级

    def test_2(self):
        """
        纬度上加一个值
        """
        p1 = [118, 40]
        p2 = [118, 40.1]
        p1_pointxy = QgsPointXY(*p1)
        p2_pointxy = QgsPointXY(*p2)
        line = self.disClass.measureLine(p1_pointxy, p2_pointxy)
        qgis_meters = self.disClass.convertLengthMeasurement(line, QgsUnitTypes.DistanceMeters)
        haversine_meters = self.module.haversine_metres(*p1_pointxy, *p2_pointxy)
        self.assertTrue(np.isclose(qgis_meters - haversine_meters, 0))  # 毫米量级

    def test_3(self):
        """
        测试相同的点
        """
        p1 = [0, 40]
        p2 = [0, 40]
        p1_pointxy = QgsPointXY(*p1)
        p2_pointxy = QgsPointXY(*p2)
        line = self.disClass.measureLine(p1_pointxy, p2_pointxy)
        qgis_meters = self.disClass.convertLengthMeasurement(line, QgsUnitTypes.DistanceMeters)
        haversine_meters = self.module.haversine_metres(*p1_pointxy, *p2_pointxy)
        self.assertTrue(np.isclose(qgis_meters - haversine_meters, 0))  # 毫米量级

    def test_4(self):
        """
        跨南北半球
        """
        p1 = [-0.1, 0]
        p2 = [0.1, 0]
        p1_pointxy = QgsPointXY(*p1)
        p2_pointxy = QgsPointXY(*p2)
        line = self.disClass.measureLine(p1_pointxy, p2_pointxy)
        qgis_meters = self.disClass.convertLengthMeasurement(line, QgsUnitTypes.DistanceMeters)
        haversine_meters = self.module.haversine_metres(*p1_pointxy, *p2_pointxy)
        self.assertTrue(np.isclose(qgis_meters - haversine_meters, 0))  # 毫米量级

    def test_5(self):
        """
        极大
        """
        p1 = [90, 0]
        p2 = [-90, 180]
        p1_pointxy = QgsPointXY(*p1)
        p2_pointxy = QgsPointXY(*p2)
        line = self.disClass.measureLine(p1_pointxy, p2_pointxy)
        qgis_meters = self.disClass.convertLengthMeasurement(line, QgsUnitTypes.DistanceMeters)
        haversine_meters = self.module.haversine_metres(*p1_pointxy, *p2_pointxy)
        print(qgis_meters, haversine_meters)
        self.assertTrue(np.isclose(qgis_meters - haversine_meters, 0))  # 毫米量级


class TestNDS(unittest.TestCase):
    def test_nds_array(self):
        x = [119.135671785614] * 20
        y = [34.5738355769335] * 20
        z = nds.get_tile_id(x, y, 13)

        self.assertEqual(len(z), 20)
        for each in z:
            self.assertEqual(each, 557386867)
