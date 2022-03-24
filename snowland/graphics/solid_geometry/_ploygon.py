# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 深圳星河软通科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.astar.ltd
# @file: _ploygon.py
# @time: 2019/8/12 20:48
# @Software: PyCharm

import logging
from typing import List, Union

import numpy as np
from scipy.spatial.ckdtree import cKDTree

from snowland.graphics.core.computational_geometry_2d import Point2D, Polygon, PolygonWithoutHoles, ConvexPolygon
from snowland.graphics.utils import get_intersect_by_two_point
from snowland.graphics.utils import get_rotate_angle_degree, get_angle_rad

npl = np.linalg
npa = np.array
npr = np.random

__all__ = [
    'concave_hull',
    'coss_multi',
    'get_bottom_point_index',
    'graham_scan',
    'in_polygon',
    'on_polygon_edge',
    'sort_polar_angle_by_vector',
    'sort_polar_angle_by_vector_index',
    'sort_polar_angle_cos',
    'sort_polar_angle_cos_index',

]


def __on_polygon_edge(p: Point2D, polygon: (Polygon, list), eps=1e-8):
    p = Point2D(p)
    polygon = Polygon(polygon)
    for point in polygon.p:
        if p == point:  # 使用重载的等于方法
            return True
    edge = np.vstack((polygon.p, polygon.p[0]))
    s1 = np.sign(edge[:-1, 0] - p[0]) * np.sign(edge[1:, 0] - p[0]) < eps
    s2 = np.sign(edge[:-1, 1] - p[1]) * np.sign(edge[1:, 1] - p[1]) < eps
    s = s1 & s2
    if np.any(s):
        # 快速检测
        inds, = np.where(s)
        for each_ind in inds:
            if -eps < get_angle_rad(p.p - edge[each_ind], edge[each_ind + 1] - p.p) < eps:
                return True

    if polygon.holes:
        for hole in polygon.holes:
            hole = PolygonWithoutHoles(hole)
            if on_polygon_edge(p, hole):
                return True
    return False


def on_polygon_edge(point, polygon: (Polygon, np.ndarray)):
    """
    判断点是否在多边形内
    :param point:
    :param polygon:
    :return:
    """
    if isinstance(polygon, (list, np.ndarray)):
        polygon = Polygon(polygon)
    if isinstance(point, Point2D):
        return __on_polygon_edge(point, polygon)
    if isinstance(point, np.ndarray) and len(point.shape) == 1:
        return __on_polygon_edge(Point2D(point), polygon)
    else:
        # 多个点判断， 返回多个值
        if isinstance(point[0], Point2D):
            return npa([__on_polygon_edge(p, polygon) for p in point])
        if isinstance(point[0], np.ndarray) and len(point[0].shape) == 1:
            return npa([__on_polygon_edge(Point2D(p), polygon) for p in point])
        else:
            # 一个点的list/tuple
            return npa([__on_polygon_edge(Point2D(p), polygon) for p in point])


def __in_polygon(p: Point2D, polygon: Polygon):
    """
    判断点是否在多边形内（不考虑边界情况）
    :param point:
    :param polygon:
    :return:
    """
    for point in polygon.p:
        if p == point:  # 使用重载的等于方法
            return True

    for hole in polygon.holes:
        for point in hole:
            if p == point:  # 使用重载的等于方法
                return True
    count = 0
    flag = False
    for i, point in enumerate(polygon.p):  # 注意，这个i取0的时候，i-1值是-1，所以这个是循环到所有的边
        if point[1] <= p[1] < polygon.p[i - 1, 1] or polygon.p[i - 1, 1] <= p[1] < point[1]:
            a, b, c = point[1] - polygon.p[i - 1, 1], polygon.p[i - 1, 0] - point[0], point[0] * polygon.p[i - 1, 1] - \
                      point[1] * polygon.p[i - 1, 0]
            if a > 0:
                if p[0] * a + b * p[1] + c > 0:
                    flag = not flag
                    count += 1
            else:
                if p[0] * a + b * p[1] + c < 0:
                    flag = not flag
                    count += 1
    if polygon.holes:
        for hole in polygon.holes:
            polygon_temp = PolygonWithoutHoles(hole)
            for i, point in enumerate(polygon_temp.p[:, :]):  # 注意，这个i取0的时候，i-1值是-1，所以这个是循环到所有的边
                if (point[1] <= p[1] < polygon_temp.p[i - 1, 1] or polygon_temp.p[i - 1, 1] <= p[1] < point[1]):
                    a, b, c = point[1] - polygon_temp.p[i - 1, 1], polygon_temp.p[i - 1, 0] - point[0], point[0] * \
                              polygon_temp.p[
                                  i - 1, 1] - point[1] * polygon_temp.p[i - 1, 0]
                    if a < 0:
                        if p[0] * a + b * p[1] + c > 0:
                            flag = not flag
                            count += 1
                    else:
                        if p[0] * a + b * p[1] + c < 0:
                            flag = not flag
                            count += 1
    return flag


