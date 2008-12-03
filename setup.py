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

from distutils.core import setup

setup ( name = 'sigbox',
        version = '0.0.1',
        author = 'Adrian Alonso',
        author_email = 'aalonso00@gmail.com',
        url = 'http://aalonso.wordpress.com',
        license = "GPLv2",
        plataforms = ['any'],
        download_url = 'git://github.com/aalonso/sigbox.git',
        description = 'A simple tool for digital filter design',
        package_dir = {'sigbox': 'src'},
        packages = ['sigbox'],
        #package_data = {'sigbox': ['data/sigbox.glade']},
        #py_modules = [  'about_dialog',
        #                'common_utils',
        #                'config',
        #                'filechooser_dialog',
        #                'filter_design',
        #                'filter_dialog',
        #                'fir2',
        #                'freqs_dialog',
        #                'graphic',
        #                'sigbox',
        #                'signal_utils',
        #                ],
        data_files = [  ('lib/sigbox', ['data/sigbox.glade', 'src/config.yaml']),
                        ('share/sigbox', ['data/aaah.wav']),
                        ],
        )
        
