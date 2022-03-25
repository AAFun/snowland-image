#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.snowland.ltd
# @file: color.py
# @time: 2018/7/26 0:24
# @Software: PyCharm

import numpy as np

npa = np.array


def rgb2ycbcr(img):
    origT = npa([[65.481, 128.553, 24.966], [-37.797, -74.203, 112], [112, -93.786, -18.214]])
    oriOffset = npa([[16], [128], [128]])

    if isinstance(img, np.uint8):
        t = 1
        offset = 1.0 / 255
    # elif img.dtype.name == 'float64':
    elif isinstance(img, (np.float, np.float64, float)):
        t = 1.0 / 255
        offset = 1.0 / 255
    elif isinstance(img, np.uint16):
        t = 257.0 / 65535
        offset = 257
    else:
        raise ValueError('image type not support ')
    T = origT * t
    Offset = oriOffset * offset

    ycbcr = np.zeros(img.shape, dtype=img.dtype)
    for p in range(3):
        ycbcr[:, :, p] = T[p, 0] * img[:, :, 0] + T[p, 1] * img[:, :, 1] + T[p, 2] * img[:, :, 2] + Offset[p]

    return ycbcr


def ycbcr2rgb(img):
    origT = npa([[65.481, 128.553, 24.966], [-37.797, -74.203, 112], [112, -93.786, -18.214]])
    oriOffset = npa([[16], [128], [128]])
    tinv = np.linalg.inv(origT)
    if isinstance(img, np.uint8):
        t = 255
        offset = 255
    elif isinstance(img, (np.float, np.float64)):
        t = 255
        offset = 1
    elif isinstance(img, np.uint16):
        t = 65535 / 257.0
        offset = 65535
    else:
        raise ValueError('image type not support ')
    T = tinv * t
    Offset = offset * tinv.dot(oriOffset)

    rgb = np.zeros(img.shape, dtype=img.dtype)

    for p in range(3):
        rgb[:, :, p] = T[p, 0] * img[:, :, 0] + T[p, 1] * img[:, :, 1] + T[p, 2] * img[:, :, 2] - Offset[p]

    if isinstance(img, (float, np.float64)):
        rgb[rgb > 1.0] = 1.0
        rgb[rgb < 0] = 0
    return rgb
