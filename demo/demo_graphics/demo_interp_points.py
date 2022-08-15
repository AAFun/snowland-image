# -*- coding: utf-8 -*-

import numpy as np
from matplotlib import pylab as plt

from snowland.graphics.utils import interp_points
from snowland.plot_helper.plot_geometry import plot_geometry

npa = np.array

line1 = [[1, 1], [4, 0]]
line2 = [[1, 1.5], [2, 2], [3, 3.5], [4, 4]]
line1 = npa(line1)
line2 = npa(line2)

new_line1, new_line2 = interp_points(line1, line2)

plt.subplot(121)
plot_geometry(line1, 'ro-', label='line1')
plot_geometry(line2, 'b+-', label='line2')
plt.legend(loc=0)
plt.subplot(122)
plot_geometry(new_line1, 'ro--', label='line1')
plot_geometry(new_line2, 'b+--', label='line2')
plt.legend(loc=0)
plt.show()
