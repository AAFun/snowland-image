# -*- coding: utf-8 -*-

from collections import Counter
import numpy as np

npa = np.array


def histogram(image: np.ndarray):
    """
    像素直方图统计
    :param image:
    :return:
    """
    image: np.ndarray = npa(image)
    return Counter(image.flatten())
