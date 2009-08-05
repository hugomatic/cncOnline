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
# http://github.com/hugomatic
#
# You can contact me at the following email address:
# ugomatik@gmail.com
#

import hugomatic.toolkit    # the GUI stuff
import hugomatic.code       # the GCODE routines

      
def takeAbreak():
    """This function is called when the debug line is printed. Add a breakpoint here
    but don't call print, because the program will go into an infinite loop."""
    a = 42

def hole(x, y, zsafe, rapid_plane, peck, z, feed ):
    print "g0 Z%.4f (move tool out of the way)" % z_safe
    print "g0 x%.4f y%.4f" % (x,y)
    print "G4 p0.1 (0.1 sec Pause)"
    #print "M0 (Pause)"
       
    print "G83 x%.4f y%.4f z%.4f r%.4f q%.4f" %(x,y, z, rapid_plane, peck)
    print "g0 Z%.4f (move tool out of the way)" % z_safe
    print "G4 p0.1 (0.1 sec Pause)"


class PillowContour(object):
    
    def __init__(self, 
                 floor, 
                 head,
                 y_shoulder, # shoulder height
                 x_length,
                 bearing_center_y,
                 bearing_head_dia,
                 x0,
                 y0,
                 tool_dia,
                 z_safe, 
                 z_rapid):
        """
        Creates a Pillow contour object.
        """
        self.floor = floor
        self.head = head
        
        self.y_shoulder = y_shoulder
        self.x_length = x_length
        self.bearing_center_y = bearing_center_y
        self.bearing_head_dia = bearing_head_dia
        
        self.x0 = x0
        self.y0 = y0
        self.tool_dia = tool_dia
        
        self.z_safe = z_safe
        self.z_rapid = z_rapid
        
        self.tool_rad = 0.5 * tool_dia
        
        self.x_bottom_right = self.x0 + self.x_length * 0.5 + self.tool_rad
        self.y_bottom_right = self.y0 - self.tool_rad
        
        self.x_bottom_right_mirror = self.x0 - (self.x_length * 0.5 + self.tool_rad)
        self.x_shoulder_top_right = self.x_bottom_right
        
        self.y_shoulder_top_right = self.y0 + self.y_shoulder + self.tool_rad
        
        self.head_radius = (0.5 * self.bearing_head_dia) + self.tool_rad
        self.x_neck_bottom = self.x0 + self.head_radius
        self.x_neck_top_mirror = self.x0 - self.head_radius
        
        self.y_neck_bottom = self.y_shoulder_top_right
        
        self.x_neck_top = self.x_neck_bottom
        self.y_neck_top = self.y0 + self.bearing_center_y
        
        self.contour_j = 0.
        self.contour_i = - self.head_radius
   
    def _approach(self):
       #print "g0 z%.4f" % z_safe
        print "g0 z%.4f" % self.z_safe
        if self.head:
            print "g0 x%.4f y%.4f" % (self.x_bottom_right, self.y_bottom_right)
        else:
            if self.floor:
                print "g0 x%.4f y%.4f" % (self.x_bottom_right_mirror, self.y_bottom_right)
        print "g0 z%.4f" % self.z_rapid
        #print "g0 x%.4f y%.4f" % (self.x0, self.y0)
        
    def _retract(self):
        print "g0 z%.4f" % self.z_safe 
        
    def _mill(self, z):
        print "(PillowContour._mill z=%.4f)" % z
    
        
        if self.head:
            print "g1 z%.4f" % z 
            print "g1 x%.4f y%.4f (right shoulder)" % (self.x_shoulder_top_right, self.y_shoulder_top_right)
            print "g1 x%.4f y%.4f (right shoulder top)" % (self.x_neck_bottom , self.y_neck_bottom ) 
            print "g1 x%.4f y%.4f (right neck)" % (self.x_neck_bottom , self.y_neck_top)
            
            print "g3 x%.4f y%.4f i%.4f j%.4f (head)"% (self.x_neck_top_mirror, self.y_neck_top, self.contour_i, self.contour_j)
            
            print "g1 x%.4f y%.4f (left neck)" % (self.x_neck_top_mirror , self.y_neck_bottom ) 
            print "g1 x%.4f y%.4f (left shoulder top)" % (self.x_bottom_right_mirror , self.y_neck_bottom )
            print "g1 x%.4f y%.4f (left shoulder)" % (self.x_bottom_right_mirror, self.y_bottom_right)
        else:
            print "(no head)"
            #print "g0 z%.4f" % self.z_safe
            print "g0 x%.4f y%.4f (bottom left)" % (self.x_bottom_right_mirror, self.y_bottom_right)
            
        if self.floor:
            print "(floor you)"
            print "g1 z%.4f" % z 
            print "g1 x%.4f y%.4f (bottom cut)" % (self.x_bottom_right, self.y_bottom_right)
            if not self.head:
                print "g0 z%.4f" % self.z_rapid
        else:
            print "g0 z%.4f" % self.z_safe
            print "g0 x%.4f" % self.x_bottom_right
          
    def cut(self, cuts):
        
        if not self.head and not self.floor:
            return
        
        print "(Cutting pillow contour)"
        
        #self._approach()
        self._approach()
        for z in cuts:
            
            self._mill(z)
            #
            
        self._retract()
        
        
    
    
# Create the Parameters object. It is used to create the GUI and set values in global variables
params = hugomatic.toolkit.Parameters('Load cell pillow connector', '1.125 stock, origin  is left side, center', 
                                      picture_file="pillow_block.gif", # picture on the left
                                      debug_callback=takeAbreak)

