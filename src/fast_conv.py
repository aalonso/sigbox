#!/usr/bin/python
# -*- coding: UTF-8 -*-

#
# Copyright (C) 2006 by Hernán Ordiales
# <audiocode@uint8.com.ar>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#

# Convolución rápida de una señal de audio con la respuesta impulsiva de algún sistema modelado como LTI
# Uso: fast_conv.py archivo_a_procesar.wav respuesta_al_impulso.wav archivo_de_salida.wav

from wav_utils import *
from FFT import fft, inverse_fft
from pylab import size
import sys

def nextpow2( L ):
	N = 2
	while N < L: N = N * 2
	return N
	
def fast_conv_vect( x, h ):
	# busca la cantidad de puntos que debo utilizar para realizar la FFT
	L = size(h) + size(x) - 1 # el tamaño de la convolución lineal
	N = nextpow2( L )
	# Nota: se pide N>=L ya que la IDFT de la multiplicacion es la convolución circular y para que esta
	# equivalga a la tradicional se debe pedir N>=L (donde L=N1+N2-1;N1=longitud(x);N2=longitud(h))
	
	# FFT(X,N) es la FFT de N puntos, rellenada con ceros si X tiene más de N puntos y truncada si tiene demás.
	H = fft( h, N ) # transformada de Fourier del impulso
	X = fft( x, N ) # transformada de Fourier de la señal de entrada
	
	Y = H * X # multiplicación de espectros
	y = inverse_fft( Y ) # se vuelve al dominio del tiempo
	return y

archivo = sys.argv[1]
impulso = sys.argv[2]
salida = sys.argv[3]

clip_factor = 1.01 # valor por defecto

[ h1, Fs1, h_bits ] = wavread( impulso ) # respuesta impulsiva:
[ x1, Fs2, x_bits ] = wavread( archivo ) # archivo a procesar:

if Fs1 == Fs2 : # si las frecuencias de muestreo coinciden

	print "Procesando..."
	y1 = fast_conv_vect( x1, h1 ).real 	# se queda con la parte real porque quedan factores complejos muy pequeños (despreciables), tipo e-18: TypeError: no ordering relation is defined for complex numbers

	# normalización del audio:	si "y = y/max(y)" -> "los valores fuera del rango [-1,+1] son recortados"
	y1 = y1/( max(y1)*clip_factor ) # para que no "clipee"
	
	wavwrite( y1, Fs1, salida )

	print "Archivo de salida:", salida
	print "Convolución realizada con éxito. Fin."
	
else:
	
	print "Error: los archivos no tienen la misma frecuencia de muestreo. No se puede realizar la convolución."
