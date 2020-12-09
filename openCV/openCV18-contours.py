import cv2
import numpy as np
print(cv2.__version__)
scale = 2
dispW = 320 * scale
dispH = 240 * scale
flip = 0

# USER INPUTS
picam    = True # WS mod: False for logitech camera, True for picam
color_ch = 0    # WS mod: 0, 1, 2 to track blue, green, red objects, respectively

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
print('')
print('ACTUAL DISPLAY WIDTH, HEIGHT:', actual_dispW, actual_dispH)

while True:
    ret, frame = cam.read()
    #frame = cv2.imread('smarties.png')

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
    # don't need to sort contours if using loop below
    #contours = sorted(contours, key=lambda x:cv2.contourArea(x), reverse=True)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area >= 50:
            (x, y, w, h) = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 3)
            #cv2.drawContours(frame, [cnt], 0, (0, 255, 255), 3)

    cv2.imshow(camNam, frame)
    cv2.moveWindow(camNam, 0, 0)


    if cv2.waitKey(1) == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()

