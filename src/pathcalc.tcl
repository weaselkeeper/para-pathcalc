#!/usr/bin/env	wish
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


# ChangeLog
# Revision 0.0.4:   
#   Changed step size of various variable to be equal to
# the variable minimum. 
# Revision 0.0.3: 
#   Bugfree, narrowed the limits to make more useful
# in the low GHz bands (<10GHz)
#
# Revision 0.0.2:
#   Bugfree, simple, first public release
#


set VERSION 0.04

wm title  . "Parabolic Path Calculator. Rev. $VERSION"
. config -bd 2


#set upper and lower limits for freq, path length etc
#

set min_freq 0.1	;#100 MHz
set max_freq 10		;#10 GHz

set min_path 0.05	;#50 m
set max_path 10		;#10 Km

set min_dia .1		;#10 cm
set max_dia 1.2		;#1.2 m

#Set some defaults
#Units are metric

set path_length 2
set para_dia .5
set freq 2.5
set fresnel 50

#temps
set z1 [expr 2*2]
set n_zone 0
set para_gain 1
set path_loss 1

#frame for sliders

frame .main -width 400 -height 200 -bd 10
label .main.welcome -text "Welcome"
scale .main.fresnel -orient horiz -from 0 -to 50 \
	-resolution .5 -variable $fresnel \
	-label "Fresnel spot  % " -command {change_fresnel}

pack .main
foreach widgets  {fresnel} {
pack .main.$widgets -side top
}

#Frame for path
global min_path max_path path_length
frame .path -width 400 -height 20 -bd 10
label .path.label -text "Path in Km"
scale .path.pathlength -orient horiz -from $min_path -to $max_path\
	-resolution $min_path -variable $path_length \
	-label "Path Km" -command {dist_change}
button .path.min_path_minus -text "-" -command {min_path 0.5}
button .path.min_path_plus -text "+" -command {min_path 2 }
button .path.max_path_minus -text "-" -command {max_path 0.5}
button .path.max_path_plus -text "+" -command {max_path 2 }
pack .path
foreach widgets {min_path_minus min_path_plus pathlength max_path_minus max_path_plus} {
pack .path.$widgets -side left
}

#frame for dish diameter
global min_dia max_dia
frame .dish -width 400 -height 20 -bd 10
label .dish.label -text "Dia"
scale .dish.dia -orient horiz -from  $min_dia -to $max_dia \
	-resolution $min_dia -variable $para_dia \
	-label "Dish Dia. m" -command {dia_change}
button .dish.min_dia_minus -text "-" -command {min_dia 0.5}
button .dish.min_dia_plus -text "+" -command {min_dia 2 }
button .dish.max_dia_minus -text "-" -command {max_dia 0.5}
button .dish.max_dia_plus -text "+" -command {max_dia 2 }
pack .dish
foreach widgets {min_dia_minus min_dia_plus dia max_dia_minus max_dia_plus} {
pack .dish.$widgets -side left
}

#frame for freq
global min_freq max_freq freq
frame .freq -width 400 -height 20 -bd 10
label .freq.freek -text "freq"
scale .freq.freq -orient horiz -from $min_freq -to $max_freq \
	-resolution 0.1 -variable $freq \
	-label "Frequency  GHz" -command {freq_change}
button .freq.min_freq_minus -text "-" -command {min_freq 0.5}
button .freq.min_freq_plus -text "+" -command {min_freq 2 }
button .freq.max_freq_minus -text "-" -command {max_freq 0.5}
button .freq.max_freq_plus -text "+" -command {max_freq 2 }
pack .freq
foreach widgets {min_freq_minus min_freq_plus freq max_freq_minus max_freq_plus} {
pack .freq.$widgets -side left
}
pack info .freq
frame .results
frame .results.labels
frame .results.values
pack .results
pack .results.labels -side left
  label .results.labels.para_gain -text "Para Gain (db)"
  label .results.labels.loss  -text "Path Loss (db)" 
  label .results.labels.f_zone -text "Fresnel Zone (m)"
  label .results.labels.n_zone -text "Near Zone (m)"
  label .results.labels.total_path_att -text "Total Path Gain (db)"
  label .results.labels.theta -text "3db Beamwidth (theta)"
  label .results.labels.lambda -text "lamdba(mm)"
