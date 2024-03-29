# -*- coding: utf-8 -*-

import numpy as np
from matplotlib import pylab as plt

from snowland.graphics.utils import rotate_geometry


def plot_line(p1, p2, *args, **kwargs):
    """
    绘制一条线
    """
    plt.plot([p1[0], p2[0]], [p1[1], p2[1]], *args, **kwargs)


def plot_arrow(x, y, *args, **kwargs):
    """
    绘制一个箭头
    """
    ps = np.vstack((x, y)).T
    vec = ps[1:, :] - ps[:-1, :]
    left = rotate_geometry(vec, np.pi / 6) * 0.1
    right = rotate_geometry(vec, -np.pi / 6) * 0.1
    tuple_args = (x, y) + args
    cnt = 0
    for p, l, r in zip(ps[1:], left, right):
        p1, p2 = p - l, p
        tuple_args += ([p1[0], p2[0]], [p1[1], p2[1]]) + args
        p1, p2 = p - r, p
        tuple_args += ([p1[0], p2[0]], [p1[1], p2[1]]) + args
        cnt += 2
    plt.plot(*tuple_args, **kwargs)
