from typing import List

import numpy as np
from snowland.gis_tool.qgis_tool import QgsGeometry
from qgis.core import QgsPoint, QgsLineString, QgsFeature


class GeometryStructure:
    def __init__(self):
        self.geometry_points = np.empty((0, 3))
        self.geometry = None
        self.features = []
        self.road_id = set()
        self.feature_id = []

    @classmethod
    def init_by_features(cls, features: List[QgsFeature]):
        geom_item = GeometryStructure()
        f = features[0]
        geom_item.geometry_points = f.geometry().points()
        geom_item.features.append(f)
        for f in features[1:]:
            points = f.geometry().points()
            geom_item.geometry_points = np.vstack((geom_item.geometry_points, points[1:, :]))
            geom_item.features.append(f)
        geom_item.create_geometry()
        geom_item.create_road_id()
        geom_item.create_id()
        geom_item.create_tile_road_id()
        return geom_item

    def create_geometry(self):
        self.geometry = QgsGeometry(). \
            fromPolyline(QgsLineString(self.geometry_points[:, 0],
                                       self.geometry_points[:, 1],
                                       self.geometry_points[:, 2],
                                       np.zeros_like(self.geometry_points[:, 0])
                                       ))

    def create_road_id(self):
        self.road_id = set(f['road_id'] for f in self.features)

    def create_tile_road_id(self):
        self.tile_road_id = [(f['tile_id'], f['road_id']) for f in self.features]

    def create_id(self):
        self.feature_id = set(f['id'] for f in self.features)

    def split_to_geometry(self):
        result = []
        z = self.geometry_points[:, :]
        for feature in self.features:
            ps = feature.geometry().asPolyline()
            y_new = z[:len(ps)]
            z = z[len(ps) - 1:]
            geo_new = QgsGeometry(QgsLineString(y_new[:, 0], y_new[:, 1], y_new[:, 2], np.zeros_like(y_new[:, 0])))
            result.append(geo_new)
        return result

    def reset_geometry(self, geometry: QgsGeometry):
        self.geometry = geometry
        self.geometry_points = geometry.points()
