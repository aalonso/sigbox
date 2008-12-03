#!/usr/bin/env python

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

class aboutDialog:
    """About dialog"""

    def __init__ (self):
        #Set the Glade file
        self.gladefile = "sigbox.glade"  
        self.wTree = gtk.glade.XML(self.gladefile, "aboutdialog") 
        #Create our dictionay and connect it
        #dic = {
		#		"on_aboutdialog_response"	: self.on_aboutdialog_response,
		#		"on_aboutdialog_close"		: self.on_aboutdialog_close,
        #      }
        
        #self.wTree.signal_autoconnect(dic)
        self.dialog = self.wTree.get_widget("aboutdialog")

    def run (self):
        """Run About dialog"""
        self.dialog.run()
        self.dialog.destroy()

    #def on_aboutdialog_response (self, widget, response):
    #    "on about dialog response"
    #    #self.dialog.destroy()
    #    print "On about response"
        
    #def on_aboutdialog_close (self, widget):
    #    "on about dialog close"
    #    #self.dialog.destroy()
    #    print "On about close"
