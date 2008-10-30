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
    from gnuradio import gr
    from scipy.signal import *
    from pylab import *
except:
    print 'libraries missing'
    sys.exit(1)

from graphic import *

def fir_design(options = {}):
    """ Fir design wrapper for gnuradio firdes funtion
        Parameters:
            type
                    low_pass
                    band_pass
                    band_reject
                    high_pass
            options
                gain : Filter gain
                fs   : Sampling frecuency
                fc   : Cut off frequency
                fh   : High cut off frequency
                win  : Window type
    """

    window = {
        'Hamming' : gr.firdes.WIN_HAMMING,
        'Black man' : gr.firdes.WIN_BLACKMAN,
        'Hanning' : gr.firdes.WIN_HANN,
        'Kaiser' : gr.firdes.WIN_KAISER,
        'Rectangular' : gr.firdes.WIN_RECTANGULAR,
    }
    # Get window type
    win = window[options['win']]

    # Create frequency vector
    fs = options['fs']
    #f = r_[0:(fs/2)]
    #n = len(f)
    #print n

    if options['ftype'] == 'Low pass':
        b = gr.firdes.low_pass (options['gain'], fs,        
                                   options['fc'], 10, win)
        return b
    elif options['ftype'] == 'Band pass':
        b = gr.firdes.band_pass (options['gain'], fs,
                                   options['fc'], options['fh'],
                                   10, win)
        return b
    elif options['ftype'] == 'Band reject':
        b = gr.firdes.band_reject (options['gain'], fs,
                                     options['fc'], options['fh'],
                                     10, win)
        return b
    elif options['ftype'] == 'High pass':
        b = gr.firdes.high_pass (options['gain'], fs,        
                                   options['fc'], 10, win)
        return b
    else:
        return None


def iir_design(options = {}):
    """IIR design wrapper for iirdesign fuction from scipy.signals
        
        Parameters:
            type
                    low_pass
                    band_pass
                    band_reject
                    high_pass
            options
                gain : Filter gain
                fs   : Sampling frecuency
                fc   : Cut off frequency
                fh   : High cut off frequency
        
    """ 
    _ftype = {
        'Bassel' : 'bessel',
        'Butterworth' : 'butter',
        'Chebyshev 1' : 'cheby1',
        'Chebyshev 2' : 'cheby2',
        'Elliptic' : 'ellip',
    }

    iirtype = _ftype[options['iirftype']]

    # Normalize cut off frecuencies
    wp = (2*options['fc'])/options['fs']
    
    if options['ftype'] == 'Low pass':
        #ws = wp + 0.1
        #b, a = iirdesign(wp, ws, gpass = 30, gstop = 1,
        #                ftype = iirtype)
        b, a = iirfilter(30, wp, btype = 'lowpass', ftype = iirtype)
        return (b, a)
    elif options['ftype'] == 'High pass':
        #ws = wp - 0.1
        #b, a = iirdesign(wp, ws, gpass = 30, gstop = 5,
        #                ftype = iirtype)
        b, a = iirfilter(30, wp, btype = 'highpass', ftype = iirtype)
        return (b, a)
    elif options['ftype'] == 'Band pass':
        wph = (2*options['fh'])/options['fs']
        Wp = [wp, wph]
        #Ws = [(wp-0.1), (wph+0.1)]
        #b, a = iirdesign(Wp, Ws, gpass = 1, gstop = 10,
        #                ftype = iirtype)
        b, a = iirfilter(30, Wp, btype = 'bandpass', ftype = iirtype)
        return (b, a)
    elif options['ftype'] == 'Band reject':
        wph = (2*options['fh'])/options['fs']
        Wp = [wp, wph]
        #Ws = [(wp+0.1), (wph-0.1)]
        #b, a = iirdesign(Wp, Ws, gpass = 30, gstop = 5,
        #                ftype = iirtype)
        b, a = iirfilter(30, Wp, btype = 'bandstop', ftype = iirtype)
        return (b, a)
        

def filter_response(b, a, n=512, graph = None):
    """ Generate filter response image
    """
    
    [w, h] = freqz(b, a, worN =n)

    if graph:
        graph.axes.set_title('Frequency Response')
        graph.axes.set_xlabel('f(Hz)')
        graph.axes.set_ylabel('Amplitude')
        graph.axes.plot(w/pi, abs(h))
    else:
        semilogy(w/pi, abs(h))
        title('Frequency response')    
        xlabel('Frequency')
        ylabel('Amplitude')
        savefig('../data/fir_resp.png');


if __name__ == '__main__':

    options = {
        'gain' : 2020.0,
        'fs' : 44100.0,
        'fc' : 1200.0,
        'fh' : 1600.0,
        'win' : 'Hamming',
        'iirftype' : 'Kaiser',
        'ftype' : 'Low pass',
    }

    fir = fir_design(options=options)
    [w, h] = freqz(fir)
    #print n
    semilogy(w/pi, abs(h))
    #b, a = iir_design(options=options)
    #[w, h] = freqz(b, a)
    #semilogy(w/pi, abs(h))

    show()
