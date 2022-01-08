#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: 
# @file: __init__.py.py
# @time: 2018/7/26 10:30
# @Software: PyCharm

from astartool.setuptool import get_version

version = (0, 1, 5, 'alpha', 1)
__version__ = get_version(version)

del get_version
