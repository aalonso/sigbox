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
from common_utils import *
try:
    #from numpy import *
    from scipy.signal import *
    from scipy.fftpack import *
    from scipy import *
    from pylab import *
except:
	sys.exit(1)


def fft_sig(options = {}, graph_ifft = None, graph_fft = None):
    if options:  
        # Load wav file data
        y, fs, bits = wavread(options['file'])
        
        fs = float(fs)
        time = len(y)/fs        #Calculate total time 
        t = r_[0:time:1/fs]     #Create time vector
        N = len(y)
        print N
        n = options['seg_n']
        m = options['seg_m']
        
        if  m == n and n < N:           # Trunk vectors
            t = t[:n]
            y = y[:n]
        elif m < n and m < N:
            t = t[:m]
            y = y[:m]
            n = m
        else:
            n = N
        
        Y = fft(y, int(n))
        f = (fs/n)*r_[0:n]

        #xlabel('Time (sec)'); ylabel('Amplitude');     
        #title('Original signal'); plot(t, y)
        #savefig('../data/orig_sig.png')

        if options['apply_ifft'] == True:
            ys = ifft(Y)
            #graph_ifft.axes.clear()
            #graph_ifft.axes.grid(True)
            #graph_ifft.axes.axis([0,n,0,max(ys)])
            graph_ifft.axes.plot(t, ys)
            graph_ifft.axes.draw()

        #graph_fft.axes.clear()
        #graph_fft.axes.grid(True)

        if options['apply_win'] == True:
            win = hamming(int(n))            
            Yw = Y*win

            if options['linear'] == 'True':
                #graph_fft.axes.axis([0,n,0,max(abs(Yw))])
                graph_fft.axes.plot(f[int(n/2):], abs(Yw[int(n/2):]))
                #savefig('../data/fft_sig.png')
            else:
                #graph_fft.axes.axis([0,n,0,log(max(abs(Y)))])
                graph_fft.axes.semilogy(f[int(n/2):], abs(Yw[int(n/2):]))
                #savefig('../data/fft_sig.png')                        
        else:
            if options['linear'] == 'True':
                #graph_fft.axes.axis([0,n,0,max(abs(Y))])
                graph_fft.axes.plot(f[int(n/2):], abs(Y[int(n/2):]))
                #savefig('../data/fft_sig.png')
            else: 
                #graph_fft.axes.axis([0,n,0,log(max(abs(Y)))])
                graph_fft.axes.semilogy(f[int(n/2):], abs(Y[int(n/2):]))
                #savefig('../data/fft_sig.png')

        graph_fft.axes.draw()

        
def cepstrum(options = {}, graph_ceps = None):
    if options:
        # Load wav file data
        y, fs, bits = wavread(options['file'])
        
        fs = float(fs)
        #time = len(y)/fs        #Calculate total time 
        #t = r_[0:time:1/fs]     #Create time vector
        N = len(y)
        n = options['seg_n']
        m = options['seg_m']
        
        if  m == n and n < N:           # Trunk vectors
            y = y[:n]
        elif m < n and m < N:
            y = y[:m]
            n = m
        else:
            n = N
        
        Y = fft(y, int(n))
        f = (fs/n)*r_[0:n]
    
        Ys = real(ifft(log(abs(Y)))) 
        
        #graph_ceps.axes.clear()
        #graph_ceps.axes.grid(True)
         
        if options['linear'] == 'True':
            graph_ceps.axes.plot(f, Ys[0:n], 'r')
            #savefig('../data/ceps_sig.png')
        else:            
            graph_ceps.axes.semilogy(f, Ys[0:n], 'r')
            #savefig('../data/ceps_sig.png')

        graph_ceps.axes.draw()


#def impulse_response(t):
#    return (exp(-t) - exp(-5*t))*dt

