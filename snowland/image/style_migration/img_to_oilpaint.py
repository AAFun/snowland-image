#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.snowland.ltd
# @file: ing_to_oilpaint.py
# @time: 2018/8/12 2:15
# @Software: PyCharm

from copy import deepcopy

import numpy as np


# https://www.cnblogs.com/lonelyxmas/p/ 8564738.html
def oilpaint(img, intensity=5):
    if np.max(img) > 1.1:
        img = img / 255
    tempValues = deepcopy(img)
    w, h, _ = img.shape
    rand = np.random.randint(0, intensity, (w, h))
    X, Y = np.meshgrid(range(h), range(w))
    X, Y = X + rand, Y + rand
    X[X >= h] = h - 1
    Y[Y >= w] = w - 1
    tempValues[:, :, :] = img[Y, X, :]
    return tempValues
