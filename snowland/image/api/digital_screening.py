#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.snowland.ltd
# @file: digital_screening.py
# @time: 2018/10/9 1:50
# @Software: PyCharm

import numpy as np
from functools import reduce
from skimage.transform import resize
from skimage._shared.utils import assert_nD
from skimage.data import chelsea

npa = np.array

Mask_0_degree = npa([[144, 140, 132, 122, 107, 63, 54, 93, 106, 123, 133, 142],
                     [143, 137, 128, 104, 94, 41, 31, 65, 98, 116, 120, 139],
                     [135, 131, 114, 97, 61, 35, 24, 55, 80, 103, 113, 125],
                     [126, 117, 88, 83, 56, 29, 15, 51, 68, 90, 99, 111],
                     [109, 100, 81, 77, 48, 22, 8, 28, 47, 76, 85, 96],
                     [91, 44, 16, 12, 9, 3, 5, 21, 25, 33, 37, 73],
                     [59, 58, 30, 18, 10, 1, 2, 4, 11, 19, 34, 42],
                     [92, 64, 57, 52, 26, 6, 7, 14, 32, 46, 53, 74],
                     [101, 95, 70, 67, 38, 13, 20, 36, 50, 75, 82, 108],
                     [121, 110, 86, 78, 45, 17, 27, 39, 69, 79, 102, 119],
                     [134, 129, 112, 89, 49, 23, 43, 60, 71, 87, 115, 127],
                     [141, 138, 124, 118, 66, 40, 62, 72, 84, 105, 130, 136]])

Mask_0_degree_shape = Mask_0_degree.shape
# Mask_0_degree = Mask_0_degree.flatten()
Mask_0_degree_N = Mask_0_degree_shape[0] * Mask_0_degree_shape[1]  # len(Mask_0_degree)

Mask_15_degree = npa([153, 148, 120, 77, 53, 28, 26, 60, 87, 122, 131, 135, 132, 124, 116, 104, 73, 47, 23, 6, 56, 66,
                      85, 57, 51, 39, 19, 8, 15, 2, 7, 17, 55, 79, 83, 99, 102, 109, 112, 117, 105, 74, 54, 14, 24, 64,
                      84, 121, 137,
                      142, 150, 145, 139, 101, 69, 48, 11, 34, 68, 100, 128, 138, 143, 147, 141, 125, 97, 71, 43, 13,
                      30, 62, 90,
                      107, 110, 96, 91, 76, 52, 27, 20, 5, 4, 21, 25, 37, 45, 82, 92, 94, 95, 98, 63, 41, 1, 38, 67, 89,
                      127, 134, 140,
                      149, 136, 126, 88, 59, 31, 12, 46, 75, 114, 130, 146, 151, 152, 144, 136, 86, 61, 40, 18, 49, 70,
                      103,
                      119, 123, 115, 111, 108, 93, 80, 65, 36, 3, 22, 50, 35, 9, 16, 32, 44, 81, 78, 58, 29, 10, 42, 72,
                      106, 113, 118, 129,
                      133]).reshape((3, 51))

Mask_15_degree_shape = Mask_15_degree.shape
# Mask_15_degree = Mask_15_degree.flatten()
Mask_15_degree_N = Mask_15_degree_shape[0] * Mask_15_degree_shape[1]

Mask_45_degree = npa([[128, 120, 109, 92, 74, 66, 46, 8, 15, 10, 64, 79, 97, 111, 122, 127],
                      [123, 116, 87, 69, 62, 38, 6, 39, 42, 3, 19, 55, 86, 105, 115, 119],
                      [107, 96, 71, 59, 24, 12, 28, 52, 63, 47, 20, 1, 58, 95, 108, 112],
                      [84, 73, 56, 2, 18, 23, 48, 78, 82, 67, 35, 5, 31, 61, 91, 101],
                      [77, 53, 32, 4, 25, 43, 75, 85, 100, 89, 60, 30, 9, 34, 68, 80],
                      [51, 41, 21, 27, 40, 70, 94, 102, 110, 103, 93, 57, 26, 11, 37, 65],
                      [44, 29, 33, 45, 72, 90, 104, 121, 117, 114, 106, 88, 54, 17, 13, 16],
                      [14, 36, 49, 76, 83, 98, 118, 126, 125, 124, 113, 99, 81, 50, 22, 7]])

