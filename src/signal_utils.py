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
from graphic import *
try:
    from numpy import zeros, linspace
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
        
        if m < n and n < N:
            t = t[m:n]
            y = y[m:n]
            n = n - m
        else:
            n = N
        

        Y = fft(y, n=int(n))
        f = (fs/n)*r_[0:n]
        #freq = linspace(0., fs/2, num=n/2)
        #times = linspace(0., float(n/fs), num=n)
        #xlabel('Time (sec)'); ylabel('Amplitude');     
        #title('Original signal'); plot(t, y)
        #savefig('../data/orig_sig.png')

        if options['apply_ifft'] == True:
            ys = ifft(Y, n = n)
            #graph_ifft.axes.clear()
            #graph_ifft.axes.grid(True)
            #graph_ifft.axes.axis([0,n,0,max(ys)])
            #graph_ifft.axes.plot(t, ys)
            #graph_ifft.axes.draw()
            graph_ifft.plot(t, ys[0:n])

        #graph_fft.axes.clear()
        #graph_fft.axes.grid(True)

        if options['apply_win'] == True:
            win = hamming(int(n))            
            Yw = Y*win

            if options['linear'] == 'True':
                #graph_fft.axes.axis([0,n,0,max(abs(Yw))])
                graph_fft.plot(f[0:int(n/2)], abs(Yw[0:int(n/2)]))
                #savefig('../data/fft_sig.png')
            else:
                #graph_fft.axes.axis([0,n,0,log(max(abs(Y)))])
                graph_fft.semilogy(f[0:int(n/2)], abs(Yw[0:int(n/2)]))
                #savefig('../data/fft_sig.png')                        
        else:
            if options['linear'] == 'True':
                #graph_fft.axes.axis([0,n,0,max(abs(Y))])
                graph_fft.plot(f[0:int(n/2)], abs(Y[0:int(n/2)]))
                #savefig('../data/fft_sig.png')
            else: 
                #graph_fft.axes.axis([0,n,0,log(max(abs(Y)))])
                graph_fft.semilogy(f[0:int(n/2)], abs(Y[0:int(n/2)]))
                #savefig('../data/fft_sig.png')

        #graph_fft.axes.draw()

        
def cepstrum(options = {}, graph_ceps = None):
    if options:
        # Load wav file data
        y, fs, bits = wavread(options['file'])
        
        fs = float(fs)
        time = len(y)/fs        #Calculate total time 
        t = r_[0:time:1/fs]     #Create time vector
        N = len(y)
        n = options['seg_n']
        m = options['seg_m']
        
        if  m < n and n < N:           # Trunk vectors
            t = t[m:n]
            y = y[m:n]
            n = n -m
        else:
            n = N
        
        Y = fft(y, n = int(n))
        #f = (fs/n)*r_[0:n]
    
        Ys = real(ifft(log(abs(Y)), n = int(n)))
         
        if options['linear'] == 'True':
            graph_ceps.plot(t[0:n], Ys[0:n])
            #savefig('../data/ceps_sig.png')
        else:            
            graph_ceps.semilogy(t[0:n], Ys[0:n])
            #savefig('../data/ceps_sig.png')

def power_spectrum(options = {}, graph_spec = None):
    if options:
        # Load wav file data
        y, fs, bits = wavread(options['file'])
        
        fs = float(fs)
        
        N = len(y)
        n = options['seg_n']
        m = options['seg_m']
        
        if  m < n and n < N:           # Trunk vectors
            y = y[m:n]
            n = n -m
        else:
            n = N
        
        if n%2:
            n = n - n%2
            y = y[0:n]

        graph_spec.power_spectrum(y,n,fs)
