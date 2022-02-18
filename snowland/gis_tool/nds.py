# -*- coding: utf-8 -*-
from typing import Union, List

import numpy as np

npl = np.linalg
npa = np.array


def dms_to_nds(dms: Union[np.ndarray, List, float]):
    if isinstance(dms, (np.ndarray, list)):
        nds = ((1 << 32) / 360 * npa(dms)).astype(np.uint64)
    else:
        nds = npa([(1 << 32) / 360 * dms]).astype(np.uint64)
    return nds


def nds_to_morton(nds_lon, nds_lat):
    if isinstance(nds_lon, (float, int)) and isinstance(nds_lat, (float, int)):
        bit = 1
        mortonCode = 0
        x, y = nds_lon, nds_lat
        if y < 0:
            y += 0x7FFFFFFF

        y <<= 1

        for i in range(32):
            mortonCode |= x & bit
            x <<= 1
            bit <<= 1
            mortonCode |= y & bit
            y <<= 1
            bit <<= 1

        return mortonCode
    if isinstance(nds_lon, list):
        nds_lon = npa(nds_lon)
    if isinstance(nds_lat, list):
        nds_lat = npa(nds_lat)

    assert len(nds_lon) == len(nds_lat)
    bit = 1
    morton_code = np.zeros_like(nds_lat, dtype=np.uint64)
    x, y = nds_lon, nds_lat
    y[y < 0] += 0x7FFFFFFF
    y <<= 1
    for i in range(32):
        morton_code |= x & bit
        x <<= 1
        bit <<= 1
        morton_code |= y & bit
        y <<= 1
        bit <<= 1
    return morton_code


def get_tile_id(lon, lat, level=13):
    ndsLon = dms_to_nds(lon)
    ndsLat = dms_to_nds(lat)

    morton = nds_to_morton(ndsLon, ndsLat)
    nTileID = (((morton >> (2 * (31 - level))) & 0xffffffff) + (1 << (16 + level)))
    return nTileID

