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

from disutils.core import setup

setup ( name = 'Sigbox',
        version = '0.0.1',
        author = 'Adrian Alonso',
        author_email = 'aalonso00@gmail.com',
        url = 'http://aalonso.wordpress.com',
        download_url = 'git://github.com/aalonso/sigbox.git'
        description = 'A simple tool for digital filter design',
        packages = ['sigbox'],
        py_modules = [  'src/about_dialog',
                        'src/common_utils',
                        'src/config',
                        'src/fast_conv',
                        'src/filechooser_dialog',
                        'src/filter_design',
                        'src/filter_dialog',
                        'src/freqs_dialog',
                        'src/graphic',
                        'src/sigbox',
                        'src/signal_utils'
                        ]
        data_files = [  ('lib/sigbox', ['data/sigbox.glade']),
                        ('lib/sigbox', ['src/config.yaml']),
                        ('share/sigbox'), ['data/aaah.wav']),
                        ('share/doc/sigbox', ['doc/sigbox.odp'])
                        ]
        )
        
