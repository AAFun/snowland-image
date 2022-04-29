from qgis.core import QgsGeometry

from snowland.gis_tool.qgis_tool.qgis_util import vector, vector_end, vector_start,\
    points, pointsXY, pointsZM, start_pointXY, end_pointXY
from snowland.gis_tool.qgis_tool import distance_area, qgis_util, utils

QgsGeometry.points = points
QgsGeometry.pointsXY = pointsXY
QgsGeometry.pointsZM = pointsZM
QgsGeometry.vector = vector
QgsGeometry.vector_start = vector_start
QgsGeometry.vector_end = vector_end
QgsGeometry.start_pointXY = start_pointXY
QgsGeometry.end_pointXY = end_pointXY
