#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry

"""
Usage:

    tmpelate.py  [-q | --quiet] [-l | --log] [-d | --debug]
    tmpelate.py (-h | --help)
    tmpelate.py --version

Options:
    -h --help     Show this screen.
    --version     Show version.
    -l --log      Logging in makemd.log file.
    -q --quiet    Quiet output.
    -d --debug    Debug output.

Notes:
   my tmpelate
"""

import matplotlib.pyplot as plt

# 1D data
x = [1,2,3,4,5]
y = [2.3,3.4,1.2,6.6,7.0]

plt.figure(figsize=(12,6))

plt.subplot(231)
plt.plot(x,y)
plt.title("plot")

plt.subplot(232)
plt.scatter(x, y)
plt.title("scatter")

plt.subplot(233)
plt.pie(y)
plt.title("pie")

plt.subplot(234)
plt.bar(x, y)
plt.title("bar")

# 2D data
import numpy as np
delta = 0.025
x = y = np.arange(-3.0, 3.0, delta)
X, Y = np.meshgrid(x, y)
Z    = Y**2 + X**2

plt.subplot(235)
plt.contour(X,Y,Z)
plt.colorbar()
plt.title("condtour")

# read image
import matplotlib.image as mpimg
# img=mpimg.imread('marvin.jpg')

# plt.subplot(236)
# plt.imshow(img)
# plt.title("imshow")

plt.savefig("matplot_sample.jpg")
# plt.show()
# object-oriented plot

from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

fig    = Figure()
canvas = FigureCanvas(fig)
ax     = fig.add_axes([0.1, 0.1, 0.8, 0.8])

line,  = ax.plot([0,1], [0,1])
ax.set_title("a straight line (OO)")
ax.set_xlabel("x value")
ax.set_ylabel("y value")

canvas.print_figure('demo.jpg')