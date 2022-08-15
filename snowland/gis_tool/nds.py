# -*- coding: utf-8 -*-

from typing import Union, List, Iterable

import numpy as np
from astartool.common import BIT_EACH
from snowland.gis_tool import NDS_180_DEGREES, NDS_360_DEGREES, NDS_90_DEGREES, RULE_MORTON_TO_LONLAT

npl = np.linalg
npa = np.array


def dms_to_nds(dms: Union[np.ndarray, List, float]):
    if isinstance(dms, (np.ndarray, list)):
        nds = ((1 << 32) / 360 * npa(dms)).astype(np.uint64)
    else:
        nds = npa([(1 << 32) / 360 * dms]).astype(np.uint64)
    return nds


def nds_to_morton(nds_lon, nds_lat):
    if isinstance(nds_lon, (np.uint, int)) and isinstance(nds_lat, (np.uint, int)):
        mortonCode = 0
        x, y = nds_lon, nds_lat
        if y < 0:
            y += 0x7FFFFFFF

        y <<= 1

        for i in range(32):
            mortonCode |= x & BIT_EACH[i * 2]
            x <<= 1
            mortonCode |= y & BIT_EACH[i * 2 + 1]
            y <<= 1

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


def get_tile_id(lon: (np.ndarray, List[float]), lat: (np.ndarray, List[float]), level=13):
    """
    获得level层的瓦片
    """
    if isinstance(lon, Iterable):
        ndsLon = dms_to_nds(lon)
        ndsLat = dms_to_nds(lat)

        morton = nds_to_morton(ndsLon, ndsLat)
        ntile_id = (((morton >> (2 * (31 - level))) & 0xffffffff) + (1 << (16 + level)))
    else:
        tileids = get_tile_id([lon], [lat], level=level)
        ntile_id = tileids[0]
    return ntile_id


def get_level_of_tile_id(tile_id: int) -> int:
    tId = tile_id >> 16
    level = 0
    while tId:
        tId = tId >> 1
        level += 1
    return level


def get_left_bottom_of_tile(tile_id, level=None):
    if level is None:
        level = get_level_of_tile_id(tile_id)
    return get_left_bottom_of_tile_with_level(tile_id, level)


def get_index_of_tile_id_with_level(tile_id: int, level: int):
    offset = 1 << (16 + level)
    return tile_id - offset


def normalize_coord(result):
    """纠偏"""
    # if x > 180 degrees, then subtract 360 degrees
    if result[0] > NDS_180_DEGREES:
        result[0] -= NDS_360_DEGREES + 1  # add 1 because 0 must be counted as well
    elif result[0] < -NDS_180_DEGREES:  # if x < 180 , x += 360
        result[0] += NDS_360_DEGREES + 1  # add 1 because 0 must be counted as well

    # if y > 90 degrees, then subtract 180 degrees
    if result[1] > NDS_90_DEGREES:
        result[1] -= NDS_180_DEGREES + 1  # add 1 because 0 must be counted as well
    elif result[1] < -NDS_90_DEGREES:  # if y < 90, y += 180
        result[1] += NDS_180_DEGREES + 1  # add 1 because 0 must be counted as well
    return result


def morton_code_to_coord(morton_code_param):
    coord = np.zeros(2, dtype=np.uint32)
    morton_code = morton_code_param
    bit = 1
    for i in range(32):
        coord[0] = coord[0] | (morton_code & bit)
        morton_code = morton_code >> 1
        coord[1] = coord[1] | (morton_code & bit)
        bit = bit << 1
    return coord


def get_left_bottom_of_tile_with_level(tile_id: int, level: int = None):
    if level is None:
        level = get_level_of_tile_id(tile_id)
    indexOfTile = get_index_of_tile_id_with_level(tile_id, level)
    mortonCode = indexOfTile << (2 * (31 - level))
    coord = morton_code_to_coord(mortonCode)
    coord = normalize_coord(coord)
    coord += 1
    return coord


def get_lon_lat_of_tile(tile_id: int, level: int = None):
    if level is None:
        level = get_level_of_tile_id(tile_id)
    coord = get_left_bottom_of_tile_with_level(tile_id, level)
    result = coord * RULE_MORTON_TO_LONLAT
    return result


def get_tile_bounding_box(tile_id: int, level=13):
    """
    获得tile所在的矩形框
    """
    if level is None:
        level = get_level_of_tile_id(tile_id)
    p = get_left_bottom_of_tile(tile_id, level)
    length = 180 / (1 << level)
    return p, length, length


def get_a_set_of_tiles(start_point, end_point, level=13):
    """
    获取一系列的tile快
    :param start_point:
    :param end_point:
    :param level:
    :return:
    """
    points: np.ndarray = np.vstack((start_point, end_point))
    start_point, end_point = points.min(axis=0), points.max(axis=0)
    start, _, _ = get_left_bottom_of_tile(get_tile_id(*start_point, level=level), level=level)
    end, len1, len2 = get_left_bottom_of_tile(get_tile_id(*end_point, level=level), level=level)
    end[0] += len1
    end[1] += len2
    xi = np.arange(start[0], end[0], len1)
    yi = np.arange(start[1], end[1], len2)
    XI, YI = np.meshgrid(xi, yi)
    points = np.concatenate((np.expand_dims(XI, axis=0), np.expand_dims(YI, axis=0)), axis=0)
    points_all = np.expand_dims(points, axis=0)
    points0 = points_all[:, :, :-1, :-1]
    points1 = points_all[:, :, 1:, :-1]
    points2 = points_all[:, :, 1:, 1:]
    points3 = points_all[:, :, :-1, 1:]
    blocks = np.concatenate((points0, points1, points2, points3, points0), axis=0)
    return blocks
