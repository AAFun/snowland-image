# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.snowland.ltd
# @file: demo.py
# @time: 2019/8/02 18:44
# @Software: PyCharm


from snowland.image.style_migration import sketch, oilpaint, freehand, cartoonise
from skimage.io import imread, imshow, imsave
from skimage.data import chelsea
from matplotlib import pylab as plt

from pencildraw import pencil2
from pencildraw import pencil_drawing

plt.rcParams['font.sans-serif'] = ['SimHei']  # 步骤一（替换sans-serif字体）

plt.rcParams['axes.unicode_minus'] = False  # 步骤二（解决坐标轴负数的负号显示问题）


if __name__ == '__main__':
    # img = chelsea()
    img = imread('222.jpg')
    plt.figure()

    plt.subplot(2, 3, 1)
    plt.imshow(img)
    imsave('原图.jpg', img)
    plt.title('原图')
    plt.axis('off')

    plt.subplot(2, 3, 2)
    plt.title('铅笔画')
    I = pencil_drawing(img, 8, 1, 8, 1.0, 1.0, pencil2)
    imsave('铅笔画.jpg', I)
    plt.axis('off')
    plt.imshow(I)

    plt.subplot(2, 3, 3)
    plt.title('手绘')
    out = freehand(img)
    imsave('手绘.jpg', out)
    plt.axis('off')
    plt.imshow(out, cmap='gray')

    plt.subplot(2, 3, 4)
    plt.title('油画')
    out = oilpaint(img)
    imsave('油画.jpg', out)
    plt.axis('off')
    plt.imshow(out)

    plt.subplot(2, 3, 5)
    plt.title('卡通画')
    out = cartoonise(img)
    imsave('卡通画.jpg', out)
    plt.axis('off')
    plt.imshow(out)

    plt.subplot(2, 3, 6)
    plt.title('素描')
    out = sketch(img, 10)
    imsave('素描.jpg', out)
    plt.imshow(out, cmap='gray')
    plt.axis('off')
    plt.show()
