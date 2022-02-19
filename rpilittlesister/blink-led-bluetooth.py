
import serial
import time

evenement=""
print("Start")
port="/dev/rfcomm0" #This will be different for various devices and on windows it will probably be a COM port.
bluetooth=serial.Serial(port, 9600)#Start communications with the bluetooth unit
print("Connected")
bluetooth.flushInput() #This gives the bluetooth a little kick
x=1 
while True:
	time.sleep(1)
	x=1-x
	msg=str(x)+"\n"
	bluetooth.write(msg.encode("utf_8"))
