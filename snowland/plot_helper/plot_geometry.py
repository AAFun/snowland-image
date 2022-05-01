# -*- coding: utf-8 -*-

import numpy as np
from astartool.error import ParameterError
from matplotlib import pylab as plt

from snowland.graphics.core.analytic_geometry_2d import Line2D, Ellipse

npa = np.array


def plot_geometry(points, *args, **kwargs):
    points = npa(points)
    plt.plot(points[:, 0], points[:, 1], *args, **kwargs)


def plot_line2d_geometry(line: Line2D, x=None, y=None, *args, **kwargs):
    """
    绘制line_2d
    """
    if x is not None:
        y = line.get(x=x)
        plt.plot(x, y, *args, **kwargs)
    elif y is not None:
        x = line.get(y=y)
        plt.plot(x, y, *args, **kwargs)
    else:
        raise ParameterError("错误的输入数据")
