#!/usr/bin/env python
import time
import rospy
from math import pi, cos,sin,atan,sqrt
from std_msgs.msg import Float32, Empty, String, Int16MultiArray
from sensor_msgs.msg import Range,LaserScan
pub_lin = rospy.Publisher('move', Int16MultiArray, queue_size=50)
pub_rot = rospy.Publisher('rotate', Int16MultiArray, queue_size=50)
pub_stop = rospy.Publisher('stop',Empty,queue_size=50)
pub_start = rospy.Publisher("start", Empty, queue_size=50)

i=0
msg = Int16MultiArray()
tour=485.0
distancepartour=22.0
rayon=3.5
tick50cm = tour*50//distancepartour 
wheelsep  = 24.0
tick90deg = ((pi/2)*wheelsep*tour)//(2*distancepartour) 
x0=1000
y0=0
positions=[0,0]
x,y=x0,y0
ang=pi/2
angletodo=pi/2
forwardtodo=0
def lin():
	msg.data=[50,int(forwardtodo/10*tour/distancepartour)]
    	pub_lin.publish(msg)
def rot():
	msg.data=[50,int(((angletodo*pi/180)*wheelsep*tour)//(2*distancepartour))]
    	pub_rot.publish(msg)
def stop():
	pub_stop.publish()
def Traitement(msg):
	global ang
	global i
	global  x
	global y
	global positions
	global angletodo
	global forwardtodo
	#print(msg.data[1])
	dg=msg.data[1] -positions[0]
	dd=msg.data[2] -positions[1]
	#print(tour,distancepartour,wheelsep)

	dc= 10*(dg+dd)/2*distancepartour/tour
	ang +=float(((dd-dg)*distancepartour)/(tour*wheelsep))
	degang=ang%(2*pi)*180.0/pi
	ang=ang%(2*pi)
	#print(dc,ang)
	x+=dc*cos(ang)
	y+=dc*sin(ang)
	print(x,y,degang)
	positions = msg.data[1:3]
	#print("sams  ,tickL,tickR,tickFL,tickFR")
	#print(msg.data)
	if i%2==0:
		goto=raw_input("Choose a position :")
		listgoto=goto.split(";")
		xf=int(listgoto[0])
		yf=int(listgoto[1])
		#print(xf,yf)
		if xf-x==0:
			if yf-y>=0:
				anglepos=90
			else:
				anglepos=270
		elif yf-y==0:
			if xf-x>=0:
				anglepos=0
			else:
				anglepos=180
		elif xf-x>0:
			anglepos=atan((yf-y)/(xf-x))*180/pi
			if anglepos<0:
				anglepos+=360
		else:
			anglepos=atan((yf-y)/(xf-x))*180/pi+180
		angletodo = anglepos-degang
		if abs(angletodo)>180:
			if angletodo<0:
				angletodo+=360
			else:
				angletodo-=360
		forwardtodo= sqrt((xf-x)**2+(yf-y)**2)
		print("angtodo",angletodo)
		print(forwardtodo/10*tour/distancepartour)
	#if i<8<:
        actions[i%2]()
        i+=1
def UltraSoundUpdate(msg):
	if msg.range >0:
		i=0
		stop()
def showlidar(msg):
	print(msg.ranges)
	lidarpositions=[]
	for elem in msg.ranges:

	
def listener():
	rospy.init_node('listener')
	rate=rospy.Rate(10)
	#rospy.Subscriber("ultrasound_1",Range,Traitement)
	rospy.Subscriber("position",Int16MultiArray,Traitement)
	rospy.Subscriber("ultrasound_6",Range,UltraSoundUpdate)
	rospy.Subscriber("ultrasound_5",Range,UltraSoundUpdate)
	rospy.Subscriber("ultrasound_4",Range,UltraSoundUpdate)
	rospy.Subscriber("ultrasound_3",Range,UltraSoundUpdate)
	rospy.Subscriber("ultrasound_2",Range,UltraSoundUpdate)
	rospy.Subscriber("ultrasound_1",Range,UltraSoundUpdate)
	rospy.Subscriber("scan",LaserScan,showlidar)
	r=rospy.Rate(10)
	print("started Working")
	try:
		r.sleep()
		pub_start.publish()
		while not rospy.is_shutdown():
			r.sleep()
	except Exception as e:
		print(e)

actions=[rot,lin]
listener()
showlidar(Range)
