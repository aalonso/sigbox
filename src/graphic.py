#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Copyright (C) 2008 by Adrian Alonso
# <aalonso00@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#

import sys
try:
    import pygtk
    pygtk.require("2.0")
except:
    pass
try:
    import gtk
    import gtk.glade
except:
    sys.exit(1)

import matplotlib
matplotlib.use('GTK')
#from matplotlib.plot as ptl
from matplotlib.figure import Figure
from matplotlib.axes import Subplot
from matplotlib.backends.backend_gtk import FigureCanvasGTK, NavigationToolbar

class Graphic:
    def __init__(self, widget):
        self.figure = Figure(figsize=(10,6), dpi=96)
        self.axes = self.figure.add_subplot(111)
        self.axes.grid(True)
        #self.plot = ptl
        self.canvas = FigureCanvasGTK(self.figure)
        self.canvas.show()
        self.graphview = widget
        self.graphview.pack_start(self.canvas, True, True)
        self.on_click_cb = self.canvas.mpl_connect('button_press_event', self.on_click)

    def on_click(self, event):       
        print 'x=%d y=%d' %(event.x, event.y)
        print 'xdata=%d ydata=%d' %(event.xdata, event.ydata)

    def destroy(self):
        self.canvas.mpl_disconnect(self.on_click_cb)

