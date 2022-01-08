# -*- coding: utf-8 -*-

import numpy as np

npl = np.linalg
npa = np.array


def DMS2NDS(dms):
    nds = int((1 << 32) / 360 * dms)
    return nds


def NDS2Morton(ndsLon, ndsLat):
    bit = 1
    mortonCode = 0
    x, y = ndsLon, ndsLat

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


def get_tile_ID(lon, lat, level):
    ndsLon = DMS2NDS(lon)
    ndsLat = DMS2NDS(lat)
    morton = NDS2Morton(ndsLon, ndsLat)
    nTileID = (((morton >> (2 * (31 - level))) & 0xffffffff) + (1 << (16 + level)))
    return nTileID
