#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.snowland.ltd
# @file: demo_digital_screening.py
# @time: 2018/10/9 2:28
# @Software: PyCharm


# 运行时请确定电脑已经安装scikit-snowland 0.1.1以上版本
# 否则请先
# pip install scikit-snowland


from snowland.image.api import *
from skimage.io import imread, imshow, imsave
from skimage.color import rgb2grey
from skimage.data import chelsea
from matplotlib import pylab as plt

if __name__ == '__main__':
    img = chelsea()
    img_gray = rgb2grey(img)
    # img_gray = npa([[0,1],[2,3]])
    out_0 = digital_screening_0_degree(img_gray)
    out_1 = digital_screening_15_degree(img_gray)
    out_2 = digital_screening_45_degree(img_gray)
    out_3 = digital_screening_75_degree(img_gray)
    plt.subplot(141)
    plt.axis('off')
    plt.imshow(img_gray, cmap='gray')


    plt.subplot(142)
    plt.imshow(out_1, cmap='gray')
    plt.axis('off')

    plt.subplot(143)
    plt.imshow(out_2, cmap='gray')
    plt.axis('off')


    plt.subplot(144)
    plt.imshow(out_3, cmap='gray')
    plt.axis('off')

    # imsave('lena0.jpg', img)



    from PIL import Image

    # time = 12
    # K = 12
    # L = 12
    # N = 144
    #
    # im = Image.open('lena0.jpg').convert('L')
    # im2 = Image.new("1", (im.size[0] * time, im.size[1] * time))
    #
    # Mask = [144, 140, 132, 122, 107, 63, 54, 93, 106, 123, 133, 142,
    #         143, 137, 128, 104, 94, 41, 31, 65, 98, 116, 120, 139,
    #         135, 131, 114, 97, 61, 35, 24, 55, 80, 103, 113, 125,
    #         126, 117, 88, 83, 56, 29, 15, 51, 68, 90, 99, 111,
    #         109, 100, 81, 77, 48, 22, 8, 28, 47, 76, 85, 96,
    #         91, 44, 16, 12, 9, 3, 5, 21, 25, 33, 37, 73,
    #         59, 58, 30, 18, 10, 1, 2, 4, 11, 19, 34, 42,
    #         92, 64, 57, 52, 26, 6, 7, 14, 32, 46, 53, 74,
    #         101, 95, 70, 67, 38, 13, 20, 36, 50, 75, 82, 108,
    #         121, 110, 86, 78, 45, 17, 27, 39, 69, 79, 102, 119,
    #         134, 129, 112, 89, 49, 23, 43, 60, 71, 87, 115, 127,
    #         141, 138, 124, 118, 66, 40, 62, 72, 84, 105, 130, 136]
    #
    # for m in range(im2.size[0]):
    #     k = m % K
    #     print(k)
    #     for n in range(im2.size[1]):
    #         l = n % L
    #         pix = int(im.getpixel((m // time, n // time)) / 255.0 * N + 0.5)
    #         if pix > Mask[k * L + l]:
    #             im2.putpixel((m, n), 1)
    #         else:
    #             im2.putpixel((m, n), 0)
    # plt.subplot(133)
    # plt.imshow(im2)
    plt.show()
