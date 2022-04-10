# -*- coding: utf-8 -*-

from astartool.number import equals_zero_all
import numpy as np
from snowland.graphics.core.computational_geometry_2d import Arc2D
from snowland.plot_helper.plot_helper import plot_arrow
from matplotlib import pylab as plt


arc1 = Arc2D((0, 0), 1, np.pi/2, np.pi)

arc2 = Arc2D((0, 0), 1, np.pi, np.pi/2, -1)

arc3 = Arc2D((1, 3), 3, 0, 3 * np.pi)

arc1_line = arc1.as_linestring2d()

arc2_line = arc2.as_linestring2d()

arc3_line = arc3.as_linestring2d(15)

assert equals_zero_all(arc2_line.X - arc1_line.X[::-1])

plt.subplot(221)
plot_arrow(arc1_line.X[:, 0], arc1_line.X[:, 1], 'r-')
plt.subplot(222)
plot_arrow(arc2_line.X[:, 0], arc2_line.X[:, 1], 'g-')
plt.subplot(223)
plot_arrow(arc3_line.X[:, 0], arc3_line.X[:, 1], 'b-')

plt.show()

print("length(arc1):", arc1.length())
print("length(arc2):", arc2.length())
print("length(arc3):", arc3.length())
