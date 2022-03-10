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

from snowland.gis_tool import EARTH_RADIUS

npa = np.array


def haversine_centimetres(Olon, Olat, Dlon, Dlat, earth_radius=EARTH_RADIUS):
    """
    通过两经纬度点计算地表实际距离
    """
    d_lat = np.radians(Dlat - Olat)
    d_lon = np.radians(Dlon - Olon)
    a = (np.sin(d_lat / 2.) * np.sin(d_lat / 2.) +
         np.cos(np.radians(Olat)) * np.cos(np.radians(Dlat)) *
         np.sin(d_lon / 2.) * np.sin(d_lon / 2.))
    c = 2. * np.arctan2(np.sqrt(a), np.sqrt(1. - a))
    d = earth_radius * c
    return d * 100000  # 转换到cm为单位


def haversine_metres(Olon, Olat, Dlon, Dlat, earth_radius=EARTH_RADIUS):
    return haversine_centimetres(Olon, Olat, Dlon, Dlat, earth_radius) / 100


def length_centimetres(Olon, Olat, earth_redius=EARTH_RADIUS):
    """
    通过两经纬度点计算地表实际距离

    """
    return np.sum(haversine_centimetres(Olon[:-1], Olat[:-1], Olon[1:], Olat[1:], earth_redius))


def length_metres(Olon, Olat, earth_radius=EARTH_RADIUS):
    """
    通过两经纬度点计算地表实际距离
    """
    return np.sum(haversine_metres(Olon[:-1], Olat[:-1], Olon[1:], Olat[1:], earth_radius))


def haversine_centimetres_by_points(p1, p2, earth_radius=EARTH_RADIUS):
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
    d = earth_radius * c
    return d * 100000  # 转换到cm为单位


def haversine_metres_by_points(p1, p2, earth_radius=EARTH_RADIUS):
    return haversine_centimetres_by_points(p1, p2, earth_radius) / 100


def haversine_metres_by_two_points(p1, p2, earth_radius=EARTH_RADIUS):
    """
    通过两经纬度点计算地表实际距离（单位是米）
    """
    Olon, Olat = p1
    Dlon, Dlat = p2
    d_lat = np.radians(Dlat - Olat)
    d_lon = np.radians(Dlon - Olon)
    a = (np.sin(d_lat / 2.) * np.sin(d_lat / 2.) +
         np.cos(np.radians(Olat)) * np.cos(np.radians(Dlat)) *
         np.sin(d_lon / 2.) * np.sin(d_lon / 2.))
    c = 2. * np.arctan2(np.sqrt(a), np.sqrt(1. - a))
    d = earth_radius * c
    return d * 1000


def haversine_centimetres_by_two_points(p1: (np.ndarray, Tuple, List),
                                        p2: (np.ndarray, Tuple, List),
                                        earth_radius=EARTH_RADIUS):
    """
    通过两经纬度点计算地表实际距离（单位是厘米）
    """
    Olon, Olat = p1
    Dlon, Dlat = p2
    d_lat = np.radians(Dlat - Olat)
    d_lon = np.radians(Dlon - Olon)
    a = (np.sin(d_lat / 2.) * np.sin(d_lat / 2.) +
         np.cos(np.radians(Olat)) * np.cos(np.radians(Dlat)) *
         np.sin(d_lon / 2.) * np.sin(d_lon / 2.))
    c = 2. * np.arctan2(np.sqrt(a), np.sqrt(1. - a))
    d = earth_radius * c
    return d * 100000  # 转换到cm为单位
