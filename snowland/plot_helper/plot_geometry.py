# -*- coding: utf-8 -*-

import numpy as np
from astartool.error import ParameterError
from matplotlib import pylab as plt

from snowland.graphics.core.analytic_geometry_2d import Line2D, Polynomial

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


def plot_polynomial(polynomial: Polynomial, interval, points=10, *args, handle=plt, **kwargs):
    """
    绘制多项式
    :param handle: 绘图句柄
    :param polynomial: 多项式对象
    :param interval: 绘制的区间（左右均为闭区间）
    :param points: 绘制的点数
    :param args: matplotlib参数
    :param kwargs: matplotlib参数
    :return:
    """
    x = np.linspace(interval[0], interval[1], points)
    res = handle.plot(x, polynomial.get(x), *args, **kwargs)
    return res
