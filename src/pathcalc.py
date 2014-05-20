#!/usr/bin/env	python
#
#
#Copyright (C) 2000 Jim Richardson
#email	weaselkeeper@gmail.com
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
#	02111-1307, USA.
#
#This program is a simple calculator for some basic parabolic
#antenna equations. It's crude, but at least seems bug free. It
#makes a few assumptions, first that the numbers are all related
#to free space, so any atmospheric losses, including rain fade
#must be calculated seperately (I may add this at a future time)
#Second, it assumes that you know not to use dumb combinations of
#numbers, like a parabolic dish of 10cm, with a freq of 100Mhz.
#The numbers generated in such a combo are mathematically
#correct, and in practical terms, bogus.
#I also assume that both antennas are the same diameter, this
#will change in future revisions.
#
#Most of the calculations come from a GTE microwave journal
#that is over 30 years old :) Information is forever.
#
#Comments, bug notices, feature lists are welcome at
#weaselkeeper@gmail.com, please direct flames to /dev/null, I will...


# Reimplementation of pathcalc in python+tkinter

"""

License: GPL V2 See LICENSE file
Author: Jim Richardson
email: weaselkeeper@gmail.com

"""

PROJECTNAME = 'pathcalc'

import sys
import os
import ConfigParser
import Tkinter as Tk
import logging

# Setup logging
logging.basicConfig(level=logging.WARN,
                    format='%(asctime)s %(levelname)s - %(message)s',
                    datefmt='%y.%m.%d %H:%M:%S')

# Setup logging to console.
console = logging.StreamHandler(sys.stderr)
console.setLevel(logging.WARN)
logging.getLogger(PROJECTNAME).addHandler(console)
log = logging.getLogger(PROJECTNAME)


#set upper and lower limits for freq, path length etc
#

class PathCalc(object):
    """ Instantiate a path calc object """
    log.debug(' in class PathCalc')

    def __init__(self):
        """ Set some basic starting limits """
        self = read_config(self)
        self.title = 'Parapath Calculator'

    def run(self):
        """ Execute the run method """
        log.debug('In run()')
        self.drawCanvas()

    def drawSlider(self, window):
        Tk.Scale(window,
                label='Second slider',
                from_=0.1,
                to=10.0,
                resolution = 0.1,
                orient='horizontal',
                length=250,
                ).pack()


    def drawCanvas(self):
        """ Draw the canvas """
        log.debug(' in drawCanvas')
        root = Tk.Tk()
        var = Tk.StringVar()
        var.set(self.title)
        Tk.Label(root, textvariable=var).pack()
        self.drawSlider(root)
        Tk.Button(root, text="Quit", command=root.quit).pack()
        root.mainloop()

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

    # If we specify a config, then we use it, if not, we go with supplied options
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

    _object.min_freq = config.get('Default', 'FreqMin')
    _object.max_freq = config.get('Default', 'FreqMax')
    _object.min_dia = config.get('Default', 'DiaMin')
    _object.max_dia = config.get('Default', 'DiaMax')
    _object.min_path = config.get('Default', 'PathMin')
    _object.max_path = config.get('Default', 'PathMax')
    return _object

if __name__ == '__main__':
    # This is where we will begin when called from CLI. No need for argparse
    # unless being called interactively, so import it here, or at least, in
    # get_options
    args = get_options()

    if args.debug:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.WARN)

    canvas = PathCalc()
    canvas.run()
