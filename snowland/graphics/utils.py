# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 深圳星河软通科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.astar.ltd
# @file: utils.py
# @time: 2022/01/06 20:48
# @Software: PyCharm


import numpy as np
from scipy.spatial.distance import cdist, pdist, euclidean
from astartool.number import equals_zero

npa = np.array
npl = np.linalg


def middle(x, x1, x2, eps=1e-8):
    """
    判断点是否在x1, x2之间
    x, x1, x2 均为ndarray
    """
    dx1 = x - x1
    dx2 = x - x2
    return ((x1 < x) & (x < x2)) | ((x1 > x) & (x > x2)) | ((-eps < dx1) & (dx1 < eps)) | ((-eps < dx2) & (dx2 < eps))


def get_lines(line_points):
    """
    """
    A = line_points[1:, 1] - line_points[:-1, 1]
    B = line_points[:-1, 0] - line_points[1:, 0]
    C = line_points[1:, 0] * line_points[:-1, 1] - line_points[:-1, 0] * line_points[1:, 1]
    return np.vstack((A, B, C)).T * 10000


def get_foot(point, line=None, A=None, B=None, C=None):
    """
    point: 单点, ndarray/list len(points) = 2
    line: Ax+By+C=0
    返回 foot_x, foot_y, 垂足坐标

    """
    if line is not None:
        A, B, C = line[:, 0], line[:, 1], line[:, 2]
    elif A is not None and B is not None and C is not None:
        pass

    x, y = point[0], point[1]
    A2, B2, AB, AC, BC = A * A, B * B, A * B, A * C, B * C
    # foot_x, foot_y 即为垂足坐标
    foot_x = (B2 * x - AB * y - AC) / (A2 + B2)
    foot_y = (A2 * y - AB * x - BC) / (A2 + B2)

    return foot_x, foot_y


def get_intersect_point(line):
    """
    line_points 是 n x 3 矩阵，代表组成线标准式的参数 Ax+By+C=0 的系数 ABC
    返回这些线的交点
    """
    line1 = line[:-1, :]
    line2 = line[1:, :]

    a1 = line1[:, 0]
    b1 = line1[:, 1]
    c1 = line1[:, 2]
    a2 = line2[:, 0]
    b2 = line2[:, 1]
    c2 = line2[:, 2]
    b1c2 = b1 * c2
    b2c1 = b2 * c1
    a1c2 = a1 * c2
    a1b2 = a1 * b2
    a2b1 = a2 * b1
    a2c1 = a2 * c1

    x = (b1c2 - b2c1) / (a1b2 - a2b1)
    y = (a2c1 - a1c2) / (a1b2 - a2b1)
    return x, y


def distance_point_line(points, line_points, metric=euclidean):
    """
    points: 单点, ndarray/list len(points) = 2
    line_points: 每两点组成的一条线， 代表一条linestring
    返回tuple(isVe, ind, d)
    isVe: 找到的最近点是不是线的顶点
    p: 距离最近的点，ndarray
    d: 最近距离是多少
    """
    # ABC即为线的参数 Ax + By + C = 0
    A = line_points[1:, 1] - line_points[:-1, 1]
    B = line_points[:-1, 0] - line_points[1:, 0]
    C = line_points[1:, 0] * line_points[:-1, 1] - line_points[:-1, 0] * line_points[1:, 1]

    foot_x, foot_y = get_foot(points, A=A, B=B, C=C)
    # 是否为顶点坐标
    is_vertex = True

    index = middle(foot_x, line_points[1:, 0], line_points[:-1, 0]) & middle(foot_y, line_points[1:, 1],
                                                                             line_points[:-1, 1])
    if np.any(index):
        is_vertex = False
        points_check = np.vstack((foot_x[index].T, foot_y[index].T)).T
    else:
        points_check = line_points

    dist = cdist(npa([points]), points_check, metric=metric)
    ind = np.argmin(dist)
    return is_vertex, points_check[ind], dist[0, ind]


def distance_point_line_index(point, line_points, metric=euclidean):
    """
    points: 单点(x, y), ndarray/list len(points) = 2
    line_points: 每两点组成的一条线， 代表一条linestring
    返回tuple(isVe, ind, d)
    is_vertex: 找到的最近点是不是线的顶点
    p: 距离最近的点，ndarray
    d: 最近距离是多少
    ind: index
    """
    # ABC即为线的参数 Ax + By + C = 0
    A = line_points[1:, 1] - line_points[:-1, 1]
    B = line_points[:-1, 0] - line_points[1:, 0]
    C = line_points[1:, 0] * line_points[:-1, 1] - line_points[:-1, 0] * line_points[1:, 1]

    foot_x, foot_y = get_foot(point, A=A, B=B, C=C)
    # 是否为顶点坐标
    is_vertex = True

    index = middle(foot_x, line_points[1:, 0], line_points[:-1, 0]) & middle(foot_y, line_points[1:, 1],
                                                                             line_points[:-1, 1])
    if np.any(index):
        is_vertex = False
        index_ind, = np.where(index)
        points_check = np.vstack((foot_x[index].T, foot_y[index].T)).T

        dist = cdist(npa([point]), points_check, metric=metric)
        ind = np.argmin(dist)
        return is_vertex, points_check[ind], dist[0, ind], index_ind[ind]
    else:
        points_check = line_points
        dist = cdist(npa([point]), points_check, metric=metric)
        ind = np.argmin(dist)
        return is_vertex, points_check[ind], dist[0, ind], ind


