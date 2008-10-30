# Code by "tash" from Scipy ticket 457
# http://projects.scipy.org/scipy/scipy/attachment/ticket/457/fir2.py
# Includes from filter_design.py
import numpy
from numpy.core.umath import *
from numpy import atleast_1d, poly, polyval, roots, imag, real, asarray,\
     allclose, resize, pi, concatenate, absolute, logspace
from numpy import mintypecode, select
from scipy import special, optimize, linalg
from scipy.misc import comb
import string, types

def fir2(n, f, a, ntp=512, window='hamming', nyq=1.):
    """
    FIR Filter Design using inverse fft method.

    Inputs:
      n      -- order of filter (number of taps)
      f      -- frequency sampling points. Typically 0.0 to 1.0 with
                1.0 being nyquist. Nyquest can be redefined via nyq
      a      -- amplitude at frequency sampling points
      ntp    -- FFT size - Default is 512 points
      window -- Window function to use. Default is Hamming
      nyq    -- Frequency for nyquist. Default is 1.0
    """
    from scipy.signal.signaltools import get_window
    from scipy.fftpack import ifft

    # Handle input checking
    nyq = float(nyq)
    if (len(f) != len(a)):
        print 'f and a must be of same length!'
        return numpy.array([])

    # Create window to apply to final filter
    wind = get_window(window,n,fftbins=0)

    # Create a series of equally spaced frequencies and linearly interpolate
    #   amplitude from input 'a'. This will the frequency spaced used for the
    #   ifft
    x = numpy.linspace(0.0, nyq, ntp+1)
    fx = numpy.array(numpy.interp(x, f, a))

    # This uses the Fourier Time Shift to properly align the coefficients in post-ifft
    #   array. See http://www.engineering.usu.edu/classes/ece/3640/lecture5/node6.html
    #   and check under Time Shift Property for description of Fourier Time Shift
    shift = exp(-(n-1)/2.*1.j*pi*numpy.arange(len(fx))/(len(fx)-1))
    fx2 = fx * shift

    # Up until this point, we've been working 0 <= theta <= pi. Must fill in pi < theta < 2pi.
    #  to allow the ifft to work properly.     
    fx3 = concatenate( (fx2, conjugate(fx2[::-1][1:len(fx2)-1])) )

    # Perform ifft and take real portion
    out = real(ifft(fx3))

    # Multiply by window and return
    out = out[0:n]*wind
    return out
