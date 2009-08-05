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

import hugomatic.toolkit    # the GUI stuff
import hugomatic.code       # the GCODE routines

      
def take_a_break():
    """This function is called when the debug line is printed. Add a breakpoint here
    but don't call print, otherwise the program will go into an infinite loop."""
    a = 42
    
# Create the Parameters object. It is used to create the GUI and set values in global variables
params = hugomatic.toolkit.Parameters('Round rectangle', 'Not so square', 
                                      picture_file="roundrect.gif", # picture on the left
                                      debug_callback=take_a_break)
# publish a string. Force the user to select the value from a predetermined list 
gcodeUnits = 'Inches'  
params.addArgument( gcodeUnits, 'Program units... 1 inch = 25.4 millimeters', choices=('Inches', 'mm'), group='setup' )
# When publishing numbers. the default value determines the type (int or float...)                    
tooldia = 0.125
params.addArgument(tooldia,  'Tool diameter in units', group='setup' )
feed = 4.0 
params.addArgument(feed,  'Feed rate in units per minute', group='setup' )
zsafe = 0.1
params.addArgument(zsafe, 'Safe Z above surface in units', group='setup')   
zsurf = 0.
params.addArgument(zsurf, 'Surface Z', group='setup')  
cut = 0.05
params.addArgument(cut, 'Cut per pass in units', group='setup')          
zdepth = -0.1
params.addArgument(zdepth,  'Depth of cut in units', group='setup' ) 


modes=('Tool outside rectangle', 'Tool inside rectangle', 'Tool on rectangle')
mode = modes[2]
params.addArgument(mode,  'dimensions mode', choices=modes, group='round rect' ) 
x0 = 0.
params.addArgument(x0, 'x0 left', group='round rect' ) 
y0 = 0.
params.addArgument(y0, 'y0 bottom', group='round rect' ) 
x1 = 1.
params.addArgument(x1,  'x1 right', group='round rect' ) 
y1 = 1.
params.addArgument(y1,  'y1 top', group='round rect' )
corner_radius = 0.25
params.addArgument(corner_radius,  'corner radius', group='round rect' )

ycount = 1
params.addArgument(ycount,  'Rows', group='grid' )
xcount = 1
params.addArgument(xcount,  'Columns', group='grid' )
dx = 1.
params.addArgument(dx,  'Distance along X', group='grid' )
dy = 1.
params.addArgument(dy,  'Distance along Y', group='grid' )


# Show the GUI, wait for the user to press the OK button
if params.loadParams():  # the result is False if the window is closed without pressing OK
    
    print
    print "(Round rectangle)"
    print 
    print "(Units: %s)" % gcodeUnits    
    # generate GCODE here!
    hugomatic.code.header(gcodeUnits, feed)   
         
    cuts = hugomatic.code.z_cut_compiler(zdepth, cut); # an array of depths
    
    for j in range(ycount):
        for i in range (xcount):
            xleft   = x0 + i * dx
            ybottom = y0 + j * dy
            xright  = x1 + i * dx 
            ytop    = y1 + j * dy
            
            if mode == modes[0]: # tool outside
                hugomatic.code.round_rectangle_tool_outside(xleft, ybottom, xright, ytop, corner_radius, zsafe, zsurf,  tooldia, cuts)
            
            if mode == modes[1]: # tool inside
                hugomatic.code.round_rectangle_tool_inside(xleft, ybottom, xright, ytop, corner_radius, zsafe, zsurf,  tooldia, cuts)
            
            if mode == modes[2]: # tool on
                hugomatic.code.round_rectangle(xleft, ybottom, xright, ytop, corner_radius, zsafe, zsurf,  tooldia, cuts)                
            
               
    print "g0 Z%.4f (move tool out of the way)" % zsafe
    hugomatic.code.footer()