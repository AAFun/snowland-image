# -*- coding: utf-8 -*-

import numpy as np
from pyproj import Transformer


def utm_transformer(latitude, longitude):
    """
    4326转utm坐标系
    """
    utm_x = np.empty_like(latitude)
    utm_y = np.empty_like(longitude)
    for i, (x, y) in enumerate(zip(longitude, latitude)):
        zone_num = int(x / 6) + 31
        utm_source_str = f"EPSG:326{zone_num}"
        transformer = Transformer.from_crs("EPSG:4326", utm_source_str)
        utm_x[i], utm_y[i] = transformer.transform(y, x)
    return utm_x, utm_y