#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Copyright (C) 2008 by Adrian Alonso <aalonso00@gmail.com>
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

from config import *
from common_utils import *

class filterDialog:
    """Filter dialog"""
    def __init__ (self):
        # Set the Glade file
        self.gladefile = "sigbox.glade"    
        self.wTree = gtk.glade.XML(self.gladefile, "filterdialog")
        #Create our dictionay and connect it
        dic = {
                "on_filterdialog_response"         : self.on_filterdialog_response
        }
 
        self.wTree.signal_autoconnect(dic)
        self.dialog = self.wTree.get_widget("filterdialog")
        self.dialog.set_default_response(gtk.RESPONSE_CANCEL)

        self.config = Config()
        self.filter_opt = self.config.getConfig('filter_opt')


    def run(self):
        """Load user settings""" 
        entry = self.wTree.get_widget('spinbutton_fs')
        entry.set_value(self.filter_opt['fs'])
        entry = self.wTree.get_widget('spinbutton_fc')
        entry.set_value(self.filter_opt['fc'])
        entry = self.wTree.get_widget('spinbutton_fh')
        entry.set_value(self.filter_opt['fh'])
        entry = self.wTree.get_widget('spinbutton_gain')
        entry.set_value(self.filter_opt['gain'])
        entry = self.wTree.get_widget('spinbutton_order')
        entry.set_value(self.filter_opt['order'])

        combobox = self.wTree.get_widget('combobox_wtype')
        pattern = str(self.filter_opt['win'])
        combobox_set_active_from_pattern(combobox, pattern)

        combobox = self.wTree.get_widget('combobox_ftype')
        pattern = str(self.filter_opt['ftype'])
        combobox_set_active_from_pattern(combobox, pattern)
        
        combobox = self.wTree.get_widget('combobox_iirftype')
        pattern = str(self.filter_opt['iirftype'])
        combobox_set_active_from_pattern(combobox, pattern)

        self.dialog.run()


    def on_filterdialog_response(self, widget, response):
        """Filter response callback"""
        if (response == gtk.RESPONSE_APPLY):
            # Get FIR options
            entry = self.wTree.get_widget('spinbutton_fs')
            self.filter_opt['fs'] = entry.get_value()
            entry = self.wTree.get_widget('spinbutton_fc')
            self.filter_opt['fc'] = entry.get_value()
            entry = self.wTree.get_widget('spinbutton_fh')
            self.filter_opt['fh'] = entry.get_value()
            entry = self.wTree.get_widget('spinbutton_gain')
            self.filter_opt['gain'] = entry.get_value()
            entry = self.wTree.get_widget('spinbutton_order')
            self.filter_opt['order'] = entry.get_value()

            combobox = self.wTree.get_widget('combobox_wtype')
            self.filter_opt['win'] = combobox_get_active_item_text(combobox) 
        
            combobox = self.wTree.get_widget('combobox_ftype')
            self.filter_opt['ftype'] = combobox_get_active_item_text(combobox)

            combobox = self.wTree.get_widget('combobox_iirftype')
            self.filter_opt['iirftype'] = combobox_get_active_item_text(combobox)

            # Save options
            self.config.updateConfig('filter_opt', self.filter_opt)
            self.config.writeConfig()

        self.dialog.destroy()

