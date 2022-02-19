#!/usr/bin/env python
import time
import rospy
from std_msgs.msg import Float32, Empty, String, Int16MultiArray
from sensor_msgs.msg import Range
pub_lin = rospy.Publisher('move', Float32, queue_size=50)
pub_rot = rospy.Publisher('rotate', Float32, queue_size=50)
pub_stop = rospy.Publisher('stop',Empty,queue_size=50)

def lin(dist):
    	pub_lin.publish(dist)
def rot(ang):
    	pub_rot.publish(ang)
def stop():
	stop.publish()
def Traitement(msg):
	print(msg.data[1:3])
def listener():
	rospy.init_node('listener')
	rate=rospy.Rate(10)
	#rospy.Subscriber("ultrasound_1",Range,Traitement)
	rospy.Subscriber("position",Int16MultiArray,Traitement)
	r=rospy.Rate(10)
	print("started Working")
	try:
		while not rospy.is_shutdown():
			lin(10)
			r.sleep()
	except:
		print("Extinction")
		stop()
listener()
