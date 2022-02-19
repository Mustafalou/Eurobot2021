from rplidar import RPLidar
from math import cos, sin, pi, floor
import time
lidar = RPLidar('/dev/ttyUSB0')

info = lidar.get_info()
print(info)

health = lidar.get_health()
print(health)
scan_data = [0]*360
try:
    for i, scan in enumerate(lidar.iter_scans()):
        for (_, angle, distance) in scan:
            scan_data[min([359, floor(angle)])] = distance
        print(scan_data)
except KeyboardInterrupt:
    print("stopping")
    

lidar.stop()
lidar.stop_motor()
lidar.disconnect()
