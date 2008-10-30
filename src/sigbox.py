#!/usr/bin/env python
import os
import sys
import optparse
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

from about_dialog import *
from filter_dialog import *
from filter_design import *
from filechooser_dialog import *
from freqs_dialog import *
from common_utils import *
from signal_utils import *
from graphic import *

class sigBox:
    """SigBox main class"""
    def __init__(self):
        self.gladefile = "../data/sigbox.glade"
        #self.window = "window_main"
        self.wTree = gtk.glade.XML(self.gladefile, "window_main")
        self.dialog = None

        self.config = Config()
        self.glob_opt = self.config.getConfig('glob_opt')
        self.config = None
        
        combobox = self.wTree.get_widget('combobox_exec')
        pattern = str(self.glob_opt['exec'])
        combobox_set_active_from_pattern(combobox, pattern)

        dic = {
        "on_window_main_destroy"		: self.on_sigbox_destroy,
   	    "on_file_new_activate"			: self.on_menu_file_new,
   	    "on_file_open_activate"			: self.on_toolbutton_open,
   	    "on_file_save_activate"			: self.on_menu_file_save,
   	    "on_file_save_as_activate"		: self.on_menu_file_save_as,
   	    "on_file_quit_activate"			: self.on_menu_file_quit,
        "on_filter-design_activate"     : self.on_menu_design_filter,
        "on_frec-response_activate"     : self.on_menu_design_frec_resp,
        "on_cepstral-response_activate" : self.on_menu_design_cepstral,
   	    "on_original_signal_activate"	: self.on_menu_orig_sig,
   	    "on_about_activate"				: self.on_menu_about,
   	    "on_toolbutton_open_clicked"	: self.on_toolbutton_open,
        "on_toolbutton_clear_clicked"   : self.on_toolbutton_clear,
        "on_toolbutton_execute_clicked"	: self.on_toolbutton_execute    
   		}
		
        self.wTree.signal_autoconnect(dic)
        
        self.signal_graph = Graphic(self.wTree.get_widget('vbox_signal'))
        self.fft_graph = Graphic(self.wTree.get_widget('vbox_fft'))
        self.ifft_graph = Graphic(self.wTree.get_widget('vbox_ifft'))
        self.ceps_graph = Graphic(self.wTree.get_widget('vbox_ceps'))
        
        self.signal_graph.axes.set_xlabel('Time')
        self.signal_graph.axes.set_ylabel('Amplitude')
        self.signal_graph.axes.set_title('Signal')
        
        self.fft_graph.axes.set_title('Frequency Response')
        self.fft_graph.axes.set_xlabel('f(Hz)')
        self.fft_graph.axes.set_ylabel('Amplitude')

        self.ifft_graph.axes.set_title('Ifft')
        self.ifft_graph.axes.set_xlabel('Time')
        self.ifft_graph.axes.set_ylabel('Amplitude')

        self.ceps_graph.axes.set_title('Cepstrum')
        self.ceps_graph.axes.set_xlabel('Time')
        self.ceps_graph.axes.set_ylabel('Amplitude')

        self.wTree.get_widget("window_main").show_all()

    def on_sigbox_destroy(self, widget):
    	"""" sigbox destroy """
        self.signal_graph.destroy()
        self.fft_graph.destroy()
        self.ifft_graph.destroy()
        self.ceps_graph.destroy()
    	gtk.main_quit ()

    def on_menu_file_new(self, widget):
    	""" File new selected """ 

    def on_menu_file_open(self, widget):
    	""" File open selected """

    def on_menu_file_save(self, widget):
    	""" File save selected """

    def on_menu_file_save_as(self, widget):
    	""" File save_as selected """
	
    def on_menu_file_quit(self, widget):
    	""" File quit selected """ 
        self.signal_graph.destroy()
        self.fft_graph.destroy()
        self.ifft_graph.destroy()
        self.ceps_graph.destroy()
    	gtk.main_quit()
	
    def on_menu_design_filter(self, widget):
        """Design filter options"""
        self.dialog = filterDialog()
        self.dialog.run()
        self.dialog = None

    def on_menu_design_frec_resp(self, widget):
        """Frec response options"""
        self.dialog = freqsDialog()
        self.dialog.run()
        self.dialog = None

    def on_menu_design_cepstral(self, widget):
        """Cepstral response options"""

    def on_menu_prefs(self, widget):
    	""" Menu preferences selected """

    def on_menu_orig_sig(self, widget):
    	""" View original signal selected """

    def on_menu_about(self, widget):
    	""" Menu About selected """
    	self.dialog = aboutDialog()
        self.dialog.run()
        self.dialog = None

    def on_toolbutton_open(self, widget):
    	""" Toolbutton open clicked """
    	self.dialog = fileChooserDialog()
        self.dialog.run()
        
        if self.dialog.file:
            self.signal_graph.axes.clear()
            y, fs, bits = wavread(self.dialog.file)
            Fs = 'Fs = %d' %(fs)
            fs = float(fs)
            time = len(y)/fs
            t = r_[0:time:1/fs]
        
            self.signal_graph.axes.plot(t, y)
            self.signal_graph.axes.draw()
            show()

        self.dialog = None
	
    def on_toolbutton_clear(self, widget):
    	""" Toolbutton clear clicked """ 
        

    def on_toolbutton_execute(self, widget):
    	""" Toolbutton exceute clicked """
        # Load user options
        self.config = Config()

        combobox = self.wTree.get_widget('combobox_exec')
        self.glob_opt['exec'] = combobox_get_active_item_text(combobox)

        if self.glob_opt['exec'] == 'FIR filter design':
            opt = self.config.getConfig('filter_opt')
            b = fir_design(options = opt)
            filter_response(b, 1, graph = self.fft_graph)
            #self.image_freq.set_from_file('../data/fir_resp.png')
        elif self.glob_opt['exec'] == 'IIR filter design':
            opt = self.config.getConfig('filter_opt')
            b, a = iir_design(options = opt)
            filter_response(b, a, graph = self.fft_graph)            
            #self.image_freq.set_from_file('../data/fir_resp.png')
        elif self.glob_opt['exec'] == 'Frecuency response':
            options = self.config.getConfig('freq_opt')
            fft_sig(options, graph_fft = self.fft_graph, graph_ifft = self.ifft_graph)
            cepstrum(options, graph_ceps = self.ceps_graph)
            #self.image_freq.set_from_file('../data/fft_sig.png')
            #self.image_time.set_from_file('../data/orig_sig.png')
            #self.image_ifft.set_from_file('../data/ifft_sig.png')
        #elif self.glob_opt['exec'] == 'Cepstral response':
        #    options = self.config.getConfig('freq_opt')
            #self.image_freq.set_from_file('../data/ceps_sig.png')
            #cepstrum(options)
        
        # Display graphics
        show()
        # Unref options
        self.config = None
       
         

def parse_options(argv):
	"""Command line interface, parse user options"""
	done = False
	parser = optparse.OptionParser()
	parser.add_option("-i", "--input", action="store", dest="file",
						type="string", help="Input wav file")
	parser.add_option("-f", "--filter_type", action="store", dest="type", default="fir",
						type="string", help="Filter type: fir | iir")
	#parser.add_option("-r", "--resp_frec", dest="resp_frec", default=0,
	#					type="Int", help="Extract frequency response")
	parser.add_option("-w", "--window", action="store", dest="window", default="hamming",
						type="string", help="Apply window type: hamming | hanning")

	(options, args) = parser.parse_args(argv)
	
	if options.file:
	    done = True
	if done:
	    return options
	else:
	    parser.print_help()


def main(argv):
	
    #options = parse_options(argv)
	
    #if not options:		
	sigbox = sigBox()
	gtk.main()
	

if __name__ == "__main__":
	sys.exit(main(sys.argv))


