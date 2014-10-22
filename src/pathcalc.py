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


# set up some default settings, use if no config presented.
defaults = {'dia': (0.1, 1), 'freq': (0.1, 10), 'path': (0.05, 10.0), 'lambda': (0, 50)}
print defaults


#set upper and lower limits for freq, path length etc
#

class PathCalc(object):
    """ Instantiate a path calc object """

    def __init__(self):
        """ Set some basic starting limits """
        self = read_config(self)
        self.title = 'Parapath Calculator'

    def run(self):
        """ Execute the run method """
        log.debug('In run()')
        # Draw the canvas
        root = Tk.Tk()
        var = Tk.StringVar()
        var.set(self.title)
        Tk.Label(root, textvariable=var).pack()
        for variable in self.settings:
            _min, _max = getattr(self, variable).split(',')
            slider = Tk.Scale(root, label=variable, from_=_min,
                              to=_max, resolution=0.1, orient='horizontal',
                              length=250, command=variable)
            slider.pack()

        Tk.Button(root, text="Quit", command=root.quit).pack()
        root.mainloop()

    def change_freq(self):
        """ when freq changes, recalculate all the stuff that changes as a
        result"""
        log.debug('in change_freq')
        log.warn('now recalc pathloss, paragain, 3dbTheta and lambda')
        self.paragain()
        self.threedb_theta()
        self.lambdaCalc()
        self. pathloss()

    def lambdaCalc(self):
        """ Calculating lambda (wavelength) """
        log.debug('in lambdaCalc')
        self._lambda = 300.00/self.freq
        print self._lambda

    def threedb_theta(self):
        """ Calculating the 3db theta point """
        log.debug('In threedb_theta')
        self.threedb_theta = 22.00/self.freq*self.para_dia

    def paraGain(self):
        """ Calculating the dish gain per side """
        log.debug('in paraGain calculation')
        self.para_gain = (20*math.log(10, self.dia)+(20*math.log(10, self.freq)+17.8))

    def pathloss(self):
        """ Calculate the full path loss """
        self.path_loss = (92.4+20*math.log(10, self.freq)+20*math.log(10, self.path_length))

    def pathgain(self):
        """ Calc total path gain """
        self.path_gain = self.path_loss + self.para_gain


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