Mask_45_degree_shape = Mask_45_degree.shape
# Mask_45_degree = Mask_45_degree.flatten()
Mask_45_degree_N = Mask_45_degree_shape[0] * Mask_45_degree_shape[1]  # len(Mask_45_degree)

Mask_75_degree = npa(
    [[153, 145, 136, 117, 95, 81, 8, 52, 93, 104, 97, 86, 77, 69, 59, 54, 41, 29, 7, 5, 36, 23, 13, 18, 26, 34,
      46, 64, 67, 72, 79, 25, 50, 66, 90, 103, 122, 128, 130, 137, 134, 118, 102, 82, 16, 51, 96, 115, 132, 147, 152],
     [148, 139, 126, 105, 98, 78, 15, 27, 80, 73, 71, 61, 53, 48, 31, 14, 1, 10, 17, 4, 3, 6, 30, 49, 60, 68,
      75, 84, 89, 106, 83, 37, 35, 85, 107, 119, 131, 138, 146, 142, 140, 129, 109, 92, 32, 39, 91, 111, 124, 141, 144],
     [120, 101, 88, 74, 63, 58, 2, 20, 65, 47, 43, 40, 28, 11, 12, 24, 38, 42, 55, 21, 22, 56, 62, 70, 87, 100,
      114, 121, 127, 113, 99, 45, 9, 57, 110, 123, 135, 143, 151, 150, 149, 133, 112, 94, 44, 19, 76, 108, 116, 125,
      136]])

Mask_75_degree_shape = Mask_75_degree.shape
# Mask_75_degree = Mask_75_degree.flatten()
Mask_75_degree_N = Mask_75_degree_shape[0] * Mask_75_degree_shape[1]  # len(Mask_75_degree)

time = 12


def digital_screening(img: np.ndarray, mask=Mask_0_degree, mask_shape=Mask_0_degree_shape, degree=None):
    assert_nD(img, 2)
    if degree is not None:
        assert degree in [0, 15, 45, 75], "degree must in (0, 15, 45, 75, )"
        if degree is 0:
            mask, mask_shape = Mask_0_degree, Mask_0_degree_shape
        elif degree is 15:
            mask, mask_shape = Mask_15_degree, Mask_15_degree_shape
        elif degree is 45:
            mask, mask_shape = Mask_45_degree, Mask_45_degree_shape
        elif degree is 75:
            mask, mask_shape = Mask_75_degree, Mask_75_degree_shape
    time = 12
    img_shape = img.shape
    img_newshape = (img_shape[0] * time, img_shape[1] * time)
    len_img_res = img_newshape[0] * img_newshape[1]
    # f = lambda x, y: x.extend([y]*time)
    # [reduce(f, img[]) for j in range(img.shape[1])]
    res_list = []
    for i in range(img_shape[0]):
        row = []
        [row.extend([img[i, j]] * time) for j in range(img_shape[1])]
        res_list.extend(row * time)
    img_res = npa(res_list).reshape(img_newshape)
    # img_temp = np.zeros(img_newshape)
    # for i in range(img_shape[0]):
    #     for j in range(img_shape[1]):
    #         img_temp[i * time:i * time + time, j * time:j * time + time] = img[i, j]
    # img_temp = img_temp.flatten()
    # assert np.sum(img_temp - img_res) < 1e-10
    len_mask = len(mask)
    rep = len_img_res // len_mask + 1
    # mask_rep = np.tile(mask, rep)[:len_img_res]
    mask_rep = np.repeat(mask, img_shape)
    bw = img_res * len_mask >= mask_rep
    return bw.astype(float).reshape(img_newshape)


def digital_screening_0_degree(img):
    return digital_screening(img, degree=0)


def digital_screening_15_degree(img):
    return digital_screening(img, degree=15)


def digital_screening_45_degree(img):
    return digital_screening(img, degree=45)


