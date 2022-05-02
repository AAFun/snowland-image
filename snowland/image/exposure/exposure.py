# -*- coding: utf-8 -*-

from collections import Counter
import numpy as np

npa = np.array


def histogram(image:np.ndarray):
    image: np.ndarray = npa(image)
    return Counter(image.flatten())
