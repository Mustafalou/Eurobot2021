#!/usr/bin/env python
import time
import rospy
from std_msgs.msg import Float32, Empty, String, Int16MultiArray
from sensor_msgs.msg import Range
pub_lin = rospy.Publisher('move', Int16MultiArray, queue_size=50)
pub_rot = rospy.Publisher('rotate', Int16MultiArray, queue_size=50)
pub_stop = rospy.Publisher('stop',Empty,queue_size=50)
pub_start = rospy.Publisher("start", Empty, queue_size=50)
positions=[None,None]
i=0
msg = Int16MultiArray()
msg.data = [50,500]
def lin():
    	pub_lin.publish(msg)
def rot():
    	pub_rot.publish(msg)
def stop():
	pub_stop.publish()
def Traitement(msg):
	global i
	positions = msg.data[1:3]
	print(positions)
	actions[i%2]
	i+=1
def listener():
	rospy.init_node('listener')
	rate=rospy.Rate(10)
	#rospy.Subscriber("ultrasound_1",Range,Traitement)
	rospy.Subscriber("position",Int16MultiArray,Traitement)
	r=rospy.Rate(10)
	print("started Working")
	try:
		pub_start.publish()
		while not rospy.is_shutdown():
			r.sleep()
	except Exception as e:
		print(e)

actions=[lin,rot]
listener()