units = "Inches"
params.addArgument(units,  'Units', choices=("mm","Inches"), group='setup' )
feed = 2.0 
params.addArgument(feed,  'Feed rate in units per minute', group='setup' )
cut = 0.05
params.addArgument(cut, 'Cut per pass in units', group='setup')
z_safe = 0.25
params.addArgument(z_safe , 'Safe Z above surface  and clamps in units', group='setup')                
z_rapid = 0.05
params.addArgument(z_rapid , 'Rapid plane above surface where rapid movements stop', group='setup')                

tool_dia = 0.25
params.addArgument(tool_dia, 'Tool diameter in units', group='setup')    

z_bearing = -0.5
params.addArgument(z_bearing, 'Stock thickness along z', group='setup')

bearing_center_y = 1.0
params.addArgument(bearing_center_y, 'Bearing hole center height along y', group='setup')
                   
operation_bearing_large = True
params.addArgument(operation_bearing_large, 'Cut bearing large hole', group='bearing')                

bearing_large_dia = 0.5
params.addArgument(bearing_large_dia, 'Bearing large diameter', group='bearing')
bearing_large_depth = -0.25
params.addArgument(bearing_large_depth, 'Bearing large hole depth along z', group='bearing')


operation_bearing_small = True
params.addArgument(operation_bearing_small, 'Cut bearing small hole', group='bearing')
bearing_small_dia = 0.45
params.addArgument(bearing_small_dia, 'Bearing hole small diameter', group='bearing')

operation_bearing_floor = True
params.addArgument(operation_bearing_floor, 'Cut bearing floor', group='contour')

operation_bearing_head = True
params.addArgument(operation_bearing_head, 'Cut bearing head', group='contour')
bearing_head_dia = 0.75
params.addArgument(bearing_head_dia, 'Bearing head contour diameter', group='contour')


x_length = 2.000
params.addArgument(x_length, 'Pillow block length along x', group='contour')
y_shoulder = 0.5
params.addArgument(y_shoulder, 'Pillow block shoulder height', group='contour')

operation_bearing_large_drill = True
params.addArgument(operation_bearing_large_drill, 'Drill bearing large hole', group='drill')

operation_bearing_small_drill = True
params.addArgument(operation_bearing_small_drill, 'Drill bearing small hole', group='drill')

operation_mount_holes_drill = True
params.addArgument(operation_mount_holes_drill, 'Top side: Drill mounting holes', group='drill')

mount_hole_distance = 0.75
params.addArgument(mount_hole_distance, 'Distance between mount holes', group='top')
        
mount_hole_dia = 0.125
params.addArgument(mount_hole_dia, 'Mount holes diameter', group='top')

mount_hole_y = 0.25
params.addArgument(mount_hole_y, 'Mount hole y position', group='top')

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
    
    # generate GCODE here!
    hugomatic.code.header(units, feed)   
    
    positions = []
    
    tool_changer = hugomatic.code.ToolChanger(0., 0.,  2.,  z_safe)
    # prepare a list with the origin for each pillow block
    for i in range(xcount):
        for j in range(ycount):
            x0 = 0. + i * dx
            y0 = 0. + j * dy 
            positions.append( (x0, y0) )

    for origin in positions:
        x0 = origin[0]
        y0 = origin[1]
                    
        if operation_mount_holes_drill:
            tool_changer.change_tool(mount_hole_dia, 'mount hole drill', 'drill')
            print "(Drilling mount holes)"
            x_left = x0 - mount_hole_distance * 0.5
            x_right = x0 + mount_hole_distance * 0.5
            y = y0 + mount_hole_y
            z = z_bearing
            peck = mount_hole_dia
            hole(x_left, y, z_safe, z_rapid, peck, z, feed)
            hole(x_right, y, z_safe, z_rapid, peck, z, feed)
            
    for origin in positions:
        x0 = origin[0]
        y0 = origin[1]
        
        if operation_bearing_large_drill:
            tool_changer.change_tool(bearing_large_dia, 'Large hole drill', 'drill')
            print "(Drilling large bearing hole)"
            
    for origin in positions:
        x0 = origin[0]
        y0 = origin[1]        
        if operation_bearing_small_drill:
            tool_changer.change_tool(bearing_small_dia, 'Small hole drill', 'drill')
            print "(Drilling small bearing hole)"

    for origin in positions:
        
        x0 = origin[0]
        y0 = origin[1]        
                     
        if operation_bearing_large:
           tool_changer.change_tool(tool_dia, 'Contour mill', 'end mill')
           x = x0
           y = y0 + bearing_center_y
           z = bearing_large_depth
           diameter = bearing_large_dia
           hugomatic.code.circle_heli_tool_inside(x, y, diameter, z, z_safe, z_rapid, tool_dia, cut)
        
        if operation_bearing_small:
            tool_changer.change_tool(tool_dia, 'Contour mill', 'end mill')
            x = x0
            y = y0 + bearing_center_y
            diameter = bearing_small_dia
            z = z_bearing
            hugomatic.code.circle_heli_tool_inside(x, y, diameter, z, z_safe, z_rapid, tool_dia, cut)
           
        if operation_bearing_floor or operation_bearing_head:
            tool_changer.change_tool(tool_dia, 'Contour mill', 'end mill')
            cuts = hugomatic.code.z_cut_compiler(z_bearing, cut)    
            print "(cut contour)"
            
            pillow = PillowContour(operation_bearing_floor, 
                                   operation_bearing_head,
                                   y_shoulder, 
                                   x_length,
                                   bearing_center_y,
                                   bearing_head_dia,
                                   x0,
                                   y0,
                                   tool_dia,
                                   z_safe, 
                                   z_rapid)
            pillow.cut(cuts)
        
    hugomatic.code.footer()
