#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: 
# @file: test.py
# @time: 2018/7/26 10:38
# @Software: PyCharm


if __name__ == '__main__':
    from snowland.image.api import cartoonise
    from skimage.io import imread, imshow
    from skimage.data import chelsea
    from matplotlib import pylab as plt
    img = chelsea()
    out = cartoonise(img)
    plt.imshow(out)
    plt.show()
