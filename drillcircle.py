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
# g81 g83 contributed by Michael Haberler
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
                   
params = hugomatic.toolkit.Parameters('Drill Circular holes', 
                                      'Perform a uniform drill holes around a point using the drilling code g81. If the hole depth is greater than twice the drill diameter,  g83 (drill pecking) is used instead.', 
                                      picture_file="holecircle.gif",
                                      debug_callback=take_a_break)



gcodeUnits = 'mm'  
params.addArgument( gcodeUnits, 'Program units... 1 inch = 25.4 millimeters', choices=('Inches', 'mm'), group='setup')

feed = 100
params.addArgument(feed , 'Feed rate in units/min', group="setup")
dwell = 0.1
params.addArgument(dwell , 'Dwell time or 0 for no dwell', group="setup")
zSafe = 5
params.addArgument(zSafe , 'Safe height above work piece', group="setup")
drillDiameter = 3
params.addArgument(drillDiameter , 'Drill diameter', group="setup")


zDepth = -2
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
holeCount = 6
params.addArgument(holeCount, 'Hole count')


angle = 0.
x = 0.
y = 0.
z = 0.


# if drill depth > maxvertical, switch to G83 peck cycle
maxvertical = drillDiameter * 2.0
# retract to drillDiamater above piece every maxvertical feeds
retractlevel = drillDiameter
#
# Generation
#
if params.loadParams():
    hugomatic.code.header(gcodeUnits, feed)
    
    for i in range(holeCount):
        print "G0 z%.4f" % zSafe
        angle = startAngle + i * IncrementAngle
        rads = math.radians(angle)
        x = radius * math.cos(rads)
        y = radius * math.sin(rads)
        print
        print "(hole number %d)" % (i+1)        
        # use peck drilling if depth > 2 times drill diameter
        if math.fabs(zDepth) > maxvertical:
            print "g83 x%(x).4f y%(y).4f z%(zDepth).4f q%(maxvertical).4f r%(retractlevel).4f" % globals()
        else:
            print "g81 x%(x).4f y%(y).4f z%(zDepth).4f" % globals()
    
    print    
    print hugomatic.code.footer()