def move_distance(a, dist, flag):
    """
    移线
    """
    lines = get_lines(a)
    norm_line = npl.norm(lines[:, :2], axis=1)
    delta_c = dist * norm_line
    lines_new = lines
    if flag:
        lines_new[:, 2] -= delta_c
    else:
        lines_new[:, 2] += delta_c
    x, y = get_intersect_point(lines_new)
    if len(x):
        x_start, y_start = get_foot(a[0, :], lines[:1, :])
        x_end, y_end = get_foot(a[-1, :], lines[-1:, :])
        x = np.hstack((x_start, x, x_end))
        y = np.hstack((y_start, y, y_end))
    return x, y


def move_distance_with_endpoints(a, dist, flag):
    """
    移线，注意和move_distance移线不同！！！
    此函数带有端点
    """
    lines = get_lines(a)
    norm_line = npl.norm(lines[:, :2], axis=1)
    delta_c = dist * norm_line
    lines_new = lines
    if flag:
        lines_new[:, 2] -= delta_c
    else:
        lines_new[:, 2] += delta_c
    x, y = get_intersect_point(lines_new)
    x_start, y_start = get_foot(a[0, :], lines[:1, :])
    x_end, y_end = get_foot(a[-1, :], lines[-1:, :])
    x = np.hstack((x_start, x, x_end))
    y = np.hstack((y_start, y, y_end))

    return x, y


def alignment(linestring1: np.ndarray, linestring2: np.ndarray, metric=euclidean, eps=1):
    """
    化简车道线,使之按垂直方向对齐
    linestring1: 第一根线 m x 2 ndarray
    linestring2: 第二根线 n x 2 ndarray
    metric: 距离计算函数
    eps: 若距离小于 eps, 则不需要截取
    """
    assert linestring1.shape[1] == 2
    assert linestring2.shape[1] == 2
    is_vertex, points_check, dist, ind = distance_point_line_index(linestring2[0], linestring1)
    if (not is_vertex) and metric(points_check, linestring1[0]) > eps:
        linestring1 = linestring1[ind + 1:]
        linestring1 = np.vstack((points_check, linestring1))
    else:
        is_vertex, points_check, dist, ind = distance_point_line_index(linestring1[0], linestring2, metric)
        if (not is_vertex) and metric(points_check, linestring2[0]) > eps:
            linestring2 = linestring2[ind + 1:]
            linestring2 = np.vstack((points_check, linestring2))

    is_vertex, points_check, dist, ind = distance_point_line_index(linestring2[-1], linestring1, metric)
    if (not is_vertex) and metric(points_check, linestring1[-1]) > eps:
        linestring1 = linestring1[:ind + 1]
        linestring1 = np.vstack((linestring1, points_check))
    else:
        is_vertex, points_check, dist, ind = distance_point_line_index(linestring1[-1], linestring2, metric)
        if (not is_vertex) and metric(points_check, linestring2[-1]) > eps:
            linestring2 = linestring2[:ind + 1]
            linestring2 = np.vstack((linestring2, points_check))

    return linestring1, linestring2


def rotate_geometry(poly: np.ndarray, rad):
    matrix = np.asarray([[np.cos(rad), np.sin(rad)],
                         [-np.sin(rad), np.cos(rad)]])
    new_poly = np.dot(poly, matrix)
    return new_poly


def bounding_box(poly: np.ndarray, eps=1e-10):
    """
    boundingBox
    """
    # shape of min_rect: [4, 2]
    x_min, y_min = np.min(poly, axis=0)
    x_max, y_max = np.max(poly, axis=0)
    min_rect = np.asarray([[x_min, y_min],
                           [x_max, y_min],
                           [x_max, y_max],
                           [x_min, y_max]])
    area = (x_max - x_min) * (y_max - y_min)
    return min_rect, area