foreach titles {f_zone n_zone para_gain loss total_path_att theta lambda } {
pack .results.labels.$titles
	}



frame .system -width 400 -height 20 -bd 10
button .system.quit -text "quit" -command exit
pack .system
foreach widget {quit} { pack .system.$widget -side bottom }



pack .results.values -side right
	label .results.values.para_gain -width 10 \
		-relief groove -textvariable para_gain

	label .results.values.loss -width 10 \
		-relief groove -textvariable path_loss

	label .results.values.f_zone -width 10 \
		-relief groove -textvariable z1
	
	label .results.values.n_zone -width 10 \
		-relief groove -textvariable n_zone
	
	label .results.values.total_path_att -width 10 \
		-relief groove -textvariable path_att

	label .results.values.theta -width 10 \
		-relief groove -textvariable theta

	label .results.values.lambda -width 10 \
		-relief groove -textvariable lambda

foreach values { f_zone n_zone para_gain loss total_path_att theta lambda } {
pack .results.values.$values -side top

	}


# Changing variables here
proc min_freq {adjust} {
	global min_freq
	set min_freq [expr $min_freq * $adjust ]
	.freq.freq configure -from $min_freq
	}

proc max_freq {adjust} {
	global max_freq
	set max_freq [expr $max_freq * $adjust ]
	.freq.freq configure -to $max_freq
	}

proc min_dia {adjust} {
	global min_dia
	set min_dia [expr $min_dia * $adjust ]
	.dish.dia configure -from $min_dia
	}

proc max_dia {adjust} {
	global max_dia
	set max_dia [expr $max_dia * $adjust ]
	.dish.dia configure -to $max_dia
	}

proc min_path {adjust} {
	global min_path
	set min_path [expr $min_path * $adjust ]
	.path.pathlength configure -from $min_path
	}

proc max_path {adjust} {
	global max_path
	set max_path [expr $max_path * $adjust ]
	.path.pathlength configure -to $max_path
	}


#Calculations begin here
#
proc pathloss {} {
	global path_length path_loss freq
	set path_loss -[format %2.2f \
		[expr (92.4+20*log10($freq)+20*log10($path_length))]]
	total_path_att
	}
proc total_path_att {} {
	global dia  para_gain path_loss path_att
	set path_att  [format %2.2f [expr ($para_gain*2)+$path_loss]]

	}
proc near_zone {} {
	global n_zone freq para_dia
	set n_zone [format %2.2f [expr (6.6*$freq*(pow($para_dia,2)))]]
	}

proc parabolic_gain {} {
	global para_gain para_dia freq
	set para_gain [format %2.2f \
		[expr (20*log10($para_dia)+20*log10($freq)+17.8)]]
	total_path_att
	}

proc fresnel_zone1 {} {
	global n_zone z1 freq  path_length f_zone
	set d1 [expr $path_length*$f_zone/100]
	set d2 [expr $path_length-$d1]
	set z1 [format %2.2f \
		[expr 17.3*sqrt(($d1*$d2)/($freq*$path_length))]]
	}

proc 3db_theta {} {
	global freq para_dia theta
	set theta [format %2.2f [expr 22/($freq*$para_dia)]]
	}

proc lambda {} {
	global freq lambda
	set lambda [format %2.2f [expr (300/$freq)]]
	}

#######################################33

proc dia_change {new_dia} { 
	#recalc all the parameters that are affected by 
	#change in parabolic diameter eg parabolic gain 
	#and near zone, also total path gain via parabolic gain
	
	global freq para_dia n_zone para_gain
	set para_dia $new_dia
	near_zone
	parabolic_gain 
	3db_theta
	}

proc freq_change {new_freq} {
	#Recalc all the paramaters which are affected by 
	#changes in the freq  eg all of them
	global freq
	set freq $new_freq
	near_zone 
	parabolic_gain 
	pathloss
	fresnel_zone1
	3db_theta
	lambda
	}

proc dist_change {new_length} {

	global path_length
	set path_length $new_length
	pathloss 
	fresnel_zone1
	}


proc change_fresnel {d1} {
	global f_zone
	set f_zone $d1
	fresnel_zone1
	}


