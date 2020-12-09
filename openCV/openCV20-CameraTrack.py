import cv2
import numpy as np
#from adafruit_servokit import ServoKit

# USER INPUTS
picam    = False # WS mod: False for logitech camera (on servo tracker), True for picam
color_ch = 0     # WS mod: 0, 1, 2 to track blue, green, red objects, respectively
alpha    = 0.5   # WS mod: smoothing factor for tracking, (0,1): alpha = 0 means no smoothing
scale    = 2     # WS mod: scale to multiply 320x240 basic frame

print('openCV ' + cv2.__version__)
dispW = 320 * scale
dispH = 240 * scale
flip = 0

#kit  = ServoKit(channels=16)
pan  = 90
tilt = 45
#kit.servo[0].angle = pan
#kit.servo[1].angle = tilt

def nothing(x):
    pass

color_nam = ['Blue', 'Green', 'Red']             # WS mod
txt = 'Trackbars Set for ' + color_nam[color_ch] # WS mod
cv2.namedWindow(txt)

# WS mod: set the trackbar lower limits according to desired color
#         color order in list: blue limits, green limits, red limits
val_names  = ['hueLo', 'hueHi', 'hueLo2', 'hueHi2', 'satLo', 'satHi', 'valLo', 'valHi']
vals       = [[100, 135,  50,  50, 175, 255, 110, 255], # blue  settings
              [ 50, 100,  50,  50, 175, 255,  90, 255], # green settings
              [  0,  20, 150, 179, 130, 255, 145, 255]] # red   settings
up_lims    =  [179, 179, 179, 179, 255, 255, 255, 255]
for nam, val0, val1 in zip(val_names, vals[color_ch], up_lims):
    cv2.createTrackbar(nam, txt, val0, val1, nothing)

cv2.moveWindow(txt, 1320, dispH + 150)

if picam: 
    # gstreamer command line for pi camera
    # WS note: picam is hooked to '0' connector, the other is '1': apparently '0' runs by default
    #          if a second picam is used and hooked to '1' slot, then need to add a new
    #          channel variable to the command below: see comments in McWhorter vid (which one?)
    #          to see appropriate variable to add
    camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
    cam = cv2.VideoCapture(camSet)
    camNam = 'piCam'
else:
    # the following is for the webcam: use '1' if picam used in slot '0'
    cam = cv2.VideoCapture(1)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH,  dispW)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, dispH)
    camNam = 'webCam'

actual_dispW = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
actual_dispH = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
# WS note: this is not correct width, height for logitech cam display
print('')
print('ACTUAL DISPLAY WIDTH, HEIGHT: ', actual_dispW, actual_dispH)

objX, objY = 0, 0  # WS mod for implementing smoother

while True:
    ret, frame = cam.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    hueLo  = cv2.getTrackbarPos('hueLo',  txt)
    hueHi  = cv2.getTrackbarPos('hueHi',  txt)
    hueLo2 = cv2.getTrackbarPos('hueLo2', txt)
    hueHi2 = cv2.getTrackbarPos('hueHi2', txt)
    satLo  = cv2.getTrackbarPos('satLo',  txt)
    satHi  = cv2.getTrackbarPos('satHi',  txt)
    valLo  = cv2.getTrackbarPos('valLo',  txt)
    valHi  = cv2.getTrackbarPos('valHi',  txt)

    l_b = np.array([hueLo, satLo, valLo])
    u_b = np.array([hueHi, satHi, valHi])
    l_b2 = np.array([hueLo2, satLo, valLo])
    u_b2 = np.array([hueHi2, satHi, valHi])

    FGmask  = cv2.inRange(hsv, l_b,  u_b)  # if in the range, 255; out of range, 0
    FGmask2 = cv2.inRange(hsv, l_b2, u_b2) 
    FGmaskComp = cv2.add(FGmask, FGmask2)  # two masks to handle red that crosses 0-179 boundary
     
    cv2.imshow('FGmaskComp', FGmaskComp)
    cv2.moveWindow('FGmaskComp', 0, frame.shape[0] + 65)

    # opencv 4.1.1 just has 2 ouputs
    contours, _ = cv2.findContours(FGmaskComp, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # sort contours and use only largest, if big enough, for camera tracking
    contours = sorted(contours, key=lambda x:cv2.contourArea(x), reverse=True)

    # this loop can be removed when I figure out how to properly check for the existence of any 
    # contours, and then access the first one: contours[0] didn't seem to be working at first cut
    # after contours was checked on whether it was empty or not

    for cnt in contours:  # loop skipped if contours is empty
        area = cv2.contourArea(cnt)
        if area >= 50:
            (x, y, w, h) = cv2.boundingRect(contours[0])
            #cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 3)
            objX = alpha * objX + (1 - alpha) * (x + w/2)  # WS mod to smooth centroid
            objY = alpha * objY + (1 - alpha) * (y + h/2)  # WS mod
            cv2.circle(frame, (int(objX), int(objY)), 5, (0, 255, 255), -1) # WS mod
            errorPan  = objX - dispW/2  # don't use actual_dispW or actual_dispH: not correct for logitech
            errorTilt = objY - dispH/2
            
            # play with these values: 15, 43: make variables
            if abs(errorPan) > 15:
                pan  = pan - errorPan/43
            if abs(errorTilt) > 15:
                tilt = tilt - errorTilt/43

            if pan > 180: 
                pan = 180
                print("pan out of range")
            if pan < 0: 
                pan = 0
                print("pan out of range")
            if tilt > 180: 
                tilt = 180
                print("tilt out of range")
            if tilt < 0: 
                tilt = 0
                print("tilt out of range")

            #print(pan, tilt)
            # put up the pan and tilt values on the image as a red dot, though not too enlightening
            #cv2.circle(frame, (int(pan), int(tilt)), 5, (0, 0, 255), -1) # WS mod
            #kit.servo[0].angle = pan
            #kit.servo[1].angle = tilt
            break  # only show the biggest contour if big enough

    cv2.imshow(camNam, frame)
    cv2.moveWindow(camNam, 0, 0)

    if cv2.waitKey(1) == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()

