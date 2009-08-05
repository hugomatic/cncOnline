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
 
      
    
# Create the Parameters object. It is used to create the GUI and set values in global variables
params = hugomatic.toolkit.Parameters('Tap and drill sizes', 
                                      'Recommended tap drill sizes (for approx. 75% thread)',
                                      picture_file="tap_drill.gif") 
                                      
# publish a string. Force the user to select the value from a predetermined list 

tap_inch_fine_choices = ('#0-80         3/64"', 
                         '#1-72         #53',
                         '#2-64         #50',
                         '#3-56         #46',
                         '#4-48         #42',
                         '#5-44         #37',
                         '#6-40         #33',
                         '#8-36         #29',
                         '#10-32        #21',
                         '#12-28        #15',
                         '1/4-28        #3',
                         '5/16-24       I',
                         '3/8-24        Q',
                         '7/16-20       W',
                         '1/2-20        29/64',
                         '9/16-18       33/64',
                         '5/8-18        37/64',
                         '3/4-16        11/16',
                         '7/8-14        13/16',
                         '1"-14         15/16',
                         '1-1/8-12     1-3/64',
                         '1-1/4-12     1-11/64',
                         '1-1/2-12     1-27/64',
                         '1-3/4-12     1-43/64',
                         '2"-12        1-59/64',)
                                                 


tap_inch_coarse_choices = ( "#1-64         #53", 
                            "#2-56         #51", 
                            "#3-48         5/64", 
                            "#4-40         #43",
                            "#5-40         #39", 
                            "#6-32         #36", 
                            "#8-32         #29", 
                            "#10-24        #25", 
                            "#12-24        #17", 
                            "1/4-20        #7", 
                            "5/16-18       F", 
                            "3/8-16        5/16", 
                            "7/16-14       U", 
                            "1/2-13        27/64", 
                            "9/16-12       31/64", 
                            "5/8-11        17/32", 
                            "3/4-10        21/32", 
                            "7/8-9         49/64", 
                            '1"-8          7/8', 
                            '1-1/8-7     63/64', 
                            '1-1/4-7     1-7/64', 
                            '1-1/2-6     1-11/32', 
                            '1-3/4-5     1-35/64', 
                            '2"-4-1/2    1-25/32')


tap_mm_coarse_choices = (   '1mm x .25            .75mm',
                            '1.1 x .25            .85',
                            '1.2 x .25            .95',
                            '1.4 x .3            1.1',
                            '1.6 x .35           1.25',
                            '1.7 x .35           1.3',
                            '1.8 x .35           1.45',
                            '2 x .4              1.6',
                            '2.2 x .45           1.75',
                            '2.5 x .45           2.05',
                            '3 x .5              2.5',
                            '3.5 x .6            2.9',
                            '4 x .7              3.3',
                            '4.5 x .75           3.7',
                            '5 x .8              4.2',
                            '6 x 1               5',
                            '7 x 1               6',
                            '8 x 1.25            6.8',
                            '9 x 1.25            7.8',
                            '10 x 1.5            8.5',
                            '11 x 1.5            9.5',
                            '12 x 1.75           10.2',
                            '14 x 2              12',
                            '16 x 2              14',
                            '18 x 2.5            15.5',
                            '20 x 2.5            17.5',
                            '22 x 2.5            19.5',
                            '24 x 3              21',
                            '27 x 3              24',
                            '30 x 3.5            26.5',
                            '33 x 3.5            29.5',
                            '36 x 4              32',
                            '39 x 4              35',)

 
tap_mm_fine_choices = (  '4 mm x .35          3.6mm',
                         '4 x .5              3.5',
                         '5 x .5              4.5',
                         '6 x .5              5.5',
                         '6 x .75             5.25',
                         '7 x .75             6.25',
                         '8 x .5              7',
                         '8 x .75             7.25',
                         '8 x 1               7',
                         '9 x 1               8',
                         '10 x .75            9.25',
                         '10 x 1              9',
                         '10 x 1.25           8.8 ',
                         '11 x 1              10',
                         '12 x .75            11.25',
                         '12 x 1              11',
                         '12 x 1.5            10.5',
                         '14 x 1              13',
                         '14 x 1.25           12.8',
                         '14 x 1.5            12.5',
                         '16 x 1              15',
                         '16 x 1.5            14.5',
                         '18 x 1              17',
                         '18 x 2              16',
                         '20 x 1              19',
                         '20 x 1.5            18.5',
                         '20 x 2              18',
                         '22 x 1              21',
                         '22 x 1.5            20.5',
                         '22 x 2              20',
                         '24 x 1.5            22.5',
                         '24 x 2              22',
                         '26 x 1.5            24.5',
                         '27 x 1.5            25.5',
                         '27 x 2              25', 
                         '28 x 1.5            26.5',
                         '30 x 1.5            28.5',
                         '30 x 2              28',
                         '33 x 2              31',
                         '36 x 3              33',
                         '39 x 3              36',)
ansi_drills_sizes_a =    [ 'gauge  inches    mm',
 '80     0.014     0.343',
 '79     0.015     0.368',
 '78     0.016     0.406',
 '77     0.018     0.457',
 '76     0.020     0.508',
 '75     0.021     0.533',
 '74     0.023     0.572',
 '73     0.024     0.610',
 '72     0.025     0.635',
 '71     0.026     0.660',
 '70     0.028     0.711',
 '69     0.029     0.742',
 '68     0.031     0.787',
 '67     0.032     0.813',
 '66     0.033     0.838',
 '65     0.035     0.889',
 '64     0.036     0.914',
 '63     0.037     0.940',
 '62     0.038     0.965',
 '61     0.039     0.991',
 '60     0.040     1.016',
 '59     0.041     1.041',
 '58     0.042     1.067',
 '57     0.043     1.092',
 '56     0.046     1.181',
 '55     0.052     1.321',
 '54     0.055     1.397']

