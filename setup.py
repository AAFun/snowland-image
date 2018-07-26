#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: 
# @file: setup.py
# @time: 2018/7/11 15:13
# @Software: PyCharm


from setuptools import setup, find_packages
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
    url='https://gitee.com/hoops/snowland-img2cartoon',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=[
        'opencv-python>=3.4.1.15',
        'numpy>=1.0.0',
        'scikit-image>=0.13',
        'matplotlib>=2.1.2'
    ]
)
