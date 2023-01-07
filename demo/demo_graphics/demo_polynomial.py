# -*- coding: utf-8 -*-

from astartool.number import equals_zero_all
import numpy as np
from snowland.graphics.core.analytic_geometry_2d import Polynomial
from snowland.plot_helper.plot_geometry import plot_polynomial, plot_line2d_geometry
from matplotlib import pylab as plt

polynomial = Polynomial(coefficient=[40, 50, -20, -30, 90, 20], exponent=[1, 3, 4, 5, 6, 7])
polynomial3 = Polynomial(coefficient=[3, -4, 2], exponent=[2, 1, 0])
ax1 = plot_polynomial(polynomial3, [-10, 10], 100, label="origin line: y={}".format(polynomial3))
line = polynomial3.tangent_line(4)
ax2 = plot_line2d_geometry(line, [-10, 10], label=str(line))
polynomial5 = polynomial3 - 30
ax3 = plot_polynomial(polynomial5, [-10, 10], 100, 'g', label="sub30: y={}".format(polynomial5))
plt.title("test polynomial")
plt.legend(loc=0)
plt.show()
