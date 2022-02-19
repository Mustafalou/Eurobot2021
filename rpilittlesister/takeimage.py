from picamera import PiCamera
from time import sleep
camera = PiCamera()
camera.resolution = (1024,768)
camera.rotation = 180
camera.start_preview(fullscreen = False, window = (50,50,640,480))
#camera.capture('image.jpeg')
camera.start_recording('vid.h264')
sleep(5)
camera.stop_preview()
