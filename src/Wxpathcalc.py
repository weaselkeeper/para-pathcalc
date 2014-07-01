#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
##
##Copyright (C) 2000 Jim Richardson
##email weaselkeeper@gmail.com
##
## This program is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License
## as published by the Free Software Foundation; either version 2
## of the License, or (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
##  02111-1307, USA.
##
##This program is a simple calculator for some basic parabolic
##antenna equations. It's crude, but at least seems bug free. It
##makes a few assumptions, first that the numbers are all related
##to free space, so any atmospheric losses, including rain fade
##must be calculated seperately (I may add this at a future time)
##Second, it assumes that you know not to use dumb combinations of
##numbers, like a parabolic dish of 10cm, with a freq of 100Mhz.
##The numbers generated in such a combo are mathematically
##correct, and in practical terms, bogus.
##I also assume that both antennas are the same diameter, this
##will change in future revisions.
##
##Most of the calculations come from a GTE microwave journal
##that is over 30 years old :) Information is forever.
##
##Comments, bug notices, feature lists are welcome at
##weaselkeeper@gmail.com, please direct flames to /dev/null, I will...
#


# Reimplementation of pathcalc in python+Wx
#
"""
License: GPL V2 See LICENSE file
Author: Jim Richardson
email: weaselkeeper@gmail.com
"""

PROJECTNAME = 'pathcalc'

# Import attempt, dif if fail.

try:
    import wx
except ImportError:
    raise ImportError, "The wxPython module is required to run this program"

# Remaining imports
import sys
import os
import ConfigParser
import logging
import math
# Setup logging
logging.basicConfig(level=logging.WARN,
                    format='%(asctime)s %(levelname)s - %(message)s',
                    datefmt='%y.%m.%d %H:%M:%S')

# Setup logging to console.
console = logging.StreamHandler(sys.stderr)
console.setLevel(logging.WARN)
logging.getLogger(PROJECTNAME).addHandler(console)
log = logging.getLogger(PROJECTNAME)


class pathcalc_wx(wx.Frame):
    """ Base class, builds the frame, and fills it out """
    def __init__(self, parent, id, title):
        """ Constructor for frame"""
        self = read_config(self)
        wx.Frame.__init__(self, parent, id, title)
        self.parent = parent
        self.initialize()

    def initialize(self):
        sizer = wx.GridBagSizer()
        self.Quit = wx.Button(self, id=-1, label=u"Quit")
        self.Quit.Bind(wx.EVT_BUTTON, self.QuitClick)
        self.Quit.SetToolTip(wx.ToolTip("Click to quit"))
        self.SetSizerAndFit(sizer)
        for variable in self.settings:
            # now we add sliders ..
            pass
        self.Show(True)

    def QuitClick(self, event):
        self.Close()


def get_options():
    """ Parse for any options """
    log.debug('in get_options')
    # Default config file
    import argparse
    parser = argparse.ArgumentParser(
        description='This is a Parabolic dish path calculator.')
    parser.add_argument('-f', '--file', action='store', default=None,
        help='Input file', dest='inputfile')
    parser.add_argument('-c', '--config', action='store', help='Config file')
    parser.add_argument('-d', '--debug', action='store_true',
        help='enable debugging')
    _args = parser.parse_args()
    _args.usage = PROJECTNAME + ".py [options]"

    # If we specify a config, then we use it, if not, we go with supplied
    # options
    log.debug('leaving get_options')
    return _args


def read_config(_object):
    """ We will now pass the config settings into the object """
    log.debug('In read_config')
    configfile = os.path.join('/etc', PROJECTNAME, PROJECTNAME + '.conf')
    config = ConfigParser.SafeConfigParser()
    if args.config:
        _config = args.config
        config.read(_config)
    else:
        if os.path.isfile(configfile):
            config.read(configfile)
        else:
            log.warn('No config file found, continue with args passed')
            sys.exit(1)

    items = config.options('sliders')
    _object.settings = items
    for item in items:
        value = config.get('sliders', item)
        setattr(_object, item, value)
    return _object


if __name__ == "__main__":
    args = get_options()

    if args.debug:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.WARN)
    app = wx.App()
    frame = pathcalc_wx(None, -1, 'pathcalc')
    app.MainLoop()
