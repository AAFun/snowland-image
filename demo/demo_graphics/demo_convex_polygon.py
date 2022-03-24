# -*- coding: utf-8 -*-
from functools import reduce

import numpy as np
from astartool.number import equals_zero_all
from scipy.spatial.ckdtree import cKDTree
import matplotlib

from matplotlib import pyplot as plt
from snowland.graphics.core.computational_geometry_2d import PolygonWithoutHoles, LineString2D, LineSegment2D
from snowland.graphics.utils import get_rotate_angle_degree, get_angle_degree
from snowland.graphics.utils import rotate_geometry
from scipy.spatial.distance import euclidean
from snowland.graphics.solid_geometry import on_polygon_edge, in_polygon, get_bottom_point_index
from snowland.plot_helper.plot_helper import plot_line, plot_arrow
npl = np.linalg
npa = np.array


def length(ps):
    return sum(euclidean(a, b) for a, b in zip(ps[:-1], ps[1:]))


def concave_hull_line(lines, buffer_size=3.5*8.983152841195212e-06):
    num_lines = len(lines)
    lines = [line for line in lines if length(line) > 0.1 * 1e-5]
    start_end_feature_map = {}
    for i, line in enumerate(lines):
        s = (line[0, 0], line[0, 1])
        if s in start_end_feature_map:
            start_end_feature_map[s].append((i, line))
        else:
            start_end_feature_map[s] = [(i, line)]
        s = (line[-1, 0], line[-1, 1])
        if s in start_end_feature_map:
            start_end_feature_map[s].append((i, line[::-1]))
        else:
            start_end_feature_map[s] = [(i, line[::-1])]

    all_points = npa(list(start_end_feature_map.keys()))

    point_map = {(p[0], p[1]): ind for ind, p in enumerate(all_points)}
    first_loop = True

    tree = cKDTree(all_points)
    # dist, index_map = tree.query(end_points, k=k)
    start_ind = get_bottom_point_index(all_points)

    ps = lines[start_ind]
    used_list = np.zeros(len(lines), dtype=bool)
    i, current_line = start_ind, lines[start_ind]
    ind_list = []
    av_points = np.ones_like(all_points[:, 0], dtype=bool)
    av_points[point_map[tuple(current_line[-1])]] = False
    while (not np.all(used_list)) and (i != start_ind or first_loop):
        end_point = current_line[-1]
        p = end_point[0], end_point[1]
        connect_line = []
        for ind, line in start_end_feature_map.get(p, []):
            if (ind == start_ind and not first_loop) or ((not used_list[ind]) and ind != i):
                connect_line.append((ind, line))
        if len(connect_line) >= 1:
            ind, each = min(connect_line, key=lambda x:get_rotate_angle_degree(ps[-2]-ps[-1], x[1][-1]-ps[-1]))
            if ind == start_ind and not first_loop:
                break_flag = True
                break
            i, current_line = ind, each
            ps = np.vstack((ps, each[1:]))
            used_list[i] = True
            av_points[point_map[tuple(current_line[0])]] = False
            av_points[point_map[tuple(current_line[-1])]] = False
        elif len(connect_line) == 0:
            ball_point = tree.query_ball_point(end_point, buffer_size)
            break_flag = False
            for i_pb in ball_point:
                p_str = all_points[i_pb, 0], all_points[i_pb, 1]
                if p_str == p:
                    continue
                for ind, each in start_end_feature_map.get(p_str,[]):
                    if not used_list[ind]:
                        if ind == start_ind and not first_loop:
                            break_flag = True
                            break
                        i, current_line = ind, each
                        ps = np.vstack((ps, current_line))
                        used_list[i] = True
                        av_points[point_map[tuple(current_line[0])]] = False
                        av_points[point_map[tuple(current_line[-1])]] = False
                        break_flag = True
                        break
                if break_flag:
                    break
            else:
                # for-else
                pbs = sorted(all_points[av_points, :], key=lambda x:get_rotate_angle_degree(current_line[-2]-end_point, x-end_point))
                for pb in pbs:
                    p_str = pb[0], pb[1]
                    if len(start_end_feature_map.get(p_str, [])) >=2:
                        continue
                    break_flag=False
                    for ind, each in start_end_feature_map.get(p_str,[]):
                        if not used_list[ind]:
                            if ind == start_ind and not first_loop:
                                break_flag = True
                                break
                            i, current_line = ind, each
                            ps = np.vstack((ps, current_line))
                            used_list[i] = True
                            av_points[point_map[tuple(current_line[0])]] = False
                            av_points[point_map[tuple(current_line[-1])]] = False
                            break_flag = True
                            break
                    if break_flag:
                        break
        first_loop = False

    hull = PolygonWithoutHoles(ps.tolist())
    ps = hull.p
    ps = np.vstack((ps, ps[0]))
    return ps
    # if not(np.all(in_polygon(line_points, hull)) or np.all(on_polygon_edge(line_points, hull))):
    #     return concave_hull_line(lines, eps, step, k + step)
    # else:
    #     ps = hull.p
    #     ps = np.vstack((ps, ps[0]))
    #     print(ind_list)
    #     for i, ind in enumerate(ind_list):
    #         plt.text(lines[ind][0, 0], lines[ind][0, 1], str(i))
    #     return ps



if __name__ == '__main__':
    import json

    lines = json.load(open("../../dataset/lines.json", 'r'))
    lines = [npa(line) for line in lines]
    lines = [line for line in lines if length(line) > 0.1 * 1e-5]
    for i, line in enumerate(lines):
        plt.text(line[0, 0], line[0, 1], str(i))
        plot_arrow(line[:, 0], line[:, 1])

    ps = concave_hull_line(lines)
    plot_arrow(ps[:, 0], ps[:, 1], 'r+-')
    plt.show()

