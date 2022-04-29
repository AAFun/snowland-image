__auth__ = 'A.Star'

import numpy as np
from qgis.core import QgsDistanceArea, QgsUnitTypes, QgsPointXY
from snowland.gis_tool import ELLIPSOID

npa = np.array


class DistanceArea:
    def __init__(self, ellipsoid=ELLIPSOID, x=None, y=None):
        self.__qgs_distance = QgsDistanceArea()
        if x is None or y is None:
            if isinstance(ellipsoid, (list, tuple, np.ndarray)):
                self.__qgs_distance.setEllipsoid(*ellipsoid[:2])
            else:
                self.__qgs_distance.setEllipsoid(*ellipsoid[:2])
        else:
            self.__qgs_distance.setEllipsoid(x, y)

    def set_ellipsoid(self, x, y):
        self.__qgs_distance.setEllipsoid(x, y)

    def distance_centimetres(self, Olon, Olat, Dlon, Dlat):
        """
        通过两经纬度点计算地表每一段实际距离, 单位是厘米
        """
        if isinstance(Olon, (float, np.float64)):
            p1, p2 = QgsPointXY(Olon, Olat), QgsPointXY(Dlon, Dlat)
            return self.__qgs_distance.convertLengthMeasurement(self.__qgs_distance.measureLine(p1, p2),
                                                                QgsUnitTypes.DistanceCentimeters)
        else:
            args = [(QgsPointXY(*p1[:2]), QgsPointXY(*p2[:2])) for p1, p2 in zip(zip(Olon, Olat), zip(Dlon, Dlat))]
            return npa([self.__qgs_distance.convertLengthMeasurement(self.__qgs_distance.measureLine(p1, p2),
                                                                     QgsUnitTypes.DistanceCentimeters)
                        for p1, p2 in args])

    def distance_metres(self, Olon, Olat, Dlon, Dlat):
        """
        通过两经纬度点计算地表每一段实际距离, 单位是米
        """
        if isinstance(Olon, (float, np.float64)):
            p1, p2 = QgsPointXY(Olon, Olat), QgsPointXY(Dlon, Dlat)
            return self.__qgs_distance.convertLengthMeasurement(self.__qgs_distance.measureLine(p1, p2),
                                                                QgsUnitTypes.DistanceMeters)
        else:
            args = [(QgsPointXY(*p1[:2]), QgsPointXY(*p2[:2])) for p1, p2 in zip(zip(Olon, Olat), zip(Dlon, Dlat))]
            return npa([self.__qgs_distance.convertLengthMeasurement(self.__qgs_distance.measureLine(p1, p2),
                                                                     QgsUnitTypes.DistanceMeters)
                        for p1, p2 in args])

    def length_centimetres(self, Olon, Olat):
        """
        通过两经纬度点计算地表实际距离之和
        """
        return np.sum(self.distance_centimetres(Olon[:-1], Olat[:-1], Olon[1:], Olat[1:]))

    def length_metres(self, Olon, Olat):
        """
        通过两经纬度点计算地表实际距离
        """
        return np.sum(self.distance_metres(Olon[:-1], Olat[:-1], Olon[1:], Olat[1:]))

    def distance_centimetres_by_points(self, ps1, ps2):
        """
        通过两经纬度点计算地表实际距离，单位是厘米
        """
        args = [(QgsPointXY(*p1[:2]), QgsPointXY(*p2[:2])) for p1, p2 in zip(ps1, ps2)]
        return npa([self.__qgs_distance.convertLengthMeasurement(self.__qgs_distance.measureLine(p1, p2),
                                                                 QgsUnitTypes.DistanceCentimeters)
                    for p1, p2 in args])

    def distance_metres_by_points(self, ps1, ps2):
        """
        通过两经纬度点计算地表实际距离,单位是米
        """
        args = [(QgsPointXY(*p1[:2]), QgsPointXY(*p2[:2])) for p1, p2 in zip(ps1, ps2)]
        return npa([self.__qgs_distance.convertLengthMeasurement(self.__qgs_distance.measureLine(p1, p2),
                                                                 QgsUnitTypes.DistanceMeters)
                    for p1, p2 in args])

    def distance_centimetres_by_two_points(self, p1, p2):
        """
        通过两经纬度点计算地表实际距离， 单位是厘米
        """
        if isinstance(p1, np.ndarray):
            p1 = QgsPointXY(*p1[:2])
        if isinstance(p2, np.ndarray):
            p2 = QgsPointXY(*p2[:2])
        return self.__qgs_distance.convertLengthMeasurement(self.__qgs_distance.measureLine(p1, p2),
                                                            QgsUnitTypes.DistanceCentimeters)

    def distance_metres_by_two_points(self, p1, p2):
        """通过两经纬度点计算地表实际距离， 单位是厘米"""
        if isinstance(p1, np.ndarray):
            p1 = QgsPointXY(*p1[:2])
        if isinstance(p2, np.ndarray):
            p2 = QgsPointXY(*p2[:2])
        return self.__qgs_distance.convertLengthMeasurement(self.__qgs_distance.measureLine(p1, p2),
                                                            QgsUnitTypes.DistanceMeters)
