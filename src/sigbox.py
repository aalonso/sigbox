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
from matplotlib.backends.backend_gtkagg import NavigationToolbar2GTKAgg as NavigationToolbar

class sigBox:
    """SigBox main class"""
    def __init__(self):
        self.gladefile = "sigbox.glade"
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
   	    "on_signal_item_activate"	    : self.on_menu_signal_active,
        "on_fir_item_activate"          : self.on_menu_filter_active,
        "on_freq_item_activate"         : self.on_menu_freq_active,
        "on_ifft_item_activate"         : self.on_menu_ifft_active,
        "on_ceps_item_activate"         : self.on_menu_ceps_active,
        "on_spec_item_activate"         : self.on_menu_spec_active,
   	    "on_about_activate"				: self.on_menu_about,
   	    "on_toolbutton_open_clicked"	: self.on_toolbutton_open,
        "on_toolbutton_clear_clicked"   : self.on_toolbutton_clear,
        "on_toolbutton_select_toggled"  : self.on_toolbutton_select,
        "on_toolbutton_apply_clicked"   : self.on_toolbutton_apply,
        "on_toolbutton_execute_clicked"	: self.on_toolbutton_execute,
        "on_notebook_switch_page"       : self.on_notebook_switch_page,
   		}
		
        self.wTree.signal_autoconnect(dic)
        self.window = self.wTree.get_widget("window_main")
        
        self.signal_graph = None
        self.fft_graph = None
        self.ifft_graph = None
        self.ceps_graph = None
        self.spec_graph = None

        self._figures_init()
        
        # Set Matplotlib toolbar
        self.vbox_toolbar = self.wTree.get_widget('vbox_toolbar')
        self.toolbar = NavigationToolbar(self.signal_graph.canvas, self.window)
        self.vbox_toolbar.pack_start(self.toolbar, False, False)

        # Signal properties
        self.file = None
        self.fs = None
        self.n = None
        self.filter = None
        
        self.notebook = self.wTree.get_widget("notebook")
        self.window.show_all()

    def _figures_init(self):
        """ Initialize plot figures """
        self.signal_graph = Graphic(self.wTree.get_widget('vbox_signal'))
        self.filter_graph = Graphic(self.wTree.get_widget('vbox_filter'))
        self.fft_graph = Graphic(self.wTree.get_widget('vbox_fft'))
        self.ifft_graph = Graphic(self.wTree.get_widget('vbox_ifft'))
        self.ceps_graph = Graphic(self.wTree.get_widget('vbox_ceps'))
        self.spec_graph = Graphic(self.wTree.get_widget('vbox_spec'))
        
        self.signal_graph.axes.set_xlabel('Time [s]')
        self.signal_graph.axes.set_ylabel('Amplitude')
        self.signal_graph.axes.set_title('Audio signal')
        
        self.filter_graph.axes.set_xlabel('Frequency [Hz]')
        self.filter_graph.axes.set_ylabel('Amplitude')
        self.filter_graph.axes.set_title('Filter response')
        
        self.fft_graph.axes.set_xlabel('Frequency [Hz]')
        self.fft_graph.axes.set_ylabel('Amplitude')
        self.fft_graph.axes.set_title('Frequency response')
       
        self.ifft_graph.axes.set_title('Ifft')
        self.ifft_graph.axes.set_xlabel('Time [s]')
        self.ifft_graph.axes.set_ylabel('Amplitude')
        
        self.ceps_graph.axes.set_title('Cepstrum')
        self.ceps_graph.axes.set_xlabel('Time [s]')
        self.ceps_graph.axes.set_ylabel('Amplitude')
        
        self.spec_graph.axes.set_title('Power spectrum')
        self.spec_graph.axes.set_xlabel('Frequency [Hz]')
        self.spec_graph.axes.set_ylabel('Amplitude')

        
    def on_sigbox_destroy(self, widget):
    	"""" sigbox destroy """
        self.signal_graph.destroy()
        self.filter_graph.destroy()
        self.fft_graph.destroy()
        self.ifft_graph.destroy()
        self.ceps_graph.destroy()
        self.spec_graph.destroy()
    	gtk.main_quit ()

    def on_notebook_change_current_page(self, widget):
        print widget
        print "current changed"

    def on_notebook_select_page(self, widget):
        print widget
        print "select page"

    def on_notebook_switch_page(self, widget, data, page):
        # Remove current toolbar
        self.vbox_toolbar.remove(self.toolbar)
        # Add toolbar for selected page
        if page == 0:
            self.toolbar = NavigationToolbar(self.signal_graph.canvas, self.window)
            self.vbox_toolbar.pack_start(self.toolbar, False, False)
        elif page == 1:
            self.toolbar = NavigationToolbar(self.filter_graph.canvas, self.window)
            self.vbox_toolbar.pack_start(self.toolbar, False, False)
        elif page == 2:
            self.toolbar = NavigationToolbar(self.fft_graph.canvas, self.window)
            self.vbox_toolbar.pack_start(self.toolbar, False, False)
        elif page == 3:
            self.toolbar = NavigationToolbar(self.ifft_graph.canvas, self.window)
            self.vbox_toolbar.pack_start(self.toolbar, False, False)
        elif page == 4:
            self.toolbar = NavigationToolbar(self.ceps_graph.canvas, self.window)
            self.vbox_toolbar.pack_start(self.toolbar, False, False)
        elif page == 5:
            self.toolbar = NavigationToolbar(self.spec_graph.canvas, self.window)
            self.vbox_toolbar.pack_start(self.toolbar, False, False)


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

    def on_menu_signal_active(self, widget):
        """ Select signal view """
        self.notebook.set_current_page(0)
    
    def on_menu_filter_active(self, widget):
        """ Select filter view """
        self.notebook.set_current_page(1)

    def on_menu_freq_active(self, widget):
        """ Select frequency response view """
        self.notebook.set_current_page(2)

    def on_menu_ifft_active(self, widget):
        """ Select inverse fft response view """
        self.notebook.set_current_page(3)

    def on_menu_ceps_active(self, widget):
        """ Select cepstrum response view """
        self.notebook.set_current_page(4)

    def on_menu_spec_active(self, widget):
        """ Select power spectrum response view """
        self.notebook.set_current_page(5)
        

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
            self.file = self.dialog.file
            y, fs, bits = wavread(self.dialog.file)
            #Fs = 'Fs = %d' %(fs)
            self.fs = float(fs)
            time = len(y)/self.fs
            t = r_[0:time:1/self.fs]
            self.n = len(t)
        
            print 'segment n = %d' %(self.n)
            self.signal_graph.plot(t, y)
            self.signal_graph.axes.set_xlabel('Time [s]')
            self.signal_graph.axes.set_ylabel('Amplitude')
            self.signal_graph.axes.set_title('Audio signal')

            # Update user options
            self.config = Config()
            opt = self.config.getConfig('freq_opt')
            opt['seg_m'] = 0
            opt['seg_n'] = self.n
            opt['file'] = self.file
            self.config.updateConfig('freq_opt', opt)

            opt = self.config.getConfig('filter_opt')
            opt['fs'] = self.fs
            self.config.updateConfig('filter_opt', opt)

            # Save options
            self.config.writeConfig()
            self.config = None

            self.notebook.set_current_page(0)

        self.dialog = None
	
    def on_toolbutton_clear(self, widget):
    	""" Toolbutton clear clicked """ 
        self.file = None
        self.filter = None
        self.fs = None
        self.n = None
        self.signal_graph.clear_figure()
        self.filter_graph.clear_figure()
        self.fft_graph.clear_figure()
        self.ifft_graph.clear_figure()
        self.ceps_graph.clear_figure()
        self.spec_graph.clear_figure()

    def on_toolbutton_select(self, widget):
        """Toolbutton select clicked"""
        if self.notebook.get_current_page() == 0:
            toggled= widget.get_active()
            if toggled:
                if self.file:
                    self.signal_graph.enable_span()
            else:
                if self.file:
                    self.signal_graph.disable_span()
                    xmin = self.signal_graph.lx_min
                    xmax = self.signal_graph.lx_max
                    m = int(xmin * self.fs)
                    n = int(xmax * self.fs)
                    
                    # Update and save options
                    self.config = Config()
                    opt = self.config.getConfig('freq_opt')
                    opt['seg_m'] = m
                    opt['seg_n'] = n
                    self.config.updateConfig('freq_opt', opt)                    
                    self.config.writeConfig()
                    self.config = None

    def on_toolbutton_apply(self, widget):
        """ Toolbutton apply clicked """
        if self.file:
            # Get user options
            self.config = Config()
            opt = self.config.getConfig('freq_opt')
            
            b, a = self.filter

            filter_apply(b, a, options = opt, graph = self.filter_graph)

            self.filter_graph.axes.set_xlabel('Frequency [Hz]')
            self.filter_graph.axes.set_ylabel('Amplitude')
            self.filter_graph.axes.set_title('Freq response')
            
            self.notebook.set_current_page(1)

            self.filter = None


    def on_toolbutton_execute(self, widget):
    	""" Toolbutton exceute clicked """
        # Load user options
        self.config = Config()

        combobox = self.wTree.get_widget('combobox_exec')
        self.glob_opt['exec'] = combobox_get_active_item_text(combobox)

        if self.glob_opt['exec'] == 'FIR filter design':
            opt = self.config.getConfig('filter_opt')
            b = fir_design(options = opt)
            self.filter = [b, 1]
            filter_response(b, 1, graph = self.filter_graph, fs = opt['fs']) 
            self.filter_graph.axes.set_xlabel('Frequency [Hz]')
            self.filter_graph.axes.set_ylabel('Amplitude')
            self.filter_graph.axes.set_title('FIR response')
            self.notebook.set_current_page(1)
        elif self.glob_opt['exec'] == 'IIR filter design':
            opt = self.config.getConfig('filter_opt')
            b, a = iir_design(options = opt)
            self.filter = [b, a]
            filter_response(b, a, graph = self.filter_graph, fs = opt['fs'])            
            self.filter_graph.axes.set_xlabel('Frequency [Hz]')
            self.filter_graph.axes.set_ylabel('Amplitude')
            self.filter_graph.axes.set_title('IIR response')
            self.notebook.set_current_page(1)
        elif self.glob_opt['exec'] == 'Frecuency response':
            # Get user options
            options = self.config.getConfig('freq_opt')
            # fft and ifft
            fft_sig(options, graph_fft = self.fft_graph, graph_ifft = self.ifft_graph)
            self.fft_graph.axes.set_xlabel('Frequency [Hz]')
            self.fft_graph.axes.set_ylabel('Amplitude')
            self.fft_graph.axes.set_title('FFT')
            self.ifft_graph.axes.set_xlabel('Time [s]')
            self.ifft_graph.axes.set_ylabel('Amplitude')
            self.ifft_graph.axes.set_title('Inverse FFT')
            # Cesptrum
            cepstrum(options, graph_ceps = self.ceps_graph)
            self.ceps_graph.axes.set_xlabel('Time [s]')
            self.ceps_graph.axes.set_ylabel('Amplitude')
            self.ceps_graph.axes.set_title('Cepstrum')
            # Power spectrum
            power_spectrum(options, graph_spec = self.spec_graph)
            self.spec_graph.axes.set_xlabel('Frequency [Hz]')
            self.spec_graph.axes.set_ylabel('Amplitude')
            self.spec_graph.axes.set_title('Power spectrum')
            self.notebook.set_current_page(2)
        
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
	

#if __name__ == "__main__":
#	sys.exit(main(sys.argv))


