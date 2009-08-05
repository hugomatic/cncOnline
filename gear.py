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
import hugomatic.toolkit
import hugomatic.gearing
import hugomatic.code

      
def take_a_break():
    """
    This function is called when the debug line is printed. Add a breakpoint here
    but don't call print, because the program will go into an infinite loop.
    """
    a = 42
    
# Create the Parameters object. It is used to create the GUI and set values in global variables
params = hugomatic.toolkit.Parameters('Gear me up', 'Mill yourself nice ACME gears using a rotary table!', 
                                      picture_file="gears.gif", 
                                      debug_callback=take_a_break)

feed = 4.0
params.addArgument(feed,  'Feed rate in inches per minute', group='setup' )

cut = 0.1
params.addArgument(cut,  'cut per pass in inch', group='setup' )

ysafe = 0.1
params.addArgument(ysafe, 'Safe distance between the cutter and the blank along Y', group='setup')
                  
p = 24
params.addArgument(p, 'Diametral pitch: nb of teeth per inch of diameter')

number_of_teeth = 96
params.addArgument(number_of_teeth, 'Number of teeth')

xlength = 1.0
params.addArgument(xlength, 'Cut lenght along X')



if params.loadParams(): # Show the GUI, wait for user input
    
    # generate GCODE here!
    hugomatic.code.header_inch(feed)    
    print "g0 Y%.4f" % ysafe
    hugomatic.gearing.cut_gear(p, number_of_teeth, xlength, cut, feed, ysafe)
    print "g0 Y%.4f" % ysafe
    hugomatic.code.footer()