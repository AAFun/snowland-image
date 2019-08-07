#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.snowland.ltd
# @file: homography.py
# @time: 2018/10/8 13:01
# @Software: PyCharm


import numpy as np
import scipy.io as sio
import skimage.feature
import matplotlib.pyplot as plt


# Q2.1
# create a 2 x nbits sampling of integers from to to patchWidth^2
# read BRIEF paper for different sampling methods
def makeTestPattern(patchWidth, nbits):
    res = None
    # YOUR CODE HERE

    return res


# Q2.2
# im is 1 channel image, locs are locations
# compareX and compareY are idx in patchWidth^2
# should return the new set of locs and their descs
def computeBrief(im, locs, compareX, compareY, patchWidth=9):
    desc = None
    # YOUR CODE HERE

    return locs, desc


# Q2.3
# im is a 1 channel image
# locs are locations
# descs are descriptors
# if using Harris corners, use a sigma of 1.5
def briefLite(im):
    locs, desc = None, None
    # YOUR CODE HERE

    return locs, desc


# Q 2.4
def briefMatch(desc1, desc2, ratio=0.8):
    # okay so we say we SAY we use the ratio test
    # which SIFT does
    # but come on, I (your humble TA), don't want to.
    # ensuring bijection is almost as good
    # maybe better
    # trust me
    matches = skimage.feature.match_descriptors(desc1, desc2, 'hamming', cross_check=True)
    return matches


def plotMatches(im1, im2, matches, locs1, locs2):
    fig, ax = plt.subplots(nrows=1, ncols=1)
    skimage.feature.plot_matches(ax, im1, im2, locs1, locs2, matches, matches_color='r')
    plt.show()
    return


def testMatch():
    # YOUR CODE HERE

    return


# Q 2.5
# we're also going to use this to test our
# extra-credit rotational code
def briefRotTest(briefFunc=briefLite):
    # you'll want this
    import skimage.transform
    # YOUR CODE HERE

    return


# Q2.6
# YOUR CODE HERE


# put your rotationally invariant briefLite() function here
def briefRotLite(im):
    locs, desc = None, None
    # YOUR CODE HERE

    return locs, desc
