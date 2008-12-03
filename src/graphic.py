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
    #import gtk.glade
except:
    sys.exit(1)

import matplotlib
from pylab import *
from matplotlib.figure import Figure
#from matplotlib.axes import Subplot
from matplotlib.lines import Line2D
from matplotlib.widgets import SpanSelector, RectangleSelector
from matplotlib.backends.backend_gtk import FigureCanvasGTK, NavigationToolbar

class Graphic:
    def __init__(self, widget):
        self.figure = Figure(figsize=(4,3), dpi=64)
        self.axes = self.figure.add_subplot(111) 
        self.axes.grid(True)
        self.widget = widget
        self.canvas = FigureCanvasGTK(self.figure)
        self.graphview = widget
        self.graphview.pack_start(self.canvas, True, True)

        #self.cursor = None
        #self.on_press_cb = None
        #self.on_release_cb = None
        #self.on_motion_cb = None
        self.lx_min = None
        self.lx_max = None
        #self.rec = None
        self.axes2 = None
        self.span = None
        
        self.ticklines = self.axes.get_xticklines()
        self.ticklines.extend( self.axes.get_yticklines() )
        self.gridlines = self.axes.get_xgridlines()
        self.gridlines.extend( self.axes.get_ygridlines() )
        self.ticklabels = self.axes.get_xticklabels()
        self.ticklabels.extend( self.axes.get_yticklabels() )
 

        for line in self.ticklines:
            line.set_linewidth(2)

        for line in self.gridlines:
            line.set_linestyle('-')

        for label in self.ticklabels:
            label.set_fontsize('small')

        self.canvas.show()
        #button_ax = axes([0.7, 0.5, 0.1, 0.75])
        #button = Button(button_ax, 'Press Me')
        #button.on_clicked(self.on_button_clicked)

    def plot(self, x, y):
        self.axes.clear()
        self.axes.plot(x, y)
        self.axes.grid(True)
        self.canvas.destroy()
        self.canvas = FigureCanvasGTK(self.figure)
        self.canvas.show()
        self.widget.pack_start(self.canvas, True, True)

    def semilogy(self, x, y):
        self.axes.clear()
        self.axes.grid(True)
        self.axes.semilogy(x, y)
        self.canvas.destroy()
        self.canvas = FigureCanvasGTK(self.figure)
        self.canvas.show()
        self.widget.pack_start(self.canvas, True, True)

    def clear_figure(self):
        self.axes.clear()
        self.canvas.destroy()
        self.axes.grid(True)
        self.canvas = FigureCanvasGTK(self.figure)
        self.canvas.show()
        self.widget.pack_start(self.canvas, True, True)

    def enable_span(self):
        #self.rec = RectangleSelector(self.axes, self.line_select_callback,
        #                            drawtype='box',useblit=True,
        #                            minspanx=5,minspany=5)
        # Unref original sublot
        #xmin, xmax = self.axes.get_xlim()
        #self.lx_min = xmin
        #self.lx_max = xmax
        self.span = SpanSelector(self.axes, self.on_select, 'horizontal', useblit=False,
                                rectprops=dict(alpha=0.5, facecolor='red'))       
        self.span.visible = True
        #self.lx = self.axes.plot((0,0), (0,0), 'k-')
        #self.ly = self.axes.plot((0,0), (0,0), 'k-')
        #self.lx = Line2D([],[], 'k-')
        #self.ly = Line2D([],[], 'k-')
        #self.lx.set_axes(self.axes)
        #self.ly.set_axes(self.axes)
        #self.lx.visible = True
        #self.ly.visible = True
        #self.on_press_cb = self.canvas.mpl_connect('button_press_event', self.on_press)
        #self.on_release_cb = self.canvas.mpl_connect('button_release_event', self.on_release)
        #self.on_motion_cb = self.canvas.mpl_connect('motion_notify_event', self.on_motion)
        #self.canvas.show()
    
    def on_select(self, xmin, xmax):
        #indmin, indmax = npy.searchsorted(x, (xmin, xmax))
        #indmax = min(len(x)-1, indmax)
        #print xmin
        #print xmax
        #thisx = x[indmin:indmax]
        #thisy = y[indmin:indmax]
        #self.figure.set_data(thisx, thisy)
        self.lx_min = xmin
        self.lx_max = xmax
        self.axes.set_xlim(xmin, xmax)
        #self.axes.set_ylim(thisy.min(), thisy.max())
        self.figure.canvas.draw()

    def disable_span(self):
        self.span.visible = False
        #self.on_press_cb = None
        #self.on_release_cb = None
        #self.on_motion_cb = None


    def line_select_callback(self, event1, event2):
        x1, y1 = event1.xdata, event1.ydata
        x2, y2 = event2.xdata, event2.ydata
        print "(%3.2f, %3.2f) --> (%3.2f, %3.2f)"%(x1,y1,x2,y2)
        print " The button you used were: ",event1.button, event2.button

    def destroy(self):
        self.canvas.destroy()
        #self.canvas.mpl_disconnect(self.on_press)
        #self.canvas.mpl_disconnect(self.on_release)
        #self.canvas.mpl_disconnect(self.on_motion)

    #def on_press(self, event):
    #    print 'x=%d y=%d' %(event.x, event.y)
    #    print 'xdata=%d ydata=%d' %(event.xdata, event.ydata)        

    #    self.text = self.axes.text(0.7,0.9, '', transform=self.axes.transAxes)

    #def on_release(self, event):
    #    print 'x=%d y=%d' %(event.x, event.y)
    #    print 'xdata=%d ydata=%d' %(event.xdata, event.ydata)


    #def on_motion(self, event):
    #    if not event.inaxes: return
    #    axes = event.inaxes
    #    min_x, max_x = axes.get_xlim()
    #    min_y, max_y = axes.get_ylim()

    #    x, y = event.xdata, event.ydata
    #    print self.lx
    #    print self.ly
        # Update line position
    #    self.lx.set_data((min_x, max_x), (y, y))
    #    self.ly.set_data((x, x), (min_y, max_y))
        #self.text.set_text('x=%1.2f, y=%1.2f'%(x,y))
    #    print 'x=%1.2f, y=%1.2f'%(x,y)
    #    self.figure.canvas.draw()
    
