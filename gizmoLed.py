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
import hugomatic.code




def take_a_break():
    """
    This function is called when the debug line is printed. Add a breakpoint here
    but don't call print, because the program will go into an infinite loop.
    """
    a = 42     
        

def connector12v(x0, y0, vertical, cut):
    connector_length = 15.0 + 2.0
    connector_width = 0.5 * 10
    wire = -35.0
  
    
    if vertical:
        # Main pocket for the connector
        y_top_main = y0
        y_bottom_main = y0 -connector_length
        x_left_main = x0 - connector_width
        x_right_main = x0 + connector_width
        
        # Small pocket to allow tool to go deep
        y_top_tool    = y0 - connector_length + 10.0
        y_bottom_tool = y0 - connector_length - 2.0
        x_left_tool   = x0 - connector_width - 1.5
        x_right_tool  = x0 + connector_width + 1.5
            
        # black coax connector: deep end with solder
        y_top_deep  = y0 - connector_length
        y_bottom_deep = y0 - connector_length + 7.5
        x_right_deep = x0 - connector_width
        x_left_deep = x0 + connector_width
        
        # pocket for wires
        y_top_wire = 0.#wire
        y_bottom_wire = y0 - connector_length
        x_right_wire = x0 - 3.
        x_left_wire =  x0 + 3.
        
        
    else:
        
        # Main pocket for the connector
        x_left_main   = x0
        x_right_main  = x0 + connector_length
        y_top_main    = y0  + connector_width
        y_bottom_main = y0 - connector_width
        
        # Small pocket to allow tool to go deep
        x_left_tool   = x0 + connector_length - 10.0
        x_right_tool  = x0 + connector_length + 2.0
        y_top_tool    = y0  + connector_width + 1.5
        y_bottom_tool = y0 - connector_width - 1.5
        
        # black coax connector: deep end with solder
        x_right_deep = x0 + connector_length
        x_left_deep =  x0 + connector_length - 7.5 
        y_top_deep  =   y0   + connector_width
        y_bottom_deep = y0 - connector_width
        
        # pocket for wires
        x_right_wire  = wire
        x_left_wire   = x0 + connector_length
        y_top_wire    = y0  + 3.
        y_bottom_wire= y0  - 3.
    
    # compute various depths    
    z_surf = 0.0
    cuts_main = hugomatic.code.z_cut_compiler(-11.0, cut)
    cuts_deep = hugomatic.code.z_cut_compiler(-15.0, cut, z_surf = -11.0)
    cuts_tool = hugomatic.code.z_cut_compiler(-4.0, cut)
    cuts_wire = hugomatic.code.z_cut_compiler(-6.0, cut)
    
    hugomatic.code.pocket_rectangle(x_left_main, y_top_main, x_right_main, y_bottom_main, z_safe, z_surf,tool_dia, cuts_main)
    hugomatic.code.pocket_rectangle(x_left_tool, y_top_tool, x_right_tool, y_bottom_tool, z_safe, z_surf, tool_dia, cuts_tool)
    hugomatic.code.pocket_rectangle(x_left_deep, y_top_deep, x_right_deep, y_bottom_deep, z_safe, z_surf,  tool_dia, cuts_deep)
    hugomatic.code.pocket_rectangle(x_left_wire, y_top_wire, x_right_wire, y_bottom_wire, z_safe, z_surf, tool_dia, cuts_wire)
    
    # extra pocket for wires (vertical connector only) 
    if vertical:
        x_right_wire2  = wire
        x_left_wire2   = x0
        y_top_wire2    = 0.  + 3.
        y_bottom_wire2 = 0  - 3.
        hugomatic.code.pocket_rectangle(x_left_wire2, y_top_wire2, x_right_wire2, y_bottom_wire2, z_safe, z_surf, tool_dia, cuts_wire)


                
                    
params = hugomatic.toolkit.Parameters('Gizmo LED base', 
                                      'Metric dimensions, for 3/4 inch thick plate', 
                                      picture_file = 'gizmoLed.gif',
                                      debug_callback=take_a_break)

