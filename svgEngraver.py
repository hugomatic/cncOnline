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
from hugomatic.toolkit import *
from hugomatic.paths import *
from hugomatic.code import *

def take_a_break():
    """
    This function is called when the debug line is printed. Add a breakpoint here
    but don't call print, because the program will go into an infinite loop.
    """
    a = 42

params = Parameters('SVG Engraver', 'Convert your SVG art into GCode', 
                    'plexis.gif', 
                    debug_callback=take_a_break)

feed = 4.0
params.addArgument(feed, 'feed in inches/min', group='setup')
cut = 0.1
params.addArgument(cut, 'cut', group='setup')
zSafe = 0.1
params.addArgument(zSafe, 'Safe Z above surface in inches', group='setup') 
filename = ""
params.addArgument(filename, 'File name', filePath = True)
zDepth= -0.025
params.addArgument(zDepth, 'Final depth (neg)')
xOff = 0.0 
params.addArgument(xOff, 'X offset')
yOff = 0.0
params.addArgument(yOff, 'Y offset')
scaleX = 0.01
params.addArgument(scaleX, 'Scale X')
scaleY = -scaleX
params.addArgument(scaleY, 'Scale Y')
resolution = 1.0
params.addArgument(resolution, 'Bezier "Resolution": smaller is better')


#if __name__ == "__main__":
if params.loadParams():    
    svgFile = params.getRelativePath(filename)
    paths = readPathsFromSvgFile(svgFile)

    header_inch(feed)
    
    
    zSurf = 0.0
    cuts = z_cut_compiler(zDepth, cut);
    
    for path in paths:
        print
        print
        print "(",path[0],")"
        strokes, loop = getStrokesFromPath(path, xOff, yOff, scaleX, scaleY, resolution)
        for points in strokes:
            backAndForth(points, cuts, zSafe, zSurf)
    
    footer()