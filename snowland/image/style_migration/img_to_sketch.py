#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: 
# @file: img_to_sketch.py
# @time: 2018/8/6 1:15
# @Software: PyCharm

from skimage.color import rgb2grey
import numpy as np


def sketch(img, threshold=15):
    """
    素描画生成
    param img: Image实例
    param threshold: 介于0到100
    :return:
    """
    if threshold < 0:
        threshold = 0
    if threshold > 100:
        threshold = 100
    if len(img.shape) == 3:
        img = rgb2grey(img)
    m, n = img.shape
    diff = np.abs(img[:m - 1, :n - 1] - img[1:, 1:])
    img = np.zeros((m - 1, n - 1))
    img[diff < threshold/255] = 1
    return img
