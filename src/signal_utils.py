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


def fft_sig(options = {}):
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

        print len(Y)
        print len(f)
        # plot abs(len(f/2))
        grid() 
        xlabel('Time (sec)'); ylabel('Amplitude');     
        title('Original signal'); plot(t, y)
        savefig('../data/orig_sig.png')

        if options['apply_ifft'] == True:
            ys = ifft(Y)
            grid() 
            xlabel('Time (sec)'); ylabel('Amplitud'); 
            title('Ifft'); plot(t, ys)
            savefig('../data/ifft_sig.png')

        if options['apply_win'] == True:
            win = hamming(int(n))            
            Yw = Y*win

            if options['linear'] == 'True':
                xlabel('Frecuency (hz)'); ylabel('Amplitude');
                title('Fft')
                grid(); plot(f[int(n/2):], abs(Yw[int(n/2):]))
                savefig('../data/fft_sig.png')
            else:
                xlabel('Frecuency (hz)'); ylabel('Amplitude');     
                title('Fft')
                grid(); semilogy(f[int(n/2):], abs(Yw[int(n/2):]))
                savefig('../data/fft_sig.png')                        
        else:
            if options['linear'] == 'True':
                xlabel('Frecuency (hz)'); ylabel('Amplitude');     
                title('Fft')
                grid(); plot(f[int(n/2):], abs(Y[int(n/2):]))
                savefig('../data/fft_sig.png')
            else: 
                xlabel('Frecuency (hz)'); ylabel('Amplitude');
                title('Fft')
                grid(); semilogy(f[int(n/2):], abs(Y[int(n/2):]))
                savefig('../data/fft_sig.png')
    else:
        x = r_[0:1:512j]
        h = hamming(512)
        theta = 2*pi*x
        y = 2*sin(10*theta) + 3*cos(20*theta) + sin(30*theta) + 2*cos(45*theta)
        ys = y*h
        F = fftfreq(1024)
        Ysw = fft(ys, 1024)
        Ys = fft(y, 1024)
        Ysnw = fftshift(abs(Ysw)/max(abs(Ysw)))
        Ysn = fftshift(abs(Ys)/max(abs(Ysw)))
        ysw = ifft(Ys, 1024)
        xs = r_[0:1:1024j]
        subplot(2,2,1); grid(); plot(x, y)
        subplot(2,2,2); grid(); plot(xs, ysw)
        subplot(2,2,3); grid(); plot(F,Ysnw)
        subplot(2,2,4); grid(); plot(F,Ysn)
        show()


def cepstrum(options = {}):
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
         
        if options['linear'] == 'True':
            xlabel('Frecuency (hz)'); ylabel('Amplitude');
            title('Cepstrum')
            grid(); plot(f, Ys[0:n], 'r')
            savefig('../data/ceps_sig.png')
        else:
            xlabel('Frecuency (hz)'); ylabel('Amplitude');
            title('Cesptrum')
            grid(); semilogy(f, Ys[0:n], 'r')
            savefig('../data/ceps_sig.png')



def iir_filter(self, options = {}):
	"""Create a IIR filter"""
	b, a = iirdesign(wp=fp, ws=fs, gpass=self.gpass, gstop=self.gstop, analog=0, ftype='butter', output='ba')
	self.iir_response(b, a, n=512)


def fir_filter(f, a, w, t):
    b = remez(17, bands=f, desired=a, weight=w, type=t)
    [w, h] = freqz(b)
    semilogy(w/pi, abs(h))
    #time = arange(17)
    #plot(time,h)
    show()


def filter(ftype='fir'):
	if ftype == 'fir':			
		b = firwin(n+1, 1/q, window='hamming')
		y = lfilter(b,1,x,axis=axis)

def fir_design2(options = {}):
    """Design FIR filter"""
    if options:
        #t = r_[0:10.0:0.01]
        fig = figure()
        ax1 = fig.add_subplot(211)

        #dt = 0.01
        #t = npy.arange(0.0, 10.0, dt)
        #t_length = len(t)

        # Normalize cutoff frecuency
        fc = (2*options['fc'])/options['fs']
        n = options['order'] + 1
        b = firwin(n, fc, window=options['win'])
        #t = arange(n)
        [w, h] = freqz(b)

        #num = [b]
        #den = [t]
        #s = lti(num, t)
        #(t, yout) = impluse(s)

        #r = impulse_response(t)*dt
        #T, h = ltisys.impulse([w, h])
        #subplot(2,1,1); grid(); semilogy(w/pi, abs(h))
        #subplot(2,1,2); grid(); plot(t, yout, '.')        
        title('Frequency response'); ax1.grid()
        ax1.set_ylabel('Amplitude')
        ax1.set_xlabel('Frequency')
        ax1.semilogy(w/pi, abs(h))
        show()

#def impulse_response(t):
#    return (exp(-t) - exp(-5*t))*dt

#def iir_response(self, b, a, n=512):
#	[w, h] = freqz(b,a,n)
#	plot(w/pi,abs(h))
#	grid(True)
#	show()

#def fir_response(f, a, fir_coef, n=512):
#	[w,h] = freqz(fir_coef, n)
#	plot(f,a,w/pi,abs(h))
#	grid()
#	show()

#if __name__ == "__main__":

	#sig_utils.iir_filter(0.3, 0.2)
    #f = array((0,0.1,0.15,0.5))
    #a = array((1.0,0.0))
    #w = array((100.0,1.0))
    #fir_filter(f, a, w, t='differentiator')
	#y = sig_utils.fft_sig(x,512)
	#plot(x)
	#show()

    #options = {
    #    'fs' : 44100.0,
    #    'fc' : 2050.0,
    #    'order' : 30,
    #    'win' : 'hamming',
    #}
    
    #fir_design(options)

    #options = {
    #    'fs' : 44100.0,
    #    'file' : '../data/aaah.wav',
    #    'm' : 8192,
    #    'n' : 8192,
    #    'win' : 'hamming',
    #    'plot' : 'lineal',
    #}

    #fft_sig(options)

