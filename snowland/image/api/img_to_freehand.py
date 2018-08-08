#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: 
# @file: img_to_handpainting.py
# @time: 2018/8/8 21:42
# @Software: PyCharm

# 代码修改自 https://github.com/Leungtamir/Image-Freehand/blob/master/image.py

import numpy as np
from skimage.color import rgb2grey


def freehand(img, depth=10., el=np.pi / 2.2, az=np.pi / 4):
    """
    手绘风格图像生成
    :param img:
    :param depth: 深度，取值在0-100
    :param el: 光源的俯视角度，弧度值
    :param az: 光源的方位角度，弧度值
    :return:
    """
    img = rgb2grey(img)
    img = img * 255 if np.max(img) <= 1.1 else img
    grad = np.gradient(img)  # 取图像灰度的梯度值
    grad_x, grad_y = grad  # 分别取横纵图像梯度值
    grad_x = grad_x * depth / 100.
    grad_y = grad_y * depth / 100.
    A = np.sqrt(grad_x ** 2 + grad_y ** 2 + 1.)
    uni_x = grad_x / A
    uni_y = grad_y / A
    uni_z = 1. / A

    dx = np.cos(el) * np.cos(az)  # 光源对x轴的影响
    dy = np.cos(el) * np.sin(az)  # 光源对y轴的影响
    dz = np.sin(el)  # 光源对z轴的影响

    gd = (dx * uni_x + dy * uni_y + dz * uni_z)  # 光源归一化
    gd = gd.clip(0, 1)  # 避免数据越界，将生成的灰度值裁剪至0-1之间
    return gd