def in_polygon(point, polygon: (Polygon, np.ndarray)):
    """
    判断点是否在多边形内
    :param point:
    :param polygon:
    :return:
    """
    if isinstance(polygon, (list, np.ndarray)):
        polygon = Polygon(polygon)
    if isinstance(point, Point2D):
        return __in_polygon(point, polygon)
    if isinstance(point, np.ndarray) and len(point.shape) == 1:
        return __in_polygon(Point2D(point), polygon)
    else:
        # 多个点判断， 返回多个值
        if isinstance(point[0], Point2D):
            return npa([__in_polygon(p, polygon) for p in point])
        if isinstance(point[0], np.ndarray) and len(point[0].shape) == 1:
            return npa([__in_polygon(Point2D(p), polygon) for p in point])
        else:
            # 一个点的list/tuple
            return __in_polygon(Point2D(point), polygon)


def get_bottom_point_index(points):
    """
    返回points中纵坐标最小的点的索引，如果有多个纵坐标最小的点则返回其中横坐标最小的那个
    :param points:
    :return:
    """
    n = len(points)
    return min(range(n), key=lambda x: (points[x][-1], points[x][0]))


def sort_polar_angle_by_vector(vectors: np.ndarray, base_vector: np.ndarray):
    return sorted(vectors, key=lambda v: (get_rotate_angle_degree(base_vector, v), -npl.norm(v)))


def sort_polar_angle_by_vector_index(vectors: (np.ndarray, List[Union[np.ndarray, List]]),
                                     base_vector: (np.ndarray, List[Union[float, int]])):
    return sorted(range(len(vectors)),
                  key=lambda v: (get_rotate_angle_degree(base_vector, vectors[v]), -npl.norm(vectors[v])))


def sort_polar_angle_cos_index(points, center_point: (Point2D, np.ndarray), pre_angle=[1, 0]):
    """
    按照与中心点的极角进行排序，使用的是余弦的方法
    :param points: 需要排序的点
    :param center_point: 中心点
    :return:
    """
    if isinstance(center_point, Point2D):
        center_point = center_point.p
    vectors = [npa(each) - npa(center_point) for each in points]
    inds = sort_polar_angle_by_vector_index(vectors, pre_angle)
    return inds


def sort_polar_angle_cos(points, center_point: (Point2D, np.ndarray), pre_angle=[1, 0]):
    """
    按照与中心点的极角进行排序，使用的是余弦的方法
    :param points: 需要排序的点
    :param center_point: 中心点
    :return:
    """
    if isinstance(center_point, Point2D):
        center_point = center_point.p
    vectors = [npa(each) - npa(center_point) for each in points]
    inds = sort_polar_angle_by_vector_index(vectors, pre_angle)
    return [points[ind] for ind in inds]


def coss_multi(v1, v2):
    """
    计算两个向量的叉乘
    :param v1:
    :param v2:
    :return:
    """
    return v1[0] * v2[1] - v1[1] * v2[0]


def graham_scan(points: (np.ndarray, List[np.ndarray])):
    # 使用Graham扫描法计算凸包
    # 网上的代码好多运行效果并不好
    # 算法参见《算法导论》第三版 第605页
    # https://blog.csdn.net/john_bian/article/details/85221039
    if isinstance(points, np.ndarray):
        points = points.tolist()
    bottom_index = get_bottom_point_index(points)
    bottom_point = points.pop(bottom_index)
    sorted_points = sort_polar_angle_cos(points, bottom_point)

    m = len(sorted_points)
    if m <= 2:
        logging.warning("点的数量过少，无法构成凸包")
        return None

    stack = [bottom_point, sorted_points[0], sorted_points[1]]

    for i in range(2, m):
        length = len(stack)
        top = stack[length - 1]
        next_top = stack[length - 2]
        v1 = [sorted_points[i][0] - next_top[0], sorted_points[i][1] - next_top[1]]
        v2 = [top[0] - next_top[0], top[1] - next_top[1]]

        while coss_multi(v1, v2) >= 0:
            stack.pop()
            length = len(stack)
            top = stack[length - 1]
            next_top = stack[length - 2]
            v1 = [sorted_points[i][0] - next_top[0], sorted_points[i][1] - next_top[1]]
            v2 = [top[0] - next_top[0], top[1] - next_top[1]]

        stack.append(sorted_points[i])

    return ConvexPolygon(stack)


