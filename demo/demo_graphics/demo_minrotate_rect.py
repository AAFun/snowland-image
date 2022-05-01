# -*- coding: utf-8 -*-

import numpy as np
from snowland.graphics.utils import min_rotate_rect, bounding_box, rect_to_points
from snowland.plot_helper.plot_geometry import plot_geometry
from snowland.plot_helper.plot_helper import plot_arrow
from matplotlib import pylab as plt

npa = np.array

points = npa(
    [[0, 0],
     [1.0, 2.0],
     [2.0, 5.0],
     [1.0, 3.0],
     [0, 0]]
)

plot_arrow(points[:, 0], points[:, 1])
plot_geometry(rect_to_points(bounding_box(points)), 'r')

ps_a, a = min_rotate_rect(points, 'a')
ps_c, c = min_rotate_rect(points, 'c')

ps_a = np.vstack((ps_a, ps_a[0]))
ps_c = np.vstack((ps_c, ps_c[0]))

plot_geometry(ps_a, 'g')
plot_geometry(ps_c, 'y')
plt.axis('equal')
plt.show()
