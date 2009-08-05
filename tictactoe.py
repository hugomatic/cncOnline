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


import hugomatic.toolkit # UI and cmdline stuff
import hugomatic.code    # gcode routines



def take_a_break():
    """
    This function is called when the debug line is printed. Add a breakpoint here
    but don't call print, because the program will go into an infinite loop.
    """
    a = 42

########################################
# Global variables definition
#     
# remember: 1 inch = 25.4 millimeters


#
# Stock dimension
#
stock = False
stockX0 = 0.0
stockX1 = 95.4
stockY0 = 0.0
stockY1 = 68.8
stockZ0 = 0.0
stockZ1 = -15.0

#
#
#
feed = 100.0
cut = 0.5
zSafe = 2.0
tool1Dia = 3.0 / 8.0 * 25.4

boardSize = 66.0
borderWidth = 2.0

zPocket = -3.0 

xOffEngrave = 0.2
yOffEngrave = 0.6
scaleXEngrave = 0.8
scaleYEngrave = scaleXEngrave

########################################
# Program GUI
#                    
params = hugomatic.toolkit.Parameters('Tictactoe', 
                                      'Mill yourself a tictactoe board game today', 
                                      picture_file="tictactoe.gif",
                                      debug_callback=take_a_break)

params.addArgument(feed, 'Feed rate in mm/min', short='f', group='setup')
params.addArgument(cut,  'cut per pass in mm', short= 'c', group='setup' )
params.addArgument(zSafe, 'Safety height above blank in mm', group='setup')
params.addArgument(tool1Dia, 'Tool diameter in mm',short = 'd', help = 'The diameter of the tool', group='setup')

params.addArgument(boardSize, 'Square game board width in mm', short = 'h', group='game board')
params.addArgument(borderWidth, 'border size in mm', short = 'w', help = 'The border between pockets', group='game board')
surfacing = True
params.addArgument(surfacing,  'Perform board surfacing', group='game board')
surfaceZ = -0.2
params.addArgument(surfaceZ,  'Surfacing depth', group='game board')
pocketsTop = True
params.addArgument(pocketsTop, 'Lower the pockets aka big pocket', group='game board')
zMiddle = - 2.0
params.addArgument(zMiddle, 'Final Z depth for big pocket (negative number)', group='game board')
do_pockets = True
params.addArgument(do_pockets,    'Mill the 9 game pockets',  group='game board')
params.addArgument(zPocket, 'Game pockets Z depth (negative number)',group='game board')


#
# Bar stock dimension
#
stock = False
stockX0 = 0.0
stockDx = 95.4
stockY0 = 0.0
stockDy = 68.8
stockZ0 = 0.0
stockZ1 = -15.0

params.addArgument(stock,   'Show stock contours', group = "game board")
params.addArgument(stockX0, 'Stock dimension X0', group = "game board")
params.addArgument(stockY0, 'Stock dimension Y0', group = "game board")
params.addArgument(stockDx, 'Stock dimension length along X', group = "game board")
params.addArgument(stockDy, 'Stock dimension length along Y',  group = "game board")
params.addArgument(stockZ0, 'Stock dimension Z0',  group = "game board")
params.addArgument(stockZ1, 'Stock dimension Z1 (negative number)', group = "game board")


#x and os
xAndOs = False
xAndOsZfinish = -7.0

params.addArgument(xAndOs, 'Cut X and Os', group='X and Os')
params.addArgument(xAndOsZfinish, 'X and O plate thickness (negative number)', group='X and Os')




def drawX(x,y, a, b, zsafe, cut, zFinal):
    
    def draw(z):
        print "g01 z%.4f (plunge)" % z
        print "g01 y%.4f (W)" % (y+a)
        print "g01 x%.4f" % (x-a)
        print "g01 y%.4f" % (y+a+b)
        print "g01 x%.4f (N)" % (x+a)
        print "g01 y%.4f" % (y+a)
        
        print "g01 x%.4f" % (x+a+b)
        print "g01 y%.4f" % (y-a)
        
        print "g01 x%.4f" % (x+a)
        print "g01 y%.4f" % (y-a-b)
        
        print "g01 x%.4f" % (x-a)
        print "g01 y%.4f" % (y-a)
        
        print "g01 x%.4f (end X)" % (x-a-b)
            
    print "g0 z%.4f" %  (zSafe)
    print "g0 x%.4f y%.4f" % (x-a-b, y-a)
    z = cut * 0.75
    while z > zFinal:
        z = z - cut
        if z < zFinal:
            z = zFinal
        draw(z)
    
           
