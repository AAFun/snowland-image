#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.snowland.ltd
# @file: ing_to_oilpaint.py
# @time: 2018/8/12 2:15
# @Software: PyCharm

import numpy as np
from matplotlib import pylab as plt
from skimage.morphology import disk
from skimage.filters import median
from copy import deepcopy


# https: // www.cnblogs.com / lonelyxmas / p / 8564738.
# html
def oilpaint(img, intensity=5):
    if np.max(img) > 1.1:
        pass
    else:
        img /= 255
    tempValues = deepcopy(img)
    [w, h, _] = img.shape
    rand = np.random.randint(0, intensity, (w, h))
    X, Y = np.meshgrid(range(w), range(h))
    X, Y = X + rand, Y + rand
    X[X >= w] = w - 1
    Y[Y >= h] = h - 1
    tempValues[:, :, :] = img[Y, X, :]
    return tempValues
