#!/usr/bin/env python
import os
import sys
import optparse
try:
    import pygtk
    pygtk.require("2.0")
except:
    pass
try:
    import gtk
    import gtk.glade
except:
    sys.exit(1)

from sigbox import *
from about_dialog import *
from filter_dialog import *
from filter_design import *
from filechooser_dialog import *
from freqs_dialog import *
from common_utils import *
from signal_utils import *
from graphic import *
from matplotlib.backends.backend_gtkagg import NavigationToolbar2GTKAgg as NavigationToolbar

if __name__ == "__main__":
    sys.exit(main(sys.argv))

