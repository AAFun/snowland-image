# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.snowland.ltd
# @file: demo.py
# @time: 2019/8/02 18:44
# @Software: PyCharm


from snowland.image.api import sketch, oilpaint, freehand, cartoonise
from skimage.io import imread, imshow
from skimage.data import chelsea
from matplotlib import pylab as plt

from pencildraw import pencil2
from pencildraw import pencil_drawing

plt.rcParams['font.sans-serif'] = ['SimHei']  # 步骤一（替换sans-serif字体）

plt.rcParams['axes.unicode_minus'] = False  # 步骤二（解决坐标轴负数的负号显示问题）


if __name__ == '__main__':
    img = chelsea()
    plt.figure()

    plt.subplot(2, 3, 1)
    plt.imshow(img)
    plt.title('原图')
    plt.axis('off')

    plt.subplot(2, 3, 2)
    plt.title('铅笔画')
    I = pencil_drawing(img, 8, 1, 8, 1.0, 1.0, pencil2)
    plt.axis('off')
    plt.imshow(I)

    plt.subplot(2, 3, 3)
    plt.title('手绘')
    out = freehand(img)
    plt.axis('off')
    plt.imshow(out, cmap='gray')

    plt.subplot(2, 3, 5)
    plt.title('油画')
    out = oilpaint(img)
    plt.axis('off')
    plt.imshow(out)

    plt.subplot(2, 3, 6)
    plt.title('素描')
    out = sketch(img, 10)
    plt.imshow(out, cmap='gray')
    plt.axis('off')

    plt.show()
