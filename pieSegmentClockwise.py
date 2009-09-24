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


# remember: 1 inch = 25.4 millimeters
import sys
import hugomatic.toolkit
import hugomatic.code


  
def takeAbreak():
    """
    This function is called when the debug line is printed. Add a breakpoint here
    but don't call print, because the program will go into an infinite loop.
    """
    a = 42 

params = hugomatic.toolkit.Parameters('Pie segments', 
                                      'Disks, cylinders and in between... clockwise!', 
                                      'pieSegment.gif',
                                      takeAbreak)

units = 'Inches'  
params.addArgument( units, 'Program units', choices=('Inches', 'mm'), group='setup' )

feed = 4.0
params.addArgument(feed, 'Feed rate in units per minute', group='setup')

tool_dia = 0.25
params.addArgument(tool_dia, 'Tool diameter in units', group='setup')

cut = 0.1
params.addArgument(cut, 'Cut per pass in units', group='setup')

z_rapid = 0.05
params.addArgument(z_rapid, 'Rapid plane Z where rapid movement stops', group='setup')

z_safe = 0.1
params.addArgument(z_safe, 'Safe Z above surface', group='setup')

degAngleFromHorizonStart = 45.
params.addArgument(degAngleFromHorizonStart, 'Start angle (horizon = 0, counter clockwise positive)', group='pocket')

degAngleFromHorizonEnd = 0.
params.addArgument(degAngleFromHorizonEnd, 'End angle', group='pocket') 

x = 1.
params.addArgument(x, 'Pie center X', group='pocket') 

y = 2.
params.addArgument(y, 'Pie center Y', group='pocket') 

inside_dia = 1.0
params.addArgument(inside_dia, 'Inside diameter', group='pocket') 

outside_dia = 2.0
params.addArgument(outside_dia, 'Outside diameter', group='pocket')

z_depth = -1.
params.addArgument(z_depth, 'Final Z depth (a negative number)', group='pocket')

comp = False
params.addArgument(comp, 'Compensate for tool diameter (mill inside the specified dimensions )', group='pocket')


if params.loadParams():    

    hugomatic.code.header(units, feed)
    
    print "g0 z%.4f" % z_safe
    cuts = hugomatic.code.z_cut_compiler(z_depth, cut)
    if not comp:
        hugomatic.code.pie_segment(degAngleFromHorizonStart, degAngleFromHorizonEnd, x, y, inside_dia, outside_dia, tool_dia, z_safe, z_rapid, cuts)
    else:
        hugomatic.code.pie_segmentToolComp(degAngleFromHorizonStart, degAngleFromHorizonEnd, x, y, inside_dia, outside_dia, tool_dia, z_safe, z_rapid, cuts)
    hugomatic.code.footer()