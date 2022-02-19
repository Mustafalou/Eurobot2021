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
import pygame
import os
from math import cos, sin, pi, floor
from rplidar import RPLidar

# Set up pygame and the display
os.putenv('SDL_FBDEV', '/dev/fb1')

# Setup the RPLidar
PORT_NAME = '/dev/ttyUSB0'
lidar = RPLidar( PORT_NAME)

# used to scale data to fit on the screen
max_distance = 1

#pylint: disable=redefined-outer-name,global-statement
def process_data(data):
    global max_distance
    start_object = False
    end_object = True
    objects = 0
    list_distances = []
    for angle in range(180):
        distance = data[angle]
        if distance > 0:                  # ignore initially ungathered data points
            if end_object == True :
		start_object = True
		end_object = False
	    max_distance = max([min([5000, distance]), max_distance])
            radians = angle * pi / 180.0
            x = distance * cos(radians)
            y = distance * sin(radians)
            point = (160 + int(x / max_distance * 119), 120 + int(y / max_distance * 119))
	   # print(x,y)
            list_distances.append(distance)
	    print(list_distances)	
	else : 
	    start_object = False
	    end_object =  True
	if start_object == True and end_object ==False :
	   objects +=1
	#print(objects)

scan_data = [0]*360

try:
    print(lidar.get_info())
    for scan in lidar.iter_scans():
        for (_, angle, distance) in scan:
            scan_data[min([359, int(floor(angle))])] = distance
        process_data(scan_data)

except KeyboardInterrupt:
    print('Stoping.')
lidar.stop()
lidar.disconnect()
