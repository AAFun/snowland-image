#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: 
# @file: demo_handpainting.py
# @time: 2018/8/8 21:51
# @Software: PyCharm


from snowland.image.api import freehand
from skimage.data import astronaut
from matplotlib import pylab as plt

if __name__ == '__main__':
    img = astronaut()
    plt.figure()
    out = freehand(img)
    plt.imshow(out, cmap='gray')
    plt.show()
