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

# 运行时请确定电脑已经安装scikit-snowland 0.1.3 及以上版本
# 否则请先
# pip install scikit-snowland

if __name__ == '__main__':
    img = astronaut()
    plt.figure()
    plt.imshow(img)
    plt.figure()
    out = freehand(img)
    plt.imshow(out, cmap='gray')
    plt.axis('off')
    plt.show()
