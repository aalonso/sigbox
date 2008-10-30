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


class freqsDialog:
    """Frequency options dialog"""
    def __init__(self):
        # Set the Glade file
        self.gladefile = "../data/sigbox.glade"
        self.wTree = gtk.glade.XML(self.gladefile, "freqsdialog")
        
        #Create our dictionay and connect it        
        dic = {
                "on_freqsdialog_response"         : self.on_freqsdialog_response,
                "on_filechooserbutton_file_set" : self.on_file_set,
                "on_checkbutton_apply_win_toggled" : self.on_apply_win_toggled,
                "on_checkbutton_ifft_toggled" : self.on_apply_ifft_toggled
        }         
        
        self.wTree.signal_autoconnect(dic)
        self.dialog = self.wTree.get_widget("freqsdialog")
        self.dialog.set_default_response(gtk.RESPONSE_CANCEL)
        self.config = Config()
        self.freq_opt = self.config.getConfig('freq_opt')


    def run(self):
        """Load user options"""
        filechooser = self.wTree.get_widget('filechooserbutton')
        filechooser.set_filename(str(self.freq_opt['file']))

        entry = self.wTree.get_widget('spinbutton_seg_n')
        entry.set_value(self.freq_opt['seg_n'])
        entry = self.wTree.get_widget('spinbutton_seg_m')
        entry.set_value(self.freq_opt['seg_m'])
        entry = self.wTree.get_widget('spinbutton_rm_freqs')
        entry.set_value(self.freq_opt['rm_freqs'])

        checkbutton = self.wTree.get_widget('checkbutton_apply_win')
        if self.freq_opt['apply_win']:
            checkbutton.set_active(True)

        checkbutton = self.wTree.get_widget('checkbutton_ifft')
        if self.freq_opt['apply_ifft']:
            checkbutton.set_active(True)
        
        if self.freq_opt['linear']:
            radiobutton = self.wTree.get_widget('radiobutton_lin_scale')
            radiobutton.set_active(True)
        else:
            radiobutton = self.wTree.get_widget('radiobutton_log_scale')
            radiobutton.set_active(True)
        
        combobox = self.wTree.get_widget('combobox_wintyp')
        pattern = str(self.freq_opt['win'])
        combobox_set_active_from_pattern(combobox, pattern)

        self.dialog.run()


    def on_freqsdialog_response(self, widget, response):
        """Dialog callback """
        if(response == gtk.RESPONSE_APPLY):
            # Update user settings
            entry = self.wTree.get_widget('spinbutton_seg_n')
            self.freq_opt['seg_n'] = entry.get_value()
            entry = self.wTree.get_widget('spinbutton_seg_m')
            self.freq_opt['seg_m'] = entry.get_value()
            entry = self.wTree.get_widget('spinbutton_rm_freqs')
            self.freq_opt['rm_freqs'] = entry.get_value()

            checkbutton = self.wTree.get_widget('checkbutton_apply_win')
            self.freq_opt['apply_win'] = checkbutton.get_active()

            checkbutton = self.wTree.get_widget('checkbutton_ifft')
            self.freq_opt['apply_ifft'] = checkbutton.get_active()

            radiobutton = self.wTree.get_widget('radiobutton_lin_scale')            
            self.freq_opt['linear'] = radiobutton.get_active()
 
            combobox = self.wTree.get_widget('combobox_wintyp')
            self.freq_opt['win'] = combobox_get_active_item_text(combobox)
            
            # Save config settings
            self.config.updateConfig('freq_opt', self.freq_opt)
            self.config.writeConfig()

        self.dialog.destroy()


    def on_file_set(self, widget):
        # File selected callback
        self.freq_opt['file'] = widget.get_filename()

    def on_apply_win_toggled(self, widget):
        # Apply window checkbutton callback
        self.freq_opt['apply_win'] = widget.get_active()

    def on_apply_ifft_toggled(self, widget):
        # Apply ifft checkbutton callback
        self.freq_opt['apply_ifft'] = widget.get_active()

        
