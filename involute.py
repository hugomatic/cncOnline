#!/usr/bin/python

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
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
# You will find the latest version of this code at the following address:
# http://hugomatic.ca/source/cncOnline
#
# You can contact me at the following email address:
# hugo@hugomatic.ca
#


from math import *
import hugomatic.toolkit # UI and cmdline stuff
import hugomatic.code    # gcode routines

def take_a_break():
    """
    This function is called when the debug line is printed. Add a breakpoint here
    but don't call print, because the program will go into an infinite loop.
    """
    a = 42
    
########################################
# Program GUI
# 
# remember: 1 inch = 25.4 millimeters
                   
params = hugomatic.toolkit.Parameters('Involute', 
                                      'Involute curve', 
                                      picture_file="involute.gif",
                                      debug_callback=take_a_break)



gcodeUnits = 'Inches'  
params.addArgument( gcodeUnits, 'Program units... 1 inch = 25.4 millimeters', choices=('Inches', 'mm'), group='setup')
cut = 0.1
params.addArgument(cut , 'Cut per pass in units', group='setup')
feed = 4.0
params.addArgument(feed , 'Feed rate in units/min', group='setup')
zSafe = 0.2
params.addArgument(zSafe , 'Safe height above work piece', group='setup')
a=.1
params.addArgument(a , 'Scale factor')
angle = 100.
params.addArgument(angle , 'Angle')
steps = 2000
params.addArgument(steps , 'Number of steps')

#
# Generation
#
if params.loadParams():
    hugomatic.code.header(gcodeUnits, feed)
    #cuts = hugomatic.code.z_cut_compiler(zDepth, cut)

    print "G64 P0.001"
    print "G0 z%.4f" % zSafe
    print "F%.4f" % feed
    z = -cut
    for i in range(steps):
        t = i/angle
        x = a * (cos(t) + t * sin(t))
        y = a * (sin(t) - t * cos(t))
        if i == 0:
            print "G0 X%f Y%f" % (x,y)
            print "G01 Z%f" % z
        else:
            print "G01 X%f Y%f" % (x,y)
                  
    print "G0 z%.4f" % zSafe
    print hugomatic.code.footer()
