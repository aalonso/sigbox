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

class fileChooserDialog:

    def __init__ (self):
        #Set the Glade file
        self.gladefile = "sigbox.glade"
        self.filename = ""
        self.wTree = gtk.glade.XML(self.gladefile, "filechooserdialog") 
        #Create our dictionay and connect it
        dic = { "on_filechooserdialog_file_activated"	: self.on_filechooser_file_activated,
				"on_filechooserdialog_response"		    : self.on_filechooser_response
        }
        
        self.wTree.signal_autoconnect(dic)
        self.dialog = self.wTree.get_widget("filechooserdialog")
        self.dialog.set_default_response(gtk.RESPONSE_CANCEL) 
        filter = gtk.FileFilter()
        filter.set_name("Select wav file")
        filter.add_mime_type("audio/wav")
        filter.add_pattern("*.wav")
        self.dialog.add_filter(filter)

    def run (self):
        """Run file chooser dialog"""
        self.dialog.run()    

    def on_filechooser_file_activated(self, widget):
        """On file activeted """
        self.filename = self.dialog.get_filename()
        print "File chooser activate"
        print self.filename
        self.dialog.destroy()

    def on_filechooser_response(self, widget, response):
        """On file activeted """
        if (response == gtk.RESPONSE_OK):
            self.file = self.dialog.get_filename()

        self.dialog.destroy()
