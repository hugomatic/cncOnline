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
    
# Create the Parameters object. It is used to create the GUI and set values in global variables
params = hugomatic.toolkit.Parameters('Lathe turning', 'Turn a shaft with increasing diameter from the left', 
                                      picture_file="turn.gif", # picture on the left
                                      debug_callback=take_a_break)
# publish a string. Force the user to select the value from a predetermined list 
gcodeUnits = 'mm'  
params.addArgument( gcodeUnits, 'Program units... 1 inch = 25.4 millimeters', choices=('Inches', 'mm'), group='setup' )
# When publishing numbers. the default value determines the type (int or float...)                    
feed = 50. 
params.addArgument(feed,  'Feed rate in units per minute', group='setup' )
cut = 0.25
params.addArgument(cut, 'Cut per pass in units', group='setup')
safe_dx = 0.5
params.addArgument(safe_dx, 'X Safe distance above surface in units', group='setup')   
safe_dz = 0.5
params.addArgument(safe_dz, 'Z Safe distance right of surface in units', group='setup')               
stockDiameter = 31.15
params.addArgument(stockDiameter,  'Stock diameter', group='setup' ) 
#0 = 0.
#params.addArgument(z0,  'Z 0', group='setup' ) 

methods = ("Along Z, then X", "Along X, then Z")
method = methods[0]
params.addArgument( method, 'Cutting method', choices=methods, group='setup' )
z0 = 0.
params.addArgument(z0,  'Z start', group='turn' )
d1 = 0.
params.addArgument(d1,  'Diameter 1', group='turn' )
z1 = -0.5
params.addArgument(z1,  'Z 1', group='turn' )
d2 = 10.
params.addArgument(d2,  'Diameter 2', group='turn' )
z2 = -10.
params.addArgument(z2,  'Z 2', group='turn' )
d3 = 25.
params.addArgument(d3,  'Diameter 3', group='turn' )
z3 = -17.
params.addArgument(z3,  'Z 3', group='turn' )


def shaft_xcut(d0,d1,z0,z1, cut, delta_x, delta_z):
    x0 = 0.5 * d0
    x1 = 0.5 * d1
    cuts = hugomatic.code.z_cut_compiler(x1, cut, z_surf=x0);
    print "(shaft )"
    xsafe = x0 + delta_x
    z_safe = z0 +delta_z
    print "g0 x%.4f Z%.4f (move close)" % (xsafe, z_safe)
    
    previous_x = xsafe
    for x in cuts:
        print
        print "(radius = %.5f)" % x 
        print "g0  x%.4f (move to cut radius)" % x
        print "g01 z%.4f (cut along shaft)" % z1
        print "g01 x%.4f (cut away from center)" % (previous_x)
        print "g0 z%.4f  (move fast to beginning)" % (z0 + delta_z)
        previous_x = x
        
def shaft_zcut(d0, d1, z0, z1, cut):
    print "(Along Z, then X)"
    r0 = 0.5 * d0
    r1 = 0.5 * d1
    cuts = hugomatic.code.z_cut_compiler(z1, cut, zsurf=z0);
    
    previous_z = z1
    for z in cuts:
        print
        print "g01 X%.4f (cut towards center)" % z
        print "g0 X%.4f  " % r1
        print "g01 z%.4f" % z
        
    
# Show the GUI, wait for the user to press the OK button
if params.loadParams():  # the result is False if the window is closed without pressing OK
    
    print
    print 
    print "(Units: %s)" % gcodeUnits    
    # generate GCODE here!
    hugomatic.code.header(gcodeUnits, feed)   
    
    if method == methods[0]:
        shaft = shaft_xcut
    
    shaft(stockDiameter, d1, z0, z1, cut, safe_dx, safe_dz)
    shaft(stockDiameter, d2, z1, z2, cut,safe_dx, safe_dz)
    shaft(stockDiameter, d3, z2, z3, cut,safe_dx, safe_dz)
    print "g0 x%.4f (move out of the way)" % (stockDiameter * 0.5 + safe_dx)
    hugomatic.code.footer()
    
