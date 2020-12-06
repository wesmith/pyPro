import cv2
import numpy as np
print(cv2.__version__)
scale = 2
dispW = 320 * scale
dispH = 240 * scale
flip = 0

picam = True # WS mod

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

blank = np.zeros([dispH, dispW, 1], np.uint8)

while True:
    ret, frame = cam.read()

    #print(frame.shape)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    b, g, r = cv2.split(frame)

    blue  = cv2.merge((b, blank, blank))
    green = cv2.merge((blank, g, blank))
    red   = cv2.merge((blank, blank, r))

    grb = cv2.merge((g, r, b))  # mix up the colors
    #gbr = cv2.merge((g, b, r))  # mix
    #rgb = cv2.merge((r, g, b))  # mix
    inv = cv2.merge((255-b, 255-g, 255-r))  # color negative  WS mod

    off = 75
    cv2.imshow('Blue', blue)
    cv2.moveWindow('Blue', dispW + off, 0)
    cv2.imshow('Green', green)
    cv2.moveWindow('Green', 0, dispH + off)
    cv2.imshow('Red', red)
    cv2.moveWindow('Red', dispW + off, dispH + off)
    cv2.imshow('GRB', grb)
    cv2.moveWindow('GRB', 2*dispW + off, 0)
    cv2.imshow('INV', inv)
    cv2.moveWindow('INV', 2*dispW + off, dispH + off)

    cv2.imshow(camNam, frame)
    cv2.moveWindow(camNam, 0, 0)

    if cv2.waitKey(1) == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()

