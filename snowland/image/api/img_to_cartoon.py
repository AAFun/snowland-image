# !/usr/bin/env python
#  -*- coding: utf-8 -*-
#  @Author  : 河北雪域网络科技有限公司 A.Star
#  @contact: astar@snowland.ltd
#  @site: 
#  @file: main.py
#  @time: 2018/7/11 14:34
#  @Software: PyCharm

import cv2


def cartoonise(img_rgb, num_down=2, num_bilateral=7):
    """
    :param img_rgb: 输入图像
    :param num_down: 缩减像素采样的数目
    :param num_bilateral: 定义双边滤波的数目
    :return:
    """
    # 用高斯金字塔降低取样
    img_color = img_rgb
    for _ in range(num_down):
        img_color = cv2.pyrDown(img_color)
    # 重复使用小的双边滤波代替一个大的滤波
    for _ in range(num_bilateral):
        img_color = cv2.bilateralFilter(img_color, d=9, sigmaColor=9, sigmaSpace=7)
    # 升采样图片到原始大小
    for _ in range(num_down):
        img_color = cv2.pyrUp(img_color)
    # 转换为灰度并且使其产生中等的模糊
    img_gray = cv2.cvtColor(img_color, cv2.COLOR_RGB2GRAY)
    img_blur = cv2.medianBlur(img_gray, 7)
    # 检测到边缘并且增强其效果
    img_edge = cv2.adaptiveThreshold(img_blur, 255,
                                     cv2.ADAPTIVE_THRESH_MEAN_C,
                                     cv2.THRESH_BINARY,
                                     blockSize=9,
                                     C=2)
    # 转换回彩色图像
    img_edge = cv2.cvtColor(img_edge, cv2.COLOR_GRAY2RGB)
    img_cartoon = cv2.bitwise_and(img_color, img_edge)
    return img_cartoon


if __name__ == '__main__':
    from skimage.io import imread, imshow
    from skimage.data import chelsea
    from matplotlib import pylab as plt
    img = chelsea()
    out = cartoonise(img)
    plt.imshow(out)
    plt.show()
