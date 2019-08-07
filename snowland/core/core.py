# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 深圳星河软通科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.astar.ltd
# @file: 
# @time: 
# @Software: PyCharm


import numpy as np
npa = np.array

class Vector(object):
    def __init__(self, x=None, dim=None):
        if dim is not None:
            x = np.zeros(dim)
        else:
            # TODO: 判断x是一维的
            x = npa(x)
        self.x = x

