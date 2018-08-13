#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: 
# @file: demo_sketch.py
# @time: 2018/8/6 9:32
# @Software: PyCharm

# 运行时请确定电脑已经安装scikit-snowland 0.0.1以上版本
# 否则请先
# pip install scikit-snowland


from snowland.image.api import sketch
from skimage.io import imread, imshow
from skimage.data import chelsea
from matplotlib import pylab as plt

if __name__ == '__main__':
    img = chelsea()
    out = sketch(img, 15)
    plt.imshow(out, cmap='gray')
    plt.axis('off')
    plt.show()
