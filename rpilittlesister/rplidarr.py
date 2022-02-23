# SPDX-FileCopyrightText: 2019 Dave Astels for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
Consume LIDAR measurement file and create an image for display.

Adafruit invests time and resources providing this open source code.
Please support Adafruit and open source hardware by purchasing
products from Adafruit!

Written by Dave Astels for Adafruit Industries
Copyright (c) 2019 Adafruit Industries
Licensed under the MIT license.

All text above must be included in any redistribution.
"""

import os
from math import cos, sin, pi, floor
import pygame
from rplidar import RPLidar

# Set up pygame and the display
os.putenv('SDL_FBDEV', '/dev/fb1')
pygame.init()
lcd = pygame.display.set_mode((800,500))
pygame.mouse.set_visible(False)
lcd.fill((0,0,0))
pygame.display.update()

# Setup the RPLidar
PORT_NAME = '/dev/ttyUSB0'
lidar = RPLidar( PORT_NAME)

# used to scale data to fit on the screen
max_distance = 5000
def isclose(a,b,rel_tol,abs_tol):
    return abs(a-b) <= max(rel_tol* max(abs(a),abs(b)),abs_tol)

def make_distances(L):
    objects =[]
    count = 0
    for i in range(1,len(L),1):
        #print(L[i].get('distance'))
        try :
            if not(isclose(L[i].get('distance'),L[i+1].get('distance'),0.005,200)):
                if len(L[count:i+1])>1:
                    objects.append(L[count:i+1])
                    #print("there is an object between " + str(L[count].get('distance')) + " and " + str(L[i+1].get('distance')))
                    count = i + 1
        except :
            
            objects.append(L[count::])
            #print("there is an object between " + str(L[count].get('distance')) + " and " + str(L[-1].get('distance')))
    return objects
#pylint: disable=redefined-outer-name,global-statement
def process_data(data):
    global max_distance
    lcd.fill((0,0,0))
    list_distances = []
    for angle in range(-90,90,1):
        distance = data[angle]
        if 0<distance < max_distance:
            # ignore initially ungathered
            radians = angle * pi / 180.0
            x = distance * cos(radians)
            y = distance * sin(radians)
            list_distances.append({"distance" : distance ,"angle" : radians})
            point = (int(x/10),250+int(y/10))
            lcd.set_at(point, pygame.Color(255, 255, 255))
    pygame.display.update()
    objs = make_distances(list_distances)
    print(len(objs))
    for elem in objs :
        print("there is an object between " + str(elem[0].get('distance')) + " and " + str(elem[-1].get('distance')))
scan_data = [0]*360

try:
    print(lidar.get_info())
    for scan in lidar.iter_scans():
        for (_, angle, distance) in scan:
            scan_data[min([359, floor(angle)])] = distance
        process_data(scan_data)

except KeyboardInterrupt:
    print('Stoping.')
lidar.stop()
lidar.disconnect()
