#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.snowland.ltd
# @file: demo_pencildraw.py
# @time: 2018/8/14 16:04
# @Software: PyCharm

# 运行时请确定电脑已经安装scikit-snowland 0.1.4以上版本
# 否则请先
# pip install scikit-snowland

from matplotlib import pylab as plt
from skimage.data import chelsea

from snowland.image.api import pencil2
from snowland.image.api import pencil_drawing

if __name__ == '__main__':
    im = chelsea()
    plt.figure(0)
    plt.subplot(121)
    plt.imshow(im)
    I = pencil_drawing(im, 8, 1, 8, 1.0, 1.0, pencil2)
    plt.axis('off')
    axes = plt.subplot(122)
    plt.imshow(I)
    plt.axis('off')
    plt.show()
