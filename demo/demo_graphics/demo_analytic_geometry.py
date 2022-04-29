# -*- coding: utf-8 -*-

from snowland.graphics.core.analytic_geometry_2d import Line2D
from snowland.plot_helper.plot_geometry import plot_line2d_geometry
from matplotlib import pylab as plt

if __name__ == '__main__':
    line1 = Line2D(p1=(1., 1), p2=(2., 1))
    line2 = Line2D(p1=(0., 1), p2=(0., 5))

    p = line1.intersection(line2)
    plot_line2d_geometry(line1, x=[0., 10.])
    plot_line2d_geometry(line2, y=[-10., 10.])
    plt.plot(p.x, p.y, "ro")
    plt.show()
