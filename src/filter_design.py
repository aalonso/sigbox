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
    #from gnuradio import gr
    from scipy.signal import *
    #from pylab import *
except:
    print 'libraries missing'
    sys.exit(1)

#from fir2 import *
from graphic import *
from common_utils import *

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

    _window = {
        'Black man' : 'blackman',
        'Box car' : 'boxcar',
        'Hamming' : 'hamming',
        'Hanning' : 'hanning',
        'Triangular' : 'triang',
    }
    # Get window type
    window = _window[options['win']]
    win = get_window(window, options['order'])
    # Create frequency vector
    fs = float(options['fs'])
    
    wp = (2*options['fc'])/fs 
    gain = 1
    #gain = 20*log10(options['gain'])

    if options['ftype'] == 'Low pass':
        f = [0,wp,wp+0.1,1]
        a = [1,1,0,0]
        b = remez(options['order'], f, a[::2], Hz = 2)
        #b = firwin(N = options['order'], cutoff = wp, window = window)
        return (b*win*gain)
    elif options['ftype'] == 'Band pass':
        wh = (2*options['fh'])/fs
        f = [0,wp-0.1,wp,wh,wh+0.1,1]
        a = [0,0,1,1,0,0]
        b = remez(options['order'], f, a[::2], Hz = 2)
        #b = fir2(options['order'], f, a)
        return (b*win*gain)
    elif options['ftype'] == 'Band reject':
        wh = (2*options['fh'])/fs
        f = [0,wp-0.1,wp,wh,wh+0.1,1]
        a = [1,1,0,0,1,1]
        b = remez(options['order'], f, a[::2], Hz = 2)
        #b = fir2(options['order'], f, a)
        return (b*win*gain)
    elif options['ftype'] == 'High pass':
        f = [0,wp-0.1,wp,1]
        a = [0,0,1,1]
        #b = fir2(options['order'], f, a)
        b = remez(options['order'], f, a[::2], Hz = 2)
        return (b*win*gain)
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
        'Bassel'      :  'bessel',
        'Butterworth' : 'butter',
        'Chebyshev 1' : 'cheby1',
        'Chebyshev 2' : 'cheby2',
        'Elliptic'    : 'ellip',
    }

    iirtype = _ftype[options['iirftype']]

    # Normalize cut off frecuencies
    wp = (2*options['fc'])/options['fs']
     
    if options['ftype'] == 'Low pass':
        b, a = iirfilter(options['order'], wp, btype = 'lowpass', ftype = iirtype)
        return (b, a)
    elif options['ftype'] == 'High pass':
        b, a = iirfilter(options['order'], wp, btype = 'highpass', ftype = iirtype)
        return (b, a)
    elif options['ftype'] == 'Band pass':
        wph = (2*options['fh'])/options['fs']
        Wp = [wp, wph]
        b, a = iirfilter(options['order'], Wp, btype = 'bandpass', ftype = iirtype)
        return (b, a)
    elif options['ftype'] == 'Band reject':
        wph = (2*options['fh'])/options['fs']
        Wp = [wp, wph]
        b, a = iirfilter(options['order'], Wp, btype = 'bandstop', ftype = iirtype)
        return (b, a)
    else:
        return None
        

def filter_response(b, a, n=512, graph = None, fs = 1):
    """ Generate filter response image
    """
    
    [w, h] = freqz(b, a, worN = n)
    n = len(h)
    f = (fs/(2*n))*r_[0:n]

    if fs == 1:
        graph.plot(w/pi, abs(h))
    else:
        graph.semilogy(f, abs(h))
        #graph.plot(f, 20.0*log10(abs(h)))
    
    #savefig('../data/fir_resp.png');


def filter_apply(b, a, graph = None, options = {}):
    # Apply filter
    
    if graph and options:
        y, fs, bits = wavread(options['file'])

        fs = float(fs)
        time = len(y)/fs        #Calculate total time 
        t = r_[0:time:1/fs]     #Create time vector
        
        N = len(y)

        n = options['seg_n']
        m = options['seg_m']
     
        if m < n and n < N:
            y = y[m:n]
            t = t[m:n]
            n = n - m
        else:
            n = N
        #r = lfilter(b, a, y)
        #r = convolve(b, y)
        r = correlate(b, y)

        Y = fft(r, n = int(n))
        f = (fs/n)*r_[0:n]

        graph.plot(f[0:int(n/2)], Y[0:int(n/2)])
        #graph.semilogy(t, r[0:n])



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