tool_dia = 3.175
params.addArgument(tool_dia, 'Tool diameter, in mm', group='setup')
cut = 3.
params.addArgument(cut, 'Cut per pass, in mm', group='setup')
feed = 200.
params.addArgument(feed, 'Feed rate, in mm/min', group='setup')
z_safe = 10.0
params.addArgument(z_safe, 'Safe Z above surface in mm', group='setup') 

top = False
params.addArgument(top,'Plexiglass top side holder slot', group='top side opertation')
plexi_length = 140.
params.addArgument(plexi_length,'Plexiglass slot length', group='top side opertation')

bottom = True
params.addArgument(bottom, 'LED array hole', group='bottom side opertation')
connector_height = True
params.addArgument(connector_height, 'Horizontal 12V Connector', group='bottom side opertation')
do_vertical_connector = False
params.addArgument(do_vertical_connector, 'Vertical 12V Connector', group='bottom side opertation')

# Stock dimension
show_stock = False
#stockZ1 = -1.0
params.addArgument(show_stock,   'Show stock contours (EMC only!)')
bar_lenght = 162.0
params.addArgument(bar_lenght, 'The length of the stock, in mm')
bar_width = 44.
params.addArgument(bar_width, 'The width of the stock, in mm')


if params.loadParams():       
    hugomatic.code.header_mm(feed)
    
    z_surf = 0

    print "g0 Z%.4f" % z_safe
    
    if top:
        xleft = plexi_length *-0.5 - 2.
        xright = -xleft
        ytop    = 5.5 * 0.5
        ybottom= -ytop
        z_depth = -4.0
        
        # large pocket for the plexi
        cuts = hugomatic.code.z_cut_compiler(z_depth, cut, z_surf= 0.0)
        hugomatic.code.pocket_rectangle(xleft, ytop, xright, ybottom, z_safe, z_surf, tool_dia, cuts)
    
    # LED array
    if bottom:
        
        # first pocket for the LED circuit board
        ytop = 6
        ybottom= -ytop
        xleft = -42.0
        xright = -xleft
        z_depth = -4.0
        cuts = hugomatic.code.z_cut_compiler(z_depth, cut, z_surf= 0.0)
        hugomatic.code.pocket_rectangle(xleft, ytop, xright, ybottom, z_safe, z_surf,  tool_dia, cuts)
        
        
        
        # second pocket for the LEDs 
        zNewSurface =  z_depth
        ytop = 4.6
        ybottom= -ytop
        z_surf = -4.0
        z_depth = -9.0
        xleft = -40.0
        xright = -xleft
        cuts = hugomatic.code.z_cut_compiler(z_depth, cut, z_surf= zNewSurface)
        hugomatic.code.pocket_rectangle(xleft, ytop, xright, ybottom, z_safe, z_surf, tool_dia, cuts)
        
        # deep pocket for LEDs to the plexiglass (should go trough the stock when top is done)
        z_new_surface =  z_depth
        ytop    = 5.5 * 0.5
        ybottom = -ytop
        z_depth = -15.0
        
        xleft = -38.0
        xRight = -xleft
        cuts = hugomatic.code.z_cut_compiler(z_depth, cut, z_surf = z_new_surface)
        hugomatic.code.pocket_rectangle(xleft, ytop, xright, ybottom, z_safe, z_new_surface, tool_dia, cuts)
        z_surf = 0.0
        
    #pockets for the black 12V coax connector    
    if  do_vertical_connector:
        x0 =  0.5 * (-bar_lenght + ( bar_lenght - plexi_length) )   
        y0 = 0.5 * bar_width + 2. # 2mm outside
        connector12v(x0, y0, True, cut) 
        
    if connector_height:
        x0 = - 0.5 * bar_lenght  - 2.0 # 2mm outside
        y0 = 0.
        connector12v(x0, y0, False, cut)
    
    
    
    if show_stock:
        stockDx = bar_lenght
        stockDy = bar_width
        stockZ1 = -18.9
        stockX0 = - 0.5 * stockDx
        stockY0 = - 0.5 * stockDy
        stockZ0 = 0.0
        hugomatic.code.stock(stockX0, stockY0,  stockDx, stockDy, stockZ0, stockZ1)

    hugomatic.code.footer()