def drawO(x,y, d1, d2, zsafe, cut, zFinal):
    
    print "g0 z%.4f" %  (zSafe)
    hugomatic.code.HelicalHole(x, y, d1,  zFinal, zSafe, cut, 0.0)
    hugomatic.code.HelicalHole(x, y, d2,  zFinal, zSafe, cut, 0.0)


#
# Generation
#
if params.loadParams():

	#
	# pockets are offset to be in middle of stock
	#    
	xOff = 0.5 *((stockX1 -stockX0) - boardSize)
	yOff = 0.5 *((stockY1 -stockY0) - boardSize)
	tool1Rad =  0.5 * tool1Dia
	pocketSize =  (boardSize - 4.0 * borderWidth) / 3.0
	print "(pocket size = %.4f mm)" % pocketSize   



	hugomatic.code.header_mm(feed)
	print "G0 x0 y0 z%(zSafe).4f" % globals()
#	print "T1 M06 G43 H0.0"

	zSurf = 0.0        
	if xAndOs:
	    print "(X and O s)"
	    #print "G20 (imperial)"
	    #print "F10.0000"
		
	       
	    #x arm lengths
	    xa = pocketSize * 0.25
	    xb = xa
	    #o diameters
	    # remember to cut the small circle first
	    da = pocketSize * 0.25
	    db = pocketSize 
		         
	    k = 0
	    for j in range (1,4):
	     for i in range(1, 4):
		 k += 1
		 x0 = xOff + i * borderWidth + (i-1) * pocketSize
		 y0 = yOff + j * borderWidth + (j-1) * pocketSize 
		 x1 = x0 + pocketSize
		 y1 = y0 + pocketSize
		 x = 0.5 * (x0 + x1) # 1 inch = 25.4 millimeters
		 y = 0.5 * (y0 + y1)
		 if(k % 2 == 1): # % is the modulo, // is integer division
		     drawX(x, y, xa, xb, zSafe, cut, xAndOsZfinish)
		 else:
		     drawO(x, y, da, db, zSafe, cut, xAndOsZfinish)

	if surfacing:
	    print "(surfacing)"
		
	    zSurf = 0.0
	    zFinish = - 0.1
	    print "G0 X0 Y0 Z0"
	    print "G01 Z%.4f" % surfaceZ
	    hugomatic.code._zigzag_dy(stockX0 - tool1Dia, stockY1, stockX1 + tool1Dia, stockY0 + 1.0, -tool1Dia * 0.75)
	    


	if pocketsTop:
	    print "(pocketsTop: middle pocket)"
	    x0 = xOff + borderWidth
	    y0 = yOff + borderWidth
	    x1 = boardSize - borderWidth + xOff
	    y1 = boardSize - borderWidth + yOff
	    zSurf = 0.0
	    
	    cuts = hugomatic.code.z_cut_compiler(zMiddle, cut, zsurf= zSurf)
	    hugomatic.code.pocketRectangle(x0, y0, x1, y1, zSafe, zSurf, tool1Dia, cuts)
	    zSurf = zMiddle
	    
	if do_pockets:
	 print "(pockets: 9 pockets )" 
	 for j in range (1,4):
	     for i in range(1, 4):
		 x0 = xOff + i * borderWidth + (i-1) * pocketSize
		 y0 = yOff + j * borderWidth + (j-1) * pocketSize 
		 x1 = x0 + pocketSize
		 y1 = y0 + pocketSize
		 cuts = hugomatic.code.z_cut_compiler(zPocket, cut, zsurf= zSurf)
		 hugomatic.code.pocketRectangle(x0, y0, x1, y1, zSafe, zSurf, tool1Dia, cuts)
	    

	if stock:    
	    hugomatic.code.stock(stockX0, stockY0,  stockDx, stockDy, stockZ0, stockZ1)

	hugomatic.code.footer()
       