ansi_drills_sizes_b =    [ 'gauge  inches    mm',
 '53     0.059     1.511',
 '52     0.064     1.613',
 '51     0.067     1.702',
 '50     0.070     1.778',
 '49     0.073     1.854',
 '48     0.076     1.930',
 '47     0.079     1.994',
 '46     0.081     2.057',
 '45     0.082     2.083',
 '44     0.086     2.184',
 '43     0.089     2.261',
 '42     0.094     2.375',
 '41     0.096     2.438',
 '40     0.098     2.489',
 '39     0.099     2.527',
 '38     0.101     2.578',
 '37     0.104     2.642',
 '36     0.106     2.705',
 '35     0.110     2.794',
 '34     0.111     2.819',
 '33     0.113     2.870',
 '32     0.116     2.946',
 '31     0.120     3.048',
 '30     0.129     3.264',
 '29     0.136     3.454',
 '28     0.141     3.569',
 '27     0.144     3.658']

ansi_drills_sizes_c =    [ 'gauge  inches    mm',
 '26     0.147     3.734',
 '25     0.149     3.797',
 '24     0.152     3.861',
 '23     0.154     3.912',
 '22     0.157     3.988',
 '21     0.159     4.039',
 '20     0.161     4.089',
 '19     0.166     4.216',
 '18     0.169     4.305',
 '17     0.173     4.394',
 '16     0.177     4.496',
 '15     0.180     4.572',
 '14     0.182     4.623',
 '13     0.185     4.699',
 '12     0.189     4.801',
 '11     0.191     4.851',
 '10     0.194     4.915',
 '9     0.196     4.978',
 '8     0.199     5.055',
 '7     0.201     5.105',
 '6     0.204     5.182',
 '5     0.206     5.220',
 '4     0.209     5.309',
 '3     0.213     5.410',
 '2     0.221     5.613',
 '1     0.228     5.791']
 
ansi_drills_sizes_d =    [ 'gauge  inches    mm',
 'A     0.234     5.944',
 'B     0.238     6.045',
 'C     0.242     6.147',
 'D     0.246     6.248',
 'E     0.250     6.350',
 'F     0.257     6.528',
 'G     0.261     6.629',
 'H     0.266     6.756',
 'I     0.272     6.909',
 'J     0.277     7.036',
 'K     0.281     7.137',
 'L     0.290     7.366',
 'M     0.295     7.493',
 'N     0.302     7.671',
 'O     0.316     8.026',
 'P     0.323     8.204',
 'Q     0.332     8.433',
 'R     0.339     8.611',
 'S     0.348     8.839',
 'T     0.358     9.093',
 'U     0.368     9.347',
 'V     0.377     9.576',
 'W     0.386     9.804',
 'X     0.397     10.08',
 'Y     0.404     10.26',
 'Z     0.413     10.49']

tap_mm_fine = tap_mm_fine_choices[0]
tap_inch_coarse = tap_inch_coarse_choices[0]
tap_mm_coarse = tap_mm_coarse_choices[0]
tap_inch_fine = tap_inch_fine_choices[0]
ansi_drills_size_a = ansi_drills_sizes_a[1]
ansi_drills_size_b = ansi_drills_sizes_b[1]
ansi_drills_size_c = ansi_drills_sizes_c[1]
ansi_drills_size_d = ansi_drills_sizes_d[1]
params.addArgument(tap_inch_coarse,  'INCH SIZES - ANSI COARSE', choices= tap_inch_coarse_choices, group='ANSI size' )
params.addArgument(tap_inch_fine,  'INCH SIZES - ANSI FINE', choices= tap_inch_fine_choices, group='ANSI size' )
params.addArgument(ansi_drills_size_a,  'ANSI DRILL GAUGES', choices= ansi_drills_sizes_a, group='ANSI GAUGES' )
params.addArgument(ansi_drills_size_b,  'ANSI DRILL GAUGES', choices= ansi_drills_sizes_b, group='ANSI GAUGES' )
params.addArgument(ansi_drills_size_c,  'ANSI DRILL GAUGES', choices= ansi_drills_sizes_c, group='ANSI GAUGES' )
params.addArgument(ansi_drills_size_d,  'ANSI DRILL GAUGES', choices= ansi_drills_sizes_d, group='ANSI GAUGES' )

params.addArgument(tap_mm_coarse,  'METRIC SIZES - COARSE', choices= tap_mm_coarse_choices, group='Metric size' )
params.addArgument(tap_mm_fine,  'METRIC SIZES - FINE', choices= tap_mm_fine_choices, group='Metric size' )

# Show the GUI, wait for the user to press the OK button
if params.loadParams():  # the result is False if the window is closed without pressing OK
    
    print
    print """

Diameter of thread minus the pitch equals the tap drill size.
eg. M6 x 1
6 - 1 = 5mm
and you thought metric was difficult ;-)


This works for all 75% threads, not just metric.
For example, the tap drill for 3/8-16 is 5/16.
The pitch is 1/16". (1 / threads per inch = inches per thread)
3/8 - 1/16 = 5/16.

For other sizes that don't work out so nicely, just use the closest drill size.
"""    


    
    

