# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 深圳星河软通科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.astar.ltd
# @file: qgis_utils.py
# @time: 2022/01/06 20:52
# @Software: PyCharm


__auth__ = 'A.Star'

from typing import Tuple, List

import numpy as np

npa = np.array


EARTH_REDIUS = 6378.137  # 初始化地球半径km
try:
    from qgis.core import QgsDistanceArea, QgsUnitTypes, QgsPointXY
    Ellipsoid = (6378137, 6356752.314245179)
    disClass = QgsDistanceArea()
    disClass.setEllipsoid(Ellipsoid[0], Ellipsoid[1])
    qgis_import = True
except:
    qgis_import = False


def haversine(Olon, Olat, Dlon, Dlat):
    """
    通过两经纬度点计算地表实际距离
    """
    d_lat = np.radians(Dlat - Olat)
    d_lon = np.radians(Dlon - Olon)
    a = (np.sin(d_lat / 2.) * np.sin(d_lat / 2.) +
         np.cos(np.radians(Olat)) * np.cos(np.radians(Dlat)) *
         np.sin(d_lon / 2.) * np.sin(d_lon / 2.))
    c = 2. * np.arctan2(np.sqrt(a), np.sqrt(1. - a))
    d = EARTH_REDIUS * c
    return d * 100000  # 转换到cm为单位


def haversine_metres(Olon, Olat, Dlon, Dlat):
    return haversine(Olon, Olat, Dlon, Dlat) / 100


def length(Olon, Olat):
    """
    通过两经纬度点计算地表实际距离

    """
    return np.sum(haversine(Olon[:-1], Olat[:-1], Olon[1:], Olat[1:]))


def length_metres(Olon, Olat):
    """
    通过两经纬度点计算地表实际距离
    """
    return np.sum(haversine(Olon[:-1], Olat[:-1], Olon[1:], Olat[1:])) / 100


def haversine_by_points(p1, p2):
    """
    通过两经纬度点计算地表实际距离

    """
    Olon, Olat = p1[:, 0], p1[:, 1]
    Dlon, Dlat = p2[:, 0], p2[:, 1]
    d_lat = np.radians(Dlat - Olat)
    d_lon = np.radians(Dlon - Olon)
    a = (np.sin(d_lat / 2.) * np.sin(d_lat / 2.) +
         np.cos(np.radians(Olat)) * np.cos(np.radians(Dlat)) *
         np.sin(d_lon / 2.) * np.sin(d_lon / 2.))
    c = 2. * np.arctan2(np.sqrt(a), np.sqrt(1. - a))
    d = EARTH_REDIUS * c
    return d * 100000  # 转换到cm为单位


def haversine_metres_by_points(p1, p2):
    return haversine_by_points(p1, p2) / 100


def haversine_metres_by_two_points(p1, p2):
    if qgis_import:
        p1, p2 = QgsPointXY(*p1), QgsPointXY(*p2)
        return disClass.convertLengthMeasurement(disClass.measureLine(p1, p2), QgsUnitTypes.DistanceMeters)
    else:
        Olon, Olat = p1
        Dlon, Dlat = p2
        d_lat = np.radians(Dlat - Olat)
        d_lon = np.radians(Dlon - Olon)
        a = (np.sin(d_lat / 2.) * np.sin(d_lat / 2.) +
             np.cos(np.radians(Olat)) * np.cos(np.radians(Dlat)) *
             np.sin(d_lon / 2.) * np.sin(d_lon / 2.))
        c = 2. * np.arctan2(np.sqrt(a), np.sqrt(1. - a))
        d = EARTH_REDIUS * c
        return d * 1000


def haversine_by_two_points(p1:(np.ndarray, Tuple, List), p2:(np.ndarray, Tuple, List)):
    """
    通过两经纬度点计算地表实际距离
    """
    Olon, Olat = p1
    Dlon, Dlat = p2
    d_lat = np.radians(Dlat - Olat)
    d_lon = np.radians(Dlon - Olon)
    a = (np.sin(d_lat / 2.) * np.sin(d_lat / 2.) +
         np.cos(np.radians(Olat)) * np.cos(np.radians(Dlat)) *
         np.sin(d_lon / 2.) * np.sin(d_lon / 2.))
    c = 2. * np.arctan2(np.sqrt(a), np.sqrt(1. - a))
    d = EARTH_REDIUS * c
    return d * 100000  # 转换到cm为单位
