#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: 
# @file: setup.py
# @time: 2018/7/11 15:13
# @Software: PyCharm


from setuptools import setup, find_packages
from astartool.setuptool import load_install_requires
from snowland import __version__

setup(
    name='scikit-snowland',
    version=__version__,
    description=(
        'scikit tool for image '
    ),
    long_description=open('README.rst').read(),
    author='A.Star',
    author_email='astar@snowland.ltd',
    maintainer='A.Star',
    maintainer_email='astar@snowland.ltd',
    license='BSD License',
    packages=find_packages(),
    platforms=["all"],
    url='https://github.com/AAFun/scikit-snowland',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=load_install_requires()
)
