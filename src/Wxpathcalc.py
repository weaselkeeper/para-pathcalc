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
# """
#
#License: GPL V2 See LICENSE file
#Author: Jim Richardson
#email: weaselkeeper@gmail.com


# Import attempt, dif if fail.

try:
    import wx
except ImportError:
    raise ImportError,"The wxPython module is required to run this program"

class pathcalc_wx(wx.Frame):
    def __init__(self,parent,id,title):
        """ Constructor for frame"""
        wx.Frame.__init__(self,parent,id,title)
        self.parent = parent
        self.initialize()

    def initialize(self):
        sizer = wx.GridBagSizer()
        self.Quit = wx.Button(self, id=-1,label=u"Quit")
        self.Quit.Bind(wx.EVT_BUTTON, self.QuitClick)
        self.Quit.SetToolTip(wx.ToolTip("Click to quit"))
        self.SetSizerAndFit(sizer)
        self.Show(True)

    def QuitClick(self, event):
            self.Close()
if __name__ == "__main__":
    app = wx.App()
    frame = pathcalc_wx(None,-1,'pathcalc')
    app.MainLoop()

