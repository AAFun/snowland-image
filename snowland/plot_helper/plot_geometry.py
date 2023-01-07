# -*- coding: utf-8 -*-

import numpy as np
from astartool.error import ParameterError
from matplotlib import pylab as plt

from snowland.graphics.core.analytic_geometry_2d import Line2D, Polynomial

npa = np.array


def plot_geometry(points, *args, handle=plt, **kwargs):
    """
    绘制二维几何图形
    :param points: n x 2 ndarray
    :param args:
    :param handle: 绘图句柄
    :param kwargs:
    :return:
    """
    points = npa(points)
    ax = handle.plot(points[:, 0], points[:, 1], *args, **kwargs)
    return ax


def plot_line2d_geometry(line: Line2D, x=None, y=None, *args, handle=plt, **kwargs):
    """
    绘制线数据line_2d
    :param line: Line2D
    :param x: np.ndarray or list, 可选, x范围
    :param y: np.ndarray or list, 可选, y范围
    :param args:
    :param handle: 绘图句柄
    :param kwargs:
    :return:
    """
    if x is not None:
        y = line.get(x=x)
        ax = handle.plot(x, y, *args, **kwargs)
    elif y is not None:
        x = line.get(y=y)
        ax = handle.plot(x, y, *args, **kwargs)
    else:
        raise ParameterError("错误的输入数据")
    return ax


def plot_polynomial(polynomial: Polynomial, interval, points=10, *args, handle=plt, **kwargs):
    """
    绘制多项式
    :param polynomial: 多项式对象
    :param interval: 绘制的区间（左右均为闭区间）
    :param points: 绘制的点数
    :param args: matplotlib参数
    :param handle: 绘图句柄
    :param kwargs: matplotlib参数
    :return:
    """
    x = np.linspace(interval[0], interval[1], points)
    res = handle.plot(x, polynomial.get(x), *args, **kwargs)
    return res