def min_rotate_rect_a(hull: np.ndarray, eps=1e-10):
    """
    最小外接矩形--按面积
    """
    area = np.inf
    lines_com = []
    if equals_zero(hull[0] - hull[-1], eps):
        points_hull = np.vstack((hull, hull[0]))
    else:
        points_hull = hull

    lines = get_lines(points_hull)
    for i, p2 in hull:
        p1 = hull[i - 1, :]  # 凸包上两个点
        line = lines[i]
        dist_cmp = (points_hull[:, 0] * line[0] + points_hull[:, 1] * line[1] + line[2])
        dist = dist_cmp / npl.norm(line[:2])

        h_ind = np.argmax(np.abs(dist))  # 得到距离最大的点距离，即为高，同时得到该点坐标
        h = dist[h_ind]
        line_px = line
        line_px[2] += dist[h_ind]
        p = hull[h_ind]
        line_cz = npa([line[1], -line[0], -line[1] * p[0] + line[0] * p[1]])

        dist_cmp = (points_hull[:, 0] * line_cz[0] + points_hull[:, 1] * line_cz[1] + line[2])
        dist = dist_cmp / npl.norm(line_cz[:2])

        v_ind_max = np.argmax(dist)  # 得到距离最大的点距离，即为高
        v_ind_min = np.argmin(dist)

        w = np.abs(dist[v_ind_max]) + np.abs(dist[v_ind_min])
        a = h * w
        if area >= h * w:
            # 使面积最小
            area = a
            line_cz_1 = line_cz
            line_cz_1[2] += dist[v_ind_max]
            line_cz_2 = line_cz
            line_cz_2[2] += dist[v_ind_min]
            lines_com = [line, line_cz_1, line_px, line_cz_2, line]
    return get_intersect_point(lines_com)


def min_rotate_rect_c(hull: np.ndarray, eps=1e-10):
    """
    最小外接矩形--按周长
    """
    lines_com = []
    cir = np.inf
    if equals_zero(hull[0] - hull[-1], eps):
        points_hull = np.vstack((hull, hull[0]))
    else:
        points_hull = hull

    lines = get_lines(points_hull)
    for i, p2 in hull:
        p1 = hull[i - 1, :]  # 凸包上两个点
        line = lines[i]
        dist_cmp = (points_hull[:, 0] * line[0] + points_hull[:, 1] * line[1] + line[2])
        dist = dist_cmp / npl.norm(line[:2])

        h_ind = np.argmax(np.abs(dist))  # 得到距离最大的点距离，即为高，同时得到该点坐标
        h = dist[h_ind]
        line_px = line
        line_px[2] += dist[h_ind]
        p = hull[h_ind]
        line_cz = npa([line[1], -line[0], -line[1] * p[0] + line[0] * p[1]])

        dist_cmp = (points_hull[:, 0] * line_cz[0] + points_hull[:, 1] * line_cz[1] + line[2])
        dist = dist_cmp / npl.norm(line_cz[:2])

        v_ind_max = np.argmax(dist)  # 得到距离最大的点距离，即为高
        v_ind_min = np.argmin(dist)

        w = np.abs(dist[v_ind_max]) + np.abs(dist[v_ind_min])
        c = h + w
        if cir > h + w:
            # 使面积最小
            cir = c
            line_cz_1 = line_cz
            line_cz_1[2] += dist[v_ind_max]
            line_cz_2 = line_cz
            line_cz_2[2] += dist[v_ind_min]
            lines_com = [line, line_cz_1, line_px, line_cz_2, line]
    return get_intersect_point(lines_com)


def min_rotate_rect(hull: np.ndarray, cmp: str = 'a', eps=1e-10):
    """
    最小外接矩形
    """
    if cmp.lower().startswith('a'):
        return min_rotate_rect_a(hull, eps)
    else:
        return min_rotate_rect_c(hull, eps)


def get_angle_rad(a, b):
    """
    a, b 为一维向量， 多点会错！！！
    返回 向量a和b之间的夹角， 值域是 -pi ~ pi
    """
    a = npa(a)
    b = npa(b)
    norm_a = npl.norm(a, axis=1) if len(a.shape) == 2 else npl.norm(a)
    norm_b = npl.norm(b, axis=1) if len(b.shape) == 2 else npl.norm(b)
    # 单位化（可以不用这一步）
    # a = a / norm_a  # 不能写成 a /= norm_a
    # b = b / norm_b  # 不能写成 b /= norm_b
    # 夹角cos值
    cos_ = np.dot(a, b) / (norm_a * norm_b)
    # 夹角sin值
    sin_ = np.cross(a, b) / (norm_a * norm_b)
    arctan2_ = np.arctan2(sin_, cos_)
    return arctan2_


def get_angle_degree(a: (list, np.ndarray), b: (list, np.ndarray)):
    """
    返回量向量之间的夹角，值域是 0~180，单位是度
    """
    # 初始化向量
    degree = np.rad2deg(get_angle_rad(a, b))
    return np.abs(degree)


def get_rotate_angle_degree(v1, v2):
    """
    v1旋转到v2经历的角度， 值域0~360, 单位是度
    """
    return np.rad2deg(get_angle_rad(v1, v2)) % 360

