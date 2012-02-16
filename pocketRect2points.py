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
    print "(--- THIS IS THE DEBUG LINE! ---)"

params = hugomatic.toolkit.Parameters('Rectangular pocket', 
                                      'Very popular, beyond squares', 
                                      'pocketRectangle.gif',
                                      takeAbreak)

units = 'Inches'  
params.addArgument( units, 'Program units', choices=('Inches', 'mm'), group='setup' )

feed = 4.0
params.addArgument(feed, 'Feed rate in units per minute', group='setup')

tool_dia = 0.25
params.addArgument(tool_dia, 'Tool diameter in units', group='setup')

cut = 0.1
params.addArgument(cut, 'Cut per pass in units', group='setup')

z_safe = 0.1
params.addArgument(z_safe, 'Safe Z above surface', group='setup')
z_surf = 0.
params.addArgument(z_surf, 'Surface Z ', group='setup')

x0 = 0.
params.addArgument(x0, 'Pocket origin X0', group='pocket')
y0 = 0.
params.addArgument(y0, 'Pocket origin Y0', group='pocket')
x1 = 0.75
params.addArgument(x1, 'Pocket corner X1', group='pocket')
y1 = 2.
params.addArgument(y1, 'Pocket corner Y1', group='pocket')
z_depth = -0.2
params.addArgument(z_depth, 'Final Z depth (a negative number)', group='pocket')


#if __name__ == "__main__": b
if params.loadParams():    

    hugomatic.code.header(units, feed)
    
    print "g0 z%.4f" % z_safe
    cuts = hugomatic.code.z_cut_compiler(z_depth, cut, z_surf= z_surf) 
    hugomatic.code.pocket_rectangle(x0, y0, x1, y1, z_safe, z_surf,  tool_dia, cuts)
    hugomatic.code.footer()