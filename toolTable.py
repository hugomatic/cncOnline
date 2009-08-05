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
    but don't call print, because the program will go into an infinite loop."""
    a = 42

def tool_hole(x,y, d1,z1, d2,z2, tooldia, zsafe):
    print "g0 z%.4f" % zsafe
    r1 = 0.5 * d1
    
    cuts = hugomatic.code.z_cut_compiler(z1,cut)
    hugomatic.code.cylinder(x, y, d1, tooldia, zsafe, cuts)
    cuts = hugomatic.code.z_cut_compiler(z2,cut,zsurf=z1)
    hugomatic.code.cylinder(x, y, d2, tooldia, z1, cuts)
    
# Create the Parameters object. It is used to create the GUI and set values in global variables
params = hugomatic.toolkit.Parameters('Tool table', 'Keep your precious tools in order', 
                                      picture_file="toolTable.gif", # picture on the left
                                      debug_callback=take_a_break)
# publish a string. Force the user to select the value from a predetermined list 
gcodeUnits = 'Inches'  
params.addArgument( gcodeUnits, 'Program units. 1 inch = 25.4 millimeters', choices=('Inches', 'mm'), group='setup' )
# When publishing numbers. the default value determines the type (int or float...)                    
tooldia = 3.0/8.0
params.addArgument(tooldia, 'Tool diameter', group='setup' )
feed = 4.0 
params.addArgument(feed,  'Feed rate in units per minute', group='setup' )
cut = 0.05
params.addArgument(cut, 'Cut per pass in units', group='setup')
zsafe = 0.1
params.addArgument(zsafe, 'Safe Z above surface in units', group='setup')                
#zdepth = -0.1
#params.addArgument(zdepth,  'Depth of cut in units', group='pockets' ) 
d1 =  1.01
params.addArgument(d1, 'Large cylinder diameter', group='pockets' )
z1 = -0.75
params.addArgument(z1, 'Large cylinder z depth', group='pockets' )
d2 =  0.51
params.addArgument(d2, 'Small cylinder diameter', group='pockets' )
z2 = -1.2
params.addArgument(z2, 'Small cylinder z depth', group='pockets' )

rows = 1
params.addArgument(rows,  'Rows', group='grid' )
columns = 10
params.addArgument(columns, 'Columns', group='grid' )
dx = 2.0
params.addArgument(dx, 'Distance along X', group='grid' )
dy = 1.5
params.addArgument(dy, 'Distance along Y', group='grid' )

engrave_circles = False
params.addArgument(engrave_circles,  'Engrave circles', group='engraving' )
engrave_numbers = False
params.addArgument(engrave_numbers,  'Engrave numbers', group='engraving' )


if params.loadParams():  # the result is False if the window is closed without pressing OK 
    print "(Hey ho...)"
    hugomatic.code.header(gcodeUnits, feed)
  
    centerPositions = []
    x0 = 0.
    y0 = 0.

    for r in range(rows):
        for c in range(columns):
            x = x0 + c*dx
            y = y0 +  r*dy
            tool_hole(x,y,d1,z1,d2,z2, tooldia, zsafe)
    
    hugomatic.code.footer()