def digital_screening_75_degree(img):
    return digital_screening(img, degree=75)


# def digital_screening_15_degree(img, time=12, N=153):
#     assert_nD(img, 2)
#     img_N = img * N
#     im2 = np.zeros((img.shape[0] * time, img.shape[1] * time))
#     for n in range(N):
#         im2[i::time, j::time] = img_N + 0.5 > Mask_15_degree[n]
#         # for j in range(time):
#             # im2[i::time, j::time] = img_N + 0.5 > Mask_15_degree[i, j]
#     return im2.astype(float)
import PIL

# for m in range(im2.size[1]):
#     k = m % K
#     t = L - (q * K * (m / K)) % L
#     for n in range(im2.size[0]):
#         l = (n % L + t) % L
#         pix = int(im.getpixel((m / time, n / time)) / 255.0 * N + 0.5)
#         a.add(k*L+l)
#         if pix > Mask_15_degree[k * L + l]:
#             im2.putpixel((m, n), 1)
#         else:
#             im2.putpixel((m, n), 0)

# if __name__ == '__main__':
#     from PIL import Image
#     from skimage.color import rgb2grey
#     import pickle as pk
#
#     time = 12
#     K = 3
#     L = 51
#     N = 153
#     q = 4
#     try:
#         with open('pic.pkl') as f:
#             pk.load(f)
#     except:
#         im = Image.open('lena0.jpg').convert('L')
#         im2 = Image.new("1", (im.size[0] * time, im.size[1] * time))
#
#         Mask = [153, 148, 120, 77, 53, 28, 26, 60, 87, 122, 131, 135, 132, 124, 116, 104, 73, 47, 23, 6, 56, 66, 85, 57,
#                 51,
#                 39,
#                 19, 8, 15, 2, 7, 17, 55, 79, 83, 99, 102, 109, 112, 117, 105, 74, 54, 14, 24, 64, 84, 121, 137, 142,
#                 150,
#                 145, 139, 101, 69, 48, 11, 34, 68, 100, 128, 138, 143, 147, 141, 125, 97, 71, 43, 13, 30, 62, 90, 107,
#                 110,
#                 96, 91,
#                 76, 52, 27, 20, 5, 4, 21, 25, 37, 45, 82, 92, 94, 95, 98, 63, 41, 1, 38, 67, 89, 127, 134, 140, 149,
#                 136, 126, 88, 59, 31, 12, 46, 75, 114, 130, 146, 151, 152, 144, 136, 86, 61, 40, 18, 49, 70, 103, 119,
#                 123,
#                 115, 111,
#                 108, 93, 80, 65, 36, 3, 22, 50, 35, 9, 16, 32, 44, 81, 78, 58, 29, 10, 42, 72, 106, 113, 118, 129, 133]
#         img_gray = np.zeros((im.size[0], im.size[1]))
#         for m in range(im.size[0]):
#             for n in range(im.size[1]):
#                 img_gray[m, n] = im.getpixel((m, n))
#         img_gray /= 255
#
#         # with open('pic.pkl','w')as f:
#         #     pk.dump(img_gray)
#         #     pk.dump(im)
#         #     pk.dump(Mask)
#
#     added = digital_screening_15_degree(img_gray)
#     for m in range(im2.size[1]):
#         k = m % K
#         t = L - (q * K * (m / K)) % L
#         for n in range(im2.size[0]):
#             l = (n % L + t) % L
#             pix = int(im.getpixel((m / time, n / time)) / 255.0 * N + 0.5)
#             print("pix=", pix)
#             print("img=", img_gray[m // time, n // time] * Mask_15_degree_N)
#             if m == 0 and n == 4:
#                 print("k=%d, l=%d" % (k, l))
#                 print(added[m, n], Mask_15_degree[n])
#             if pix > Mask[int(k * L + l)]:
#                 # assert added[m,n]==1, "m, n = %d, %d is not 1" % (m, n)
#                 im2.putpixel((m, n), 1)
#             else:
#                 # assert added[m, n] == 0, "m, n = %d, %d is not 0" % (m, n)
#                 im2.putpixel((m, n), 0)
