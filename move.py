#!/usr/bin/env python
import time
import rospy
from math import pi
from std_msgs.msg import Float32, Empty, String, Int16MultiArray
from sensor_msgs.msg import Range
pub_lin = rospy.Publisher('move', Int16MultiArray, queue_size=50)
pub_rot = rospy.Publisher('rotate', Int16MultiArray, queue_size=50)
pub_stop = rospy.Publisher('stop',Empty,queue_size=50)
pub_start = rospy.Publisher("start", Empty, queue_size=50)
positions=[None,None]
i=0
msg = Int16MultiArray()
tour=485
distancepartour=22
rayon=3.5
tick50cm = tour*50//distancepartour 
wheelsep  = 24
tick90deg = ((pi/2)*wheelsep*tour)//(2*distancepartour) 
print(tick50cm)
def lin():
	msg.data=[50,tick50cm]
    	pub_lin.publish(msg)

def rot():
	msg.data=[50,tick90deg]
    	pub_rot.publish(msg)
def stop():
	pub_stop.publish()
def Traitement(msg):
	global i
	global positions
	positions = msg.data[1:3]
	print(msg.data)
	time.sleep(1)
	actions[i%2]()
	i+=1
def listener():
	rospy.init_node('listener')
	rate=rospy.Rate(10)
	#rospy.Subscriber("ultrasound_1",Range,Traitement)
	rospy.Subscriber("position",Int16MultiArray,Traitement)
	r=rospy.Rate(10)
	print("started Working")
	try:
		r.sleep()
		pub_start.publish()
		while not rospy.is_shutdown():
			r.sleep()
	except Exception as e:
		print(e)

actions=[lin,rot]
listener()
