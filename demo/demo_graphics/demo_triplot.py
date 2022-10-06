# -*- coding: utf-8 -*-

import numpy as np
from scipy.spatial import Delaunay
from snowland.plot_helper.plot_helper import plot_arrow, plot_line


def format_point(p, e):
    return ('%.10f' % p[0], '%.10f' % p[1])

#
# line1 = np.loadtxt("D:/line1.txt", delimiter=',')
# line2 = np.loadtxt("D:/line2.txt", delimiter=',')

line1 = np.load("D:/a.txt.npy")
line2 = np.load("D:/b.txt.npy")

print(line1)
print(line2)

points = np.vstack((line1, line2[::-1]))
triang = Delaunay(points[:, :2])

import matplotlib.pyplot as plt

plt.triplot(points[:, 0], points[:, 1], triang.simplices.copy())
plt.plot(points[:, 0], points[:, 1], 'o')
#
for i, p in enumerate(points):
    plt.text(p[0], p[1], str(i))

triang_sort = [tuple(sorted(tri)) for tri in triang.simplices]
triang_sort.sort()
print(triang_sort)
lines = []
for tri in triang_sort:
    a, b, c = tri
    if b < len(line1) <= c:
        lines.append(((points[a] + points[c]) / 2, (points[b] + points[c]) / 2))
    elif b >= len(line1) > a:
        lines.append(((points[a] + points[b]) / 2, (points[a] + points[c]) / 2))

# for line in lines:
#     plot_line(*line, 'r-')
# res = np.vstack((lines[0][0], lines[0][1], np.vstack([line[-1] for line in lines[1:]])))
eps=10
start_map = {format_point(line[0], eps): i for i, line in enumerate(lines)}
end_map = {format_point(line[1], eps): i for i, line in enumerate(lines)}
end_map_i = {i: format_point(line[1], eps) for i, line in enumerate(lines)}

for p_start in (start_map.keys() - end_map.keys()):
    ps = [lines[start_map[p_start]][0]]
    while p_start in start_map:
        ind = start_map[p_start]
        ps.append(lines[ind][1])
        p_start = end_map_i[ind]
print(ps)
res = np.vstack(ps)
plt.plot(res[:, 0], res[:, 1], 'r-')
print(res)
plt.show()
