
from qgis.core import QgsGeometry
from snowland.qgis_tool.qgis_util import vector, vector_end, vector_start, points, pointsXY, start_pointXY, end_pointXY

QgsGeometry.points = points
QgsGeometry.pointsXY = pointsXY
QgsGeometry.vector = vector
QgsGeometry.vector_start = vector_start
QgsGeometry.vector_end = vector_end
QgsGeometry.start_pointXY = start_pointXY
QgsGeometry.end_pointXY = end_pointXY