def concave_hull(points: np.ndarray, k=15, heigh_number_step=1):
    """计算凹壳(凹包)
    KNN - Moreira and Santos (2007): CONCAVE HULL: A K-NEAREST NEIGHBOURS APPROACH FOR THE COMPUTATION OF THE REGION OCCUPIED BY A SET OF POINTS.
    http://repositorium.sdum.uminho.pt/bitstream/1822/6429/1/ConcaveHull_ACM_MYS.pdf

    """
    dataset_set = {(p[0], p[1]) for p in points}
    dataset = npa(list(dataset_set))
    tree = cKDTree(dataset)
    kk = max(k, 3)  # make sure k>=3
    dist, index = tree.query(dataset, kk + 1)
    if len(dataset) < 3:
        return None  # a minimum of 3 dissimilar points is required
    elif len(dataset) == 3:
        return PolygonWithoutHoles(points)  # for a 3 points points, the polygon is the points itself
    points = dataset
    # kk = min(kk, len(points) - 1)  # make sure that k neighbours can be found
    first_ind = get_bottom_point_index(dataset)
    first_point = points[first_ind]
    used_flag = np.zeros(len(dataset))
    hull = [first_point]  # initialize the hull with the first point 10
    current_ind, current_point = first_ind, first_point
    used_flag[first_ind] = True  # remove the first point 12
    previous_angle, prev_angle = 0, [1, 0]
    step = 1
    while ((current_ind != first_ind) or (step == 1)) and (not np.all(used_flag)):

        if step == 4:
            used_flag[first_ind] = False  # add the first_point again
        avilable_ind = [ind for ind in index[current_ind, 1:] if not used_flag[ind]]

        kNearestPoints = [dataset[ind] for ind in avilable_ind]  # find the nearest neighbours
        cPoints_inds = sort_polar_angle_cos_index(
            kNearestPoints, current_point,
            prev_angle)  # sort the candidates (neighbours) in descending order of right-hand turn
        cPoints = [kNearestPoints[ind] for ind in cPoints_inds]
        curr_ind = None
        for i, p in enumerate(cPoints):
            if avilable_ind[cPoints_inds[i]] == first_ind:
                curr_ind = i
                break
            # select the first candidate that does not intersects any of the polygon edges
            p1, p2 = hull[step - 1], p
            for c1, c2 in zip(hull[:-2], hull[1:-1]):
                if get_intersect_by_two_point(p1, p2, c1, c2) != (None, None):
                    break
            else:
                curr_ind = i
                break
        else:
            return concave_hull(dataset,
                                kk + heigh_number_step)  # since all candidates intersect at least one edge, try again with a higher number of neighbours

        current_point = cPoints[curr_ind]
        hull.append(current_point)  # a valid candidate was found
        prev_angle = hull[step - 1] - hull[step]
        current_ind = avilable_ind[cPoints_inds[curr_ind]]
        used_flag[current_ind] = True
        step += 1
    for i, d in enumerate(dataset):  # check if all the given points are inside the computed polygon 42
        allInside = on_polygon_edge(d, hull) or in_polygon(d, hull)
        if not allInside:
            return concave_hull(dataset,
                                kk + heigh_number_step)  # since at least one point is out of the computed polygon, try again with a higher number of neighbours
    return PolygonWithoutHoles(hull)  # a valid hull was found!


convex_hull = graham_scan

if __name__ == '__main__':
    import numpy as np
    import matplotlib

    from matplotlib import pylab as plt

    r = np.random.random(1000)
    theta = np.random.random(1000) * 2 * np.pi
    ps = np.vstack((r * np.cos(theta), r * np.sin(theta))).T
    hull = convex_hull(ps)
    plt.plot(np.hstack((hull.p[:, 0], hull.p[0, 0])), np.hstack((hull.p[:, 1], hull.p[0, -1])), 'b')
    plt.plot(ps[:, 0], ps[:, 1], 'r*')
    plt.show()
