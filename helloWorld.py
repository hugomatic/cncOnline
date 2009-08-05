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
params = hugomatic.toolkit.Parameters('Hello', 'Hello programs make nice templates', 
                                      picture_file="pythonLogo.gif", # picture on the left
                                      debug_callback=take_a_break)
# publish a string. Force the user to select the value from a predetermined list 
gcodeUnits = 'Inches'  
params.addArgument( gcodeUnits, 'Program units... 1 inch = 25.4 millimeters', choices=('Inches', 'mm'), group='setup' )
# When publishing numbers. the default value determines the type (int or float...)                    
feed = 4.0 
params.addArgument(feed,  'Feed rate in units per minute', group='setup' )
cut = 0.05
params.addArgument(cut, 'Cut per pass in units', group='setup')
zSafe = 0.1
params.addArgument(zSafe, 'Safe Z above surface in units', group='setup')                
zDepth = -0.1
params.addArgument(zDepth,  'Depth of cut in units', group='hello' ) 

# Show the GUI, wait for the user to press the OK button
if params.loadParams():  # the result is False if the window is closed without pressing OK
    
    print
    print "(Hello, physical world!...)"
    print 
    print "(Units: %s)" % gcodeUnits    
    # generate GCODE here!
    hugomatic.code.header(gcodeUnits, feed)   
         
    cuts = hugomatic.code.z_cut_compiler(zDepth, cut); # an array of depths
    for z in cuts:
        print "g0 Z%.4f (move tool out of the way)" % zSafe
        print "g0 X0.06429 Y0.01676"
        print "g01 Z%0.4f" % z
        print """
g01 X0.06429 Y0.01676\ng01 X0.19421 Y0.16093\ng01 X0.33169 Y0.30040\ng01 X0.45771 Y0.44804
g01 X0.55327 Y0.61674\ng01 X0.55861 Y0.63041\ng01 X0.55861 Y0.63041\ng01 X0.61260 Y0.81890
g01 X0.62549 Y1.01445\ng01 X0.59985 Y1.16798\ng01 X0.59985 Y1.16798\ng01 X0.48432 Y1.23653
g01 X0.37699 Y1.14554\ng01 X0.37298 Y1.12248\ng01 X0.37298 Y1.12248\ng01 X0.34175 Y0.92648
g01 X0.33515 Y0.72762\ng01 X0.34130 Y0.52866\ng01 X0.34286 Y0.49266\ng01 X0.34286 Y0.49266
g01 X0.34943 Y0.29400\ng01 X0.32683 Y0.09698\ng01 X0.31794 Y0.06102\ng01 X0.31794 Y0.06102
g01 X0.36158 Y0.25343\ng01 X0.40198 Y0.36300\ng01 X0.40198 Y0.36300\ng01 X0.46700 Y0.21359
g01 X0.47682 Y0.11967\ng01 X0.47682 Y0.11967\ng01 X0.54888 Y0.02535\ng01 X0.70460 Y0.04042
g01 X0.71661 Y0.04180\ng01 X0.71661 Y0.04180\ng01 X0.85974 Y0.13575\ng01 X0.93118 Y0.30931
g01 X0.93571 Y0.34533\ng01 X0.93571 Y0.34533\ng01 X0.81107 Y0.40174\ng01 X0.71187 Y0.37534
g01 X0.71187 Y0.37534\ng01 X0.76781 Y0.19867\ng01 X0.82081 Y0.14678\ng01 X0.82081 Y0.14678
g01 X0.97314 Y0.04424\ng01 X1.10253 Y0.03885\ng01 X1.10534 Y0.04432\ng01 X1.10534 Y0.04432
g01 X1.18384 Y0.24341\ng01 X1.23930 Y0.41053\ng01 X1.26946 Y0.59076\ng01 X1.27438 Y0.74047
g01 X1.27438 Y0.74047\ng01 X1.24977 Y1.02289\ng01 X1.18258 Y1.19106\ng01 X1.11729 Y1.24706
g01 X1.11729 Y1.24706\ng01 X1.07405 Y1.05364\ng01 X1.04915 Y0.85779\ng01 X1.05301 Y0.75395
g01 X1.05301 Y0.75395\ng01 X1.06800 Y0.59683\ng01 X1.11222 Y0.38902\ng01 X1.18656 Y0.19255
g01 X1.29192 Y0.06947\ng01 X1.32418 Y0.05721\ng01 X1.32418 Y0.05721\ng01 X1.46739 Y0.11326
g01 X1.55983 Y0.25797\ng01 X1.62125 Y0.43823\ng01 X1.66624 Y0.58667\ng01 X1.66624 Y0.58667
g01 X1.73526 Y0.69848\ng01 X1.71745 Y0.88859\ng01 X1.65513 Y1.08249\ng01 X1.59059 Y1.20566
g01 X1.56961 Y1.21641\ng01 X1.56961 Y1.21641\ng01 X1.51866 Y1.00771\ng01 X1.49900 Y0.81605
g01 X1.50654 Y0.63415\ng01 X1.53721 Y0.45478\ng01 X1.58690 Y0.27065\ng01 X1.65152 Y0.07452
g01 X1.66109 Y0.04696\ng01 X1.66109 Y0.04696\ng01 X1.72627 Y0.09504\ng01 X1.79907 Y0.26347
g01 X1.80630 Y0.27330\ng01 X1.80630 Y0.27330\ng01 X1.89380 Y0.46071\ng01 X1.90766 Y0.52228
g01 X1.90766 Y0.52228\ng01 X1.88884 Y0.37091\ng01 X1.93021 Y0.15788\ng01 X2.02150 Y0.03895
g01 X2.02150 Y0.03895\ng01 X2.11073 Y0.15541\ng01 X2.16955 Y0.32616\ng01 X2.16976 Y0.49679
g01 X2.08314 Y0.61291\ng01 X2.05463 Y0.62429\ng01 X2.05463 Y0.62429\ng01 X1.93189 Y0.57714
g01 X1.97196 Y0.56514\ng01 X1.97196 Y0.56514\ng01 X2.16268 Y0.55931\ng01 X2.32826 Y0.56265
g01 X2.38978 Y0.57806\ng01 X2.38978 Y0.57806\ng01 X2.56599 Y0.70315\ng01 X2.60714 Y0.73105
    """
    print "g0 Z%.4f (move tool out of the way)" % zSafe
    hugomatic.code.footer()