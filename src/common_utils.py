#!/usr/bin/python
# -*- coding: UTF-8 -*-
#
# Copyright (C) 2006 by Hernán Ordiales <audiocode@uint8.com.ar>
# Copyright (C) 2008 by Adrian Alonso <aalonso00@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#

import sys
try:
	import wave
	import math
	import array
	from pylab import fromstring, clip
except:
	print 'libraries import error!'
	sys.exit()


# Note: at the moment only mono wav files

# Example: [ y, Fs, bits ] = wavread( 'filename' )
# Note: Only supports 8 and 16 bits wav files
def wavread( name ):
	file = wave.open( name, 'r' )
	[Channels,Bytes,Fs,Frames,Compress,CompressName] = file.getparams() # (nchannels, sampwidth in bytes, sampling frequency, nframes, comptype, compname)
	Data = file.readframes( Frames )
	Bits = Bytes*8 
	if Bits==16:  # 16 bits per sample
		Data = fromstring( Data, 'h' ) / 32767.0 # -1..1 values, Int16 because Bits=2x8=16
	elif Bits==8: # 8 bits per sample
		Data = (fromstring( Data, 'b' ) / 128.0 ) - 1.0 # -1..1 values
	else:
		print "Error. Sorry, this wavread function only supports 8 or 16 bits wav files."
		return -1, -1, -1
	file.close()
	#print "Fs: ",Fs,"\nBits: ",Bits,"\nChannels: ",Channels
	return Data, Fs, Bits

# Example: wavwrite( y, Fs, filename )
def wavwrite( data_array, Fs, name ):
	file = wave.open( name, 'w' )
	file.setframerate( Fs ) # sets sampling frequency
	file.setnchannels( 1 ) # sets number of channels
	file.setsampwidth( 2 ) # number of bytes: 16bits/8=2, 16 bits per sample

	clipped = False
	block_size = 1024*10 # write block size: 10k
	a_max = 32767 # max amp
	a_min = -32767 # min amp
	n = 0
	len_data_array = len( data_array ) # 2 bytes (int16) data
	while n < len_data_array :
		frame = '' # string frame of 'block_size'
		for i in range( block_size ) :
			if n < len_data_array :
				twodatabytes = int( data_array[n] * a_max )
				if twodatabytes > a_max or twodatabytes < a_min : clipped = True
				twodatabytes = min( max(twodatabytes,a_min), a_max ) # normalization, -32767..32767
				#twodatabytes.clip( min=a_min, max=a_max ) # normalization, -32767..32767
				frame += chr( twodatabytes & 0xFF ) # takes first byte, converts it to char and adds it to the frame
				frame += chr( (twodatabytes >> 8) & 0xFF ) # takes the second byte
				n += 1
		file.writeframes( frame )
	if clipped == True : print "Warning: Some values were clipped"
	print "Final length:", len_data_array/512,"kb" # n*2/1024 (bytes size/1024) = n/512
	file.close()

# Example: wavwrite8bits( y, Fs, filename )
def wavwrite8bits( data_array, Fs, name ):
	file = wave.open( name, 'w' )
	file.setframerate( Fs ) # sets sampling frequency
	file.setnchannels( 1 ) # sets number of channels
	file.setsampwidth( 1 ) # number of bytes, 8 bits per sample

	clipped = False
	block_size = 1024*10 # write block size: 10k
	a_max = 255 # max amp
	a_min = 0 # min amp
	n = 0
	len_data_array = len( data_array ) # 1 byte (UInt8) data
	while n < len_data_array :
		frame = '' # string frame of 'block_size'
		for i in range( block_size ) :
			if n < len_data_array :
				newbyte = int( (data_array[n]+1.0) * 128 ) # ~ 255/2
				if newbyte > a_max or newbyte < a_min : clipped = True
				newbyte = min( max(newbyte,a_min), a_max ) # normalization, 0..255
				#newbyte.clip( min=a_min, max=a_max ) # normalization, 0..255
				frame += chr( newbyte & 0xFF ) # takes the byte, converts it to char and adds it to the frame
				n += 1
		file.writeframes( frame )
	if clipped == True : print "Warning: Some values were clipped"
	#print "Final length:", len_data_array/512,"kb" # n*2/1024 (bytes size/1024) = n/512
	file.close()

def combobox_set_active_from_pattern(combobox, pattern):
    """Activate combobox item from string pattern"""
    model = combobox.get_model()
    iter = model.get_iter_first()
    for index in model:
        if index[0] == pattern:
            combobox.set_active_iter(iter)
            return
        iter = model.iter_next(iter)
    combobox.prepend_text(pattern)
    combobox_set_active_from_pattern(combobox, pattern)
 
 
def combobox_get_active_item_text(combobox):
    """Get ative combobox item string"""
    model = combobox.get_model()
    active = combobox.get_active()
 
    if active < 0:
        return None
    else:
        return model[active][0]

