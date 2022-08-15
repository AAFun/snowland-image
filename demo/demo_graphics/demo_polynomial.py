# -*- coding: utf-8 -*-

from astartool.number import equals_zero_all
import numpy as np
from snowland.graphics.core.analytic_geometry_2d import Polynomial
from snowland.plot_helper.plot_geometry import plot_polynomial
from matplotlib import pylab as plt

polynomial = Polynomial(coefficient=[40, 50, -20, -30, 90, 20], exponent=[1, 3, 4, 5, 6, 7])

plot_polynomial(polynomial, [-1000, 1000], 100)
polynomial2 = polynomial.diff()
plot_polynomial(polynomial2, [-1000, 1000], 100, 'r')
plt.show()

polynomial3 = Polynomial(coefficient=[3, -4, 2], exponent=[2, 1, 0])
plot_polynomial(polynomial3, [-10, 10], 100)
polynomial4 = polynomial3.diff()
plot_polynomial(polynomial4, [-10, 10], 100, 'r')
plt.show()
