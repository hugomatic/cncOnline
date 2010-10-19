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
# hugo
#
# Thanks to Michael Haberler for his g81 g83 contribution
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
                                      'Perform a uniform drill holes around a point using the drilling code g81 or g83.',
                                      picture_file="holecircle.gif",
                                      debug_callback=take_a_break)



units = 'mm'
params.addArgument( units, 'Program units... 1 inch = 25.4 millimeters', choices=('Inches', 'mm'), group='setup')
drill_diameter = 3.
params.addArgument(drill_diameter , 'Drill diameter', group="setup")
feed = 100.
params.addArgument(feed , 'Feed rate in units/min', group="setup")


z_safe = 5.
params.addArgument(z_safe , 'Safe height above work piece', group="height")
z_rapid = 1.5
params.addArgument(z_rapid , 'Rapid plane right above work piece where rapid movement stops', group="height")
z_depth = -2.
params.addArgument(z_depth , 'Final depth (along Z, negative)', group = 'height')

pecking = True
params.addArgument(pecking , 'Use pecking (multiple up and down to clean the drill flutes)', group = 'peck')
peck = 6.0
params.addArgument(peck , 'Peck height (positive) for each drill cut', group="peck")

center_x = 0.
params.addArgument(center_x, 'Circle center X')
center_y = 0.
params.addArgument(center_y, 'Circle center Y')
radius = 1.
params.addArgument(radius, 'Circle radius')
start_angle = 0.
params.addArgument(start_angle, 'Start Angle')
increment_angle = 15.
params.addArgument(increment_angle, 'Increment Angle (angle between operations)')
hole_count = 6
params.addArgument(hole_count, 'Hole count')
dwell = 0.1
params.addArgument(dwell , 'Dwell (pause) time before xy movement or 0 for no dwell')


angle = 0.
x = 0.
y = 0.
z = 0.



# retract to z_rapid above piece every peck feeds

#
# Generation
#
if params.loadParams():
    hugomatic.code.header(units, feed)

    for i in range(hole_count):
        print "G0 z%.4f" % z_safe
        angle = start_angle + i * increment_angle
        rads = math.radians(angle)
        x = radius * math.cos(rads) + center_x
        y = radius * math.sin(rads) + center_y
        print
        print "(hole number %d)" % (i+1)
        # use peck drilling if depth > 2 times drill diameter
        if pecking:
            print "g83 x%(x).4f y%(y).4f z%(z_depth).4f q%(peck).4f r%(z_rapid).4f" % globals()
        else:
            print "G0 z%.4f" % z_rapid
            print "g81 x%(x).4f y%(y).4f z%(z_depth).4f r%(z_rapid).4f" % globals()
        if dwell > 0:
            print "G4 p%(dwell).4f (Pause to avoid moving while drill is still in the hole)" % globals()
    print "G0 z%.4f (Done)" % z_safe
    print hugomatic.code.footer()


