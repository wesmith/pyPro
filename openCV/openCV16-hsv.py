import cv2
import numpy as np
print(cv2.__version__)
scale = 2
dispW = 320 * scale
dispH = 240 * scale
flip = 0

picam = True # WS mod

def nothing(x):
    pass

cv2.namedWindow('Trackbars')

cv2.createTrackbar('hueLo', 'Trackbars',  50, 179, nothing)
cv2.createTrackbar('hueHi', 'Trackbars', 100, 179, nothing)
cv2.createTrackbar('hueLo2', 'Trackbars',  50, 179, nothing)
cv2.createTrackbar('hueHi2', 'Trackbars', 100, 179, nothing)
cv2.createTrackbar('satLo', 'Trackbars', 100, 255, nothing)
cv2.createTrackbar('satHi', 'Trackbars', 255, 255, nothing)
cv2.createTrackbar('valLo', 'Trackbars', 100, 255, nothing)
cv2.createTrackbar('valHi', 'Trackbars', 255, 255, nothing)

cv2.moveWindow('Trackbars', 1320, dispH + 75)

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
    cv2.imshow(camNam, frame)
    cv2.moveWindow(camNam, 0, 0)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    hueLo = cv2.getTrackbarPos('hueLo', 'Trackbars')
    hueHi = cv2.getTrackbarPos('hueHi', 'Trackbars')
    hueLo2 = cv2.getTrackbarPos('hueLo2', 'Trackbars')
    hueHi2 = cv2.getTrackbarPos('hueHi2', 'Trackbars')
    satLo = cv2.getTrackbarPos('satLo', 'Trackbars')
    satHi = cv2.getTrackbarPos('satHi', 'Trackbars')
    valLo = cv2.getTrackbarPos('valLo', 'Trackbars')
    valHi = cv2.getTrackbarPos('valHi', 'Trackbars')

    l_b = np.array([hueLo, satLo, valLo])
    u_b = np.array([hueHi, satHi, valHi])
    l_b2 = np.array([hueLo2, satLo, valLo])
    u_b2 = np.array([hueHi2, satHi, valHi])

    FGmask  = cv2.inRange(hsv, l_b,  u_b)  # if in the range, 255; out of range, 0
    FGmask2 = cv2.inRange(hsv, l_b2, u_b2) 
    FGmaskComp = cv2.add(FGmask, FGmask2)  # two masks to handle red that crosses 0-179 boundary
     
    cv2.imshow('FGmaskComp', FGmaskComp)
    cv2.moveWindow('FGmaskComp', 0, frame.shape[0] + 65)

    FG = cv2.bitwise_and(frame, frame, mask=FGmaskComp)
    cv2.imshow('FG', FG)
    cv2.moveWindow('FG', frame.shape[1] + 65, 0)

    BGmask = cv2.bitwise_not(FGmaskComp)
    cv2.imshow('BGmask', BGmask)
    cv2.moveWindow('BGmask', frame.shape[1] + 65, frame.shape[0] + 65)

    BG = cv2.cvtColor(BGmask, cv2.COLOR_GRAY2BGR) # get to (x,y,3) format

    final = cv2.add(FG, BG)
    cv2.imshow('final', final)
    cv2.moveWindow('final', 2 * frame.shape[1] + 65, 0)

    if cv2.waitKey(1) == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()

