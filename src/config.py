#!/usr/bin/env python

import sys
import os

try:
    import yaml
except:
    print 'PyYaml library missing'
    sys.exit(1)

class Config:
    """Load user settings"""
    def __init__(self):
        self.config_file = 'config.yaml'

        try:
            # Load user config file
            self.config = yaml.load(open(self.config_file, 'r'))
        except IOError:
            # File missing create one
            self.config = {
                'glob_opt' : {
                    'exec' : 'FIR filter design'
                },
                'filter_opt' : {
                    'ftype' : 'Low pass',
                    'fs' : 44100,
                    'fc' : 300,
                    'fh' : 800,
                    'gain' : 1,
                    'order' : 30,
                    'win' : 'Hamming',
                    'iirftype' : 'Butterworth',
                },
                'freq_opt' : {
                    'file' : '../data/aaah.wav',
                    'seg_n' : 8192,
                    'seg_m' : 8192,
                    'rm_freqs' : 0,
                    'apply_win' : True,
                    'win' : 'hamming',
                    'apply_ifft' : True,
                    'linear' : True,
                    'log' : False,
                }
            }

            config_file_obj = open(self.config_file, "w")
            yaml.dump(self.config, config_file_obj, default_flow_style = False)
            config_file_obj.close()

        self.glob_opt = self.config.get('glob_opt', {})
        self.filter_opt = self.config.get('filter_opt', {})
        self.freq_opt = self.config.get('freq_opt',{})


    def writeConfig(self):
        """Write configuration file"""
        try:
            config = {
                'glob_opt' : self.glob_opt,
                'filter_opt' : self.filter_opt,
                'freq_opt' : self.freq_opt
            }
            config_file_obj = open(self.config_file, 'w')
            yaml.dump(config, config_file_obj, default_flow_style = False)
            config_file_obj.close()
            return True
        except yaml.YAMLError, exc:
            print 'Error in config file: ', exc
            return False
        except:
            print 'Error on saving file'
            return False


    def updateConfig(self, type='', options = {}):
        """Update config options"""
        if type == 'glob_opt':
            self.glob_opt = options
        elif type == 'filter_opt':
            self.filter_opt = options
        elif type == 'freq_opt':
            self.freq_opt = options
        else:
            return False

        return True


    def getConfig(self, type=''):
        """Get configuration options"""
        if type == 'glob_opt':
            return self.glob_opt
        elif type == 'filter_opt':
            return self.filter_opt
        elif type == 'freq_opt':
            return self.freq_opt
        else:
            return False