class SnaptoCursor:
    def __init__(self, axes, x, y):
        self.axes = axes
        self.lx = axes.plot((0,0), (0,0), 'k-')
        self.ly = axes.plot((0,0), (0,0), 'k-')
        self.x = x
        self.y = y

        self.txt = axes.text(0.7,0.9, '', transform=axes.transAxes)
        self.on_motion_cb = connect('motion_notify_event', self.motion_event)

    def motion_event(self, event):
        if not event.inaxes: return
        axes = event.inaxes
        min_x, max_x = axes.get_xlim()
        min_y, max_y = axes.get_ylim()
        
        x, y = event.xdata, event.ydata

        index = serachsorted(self.x, [x])[0]
        x = self.x[index]
        y = self.y[index]
        # Update line position
        self.lx.set_data((min_x, max_x), (y, y))
        self.ly.set_data((x, x), (min_y, max_y))

        self.txt.set_text('x=%1.2f, y=%1.2f'%(x,y))
        print '(x=%1.2f, y=%1.2f'%(x,y)
        draw()

class SelectBox:
    def __init__(self, axes):
        self.box_select = RectangleSelector(axes, self.selectbox_cb, 
                                            drawtype='box')
       
        #axes.draw()


    def selectbox_cb(self, press_event, release_event):
        x, y = press_event.xdata, press_event.ydata
        x1, y1 = release_event.xdata, release_event.ydata
        print "(%3.2f, %3.2f) --> (%3.2f, %3.2f)"%(x,y,x1,y1)
    

#if __name__ == "__main__":
#    gladefile = "../data/sigbox.glade"
#    wTree = gtk.glade.XML(gladefile, "window_main")
#    signal_graph = wTree.get_widget('vbox_signal')

#    graph = Graphic(signal_graph)
#    cursor = Cursor(graph.axes)
#    show()
