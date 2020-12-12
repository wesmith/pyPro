import cv2
import numpy as np
from adafruit_servokit import ServoKit

# note when starting up: it takes about 10 seconds for I2C to be established

# USER INPUTS
picam    = False # WS mod: False for logitech camera (on servo tracker), True for picam
alpha    = 0.2   # WS mod: smoothing factor for tracking, (0,1): alpha = 0 means no smoothing
scale    = 1     # WS mod: scale to multiply 320x240 basic frame: usually = 2
# servo-tracking params: scale may not effect these, since scale just windows
pixels_per_degree = 18 * scale  # WS mod: 30 (at scale 2) causes oscillations
do_not_move_error =  8 * scale

print('openCV ' + cv2.__version__)
dispW = 320 * scale
dispH = 240 * scale
flip = 0  # for picam in current configuration

# initial values of servos
pan  = 90
tilt = 90

print('initializing I2C ...')
kit  = ServoKit(channels=16)
pan_servo  = kit.servo[0] # WS mod
tilt_servo = kit.servo[1] # WS mod

# init
pan_servo.angle  = pan
tilt_servo.angle = tilt

def nothing(x): pass
txt  = 'Tracking Parameters'
txt1 = 'pixels_per_degree'
txt2 = 'do_not_move_error'
cv2.namedWindow(txt)
cv2.createTrackbar(txt1, txt, 40, 100, nothing)
cv2.createTrackbar(txt2, txt, 15,  30, nothing)
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

face_cascade = cv2.CascadeClassifier('cascade/face.xml')
eye_cascade  = cv2.CascadeClassifier('cascade/eye.xml')

objX, objY = 0, 0  # WS mod for implementing smoother

while True:
    ret, frame = cam.read()

    gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    # sort face area and use only largest, if big enough, for camera tracking
    faces = sorted(faces, key=lambda x:x[2]*x[3], reverse=True)  # WS mod

    pixels_per_degree = cv2.getTrackbarPos(txt1, txt)
    do_not_move_error = cv2.getTrackbarPos(txt2, txt)

    for (x, y, w, h) in faces:
        area = w * h
        if area >= 50:
            objX = alpha * objX + (1 - alpha) * (x + w/2)  # WS mod to smooth centroid
            objY = alpha * objY + (1 - alpha) * (y + h/2)  # WS mod
            cv2.circle(frame, (int(objX), int(objY)), 5, (0, 255, 255), -1) # WS mod
            #cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)

            roi_gray  = gray[y:y + h, x:x + w]
            eyes  = eye_cascade.detectMultiScale(roi_gray)

            # make roi a reference to frame, not a copy, so that circles will end up on the frame
            roi_color = frame[y:y + h, x:x + w]
            
            for (xEye, yEye, wEye, hEye) in eyes:
                xE = int(xEye + wEye/2)
                yE = int(yEye + hEye/2)
                # rule out nostril detections: eyes are above face center; yE + y is relative to the frame
                if yE + y < objY:  
                    cv2.circle(roi_color, (xE, yE), 10, (0, 0, 255), -1)

            errorPan  =   objX - dispW/2  # don't use actual_dispW or actual_dispH: not correct for logitech
            # WS mod: introduce minus sign for my servo setup: opposite of McWhorter's
            errorTilt = -(objY - dispH/2) 
            
            if abs(errorPan) > do_not_move_error:
                pan  = pan  - errorPan/pixels_per_degree
            if abs(errorTilt) > do_not_move_error:
                tilt = tilt - errorTilt/pixels_per_degree

            if pan > 180:  pan  = 180
            if pan < 0:    pan  = 0
            if tilt > 180: tilt = 180
            if tilt < 0:   tilt = 0

            pan_servo.angle  = pan
            tilt_servo.angle = tilt
            break # only track largest face area

    cv2.imshow(camNam, frame)
    cv2.moveWindow(camNam, 0, 0)

    if cv2.waitKey(1) == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()

# reset servos to neutral position
pan_servo.angle  = 90
tilt_servo.angle = 90

