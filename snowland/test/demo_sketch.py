#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: 
# @file: demo_sketch.py
# @time: 2018/8/6 9:32
# @Software: PyCharm

from snowland.image.api import sketch
from skimage.io import imread, imshow
from skimage.data import chelsea
from matplotlib import pylab as plt


if __name__ == '__main__':

    img = chelsea()
    out = sketch(img, 15)
    plt.imshow(out, cmap='gray')
    plt.show()
