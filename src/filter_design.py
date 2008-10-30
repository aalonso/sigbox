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

from fir2 import *
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

    #window = {
    #    'Hamming' : gr.firdes.WIN_HAMMING,
    #    'Black man' : gr.firdes.WIN_BLACKMAN,
    #    'Hanning' : gr.firdes.WIN_HANN,
    #    'Kaiser' : gr.firdes.WIN_KAISER,
    #    'Rectangular' : gr.firdes.WIN_RECTANGULAR,
    #}
    # Get window type
    #win = window[options['win']]

    # Create frequency vector
    fs = options['fs']
    #f = r_[0:(fs/2)]
    #n = len(f)
    #print n
    wp = (2*options['fc'])/fs

    if options['ftype'] == 'Low pass':
        if options['order'] == 0:
            #b = gr.firdes.low_pass (options['gain'], fs,        
            #                        options['fc'], 10, win)
            b = remez(options['order'], options['fc'], options['gain'])
        else:
            f = [0,wp,wp+0.1,1]
            a = [1,1,0,0]
            b = fir2(options['order'], f, a)
        return b
    elif options['ftype'] == 'Band pass':
        if options['order'] == 0:
            #b = gr.firdes.band_pass (options['gain'], fs,
            #                         options['fc'], options['fh'],
            #                         10, win)
            #wh = (2*options['fh'])/fs
            w = [options['fc'], options['fh']]
            b = remez(options['order'], w, options['gain'])
        else:
            wh = (2*options['fh'])/fs
            f = [0,wp,wh,1]
            a = [0,1,1,0]
            b = fir2(options['order'], options['fc'], options['gain'])
        return b
    elif options['ftype'] == 'Band reject':
        if options['order'] == 0:
            #b = gr.firdes.band_reject (options['gain'], fs,
            #                           options['fc'], options['fh'],
            #                           10, win)
            w = [options['fc'], options['fh']]
            b = remez(options['order'], w, options['gain'])
        else:
            wh = (2*options['fh'])/fs
            f = [0,wp,wh,1]
            a = [1,0,0,1]
            b = fir2(options['order'], f, a)
        return b
    elif options['ftype'] == 'High pass':
        if options['order'] == 0:
            #b = gr.firdes.high_pass (options['gain'], fs,        
            #                         options['fc'], 10, win)
            b = remez(options['order'], options['fc'], options['gain'])
        else:
            f = [0,wp-0.1,wp,1]
            a = [0,0,1,1]
            b = fir2(options['order'], f, a)
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
        if options['order'] == 0:
            #Minimal order filter
            ws = wp + 0.1
            b, a = iirdesign(wp, ws, gpass = 20, gstop = 1,
                            ftype = iirtype)
        else:
            b, a = iirfilter(options['order'], wp, btype = 'lowpass', ftype = iirtype)

        return (b, a)
    elif options['ftype'] == 'High pass':
        if options['order'] == 0:
            ws = wp - 0.1
            b, a = iirdesign(wp, ws, gpass = 30, gstop = 5,
                            ftype = iirtype)
        else:
            b, a = iirfilter(options['order'], wp, btype = 'highpass', ftype = iirtype)

        return (b, a)
    elif options['ftype'] == 'Band pass':
        wph = (2*options['fh'])/options['fs']
        Wp = [wp, wph]
        if options['order'] == 0:
            Ws = [(wp-0.1), (wph+0.1)]
            b, a = iirdesign(Wp, Ws, gpass = 1, gstop = 10,
                            ftype = iirtype)
        else:
            b, a = iirfilter(options['order'], Wp, btype = 'bandpass', ftype = iirtype)

        return (b, a)
    elif options['ftype'] == 'Band reject':
        wph = (2*options['fh'])/options['fs']
        Wp = [wp, wph]
        if options['order'] == 0:
            Ws = [(wp+0.1), (wph-0.1)]
            b, a = iirdesign(Wp, Ws, gpass = 30, gstop = 5,
                            ftype = iirtype)
        else:
            b, a = iirfilter(options['order'], Wp, btype = 'bandstop', ftype = iirtype)
        return (b, a)
        

def filter_response(b, a, n=512, graph = None):
    """ Generate filter response image
    """
    
    [w, h] = freqz(b, a, worN =n)
    #graph.axes.clear()
    #graph.axes.grid()
    graph.axes.semilogy(w/pi, abs(h))
    graph.axes.draw()
    
    #savefig('../data/fir_resp.png');


#if __name__ == '__main__':

    #options = {
    #    'gain' : 2020.0,
    #    'fs' : 44100.0,
    #    'fc' : 1200.0,
    #    'fh' : 1600.0,
    #    'win' : 'Hamming',
    #    'iirftype' : 'Kaiser',
    #    'ftype' : 'Low pass',
    #}

    #fir = fir_design(options=options)
    #[w, h] = freqz(fir)
    #print n
    #semilogy(w/pi, abs(h))
    #b, a = iir_design(options=options)
    #[w, h] = freqz(b, a)
    #semilogy(w/pi, abs(h))

    #show()
