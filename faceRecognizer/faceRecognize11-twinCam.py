from threading import Thread
import cv2
import numpy as np
import time

print(cv2.__version__)
scale = 2
dispW = 320 * scale
dispH = 240 * scale
flip  = 0

camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'


class vStream:

    def __init__(self, src, width, height):
        self.width   = width
        self.height  = height
        self.capture = cv2.VideoCapture(src)
        self.thread  = Thread(target=self.update, args=())  # NO parens after 'update'
        self.thread.daemon = True
        self.thread.start()
        # the below settings for the webcam, they crash? the picam
        if src == 1: # a kluge, for webcam only: this may improve latency: need to test
            self.capture.set(cv2.CAP_PROP_FRAME_WIDTH,  self.width)
            self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
            self.capture.set(cv2.CAP_PROP_FPS, 30)  # WS mod 12/21/20 default is 7.5 fps?
 


    def update(self):
        while True:
            _, self.frame = self.capture.read()
            # rename frames to ensure resized frame returned and not self.frame
            self.frame2 = cv2.resize(self.frame, (self.width, self.height))

    def getFrame(self):
        return self.frame2

# webcam: '/dev/video1' worked, but side-stepped my 'if' kluge in init(): not sure my
# kluge is helping at all: /dev/video1 may be slightly better
cam1 = vStream('/dev/video1',      dispW, dispH)
#cam1 = vStream(1,      dispW, dispH)    
cam2 = vStream(camSet, dispW, dispH) # picam

while True:

    try:
        frame1 = cam1.getFrame()
        frame2 = cam2.getFrame()
        frame3 = np.hstack((frame1, frame2))
        nam    = 'Combo'
        cv2.imshow(nam, frame3)
        cv2.moveWindow(nam, 0, 0)

    except:
        print('frame not available')

    if cv2.waitKey(1) == ord('q'):
        cam1.capture.release()
        cam2.capture.release()
        cv2.destroyAllWindows()
        exit(1)
        break



