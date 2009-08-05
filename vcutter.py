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




def depth(degrees, width):
    radians = math.radians(angle * 0.5)
    tangeant = math.tan(radians)
    opposed = 0.5 * width
    # tangeant = opposed / adjacent
    adjacent = opposed / tangeant
    return adjacent

def width(degrees, depth):
    radians = math.radians(angle * 0.5)
    tangeant = math.tan(radians)
    adjacent = depth
    # tangeant = opposed / adjacent
    opposed =  tangeant / adjacent
    return 2. * opposed

########################################
# Global variables definition
#     
# remember: 1 inch = 25.4 millimeters



########################################
# Program GUI
#                    
params = hugomatic.toolkit.Parameters('Vcutter', 
                                      'Cut Depth/Width calculator for conical end mills (V bits)', 
                                      picture_file="vcutter.gif")



angle = 60.
params.addArgument(angle, 'V bit end mill cutting angle in degrees')

calc = "depth"
params.addArgument(calc, 'Type of calculation', choices = ('depth','width'))

value = 1.0
params.addArgument(value, 'Value of known width/depth')


#
# Generation
#
if params.loadParams():
    
    print
    if calc == "depth":
        f = depth(angle, value)
        print
        print "(For a trace width of %f)" % value
        print "The depth of the cutter is: " + str(f)
    if calc == "width":
        f = width(angle, value)
        print
        print "(For a cut depth of %f)" % value
        print "The width of the trace is: " + str(f)

    print
    print "(Please adjust for tool height and spindle runnout errors)"
    print
    print "(remember: 1 inch = 25.4 millimeters)"
