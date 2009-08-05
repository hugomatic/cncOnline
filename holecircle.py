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


import math
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
                   
params = hugomatic.toolkit.Parameters('Circular holes', 
                                      'Perform a uniform operation around a point', 
                                      picture_file="holecircle.gif",
                                      debug_callback=take_a_break)



gcodeUnits = 'Inches'  
params.addArgument( gcodeUnits, 'Program units... 1 inch = 25.4 millimeters', choices=('Inches', 'mm'), group='setup')

feed = 4.0
params.addArgument(feed , 'Feed rate in units/min', group="setup")
dwell = 0.1
params.addArgument(dwell , 'Dwell time or 0 for no dwell', group="setup")
zSafe = 0.2
params.addArgument(zSafe , 'Safe height above work piece', group="setup")
cut = 0.1
params.addArgument(cut , 'Cut per pass in units', group="setup")


zDepth = -0.25
params.addArgument(zDepth , 'Final depth (negative)')
centerX = 0.
params.addArgument(centerX, 'Circle center X')
centerY = 0.
params.addArgument(centerY, 'Circle center Y')
radius = 1.
params.addArgument(radius, 'Circle radius')
startAngle = 0.
params.addArgument(startAngle, 'Start Angle')
IncrementAngle = 15.
params.addArgument(IncrementAngle, 'Increment Angle (angle between operations)')
holeCount = 5
params.addArgument(holeCount, 'Hole count')


angle = 0.
x = 0.
y = 0.
z = 0.

#
# Generation
#
if params.loadParams():
    hugomatic.code.header(gcodeUnits, feed)
    cuts = hugomatic.code.z_cut_compiler(zDepth, cut)
    
    for i in range(holeCount):
        print "G0 z%.4f" % zSafe
        angle = startAngle + i * IncrementAngle
        rads = math.radians(angle)
        x = radius * math.cos(rads)
        y = radius * math.sin(rads)
        print
        print "(hole number %d)" % (i+1)        
        print "g0 x%(x).4f y%(y).4f" % globals()
        for currentZ in cuts:
            z = currentZ
            print "   G01 f%(feed)f z%(z)f" % globals()
            print "   G0 z0" 
    
    print    
    print hugomatic.code.footer()

